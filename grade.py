import glob
import matplotlib.pyplot as plt
from pathlib import Path


MAX_GRADE = 100.0
MIN_GRADE = 75.0

score_files = glob.glob('/Users/aidanfeldman/Desktop/final-project-results/*/avg_score.txt')
scores = [float(Path(score_file).read_text()) for score_file in score_files]

min_score = min(scores)
max_score = max(scores)


# final = actual * N + base
# 100 = max * N + base
# 75 = min * N + base
# base = 75 - min * N
# 100 = max * N + 75 + min * N
# 25 = N ( max + min )

multiplier = (MAX_GRADE - MIN_GRADE) / (min_score + max_score)
base = MAX_GRADE - (max_score * multiplier)

scores = [(actual * multiplier + base) for actual in scores]

bins = int((MAX_GRADE - MIN_GRADE) / 5.0)
plt.hist(scores, bins='auto')

plt.title("Final project grades")
plt.xlabel("Student average score")
plt.ylabel("Number of students")

plt.show()
