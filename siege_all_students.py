import subprocess
import json
import os
import csv

student_list = json.loads(open('./example_student_list.json', 'r').read())

for student in student_list['Students']:
  directory = "/opt/students/" + student
  if not os.path.exists(directory):
    os.makedirs(directory)

  # create url file for siege
  siege_urls_file = open('/opt/students/' + student + '/siege_urls.txt', 'w')
  siege_err_file = open('/opt/students/' + student + '/siege_err.log', 'w')
  with open('images.csv', 'rb') as csvfile:
    csv_images = csv.reader(csvfile)
    first_part_url = "http://" + student_list['Students'][student]['URL'] + '/api/num_colors?src='
    for row in csv_images:
      siege_urls_file.write(first_part_url + row[0] + '\n')

  subprocess.Popen(["siege",  "-t100s", '--concurrent=15', "--delay=10", "-i", "--file=" + directory + "/siege_urls.txt",  "--log=" + directory + "/siege.log"], stdout=siege_err_file, stderr=siege_err_file)
  print "siege -t100s --concurrent=15 --delay=10 -i --file=" + directory + "/siege_urls.txt --log=" + directory + "/siege.log"
  siege_urls_file.close()
  siege_err_file.close()
  




 # call(["mkdir", "$HOME/" + student])
