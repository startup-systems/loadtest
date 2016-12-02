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

student = sys.argv[1]
student_list = json.loads(open(STUDENT_FILE, 'r').read())



student_dir = BASE_OUTPUT_DIR + student
first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='

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
            print " expected_result = {} actual_result = {} URL = {}".format(expected_result, http_result, hostname)
            continue
        acceptable_error = expected_result * .05
        if int(http_result) <= expected_result + acceptable_error and int(
                http_result) >= expected_result - acceptable_error:
            correct_responses += 1
        else:
            incorrect_responses += 1
            print " expected_result_range = {} < x < {} actual_result = {} URL = {}".format(expected_result - acceptable_error, expected_result + acceptable_error , http_result, hostname)


