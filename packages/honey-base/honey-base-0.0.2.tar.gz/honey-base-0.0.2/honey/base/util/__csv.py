#coding:utf-8

import csv

with open("/Users/geekfan/Downloads/jindao/chat.csv",'rU') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row['hello'],row['world'])
        print(row)