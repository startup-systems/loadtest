import subprocess, boto3
import json
import os
import csv
import urllib2
import json
import datetime
import time, csv, socket

student_list = json.loads(open('./example_student_list.json', 'r').read())
start_time = datetime.datetime.now().replace(microsecond=0)
print "-------------------------- begining siege run on all students ---------------"
s3 = boto3.resource('s3')
bucket = s3.Bucket('startup-systems-results')

for student in student_list['Students']:
  student_start_time = datetime.datetime.now().replace(microsecond=0)
  print "====================================\nStarting student " + student
  today_date = time.strftime("%m-%d-%y")
  student_dir = '/opt/students/' + student
  siege_filename = '{}/{}-siege.log'.format(student_dir, today_date)
  score_filename = '{}/{}-score.log'.format(student_dir, today_date)
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
  subprocess.Popen(["siege",  "-t5m", '--concurrent=3', "-b", "-i", "--file=" + student_dir + "/siege_urls.txt",  "--log=" + siege_filename], stdout=siege_err_file, stderr=siege_err_file)
  print "launching siege with command: siege -t5m --concurrent=30 -b -i --file=" + student_dir + "/siege_urls.txt --log=" + siege_filename
  siege_urls_file.close()
  siege_err_file.close()
  
  time.sleep(10)
  print "begining to check responses for correctness"
  # start checking responses after 30 secs of requests
  score_file = open(score_filename, 'a')
  correct_responses = 0
  incorrect_responses = 0
  failed_requests = 0
  total_requests = 0
  with open('images.csv', 'rb') as csvfile:
    csv_images = csv.reader(csvfile)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    for row in csv_images:
      total_requests += 1
      hostname = first_part_url + row[0]
      expected_result = int(row[1])
      req = urllib2.Request(hostname, headers={'User-Agent' : "Magic Browser"})
      try: http_result = urllib2.urlopen( req, timeout = 15 ).read()
      except urllib2.HTTPError as e:
          print 'The server couldn\'t fulfill the request.'
          print 'Error code: ', e.code
          failed_requests += 1
          continue
      except urllib2.URLError as e:
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
          failed_requests += 1
          continue
      except socket.timeout:
          print "Timeout reached."
          failed_requests += 1
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
  student_end_time = datetime.datetime.now().replace(microsecond=0)
  score_file.write(str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')) + ", correct responses: " + str(correct_responses) + ", incorect_responses: " + str(incorrect_responses) + ", failed requests: " + str(failed_requests) + ", total requests: " + str(total_requests) + ", elapsed time for all requests: " + str(student_end_time - student_start_time) + "\n")
  score_file.close()

  print "Finished student " + student + "\nElapsed time: " + str(student_end_time - student_start_time)
  if (student_end_time - student_start_time) < datetime.timedelta(minutes = 5):
    print "waiting for siege to complete"
    time.sleep((datetime.timedelta(minutes = 5) - (student_end_time - student_start_time)).seconds)
  print "pushing logs to s3"
  results_file = open(score_filename, 'rb')
  load_file = open(siege_filename, 'rb')
  bucket.put_object(Key = student_list['Students'][student]['URL'] + "/" + today_date + "results_check.log", Body=results_file, ContentDisposition='inline', ContentType='text/plain')
  bucket.put_object(Key = student_list['Students'][student]['URL'] + "/" + today_date + "load_test.log", Body=load_file, ContentDisposition='inline', ContentType='text/plain')
  results_file.close()
  load_file.close()
  print "===================================="
    

end_time = datetime.datetime.now().replace(microsecond=0)
print "Full siege script run time: " + str(end_time - start_time)
print "-------------------------- finished siege run on all students ---------------"


