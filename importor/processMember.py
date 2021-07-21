# coding=utf-8

import re #regular expression簡稱re，中文:正規表示式
import datetime

class ProcessMember():
    def __init__(self, diving_center):
        #print("ProcessMember_init_")
        self.diving_center = diving_center
        self.today = datetime.datetime.now()
        self.idNumberPattern = re.compile('\w[0-9]{9}')
        self.arcNumberPattern = re.compile('\w\w[0-9]{8}')
        print("ProcessMember_init_self", self.today)

    def processCell(self, notation, value):
        #print("ProcessMember_processCell_")
        if (self.diving_center == 'idiving'):
            return self.idiving(notation, value)

    def idiving(self, notation, value):
        #print("ProcessMember_idiving_")
        processed_value = value
        #basic
        #body
        #equipment

        if (notation == 'basic.mobilePhone' or notation == 'basic.homePhone' or notation == 'basic.companyPhone' or notation == 'basic.emergencyContactPhone'):
            processed_value = value.replace('-', '')
            #print("ProcessMember_idiving_Phone")
        elif notation == 'basic.zipcode':
            if not value:
                processed_value = '000'
            elif (len(value) > 3):
                processed_value = value[:3]
            
            #print("ProcessMember_idiving_zipcode")
        elif notation == 'body.bloodType':
            processed_value = value.split(' ')[0]
            #print("ProcessMember_idiving_bloodType")

        return processed_value

    def postProcess(self, member_info):
        #print("ProcessMember_postProcess_")
        #basic
        # check if the person isMember
        #if member_info['basic']['memberexpiryDate'] > self.today:
        #    member_info['basic']['isMember'] = True
        #else:
        #    member_info['basic']['isMember'] = False
        if member_info['basic']['memberexpiryDate'] != '' or member_info['basic']['identity'] == '員工' :
            member_info['basic']['isMember'] = True
        else:
            member_info['basic']['isMember'] = False
        
        #body
        #equipment
        # mask
        for license_type in member_info['equipment']:
            if member_info['equipment'][license_type]['holdType'] == '●' :
                member_info['equipment'][license_type]['holdType'] = True
                member_info['equipment'][license_type]['brand'] = "未紀錄"
                member_info['equipment'][license_type]['model'] = "未紀錄"
            else:
                member_info['equipment'][license_type]['holdType'] = False
                member_info['equipment'][license_type]['brand'] = "無"
                member_info['equipment'][license_type]['model'] = "無"
        
        #if member_info['equipment']['Counterweight'] == '●' :

        return member_info
