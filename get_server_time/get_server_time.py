#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import base64
import pycurl
import StringIO
import re
import time
import datetime

class HttpSession:
    def __init__(self):
        self.pycurl = pycurl.Curl()
#        self.pycurl.setopt(pycurl.VERBOSE, 1)

    def set_user_agent(self, agent):
        self.pycurl.setopt(pycurl.USERAGENT, agent)

    def set_referer(self, url):
        self.pycurl.setopt(pycurl.REFERER, url)

    def set_basic_authentication(self, username, password):
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        self.pycurl.setopt(c.HTTPHEADER, [
                'Authorization: Basic %s' % base64string,
                ])

    def http_request(self, url):
        response_body = StringIO.StringIO()
        response_header = StringIO.StringIO()
        self.pycurl.setopt(pycurl.URL, url)
        self.pycurl.setopt(pycurl.WRITEFUNCTION, response_body.write)
        self.pycurl.setopt(pycurl.HEADERFUNCTION, response_header.write)
        self.pycurl.perform()
        return HttpSession.parse_header(response_header.getvalue()), response_body.getvalue()

    @staticmethod
    def parse_header(header):
        headers = [hdr.split(': ') for hdr in header.strip().split('\r\n') if
                   hdr and not hdr.startswith('HTTP/')]
        return dict((header[0].lower(), header[1]) for header in headers)


def main():
    url = 'http://www.google.com'
    session = HttpSession()

    while 1:
        headers, body = session.http_request(url)
        m = re.match("\w+,\s+\d+\s+\w+\s+\d+\s+(\d+:\d+:\d+\s+\w+)", headers['date'])
        server_time = m.group(1)
        utc = datetime.datetime.strptime(server_time, '%H:%M:%S %Z')
        print (utc + datetime.timedelta(hours=9)).strftime('%H:%M:%S JST')
        
        time.sleep(0.25)

if __name__ == "__main__":
    main()
