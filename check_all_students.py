#python 2
import urllib2
import json
import datetime
import time, csv

student_list = json.loads(open('./example_student_list.json', 'r').read())

for student in student_list['Students']:
  student_dir = '/opt/students/' + student
  score_file = open(student_dir + "/score.log", 'a')
  correct_responses = 0
  incorrect_responses = 0
  with open('images.csv', 'rb') as csvfile:
    csv_images = csv.reader(csvfile)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    for row in csv_images:
      hostname = first_part_url + row[0]
      print "checking " + hostname
      expected_result = int(row[1])
      req = urllib2.Request(hostname, headers={'User-Agent' : "Magic Browser"})
      try: http_result = urllib2.urlopen( req ).read()
      except HTTPError as e:
          print 'The server couldn\'t fulfill the request.'
          print 'Error code: ', e.code
          incorrect_responses += 1
          continue
      except URLError as e:
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
          incorrect_responses += 1
          continue
      print str(http_result) + "  " + str(expected_result)
      try: http_result_int = int(http_result)
      except ValueError as e:
          incorrect_responses += 1
          continue
      acceptable_error = expected_result * .05
      if int(http_result) <= expected_result + acceptable_error and int(http_result) >= expected_result - acceptable_error:
          correct_responses += 1
          print "correct response"
      else:
          incorrect_responses += 1
  ts = time.time()
  score_file.write(str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')) + ", correct responses: " + str(correct_responses) + ", incorect_responses: " + str(incorrect_responses) + "\n")
  score_file.close()
    


