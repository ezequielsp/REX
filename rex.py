'''
REX: regular expressions explorer tool
Small utility to test and work with regular expressions in Python
'''
__author__ = 'Aurelien CROZATIER'
__version__ = '1.0a'

import argparse
import cherrypy
import json
import re

from os.path import dirname, abspath, join
from sys import argv
from xml.etree.ElementTree import Element, SubElement, tostring

import lib.pyratemp.pyratemp as pyratemp


def handleUnexpectedError():
    '''
    Custom error handler, do not display error message
    '''
    cherrypy.response.status = 302
    cherrypy.response.headers['Location'] = '/'
    return


def handleExpectedError(status, message, traceback, version):
    '''
    Custom HTTP error handler, do not display error message
    '''
    cherrypy.response.status = 302
    cherrypy.response.headers['Location'] = '/'
    return


class Rex():
    '''
    REX core class that defines the defines the structure of the web application
    '''
    def __init__(self, PROJECT_DIR, debug=False):
        if not debug:
            # If not in debug mode, activate custom error handlers
            self._cp_config = {
                                    'request.error_response': handleUnexpectedError,
                                    'error_page.default': handleExpectedError
                                }
        self._PROJECT_DIR = PROJECT_DIR
        self._APP_DIR = join(PROJECT_DIR, 'www')
        return

    @cherrypy.expose
    def index(self):
        '''
        Defines the root ("/") content of the web application
        '''
        return ''.join(open(join(self._APP_DIR, 'index.html'), 'r').readlines())

    @cherrypy.expose
    def getPageHeader(self):
        '''
        Return HTML content of the page header - Use Element and SubElement to build HTML
        '''
        table = Element('table')
        table.set('id', 'header-table')
        tr = SubElement(table, 'tr')
        td = SubElement(tr, 'td')
        td.set('id', 'pgm-name')
        td.text = 'REX'
        td = SubElement(tr, 'td')
        td.set('id', 'pgm-description')
        td.text = ' - Regular expressions explorer tool'
        return '{{"success": true, "html": {0:s}}}'.format(json.dumps(tostring(table)))

    @cherrypy.expose
    def getResult(self, regex, input_text, flags):
        '''
            Perform re operations and return results
        '''
        if not regex or not input_text:
            # We cannot perform any operation if we have not both regex and input_text
            html = 'REX cannot perform any operation if it has not a regular expression and an input text'
            return '{{"success": true, "html": {0:s}}}'.format(json.dumps(html))

        # Get flags correct value
        if flags:
            flags = flags[:-1]
        try:
            # Check if regex is valid by compiling it
            if flags:
                compiled_regex = re.compile(regex, flags=eval(flags))
            else:
                compiled_regex = re.compile(regex)
        except:
            raise
            html = 'Invalid regular expression'
            return '{{"success": true, "html": {0:s}}}'.format(json.dumps(html))

        # Compute operations and build results
        template_result = pyratemp.Template(filename='{0:s}/resources/templates/template_result.html'.format(
            self._APP_DIR), data={}, escape=pyratemp.HTML)

        # 1) Match
        match_result = compiled_regex.match(input_text)

        # 2) Search
        search_result = compiled_regex.search(input_text)

        # 3) List of all groups
        if search_result:
            groups_list = [group.__repr__() for group in search_result.groups()]
            if groups_list:
                groups_list_raw = search_result.groups().__repr__()
            else:
                groups_list_raw = ''
        else:
            groups_list = []
            groups_list_raw = ''

        # 4) List of all named group found
        if search_result:
            named_groups = search_result.groupdict()
            named_groups_list = [(group.__repr__(), named_groups[group].__repr__(),) for group in named_groups]
            if named_groups:
                named_groups_raw = named_groups.__repr__()
            else:
                named_groups_raw = ''
        else:
            named_groups_list = []
            named_groups_raw = ''

        # 5) Findall results
        findall_results = [result.__repr__() for result in compiled_regex.findall(input_text)]
        findall_results_raw = compiled_regex.findall(input_text)

        return '{{"success": true, "html": {0:s}}}'.format(json.dumps(template_result(
            match_result=match_result, search_result=search_result, groups_list=groups_list,
            groups_list_raw=groups_list_raw, named_groups_list=named_groups_list, named_groups_raw=named_groups_raw,
            findall_results=findall_results, findall_results_raw=findall_results_raw).encode('utf-8')))


def parseArguments(arguments):
    '''
    Define arguments parser for REX based on argparse
    '''
    parser = argparse.ArgumentParser(prog='REX',
                                     description='REX: Small utility to test and work with regular expressions '\
                                                 'in Python')

    # Define accepted/valid arguments
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='specify that REX will run in debug mode')
    parser.add_argument('-p', '--port', dest='server_port', type=int, action='store', default=8080,
                        help='specify the TCP port on which REX will listen to')

    return parser.parse_args(arguments)

if __name__ == '__main__':
    # Parse command line arguments and check their validity
    arguments = parseArguments(argv[1:])  # Do not include the script name

    # Get the path of the project directory
    PROJECT_DIR = dirname(abspath(__file__))

    appconf = {
        '/': {'tools.staticdir.root': join(PROJECT_DIR, 'www')},
        '/app': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'app'},
        '/extjs': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'extjs'},
        '/resources': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'resources'},
        '/favicon.ico': {'tools.staticfile.on': True, 'tools.staticfile.filename': join(PROJECT_DIR, 'www',
                                                                                        'favicon.ico')},
        '/rex.js': {'tools.staticfile.on': True, 'tools.staticfile.filename': join(PROJECT_DIR, 'www', 'rex.js')},
    }

    siteconf = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': arguments.server_port,
        'log.screen': False,
        'engine.autoreload.on': False
    }

    # Upload configuration
    cherrypy.config.update(siteconf)

    # Create server and application
    cherrypy.tree.mount(Rex(PROJECT_DIR, arguments.debug), '/', appconf)

    # Start CherryPy server
    cherrypy.server.start()
    cherrypy.engine.start()
    cherrypy.engine.block()


