# coding=utf-8

import os
import csv
import copy
import json
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from processMember import ProcessMember
from dotty_dict import dotty

# 參考 Google Sheet
#https://yanwei-liu.medium.com/%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8Epython%E5%BB%BA%E7%AB%8Bgoogle%E8%A1%A8%E5%96%AE-%E4%BD%BF%E7%94%A8google-sheet-api-314927f7a601
# 參考 Save CSV
# https://ithelp.ithome.com.tw/articles/10231217
# 參考 Save excel
# https://officeguide.cc/python-openpyxl-read-write-excel-file-tutorial-examples/

class GoogleSheet():
    def __init__(self, diving_center):
        print("GoogleSheet_init_")
        cred_file = os.path.join(os.getcwd(), 'credential', diving_center, 'gcp_service_account.json')
        print("GoogleSheet_init_cred_file->", cred_file)
        scopes = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credential = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scopes)
        self.google_cred = gspread.authorize(credential)
        self.diving_center = diving_center

    def parseMember(self, start_row, end_row, doc_key, log_file, sheet):
        #print("GoogleSheet_parseMember")
        members = []
        processMember = ProcessMember(self.diving_center)

        with open(os.path.join(os.getcwd(), 'keyMapping', self.diving_center, 'member_basic.json')) as f:
            basic_dict = dotty(json.load(f))

        with open(os.path.join(os.getcwd(), 'keyMapping', self.diving_center, 'member.json')) as f:
            mapping_dict = json.load(f)
        
        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        #worksheet = sheets.sheet1
        worksheetcol = worksheet.get_all_values()
        print("GoogleSheet_postscolname worksheetcol no  ", len(worksheetcol) )

        row = start_row
        #print("GoogleSheet_parseMember_row", row)
        #print("GoogleSheet_parseMember_mapping_dict.items()", mapping_dict.items())
        while row <= end_row:
            if row % 200 == 0:
                print('Now process > %s row' % row)
            
            currentCell = ''
            keyIdx = 0
            try:
                #取一列
                #values = worksheet.row_values(row)
                values = worksheetcol[row]
                for key, notation in mapping_dict.items():
                    if (notation):
                        currentCell = key
                        #print('Now process try (notation)-> %s: currentCell-> %s: key-> %s' % (notation, currentCell, key))
                        #抓欄位名稱
                        basic_dict[notation] = processMember.processCell(notation, values[keyIdx])
                    keyIdx = keyIdx + 1

                member_info = processMember.postProcess(copy.deepcopy(basic_dict.to_dict()))
                members.append(member_info)
                #print('Now process try ')
                row = row + 1
            except gspread.exceptions.APIError as e:
                e = json.loads(e.args[0])
                print('Now process except Exception Error ', e['error']['code'])
                if e['error']['code'] == 401:
                    print('Auth timeout, re-login')
                    gss_client.login()
                elif e['error']['code'] == 429:
                    print('Exceed the limitation on row %s, sleep 10 seconds (%s)' % (row, datetime.datetime.now()))
                    time.sleep(10)
                else:
                    print(e)
            except Exception as e:
                print('Now process except Exception Error [%s:%s] - %s' % (row, currentCell, e))
                log_file.write('Error [%s:%s] - %s\n' % (row, currentCell, e))
                row = row + 1
        
        print('total member count: %s' % len(members))
        return members

    def parseSaveCSV(self, start_row, end_row, doc_key, log_file, sheet):
        print("GoogleSheet_parseSaveCSV")
        datetime_dt = datetime.datetime.today()
        print("GoogleSheet_datetime ", datetime_dt.strftime("%Y%m%d%H%M%S") )
        postscolname = "postscol_" + datetime_dt.strftime("%Y%m%d%H%M%S") + ".csv"
        print("GoogleSheet_postscolname ", postscolname )
        
        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        worksheetcol = worksheet.get_all_values()
        
        print("GoogleSheet_postscolname worksheetcol no  ", len(worksheetcol) )
        totalrow = len(worksheetcol) 
        row = 0
        
        with open(postscolname, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            #employee_writer.writerow(['John Smith', 'Accounting', 'November'])
            #employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
            #values = worksheetcol[row]
            for row in range(totalrow):
                employee_writer.writerow(worksheetcol[row])
                row = row + 1

            #keyIdx = 0
            #for key, notation in mapping_dict.items():
        
        employee_file.close()
        
        print('Finished')




