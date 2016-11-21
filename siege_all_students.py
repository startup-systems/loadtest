import subprocess
import json
import os
import csv
import urllib2
import json
import datetime
import time, csv, socket

student_list = json.loads(open('./example_student_list.json', 'r').read())

for student in student_list['Students']:
  student_dir = '/opt/students/' + student
  # create direcotry for students stuff
  if not os.path.exists(student_dir):
    os.makedirs(student_dir)
  # create log files
  siege_urls_file = open('/opt/students/' + student + '/siege_urls.txt', 'w')
  siege_err_file = open('/opt/students/' + student + '/siege_err.log', 'w')
  # create url file for siege to read from
  with open('images.csv', 'rb') as csvfile:
    csv_images = csv.reader(csvfile)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    for row in csv_images:
      siege_urls_file.write(first_part_url + row[0] + '\n')
  # launch siege
  subprocess.Popen(["siege",  "-t5m", '--concurrent=3', "-b", "-i", "--file=" + student_dir + "/siege_urls.txt",  "--log=" + student_dir + "/siege.log"], stdout=siege_err_file, stderr=siege_err_file)
  print "launching siege with command: siege -t5m --concurrent=30 -b -i --file=" + student_dir + "/siege_urls.txt --log=" + student_dir + "/siege.log"
  siege_urls_file.close()
  siege_err_file.close()
  
  time.sleep(30)
  print "begining to check responses for correctness"
  # start checking responses after 30 secs of requests
  score_file = open(student_dir + "/score.log", 'a')
  correct_responses = 0
  incorrect_responses = 0
  with open('images.csv', 'rb') as csvfile:
    csv_images = csv.reader(csvfile)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    for row in csv_images:
      hostname = first_part_url + row[0]
      expected_result = int(row[1])
      req = urllib2.Request(hostname, headers={'User-Agent' : "Magic Browser"})
      try: http_result = urllib2.urlopen( req, timeout = 15 ).read()
      except urllib2.HTTPError as e:
          print 'The server couldn\'t fulfill the request.'
          print 'Error code: ', e.code
          incorrect_responses += 1
          continue
      except urllib2.URLError as e:
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
          incorrect_responses += 1
          continue
      except socket.timeout:
          print "Timeout reached."
          incorrect_responses += 1
          continue
      try: http_result_int = int(http_result)
      except ValueError as e:
          incorrect_responses += 1
          continue
      acceptable_error = expected_result * .05
      if int(http_result) <= expected_result + acceptable_error and int(http_result) >= expected_result - acceptable_error:
          correct_responses += 1
      else:
          incorrect_responses += 1
  ts = time.time()
  score_file.write(str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')) + ", correct responses: " + str(correct_responses) + ", incorect_responses: " + str(incorrect_responses) + "\n")
  score_file.close()
    



