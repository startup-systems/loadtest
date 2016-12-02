# https://plot.ly/matplotlib/histograms/#basic-histogram-with-the-hist-function
import matplotlib.pyplot as plt

# Run the following on the server to get the values:
#
#   find /opt/students -name avg_score.txt -exec cat {} \; -exec echo -n ',' \; 2>/dev/null; echo
#
# then paste them into the list below.
a = []

plt.hist(a, bins='auto')
plt.title("Distribution of average scores")
plt.xlabel("Student average score")
plt.ylabel("Number of students")
plt.show()
