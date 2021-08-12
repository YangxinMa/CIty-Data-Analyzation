# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 20:03:40 2021

@author: admin
"""
#https://coursys.sfu.ca/2021su-cmpt-353-d1/pages/Exercise12
import sys
from pyspark.sql import SparkSession, functions, types, Row
import math
import string, re

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

def main(in_directory):
    file=spark.read.text(in_directory)
    #https://coursys.sfu.ca/2021su-cmpt-353-d1/pages/Exercise12
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    #https://spark.apache.org/docs/3.0.0/api/python/pyspark.sql.html
    file.cache()
    file=file.select(functions.split(file['value'], wordbreak).alias('word'))
    #https://blog.csdn.net/strongyoung88/article/details/52227568
    file=file.select(functions.explode(file['word']).alias('word'))
    file=file.select(functions.lower(file['word']).alias('word'))
    #https://ggbaker.ca/data-science/content/spark-calc.html
    file=file.groupBy(file['word']).agg(functions.count(file['hostname']).alias('count'))
    file=file.sort(file['count'].desc(),file['word'].asc())
    file=file.filter(file['value']!='')
    file.write.csv('output')

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)