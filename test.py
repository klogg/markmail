'''
Created on Jul 4, 2013

@author: kinow
'''

from markmail import MarkMail
from html.parser import HTMLParser

import urllib.parse
import simplejson as json
import re
import sys

class MyHTMLParser(HTMLParser):
    topic = None

#    def handle_starttag(self, tag, attrs):
#        print("Encountered a start tag:", tag)
#
#    def handle_endtag(self, tag):
#        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if (self.topic == 'subject'):
            if (re.search(r'^Re:', data) == None):
                # this is not a reply
                info = re.match(r'\[Xen-devel\] ?\[(?P<type>PATCH|RFC) ?(?P<version>v\d+)? ?((?P<count>\d+)\/(?P<total>\d+))?\] ?(?P<topic>.+)', data)
                if (info != None):
                    # parsing successful
                    if (info.group('count')==None or int(info.group('count')) == 0):
                        print(info.group('type') + " " + info.group('topic'))
            self.topic = None
        else:
            if (data == "Subject:"):
                self.topic = 'subject'
            #else:
                #print(data)

if __name__ == '__main__':
    markmail = MarkMail()
    parser = MyHTMLParser()

    page = 1
    thread_list = []

    if (sys.argv[1] == None):
        exit(1)

    msg = 'subject:/"'+urllib.parse.quote(sys.argv[1])+'/"%20list:com.xensource.lists.xen-devel%20order:date-forward'

    while True:
        messages = markmail.search(msg, page)
        #print(json.dumps(messages, indent=4, sort_keys=True))

        if page > int(messages['search']['numpages']):
            break

        page = page + 1

        for result in messages['search']['results']['result']:

            thread = markmail.get_thread(result['thread_id'])
            if (thread not in thread_list):
                thread_list.append(thread)
                #print(json.dumps(thread, indent=4, sort_keys=True))

                for thread_msg in thread['messages']['message']:
                    message = markmail.get_message(thread_msg['id'])
                    #print(json.dumps(message, indent=4, sort_keys=True))

                    parser.feed(message['content'])
