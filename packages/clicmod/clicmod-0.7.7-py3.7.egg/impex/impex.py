import logging
import os
import ssl
import time

import requests
import urllib3
from pyfiglet import Figlet
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

from onedesk.auth.auth import get_token
from onedesk.automaton.automaton import export_automata, import_automaton, get_automaton_list_for_client, \
    delete_automata, automaton_exists, submit_automaton_for_approval, approve_automaton, get_automaton_version_latest, \
    get_automaton_list_for_category
from onedesk.category.category import get_category_list_for_client, \
    get_category_tree, delete_category, create_path
from onedesk.client.client import get_client
from util.arguments import parser
from util.arguments import version
from util.models import Category, Automaton, ExportedAutomaton
from util.util import get_directory_tree, write_json_file

f = Figlet(font='slant')
# setup main logger
ch = logging.StreamHandler()
formatter = logging.Formatter('{asctime} {levelname} {name} {filename} {lineno} | {message}', style='{')
ch.setFormatter(formatter)
logger = logging.getLogger('main')
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)  # This toggles all the logger


def do_export(args):
    print(f.renderText('Export Start !!'))
    start_time = time.time()

    directory = os.path.abspath(args.directory)
    # create export path on local file system
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info('Exporting to local directory: %s', directory)
    except Exception:
        logger.error('Failed to create export directory: %s', directory)
        raise SystemExit

    # create session object
    s = requests.Session()
    # session retry config
    retries = Retry(total=int(args.retry),
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504],
                    method_whitelist=False)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    client = get_client(s, args.instance, args.client)
    category_tree = get_category_tree(s, args.instance, client, args.category)

    for node in tqdm(category_tree, desc='Exporting node tree to {}'.format(directory)):
        if type(node.val) is Category and node.key == 'root':
            continue

        if type(node.val) is Category and len(node.children) == 0:
            continue

        data = node.val.json()
        # if type(node.val) is Category:
        # data = get_category(s, args.instance, node)

        if type(node.val) is Automaton:
            data = export_automata(s, args.instance, node.val.json())

        if data is None:
            continue

        node_path = directory + node.path

        try:
            logger.debug('Creating directory %s', node_path)
            os.makedirs(node_path, exist_ok=True)
        except Exception:
            logger.error('Failed to create export directory: %s', node_path)
            raise SystemExit

        file_name = node.val.name.strip() \
                        .replace("/", "_") \
                        .replace(":", "_") \
                        .replace("?", "") + '.json'

        file_path = os.path.join(node_path, file_name)
        write_json_file(file_path, data)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def do_import(args):
    print(f.renderText('Import Start !!'))
    start_time = time.time()
    directory = os.path.abspath(args.directory)
    if args.category is not None:
        directory = os.path.join(directory, args.category)

    if not os.path.exists(directory):
        print("Given directory does not exist! {}".format(directory))
        raise SystemExit(1)

    logger.debug('Importing automata from directory %s', directory)

    directory_tree = get_directory_tree(directory)

    # create session object
    s = requests.Session()
    # session retry config
    retries = Retry(total=int(args.retry),
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504],
                    method_whitelist=False)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    # get client and their category list
    client = get_client(s, args.instance, args.client)

    for node in tqdm(directory_tree, desc='Importing node tree into {}'.format(args.instance)):
        if type(node.val) is ExportedAutomaton:
            logger.debug('<Importing automaton: [{} > {}]'.format(node.path, node.val.name))
            existing_automaton = automaton_exists(s, args.instance, client, node.val.name)
            if existing_automaton:
                delete_automata(s, args.instance, existing_automaton)  # TODO make this not suck
                # node.val.id = existing_automaton['id']
                # update_automaton(s, args.instance, node.val)
                # continue

            # get or create parent category
            parent = create_path(s, args.instance, client, node.path)
            logger.debug('Got parent %s', parent)
            # import automata into parent category
            automata = import_automaton(s, args.instance, parent, node.val.name, node.val.json())

            if automaton is None:
                continue

            # have to do this to try to get an automata object that the update endpoint will take
            cat = Category(parent)
            automata = get_automaton_list_for_category(s, args.instance, cat)
            for automaton in automata:
                # update version to make it 'live'
                if automaton['name'] == node.val.name:
                    # new_version = automaton['latestAutomatonVersion']
                    # automaton['latestAutomatonVersion'] = None
                    # new_version['@id'] = None
                    # new_version['versionId'] = None
                    # new_version['versionNumber'] = None
                    # new_version['automaton'] = None
                    # new_version['serializedFlow'] = None
                    # new_version['live'] = True
                    # automaton['automatonVersion'] = new_version
                    # updated = update_automaton(s, args.instance, automaton)
                    latest = get_automaton_version_latest(s, args.instance, automaton)
                    submitted = submit_automaton_for_approval(s, args.instance, latest)
                    approved = approve_automaton(s, args.instance, submitted)
                    if 'approvalRequestStatus' in approved and approved['approvalRequestStatus'] == 'APPROVED':
                        logger.info('Successfully imported and approved %s', node.val.name)
                    else:
                        logger.debug('Something broke')

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def do_wipe(args):
    print(f.renderText('Wipe Start !!'))
    start_time = time.time()

    # create session object
    s = requests.Session()
    retries = Retry(total=int(args.retry),
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504],
                    method_whitelist=False)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    client = get_client(s, args.instance, args.client)
    automata_list = get_automaton_list_for_client(s, args.instance, client)
    category_list = get_category_list_for_client(s, args.instance, client)

    for automaton in tqdm(automata_list, desc='Deleting automata in {} {}'.format(args.instance, client['name'])):
        delete_automata(s, args.instance, automaton)

    for category in tqdm(category_list, desc='Deleting categories {} {}'.format(args.instance, client['name'])):
        delete_category(s, args.instance, category)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def main():
    print(f.renderText('clicmod v{}'.format(version)))

    # pars args
    subparsers = parser.add_subparsers()
    export_parser = subparsers.add_parser('export', help="Export automata from the given client/category")
    export_parser.set_defaults(func=do_export)
    import_parser = subparsers.add_parser('import', help="Import automata to the given client/category")
    import_parser.set_defaults(func=do_import)
    wipe_parser = subparsers.add_parser('wipe', help="Delete all automata and categories in the given client/category")
    wipe_parser.set_defaults(func=do_wipe)
    args = parser.parse_args()

    # for troubleshooting 
    logger.debug(ssl.OPENSSL_VERSION)

    # disable because it gets annoying
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # do something!
    args.func(args)


if __name__ == '__main__':
    main()
