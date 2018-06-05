from scipy import stats
import matplotlib.pyplot as plt
import pymysql.cursors
from Helper import Helper


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE correct = 2")
actual = []
corrected = []
for row in cur:
    print(row)
    actual.append(row[6])
    corrected.append(row[5])

result = stats.ttest_rel(actual, corrected)
print(result)

# [actual, corrected].plot(kind='box')
# # This saves the plot as a png file
# plt.savefig('files/boxplot_outliers.png')

