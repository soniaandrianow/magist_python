#!/usr/bin/python

import pymysql.cursors

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')

cur = conn.cursor()

cur.execute("SELECT * FROM genre")

print(cur.description)

print()

for row in cur:
    print(row)

cur.close()
conn.close()