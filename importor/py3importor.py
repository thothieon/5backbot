# coding=utf-8

import os, sys
import codecs
import pickle

#import pandas as pd

from googleSheet import GoogleSheet
from mongodbstore import MongodbStore

import gspread
from oauth2client.service_account import ServiceAccountCredentials


diving_center = 'idiving'
#google_sheet_doc_key = '199CaQ4LvE0iPr-XtkhtsLCLob1cSQhTNvNo1E4iyDdM'
#01 個人資料 Member
google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
#21_年度價格表 Price List
#21_google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
members_file = 'members.pickle'


def addMemberToFirestore():
    print("addMemberToFirestore_Init")

def addCourseToFirestore():
    print("addCourseToFirestore_Init")

def addMemberSaveCSV():
    print("addMemberSaveCSV_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    
    #檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        #3 4504
        #test MAX 72
        #members = googleSheet.parseMember(start_row=3, end_row=52, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
        members = googleSheet.parseSaveCSV(start_row=3, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)
    
    #mongodbstore = MongodbStore(diving_center)
    #mongodbstore.addMembers(members)
    print("addMemberSaveCSV_END")

def addMemberToMongoDB():
    print("addMemberToMongoDB_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    
    #檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        #3 4504
        #test MAX 72
        members = googleSheet.parseMember(start_row=2, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)
    
    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addMembers(members)
    print("addMemberToMongoDB_END")

#commodity
def addCommodityToMongoDB():
    print("addCommodityToMongoDB_Init")

def MongoDBTest():
    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addone()

def main(argv):
    print("main")
    #addMemberSaveCSV()
    #addMemberToMongoDB()
    #MongoDBTest()
    if argv[1] == '-Da':
        addMemberToMongoDB()
    elif argv[1] == '-Sc':
        addMemberSaveCSV()

if __name__ == '__main__':
    main(sys.argv)


