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

class rex():
    '''
        REX core class that defines the defines the structure of the web application
    '''
    def __init__(self, PROJECT_DIR, debug=False):
        if not debug:
            #If not in debug mode, activate custom error handlers
            self._cp_config =   {
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
            Return HTML content of the page header
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
        return '{"success": true, "html": %s}' %(json.dumps(tostring(table)),)
    
    @cherrypy.expose
    def getResult(self, regex, ignore_case, locale, multi_line, dot_all, unicode, verbose, input_text):
        '''
            Perform re operations and return results
        '''
        if not regex or not input_text:
            #We cannot perform any operation if we have not both regex and input_text
            html = 'REX cannot perform any operation if it has not a regular expression and an input text'
            return '{"success": true, "html": %s}' %(json.dumps(html),)
        
        #Compute regex flags value
        flags = ''
        try:
            if eval(ignore_case):
                flags += 're.IGNORECASE|'
        except:
            pass
        try:
            if eval(locale):
                flags += 're.LOCALE|'
        except:
            pass
        try:
            if eval(multi_line):
                flags += 're.MULTILINE|'
        except:
            pass
        try:
            if eval(dot_all):
                flags += 're.DOTALL|'
        except:
            pass
        try:
            if eval(unicode):
                flags += 're.UNICODE|'
        except:
            pass
        try:
            if eval(verbose):
                flags += 're.VERBOSE|'
        except:
            pass
        
        if flags:
            flags = flags[:-1] #Remove trailing "|"
        
        try:
            #Check if regex is valid by compiling it
            if flags:
                compiled_regex = re.compile(regex, flags=eval(flags))
            else:
                compiled_regex = re.compile(regex)
        except:
            html = 'Invalid regular expression'
            return '{"success": true, "html": %s}' %(json.dumps(html),)
        
        #Compute operations and build results
        div = Element('div')
        div.set('class', 'rex-result')
        
        #1) Match
        match_result = compiled_regex.match(input_text)
        
        #Build output
        p = SubElement(div, 'p')
        p.set('class', 'rex-result')
        span = SubElement(p, 'span')
        span.set('id', 'header')
        span.text = '"Match" operation:'
        span = SubElement(p, 'span')
        
        if match_result:
            span.set('class', 'success')
            span.text = ' Success'
        else:
            span.set('class', 'failure')
            span.text = ' Failure'
        
        #2) Search
        search_result = compiled_regex.search(input_text)
        
        #Build output
        p = SubElement(div, 'p')
        p.set('class', 'rex-result')
        span = SubElement(p, 'span')
        span.set('id', 'header')
        span.text = '"Search" operation:'
        span = SubElement(p, 'span')
        
        if search_result:
            span.set('class', 'success')
            span.text = ' Success'
            
            #3) List of all groups
            p = SubElement(div, 'p')
            p.set('class', 'rex-result')
            span = SubElement(p, 'span')
            span.set('id', 'header')
            span.text = 'List of the groups found:'
            br = SubElement(p, 'br')
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Instruction: '
            span = SubElement(p, 'span')
            span.text = '<regex>.groups() - '
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Python object obtained: '
            span = SubElement(p, 'span')
            span.text = 'tuple'
            br = SubElement(p, 'br')
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Values: '
            
            if search_result.groups():
                #Found some group
                br = SubElement(p, 'br')
                for group in search_result.groups():
                    span = SubElement(p, 'span')
                    span.set('class', 'padded')
                    span.text = '%s' %(group,)
                    br = SubElement(p, 'br')
                span = SubElement(p, 'span')
                span.set('class', 'bold')
                span.text = 'Raw result: '
                span = SubElement(p, 'span')
                span.text = '%s' %(search_result.groups().__repr__(),)
            else:
                #No group found
                span = SubElement(p, 'span')
                span.set('class', 'failure')
                span.text = 'No group found'
            
            #4) List of all named group found
            p = SubElement(div, 'p')
            p.set('class', 'rex-result')
            span = SubElement(p, 'span')
            span.set('id', 'header')
            span.text = 'List of the named groups found:'
            br = SubElement(p, 'br')
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Instruction: '
            span = SubElement(p, 'span')
            span.text = '<regex>.groupdict() - '
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Python object obtained: '
            span = SubElement(p, 'span')
            span.text = 'dictionary'
            br = SubElement(p, 'br')
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Values: '
            
            if search_result.groupdict():
                br = SubElement(p, 'br')
                for named_group in search_result.groupdict():
                    span = SubElement(p, 'span')
                    span.set('class', 'bold')
                    span.text = 'Group name: '
                    span = SubElement(p, 'span')
                    span.text = '%s - ' %(named_group,)
                    span = SubElement(p, 'span')
                    span.set('class', 'bold')
                    span.text = 'Value: '
                    span = SubElement(p, 'span')
                    span.text = '%s' %(search_result.groupdict()[named_group],)
                    br = SubElement(p, 'br')
                span = SubElement(p, 'span')
                span.set('class', 'bold')
                span.text = 'Raw result: '
                span = SubElement(p, 'span')
                span.text = '%s' %(search_result.groupdict().__repr__(),)
            else:
                #No named group
                span = SubElement(p, 'span')
                span.set('class', 'failure')
                span.text = 'No named group found'
        else:
            span.set('class', 'failure')
            span.text = ' Failure'
        
        #5) Findall results
        p = SubElement(div, 'p')
        p.set('class', 'rex-result')
        span = SubElement(p, 'span')
        span.set('id', 'header')
        span.text = '"Findall" operation results:'
        br = SubElement(p, 'br')
        span = SubElement(p, 'span')
        span.set('class', 'bold')
        span.text = 'Instruction: '
        span = SubElement(p, 'span')
        span.text = '<regex>.findall() - '
        span = SubElement(p, 'span')
        span.set('class', 'bold')
        span.text = 'Python object obtained: '
        span = SubElement(p, 'span')
        span.text = 'list'
        br = SubElement(p, 'br')
        span = SubElement(p, 'span')
        span.set('class', 'bold')
        span.text = 'Values: '
        
        findall_results = compiled_regex.findall(input_text)
        
        if findall_results:
            br = SubElement(p, 'br')
            for result in findall_results:
                span = SubElement(p, 'span')
                span.set('class', 'padded')
                span.text = '%s' %(result,)
                br = SubElement(p, 'br')
            span = SubElement(p, 'span')
            span.set('class', 'bold')
            span.text = 'Raw result: '
            span = SubElement(p, 'span')
            span.text = '%s' %(findall_results.__repr__(),)
        else:
            span = SubElement(p, 'span')
            span.set('class', 'failure')
            span.text = 'No "findall" results found'
            
        return '{"success": true, "html": %s}' %(json.dumps(tostring(div)),)
    
def parseArguments(arguments):
    '''
        Define arguments parser for REX based on argparse
    '''
    parser = argparse.ArgumentParser(prog='REX', description='REX: Small utility to test and work with regular expressions in Python')
    
    #Define accepted/valid arguments
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='specify that REX will run in debug mode')
    parser.add_argument('-p', '--port', dest='server_port', type=int, action='store', default=8080, help='specify the TCP port on which REX will listen to')
    
    return parser.parse_args(arguments)
    
if __name__ == '__main__':
    #Parse command line arguments and check their validity
    arguments = parseArguments(argv[1:]) #Do not include the script name
    
    #Get the path of the project directory
    PROJECT_DIR = dirname(abspath(__file__))
    
    appconf = { 
        '/': {'tools.staticdir.root': join(PROJECT_DIR, 'www')},
        '/app': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'app'},
        '/extjs': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'extjs'},
        '/resources': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'resources'},
        '/favicon.ico': {'tools.staticfile.on': True, 'tools.staticfile.filename': join(PROJECT_DIR, 'www', 'favicon.ico')},
        '/rex.js': {'tools.staticfile.on': True, 'tools.staticfile.filename': join(PROJECT_DIR, 'www', 'rex.js')},
    }
    
    siteconf = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': arguments.server_port,
        'log.screen': False,
        'engine.autoreload.on': False
    }
    
    #Upload configuration
    cherrypy.config.update(siteconf)
    
    #Create server and application
    cherrypy.tree.mount(rex(PROJECT_DIR, arguments.debug), '/', appconf)
    
    #Start CherryPy server
    cherrypy.server.start() 
    cherrypy.engine.start()
    cherrypy.engine.block()
    
    
