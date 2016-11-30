import subprocess, boto3
import json
import os, sys
import csv
import urllib2
import json
import datetime
import time, csv, socket
import logging

BUCKET_NAME = 'startup-systems-results'
MINS_TO_RUN_SIEGE = 5
BASE_OUTPUT_DIR = '/opt/students/'
CONFIG_DIR = '/home/ubuntu/'
STUDENT_FILE = '{}student_list.json'.format(CONFIG_DIR)
IMAGES_FILE = '{}images.csv'.format(CONFIG_DIR)
LOG_DIR = '/home/ubuntu/logs/'

log_filename = '{}{}siege_all_students.log'.format(LOG_DIR, int(time.time()))
logger = logging.getLogger('siege_all')
hdlr = logging.FileHandler(log_filename)
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
logger.info("-------------------------- begining siege run on all students ---------------")
student_list = json.loads(open(STUDENT_FILE, 'r').read())
start_time = datetime.datetime.now().replace(microsecond=0)
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

for student in student_list['Students']:
    student_start_time = datetime.datetime.now().replace(microsecond=0)
    logger.info("====================================")
    logger.info("Starting student " + student)
    student_dir = BASE_OUTPUT_DIR + student
    siege_filename = '{}/siege.log'.format(student_dir)
    score_filename = '{}/score.log'.format(student_dir)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    # create direcotry for students stuff
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)
    # create log files
    siege_urls_file = open(student_dir + '/siege_urls.txt', 'w')
    siege_err_file = open(student_dir + '/siege_err.log', 'w')
    # create url file for siege to read from
    with open(IMAGES_FILE, 'rb') as csvfile:
        csv_images = csv.reader(csvfile)
        for row in csv_images:
            siege_urls_file.write(first_part_url + row[0] + '\n')
    # launch siege
    siege_command = ["siege", "-t5m", '--concurrent=3', "-b", "-i", "--file=" + student_dir + "/siege_urls.txt",
                     "--log=" + siege_filename, '--user-agent=Magic Browser']
    subprocess.Popen(siege_command, stdout=siege_err_file, stderr=siege_err_file)
    logger.info("launching siege with command: {}".format(' '.join(siege_command)))
    siege_urls_file.close()
    siege_err_file.close()

    logger.info("begining to check responses for correctness")
    score_file = open(score_filename, 'a')
    correct_responses = 0
    incorrect_responses = 0
    failed_requests = 0
    total_requests = 0
    with open(IMAGES_FILE, 'rb') as csvfile:
        csv_images = csv.reader(csvfile)
        for row in csv_images:
            total_requests += 1
            hostname = first_part_url + row[0]
            expected_result = int(row[1])
            req = urllib2.Request(hostname, headers={'User-Agent': "Magic Browser"})
            try:
                http_result = urllib2.urlopen(req, timeout=15).read()
            except urllib2.HTTPError as e:
                logger.info('The server couldn\'t fulfill the request.')
                logger.info('Error code: {}'.format(e.code))
                failed_requests += 1
                continue
            except urllib2.URLError as e:
                logger.info('We failed to reach a server.')
                logger.info('Reason: {}'.format(e.reason))
                failed_requests += 1
                continue
            except socket.timeout:
                logger.info("Timeout reached.")
                failed_requests += 1
                continue
            try:
                http_result_int = int(http_result)
            except ValueError as e:
                incorrect_responses += 1
                continue
            acceptable_error = expected_result * .05
            if int(http_result) <= expected_result + acceptable_error and int(
                    http_result) >= expected_result - acceptable_error:
                correct_responses += 1
            else:
                incorrect_responses += 1
    student_end_time = datetime.datetime.now().replace(microsecond=0)
    student_elapsed_time = (student_end_time - student_start_time)
    score_file.write(
        "{}: correct responses: {} incorrect responses: {} failed requests: {} total requests: {} elapsed time total: {}\n".format(
            str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')), str(correct_responses),
            str(incorrect_responses), str(failed_requests), str(total_requests),
            str(student_elapsed_time)))
    score_file.close()

    logger.info("Finished student " + student)
    logger.info("Elapsed time: " + str(student_elapsed_time))
    if student_elapsed_time < datetime.timedelta(minutes=MINS_TO_RUN_SIEGE):
        seconds_to_wait = (datetime.timedelta(minutes=MINS_TO_RUN_SIEGE) - student_elapsed_time).seconds
        logger.info("waiting {} seconds for siege to complete".format(seconds_to_wait))
        time.sleep(seconds_to_wait)
    logger.info("pushing logs to s3")
    try:
    	results_file = open(score_filename, 'rb')
    	bucket.put_object(Key=student_list['Students'][student]['URL'] + "/" + "results_check.log",
                      Body=results_file, ContentDisposition='inline', ContentType='text/plain')
    	load_file = open(siege_filename, 'rb')
    	bucket.put_object(Key=student_list['Students'][student]['URL'] + "/" + "load_test.log", Body=load_file,
                      ContentDisposition='inline', ContentType='text/plain')
    	results_file.close()
    	load_file.close()
    except:
        logger.error("unable to upload to s3")
        logger.error(sys.exc_info()[0])
    logger.info("====================================")

end_time = datetime.datetime.now().replace(microsecond=0)
logger.info("Full siege script run time: " + str(end_time - start_time))
logger.info("-------------------------- finished siege run on all students ---------------")
