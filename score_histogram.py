# http://stackoverflow.com/a/3054314/358804
import matplotlib
matplotlib.use('Agg')

import boto3
import glob
import io
import matplotlib.pyplot as plt
from pathlib import Path


BUCKET_NAME = 'startup-systems-results'
FILENAME = 'avg_scores.png'


score_files = glob.glob('/opt/students/*/avg_score.txt')
scores = [float(Path(score_file).read_text()) for score_file in score_files]

plt.hist(scores, bins='auto')

plt.title("Distribution of average scores")
plt.xlabel("Student average score")
plt.ylabel("Number of students")

# plt.show()
# plt.savefig(FILENAME)

# http://stackoverflow.com/questions/31485660/python-uploading-a-plot-from-memory-to-s3-using-matplotlib-and-boto
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)


s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
bucket.put_object(Key=FILENAME, Body=img, ContentDisposition='inline', ContentType='image/png', ACL='public-read')
