#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fake_podcast v0.1b
#
####################
#
# Example
#
# $ python fake_podcast.py /media/basico/ 192.168.17.1:8080
# Setting up web server on 192.168.17.1:8080 ..
# Your fake podcast url is: http://192.168.17.1:8080/basico/fake_podcast.rss
#
# Then, you add http://192.168.17.1:8080/basico/fake_podcast.rss to iTunes.
# Your files in /media/basico/ will be the content of the podcast.

import sys
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urllib

# Configuration
conf = {'ip': '127.0.0.1',
        'port': 8000,
        'path': '',
        'dir': ''
}

# Valid file extension to iTunes
valid_extensions = {
    '.mp3': 'audio/mpeg',
    '.m4a': 'audio/x-m4a',
    '.mp4': 'video/mp4',
    '.m4v': 'video/x-m4v',
    '.mov': 'video/quicktime',
    '.pdf': 'application/pdf'
}

def create_rss():
    ''' Create RSS file to podcast.
        Create a header based on the directory, so you can update this later.
        Parse valid files from the directory and return the created RSS '''
    
    url = 'http://%s:%d/%s/' % (conf['ip'], conf['port'], conf['dir'])
    title = 'Fake podcast for %s' % (conf['dir'])
    body = ''
    
    # Create Podcast RSS Header
    header = '''<?xml version="1.0" encoding="UTF-8"?>
        <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
        <channel>
        <title>%s</title>
        <link>%s</link>
        <language>en-us</language>
        ''' % (title, url)
    footer = '</channel></rss>'
    
    # Get files info
    for f in os.listdir(conf['path']):
        f_name, f_ext = os.path.splitext(f) 
        
        if f_ext in valid_extensions:
            f_url = url + f
            item = '''
                <item>
                <title>%s</title>
                <enclosure url="%s" type="%s" />
                </item> 
            ''' % (f_name, f_url, valid_extensions[f_ext])
           
            body = body + item

    rss = header + body + footer
    return rss


class WebServerHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        ''' Handle GET requests '''
        files_url = '/%s/' % (conf['dir'])
        
        # Response to RSS request
        if self.path == (files_url + 'fake_podcast.rss'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(create_rss()))
        
        # Response to files requests
        elif self.path.startswith(files_url):
            file_path = conf['path'] + '/' + urllib.url2pathname(os.path.split(self.path)[1])
            if os.path.exists(file_path):
                self.send_response(200)
                self.end_headers()
                f = open(file_path, mode='rb')
                self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

        # 404 response for others    
        else:
            self.send_response(404)
            self.end_headers()
            
def setup_webserver(server_class=BaseHTTPServer.HTTPServer):
    ''' Setup webserver for serve files '''
    server_address = (conf['ip'], conf['port'])
    httpd = server_class(server_address, WebServerHandler)
    try:
        print('To exit, press Ctrl-c')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Exiting ..')
        sys.exit(0)
    
def main():
    ''' Main function'''
    global conf

    #Process command-line arguments
    if len(sys.argv) >= 2:
        conf['path'] = os.path.abspath(sys.argv[1])
        if os.path.isdir(conf['path']) is False:
            print('Provided directory: %s doesn\'t exist' % sys.argv[1])
            sys.exit(0)
            
        conf['dir'] = os.path.split(conf['path'])[1]
        
        try:
            conf['ip'] = sys.argv[2].split(':')[0]
            conf['port'] = int(sys.argv[2].split(':')[1])
        except IndexError:
            pass
    else:
        print('Use: %s <directory> <ip:port (optional)>' % sys.argv[0])
        sys.exit(0)
  
    print('Setting up web server on %s:%d ..' % (conf['ip'], conf['port']))
    print('Your fake podcast url is: http://%s:%d/%s/fake_podcast.rss' % (conf['ip'], conf['port'], conf['dir']))
    setup_webserver()
    

if __name__ == '__main__':
    main()
