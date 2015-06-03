
# -*- coding: utf-8 -*-

import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import re
import requests

from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
import csv


engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)

db = Session()

Base = declarative_base()


class IndustryCategory(Base):
    __tablename__ = 'industry_category'
    code = Column(String, primary_key=True)
    level = Column(Integer)
    name = Column(String)


def detectLevel(row):
    for i in range(5):
        if row[i].encode('hex') != 'e38080':
            return i


with open('n10191379.csv') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if len(row) != 5:
            print 'error in the file'
            sys.exit(-1)
        level = detectLevel(row)
        #print level
        category = IndustryCategory(
            code=row[level],
            level=level,
            name=row[4].strip().decode('utf-8')
        )
        db.merge(category)
        db.commit()
