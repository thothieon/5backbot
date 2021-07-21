# coding=utf-8
import os, sys, datetime
import requests
import pymysql
#import charts

#https://www.learncodewithmike.com/2020/02/python-mysql.html
#https://ithelp.ithome.com.tw/articles/10223413


# 資料庫參數設定
db_settings = {
    "host": "192.168.12.57",
    "port": 3306,
    "user": "admin",
    "password": "admin220",
    "db": "iDiving",
    "charset": "utf8"
}

msg = ''
#出團小幫手群組
tokenTest = 'FIGXSo5MEA1RJ23q7vLN5WuhkkYcdDp6JsjNmfyWvn7'
#iD. 櫃檯  出團小幫手 提醒
tokencounter = '0WMuxpiX6tYbAUkzYopqVz2Nq0APASHkrh2AWPAHU9b'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def mysqltest():
    print("mysqltestinit")
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料指令
        command = "SELECT 姓名, 身分證字號, 出生日期, 會員期限 FROM `人員名冊` WHERE (身分 = '學員' OR 身分 = '俱') and (會員期限 >= CURDATE() and 會員期限 != '' ) and (MONTH(出生日期)>4 and MONTH(出生日期)<6);"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        # 取得第一筆資料
        #result = cursor.fetchone()
        print(" ")
        print("Read",cursor.rowcount,"row(s) of data.")
        print(" ")
        print(result)
        print(" ")
    
    msg = '\n'
    msg += u'月份 當月會員生日名單\n'
    msg += u'姓名, 身分證字號, 出生日期, 會員期限\n'
    for row in result:
        print(row[0] + ', ' + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]))
        msg += row[0] + ', ' + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + '\n'
    
    print(msg)
    return msg

# 當月會員生日名單
def mysqlBC(lastMonthdata, toMonthdata, nextMonthdata, next2Monthdata):
    print("mysqlBCinit")
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料指令
        command = "SELECT 姓名, 身分證字號, 出生日期, 會員期限 FROM `人員名冊` WHERE (身分 = '學員' OR 身分 = '俱') and (會員期限 >= CURDATE() and 會員期限 != '' ) and (MONTH(出生日期)>" + str(toMonthdata) + " and MONTH(出生日期)<" + str(next2Monthdata) + ");"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        # 取得第一筆資料
        #result = cursor.fetchone()
        #print(" ")
        #print("Read",cursor.rowcount,"row(s) of data.")
        #print(" ")
        #print(result)
        #print(" ")
    
    msg = '\n'
    msg += str(nextMonthdata) + u'月份 當月會員生日名單\n'
    msg += u'姓名, 身分證字號, 出生日期, 會員期限\n'
    for row in result:
        msg += row[0] + ', ' + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + '\n'
    
    print(msg)
    return msg

# 當月會員資格到期名單 membership expiration
def mysqlmembership(lastMonthdata, toMonthdata, nextMonthdata, next2Monthdata):
    print("mysqlBCinit")
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料指令
        command = "SELECT 姓名, 身分證字號, 會員期限 FROM `人員名冊` WHERE (身分 = '學員' OR 身分 = '俱') and 會員期限 >= CURDATE() and 會員期限 != '' and MONTH(會員期限)>" + str(toMonthdata) + " and MONTH(會員期限)<" + str(next2Monthdata) + " ORDER BY 會員期限 DESC;"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        # 取得第一筆資料
        #result = cursor.fetchone()
        #print(" ")
        #print("Read",cursor.rowcount,"row(s) of data.")
        #print(result)
        #print(" ")
    
    msg = '\n'
    msg += str(nextMonthdata) + u'月份 當月會員資格到期名單\n'
    msg += u'姓名, 身分證字號, 會員期限\n'
    for row in result:
        msg += row[0] + ', ' + row[1] + ', ' + str(row[2]) + '\n'
    
    #print(msg)
    return msg

def main(argv):
    print("main")
    #取當月
    #帶下個月數值查詢，取下個月生日名單
    today = datetime.date.today()
    tomonth = datetime.date.today().strftime('%m')
    print(u'現在日期', today)
    lastMonth = int(tomonth)-1
    print(u'上個月份', lastMonth)
    toMonth = int(tomonth)
    print(u'現在月份', toMonth)
    nextMonth = int(tomonth)+1
    print(u'下個月份', nextMonth)
    next2Month = int(tomonth)+2
    print(u'下下個月份', next2Month)
    if argv[1] == '-Bc':
        msgdata = mysqlBC(lastMonth, toMonth, nextMonth, next2Month)
        #print("msgdata= \n", msgdata)
        lineNotifyMessage(tokencounter, msgdata)
        print("argv[1]=", argv[1])
        print('-Bc test')
    elif argv[1] == '-Ms':
        msgdata = mysqlmembership(lastMonth, toMonth, nextMonth, next2Month)
        #print("msgdata= \n", msgdata)
        lineNotifyMessage(tokencounter, msgdata)
        print("argv[1]=", argv[1])
        print('-Ms test')
    elif argv[1] == '-TBc':
        #msgdata = mysqltest()
        msgdata = mysqlBC(lastMonth, toMonth, nextMonth, next2Month)
        #msgdata = mysqlmembership(lastMonth, toMonth, nextMonth, next2Month)
        #print("msgdata= \n", msgdata)
        lineNotifyMessage(tokenTest, msgdata)
        print("argv[1]=", argv[1])
        print('-TBc test')
    elif argv[1] == '-TMs':
        #msgdata = mysqltest()
        #msgdata = mysqlBC(lastMonth, toMonth, nextMonth, next2Month)
        msgdata = mysqlmembership(lastMonth, toMonth, nextMonth, next2Month)
        #print("msgdata= \n", msgdata)
        lineNotifyMessage(tokenTest, msgdata)
        print("argv[1]=", argv[1])
        print('-TMs test')
    elif argv[1] == '-Ts':
        msgdata = mysqltest()
        #msgdata = mysqlBC(lastMonth, toMonth, nextMonth, next2Month)
        #msgdata = mysqlmembership(lastMonth, toMonth, nextMonth, next2Month)
        #print("msgdata= \n", msgdata)
        lineNotifyMessage(tokenTest, msgdata)
        print("argv[1]=", argv[1])
        print('-Ts test')
    #print(argv[1])
    #print(argv[2])
    #print(argv[3])

if __name__ == '__main__':
    print("__main__")
    main(sys.argv)
    
