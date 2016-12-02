# http://stackoverflow.com/a/3054314/358804
import matplotlib
matplotlib.use('Agg')

import glob
import matplotlib.pyplot as plt
from pathlib import Path


score_files = glob.glob('/opt/students/*/avg_score.txt')
scores = [float(Path(score_file).read_text()) for score_file in score_files]

plt.hist(scores, bins='auto')

plt.title("Distribution of average scores")
plt.xlabel("Student average score")
plt.ylabel("Number of students")

plt.savefig('avg_scores.png')
