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
        html = '''<table id="header-table" style="width: 100%; height: 60px; border-bottom: solid 5px #DD0000; background-color: #000000;">
                      <tr>
                          <td rowspan=3 valign=center style="padding-left: 40px; width: 135px; font-size: 40px; font-weight: bold; color: #DD0000">REX</td>
                          <td style="height: 20px"></td>
                      </tr>
                      <tr>
                          <td style="font-size: 20px; color: #FFFFFF;"> - Regular expressions explorer tool</td>
                      </tr>
                      <tr>
                          <td style="height: 20px"></td>
                      </tr>
                  </table>'''
        return '{"success": true, "html": %s}' %(json.dumps(html),)
    
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
            compiled_regex = re.compile(regex, flags=eval(flags))
        except:
            html = 'Invalid regular expression'
            return '{"success": true, "html": %s}' %(json.dumps(html),)
        
        #Compute operations and build results
        html = ''
        
        #1) Match
        match_result = compiled_regex.match(input_text)
        if match_result:
            html += '<span style="font-weight: bold; text-transform: uppercase">"Match" operation:</span> <span style="color: #0AAB15">Success</span><br/><br/>'
        else:
            html += '<span style="font-weight: bold; text-transform: uppercase">"Match" operation:</span> <span style="color: #DD0000">Failure</span><br/><br/>'
        
        #2) Search
        search_result = compiled_regex.search(input_text)
        if search_result:
            html += '<span style="font-weight: bold; text-transform: uppercase">"Search" operation:</span> <span style="color: #0AAB15">Success</span><br/><br/>'
            
            #3) List of all groups
            html += '<p style="line-height: 1.5em"><span style="font-weight: bold; text-transform: uppercase">List of the groups found:</span><br/>'
            html += '<span style="font-weight: bold">Instruction:</span> &lt;regex&gt;.groups() - <span style="font-weight: bold">Python object obtained:</span> tuple</span><br/>'
            html += '<span style="font-weight: bold">Values:</span><br/>'
            if search_result.groups():
                for group in search_result.groups():
                    html += '<span style="padding-left: 50px">%s</span><br/>' %(group,)
                html += '<span style="font-weight: bold">Raw result:</span> %s<br/><br/></p>' %(search_result.groups().__repr__(),)
            else:
                #No group
                html += '<span style="padding-left: 50px; color: #DD0000">No group found</span><br/><br/></p>'
            
            #4) List of all named group found
            html += '<p style="line-height: 1.5em"><span style="font-weight: bold; text-transform: uppercase">List of the named groups found:</span><br/>'
            html += '<span style="font-weight: bold">Instruction:</span> &lt;regex&gt;.groupdict() - <span style="font-weight: bold">Python object obtained:</span> dictionary</span><br/>'
            html += '<span style="font-weight: bold">Values:</span><br/>'
            if search_result.groupdict():
                for named_group in search_result.groupdict():
                    html += '<span style="padding-left: 50px">Group name: %s, value: %s</span><br/>' %(named_group, search_result.groupdict()[named_group])
                html += '<span style="font-weight: bold">Raw result:</span> %s<br/><br/></p>' %(search_result.groupdict().__repr__(),)
            else:
                #No group
                html += '<span style="padding-left: 50px; color: #DD0000">No named group found</span><br/><br/></p>'
        else:
            html += '<span style="font-weight: bold">"Search" operation:</span> <span style="color: #DD0000">Failure</span><br/><br/>'
        
        #5) Findall results
        html += '<p style="line-height: 1.5em"><span style="font-weight: bold; text-transform: uppercase">"Findall" operation results:</span><br/>'
        html += '<span style="font-weight: bold">Instruction:</span> &lt;regex&gt;.findall() - <span style="font-weight: bold">Python object obtained:</span> list</span><br/>'
        html += '<span style="font-weight: bold">Values:</span><br/>'
        findall_results = compiled_regex.findall(input_text)
        if findall_results:
            for result in findall_results:
                html += '<span style="padding-left: 50px">%s</span><br/>' %(result,)
            html += '<span style="font-weight: bold">Raw result:</span> %s<br/></p>' %(findall_results.__repr__(),)
        else:
            html += '<span style="padding-left: 50px; color: #DD0000">No "findall" results</span><br/></p>'
            
        return '{"success": true, "html": %s}' %(json.dumps(html),)
    
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
    
    
