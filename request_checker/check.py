#python 2
import urllib2
import json

student_list = json.loads(open('../example_student_list.json', 'r').read())
hostname = 'http://images.afeld.me/api/num_colors?src='
correct_responses = 0
incorrect_responses = 0
url_list = json.loads(open('../example_url_list.json', 'r').read())

for url in url_list['URLs']:
    req = urllib2.Request(hostname + url['URL'], headers={'User-Agent' : "Magic Browser"})
    try: http_result = urllib2.urlopen( req ).read()
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        continue
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        continue
    try: http_result_int = int(http_result)
    except ValueError as e:
        incorrect_responses += 1
        continue
    if int(http_result) == url['expected_result']:
        correct_responses += 1
    else:
        incorrect_responses += 1

print str(correct_responses) + " correct responses.  " + str(incorrect_responses) + " incorrect_responses"
    



