# fix for not having a DISPLAY
# http://stackoverflow.com/a/3054314/358804
import matplotlib
matplotlib.use('Agg')

import boto3
import datetime
import glob
import io
import matplotlib.pyplot as plt
from pathlib import Path
import pytz
import time


BUCKET_NAME = 'startup-systems-results'
FILENAME = 'avg_scores.png'

# load the scores
score_files = glob.glob('/opt/students/*/avg_score.txt')
scores = [float(Path(score_file).read_text()) for score_file in score_files]

plt.hist(scores, bins='auto')

timezone = pytz.timezone('US/Eastern')
time_obj = datetime.datetime.now(timezone)
time_str = time_obj.strftime('%a %Y-%m-%d %I:%M %p ET')
plt.title("Distribution of average scores, {}".format(time_str))
plt.xlabel("Student average score")
plt.ylabel("Number of students")

# plt.show()
# plt.savefig(FILENAME)

# save the image in memory
# http://stackoverflow.com/questions/31485660/python-uploading-a-plot-from-memory-to-s3-using-matplotlib-and-boto
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)

# upload the image to S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
bucket.put_object(
    ACL='public-read',
    Body=img,
    ContentDisposition='inline',
    ContentType='image/png',
    Key=FILENAME,
)
