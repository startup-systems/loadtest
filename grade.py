import csv
import glob
import matplotlib.pyplot as plt
from pathlib import Path


BASELINE_FILE = '/Users/aidanfeldman/Desktop/final-project-results/alf239/avg_score.txt'
BASELINE_SCORE = float(Path(BASELINE_FILE).read_text())
MAX_GRADE = 100.0
BASELINE_GRADE = 75.0

score_files = glob.glob('/Users/aidanfeldman/Desktop/final-project-results/*/avg_score.txt')
scores = [float(Path(score_file).read_text()) for score_file in score_files]

max_score = max(scores)

# final = actual * N + base
# 100 = max * N + base
# 75 = baseline * N + base
# base = 75 - min * N
# 100 = max * N + 75 + min * N
# 25 = N ( max + min )

multiplier = (MAX_GRADE - BASELINE_GRADE) / (BASELINE_SCORE + max_score)
base = MAX_GRADE - (max_score * multiplier)

grades = [(actual * multiplier + base) for actual in scores]


with open('grades.csv', 'w', newline='') as csvfile:
    grade_writer = csv.writer(csvfile)
    grade_writer.writerow(['NetID', 'Grade', 'Add Comments'])

    for i in range(len(score_files)):
        net_id = score_files[i].split('/')[5]
        if net_id in ['alf239', 'aidan', 'aidan_aws']:
            continue

        grade = int(grades[i])
        score = int(scores[i])

        comment = 'Final score: {}/{}'.format(score, int(max_score))
        grade_writer.writerow([net_id, grade, comment])


plt.hist(grades, bins=20)

plt.title("Final project grades")
plt.xlabel("Student grade")
plt.ylabel("Number of students")

plt.show()
