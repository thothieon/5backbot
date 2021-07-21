# coding=utf-8

import os, datetime
import pprint

from pymongo import MongoClient #引入 pymongo

post = {
    "author": "Maxsu",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

class MongodbStore():
    def __init__(self, diving_center):
        print("MongodbStore__init__")
        client = MongoClient(host='192.168.12.249', port=27018)

        if diving_center == 'idiving':
            self.idiving_primary = client.idiving_primary
            #self = client['idiving_primary']
            self.today = datetime.datetime.now()
            print("MongodbStore__init__self.idiving_primar", self.idiving_primary)

    def addMembers(self, members):
        print('total record: %s' % len(members))
        datetime_dt = datetime.datetime.today()
        print("addMemberToMongoDB_datetime ", datetime_dt.strftime("%Y%m%d_%H%M%S") )
        postscolname = "postscol_" + datetime_dt.strftime("%Y%m%d_%H%M%S")
        print("addMemberToMongoDB_postscolname ", postscolname )
        self.postscol = self.idiving_primary[postscolname]
        current_idx = 0
        for member in members:
            #post_id = self.postscol.insert(members[current_idx])
            post_id = self.postscol.insert_one(members[current_idx]).inserted_id
            current_idx = current_idx + 1
            if current_idx % 200 == 0:
                print('Now process > %s' % current_idx)
        print('Finished')

    def addone(self):
        print("MongodbStore__addone__")
        self.postscol = self.idiving_primary.postscol
        post_id = self.postscol.insert_one(post).inserted_id
        print ("post id is ", post_id)
        #單筆查詢
        pprint.pprint(self.postscol.find_one())
