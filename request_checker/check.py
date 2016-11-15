#python 2
import urllib2
import json

hostname = 'http://localhost:5000'

url_list = json.loads(open('../example_url_list.json', 'r').read())

for url in url_list['URLs']:
    http_result = json.loads(urllib2.urlopen(hostname + url['URL']).read())
    print http_result
    print url['expected_result']
    if http_result == url['expected_result']:
        print "they match"
    



