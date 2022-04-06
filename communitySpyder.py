
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:54:35 2021

@author: Shaogeng
"""
import tkinter as tk
import requests as re
from bs4 import BeautifulSoup
import time
import pandas as pd
import json 
from urllib.request import urlopen, quote

class App(tk.Frame):
    def __init__(self, window): 
        self.window = window 
        self.window.title("小区爬取器")
        self.window.geometry('600x300')
        self.cityDesc = tk.Label(self.window, text="请输出城市(例:西安市)：")
        self.cityDesc.grid(column=0, row=0,sticky='w')
        self.cityInput = tk.Entry(self.window, show = None,font = ('Arial',10),width = 60)
        self.cityInput.grid(column=1, row=0,sticky='w')
        self.countyDesc = tk.Label(self.window, text="请输入区县(例:临潼区)：")
        self.countyDesc.grid(column=0, row=1,sticky='w')
        self.countyInput = tk.Entry(self.window, show = None,font = ('Arial',10),width = 60)
        self.countyInput.grid(column=1, row=1,sticky='w')
        self.fullSiteDesc = tk.Label(self.window, text="请输入要爬取的网址：") #"https://xa.loupan.com/community/lintong/" # 把anning改成需要查询的地址
        self.fullSiteDesc.grid(column=0, row=2,sticky='w')
        self.fullSiteInput = tk.Entry(self.window, show = None,font = ('Arial',10),width = 60)
        self.fullSiteInput.grid(column=1, row=2,sticky='w')
        self.fullSitetip = tk.Label(self.window, text="例：https://xa.loupan.com/community/lintong/  只支持楼盘网(loupan.com)")
        self.fullSitetip.grid(column=1,row=3,sticky='w')
        self.mainSiteDesc = tk.Label(self.window, text="请输入主站地址：") #"https://xa.loupan.com/" 
        self.mainSiteDesc.grid(column=0, row=4,sticky='w')
        self.mainSiteInput = tk.Entry(self.window, show = None,font = ('Arial',10),width = 60)
        self.mainSiteInput.grid(column=1, row=4,sticky='w')
        self.mainSitetip = tk.Label(self.window, text="例：https://xa.loupan.com/ 上面地址的前半段")
        self.mainSitetip.grid(column=1,row=5,sticky='w')
        self.akDesc = tk.Label(self.window, text="请输入主站地址：") #"https://xa.loupan.com/" 
        self.akDesc.grid(column=0, row=6,sticky='w')
        self.akInput = tk.Entry(self.window, show = None,font = ('Arial',10),width = 60)
        self.akInput.grid(column=1, row=6,sticky='w')
        self.aktip = tk.Label(self.window, text="百度地图密钥ak") # 
        self.aktip.grid(column=1,row=7,sticky='w')
        self.button = tk.Button(self.window,text="开始", command=self.clicked)
        self.button.grid(row=8,column=0,columnspan=2)

    def clicked(self):
        self.xiaoqus = []
        self.city = self.cityInput.get()
        self.county = self.countyInput.get()
        self.url = self.fullSiteInput.get()
        self.mainUrl = self.mainSiteInput.get()
        self.ak = self.akInput.get()
        print(self.url)
        self.get_info(self.url)
        while self.url:
            self.url = self.get_page(self.url)
            if self.url is not None:
                print(self.url)
                self.get_info(self.url)
        self.write_csv(self.get_latLng(self.clear_address(self.xiaoqus)))
        self.start = tk.Label(self.window, text="您查询的"+self.city+self.county+"的小区信息已经完成,请在文件夹找到CSV文件使用")
        self.start.grid(column=1,row=9)
    
    def get_page(self,url):
        resp = re.get(self.url, headers=header)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        next_page = soup.find("a", class_='pagenxt')
        if next_page:
            self.url = self.mainUrl+next_page['href']
            return self.url
        
    def get_info(self,url):
        time.sleep(3)
        resp = re.get(self.url, headers=header)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find("ul",class_="list").find_all("li"):
            name = item.find("div",class_="text").h2.a.get_text().replace(' ', '').replace(',', '').replace('\r', '').replace('\n', '').replace('\t', '')
            address = item.find_all("div",class_="d")[1].find('span').get_text()
            type = item.find("div",class_="tags m_bottom_10").find('span').get_text()
            print(name,address,type)
            xiaoqu={
                'name':name,
                'address':address,
                'type':type}
            self.xiaoqus.append(xiaoqu)
        return self.xiaoqus
    
    def clear_address(self,xiaoqus):
        for i in range(0,len(self.xiaoqus)):
            if self.xiaoqus[i]["address"].rfind(']') != -1:
                self.xiaoqus[i]["address_new"] = self.city+self.county+self.xiaoqus[i]["address"][self.xiaoqus[i]["address"].rfind(']')+1:len(self.xiaoqus[i]["address"])].replace(self.city,"").replace(self.county,"").replace(" ","").replace(".","")
            else:
                self.xiaoqus[i]["address_new"] = self.city+self.county+self.xiaoqus[i]["address"].replace(self.city,"").replace(self.county,"").replace(" ","").replace(".","")
        for i in range(0,len(self.xiaoqus)):
            if self.xiaoqus[i]["address_new"].rfind('（') != -1:
                self.xiaoqus[i]["address_new2"] = self.xiaoqus[i]["address_new"][:self.xiaoqus[i]["address_new"].rfind('（')].replace(" ","")
            else:
                self.xiaoqus[i]["address_new2"] = self.xiaoqus[i]["address_new"]
        for i in range(0,len(self.xiaoqus)):
            if self.xiaoqus[i]["address_new2"].rfind('(') != -1:
                self.xiaoqus[i]["address_new3"] = self.xiaoqus[i]["address_new2"][:self.xiaoqus[i]["address_new2"].rfind('(')].replace(" ","")
            else:
                self.xiaoqus[i]["address_new3"] = self.xiaoqus[i]["address_new2"]
        for i in range(0,len(self.xiaoqus)):
            if self.xiaoqus[i]["address_new3"].rfind('，') != -1:
                self.xiaoqus[i]["address_new4"] = self.xiaoqus[i]["address_new3"][:self.xiaoqus[i]["address_new3"].rfind('，')].replace(" ","")
            else:
                self.xiaoqus[i]["address_new4"] = self.xiaoqus[i]["address_new3"]
        for i in range(0,len(self.xiaoqus)):
            if self.xiaoqus[i]["address_new4"].rfind(',') != -1:
                self.xiaoqus[i]["address_new5"] = self.xiaoqus[i]["address_new4"][:self.xiaoqus[i]["address_new4"].rfind('，')].replace(" ","")+self.xiaoqus[i]["name"]
            else:
                self.xiaoqus[i]["address_new5"] = self.xiaoqus[i]["address_new4"]+self.xiaoqus[i]["name"]
        for i in range(0,len(self.xiaoqus)):
            self.xiaoqus[i]["address"] = self.xiaoqus[i]["address_new5"]
            del self.xiaoqus[i]["address_new"]
            del self.xiaoqus[i]["address_new2"]
            del self.xiaoqus[i]["address_new3"]
            del self.xiaoqus[i]["address_new4"]
            del self.xiaoqus[i]["address_new5"]
        return self.xiaoqus
    
    def get_latLng(self,xiaoqus):
        apiUrl_part = 'http://api.map.baidu.com/geocoding/v3/'
        output = 'json'
        ak = self.ak
        for i in range(0,len(self.xiaoqus)):
            address = quote(self.xiaoqus[i]["address"])
            apiUrl = apiUrl_part + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak 
            print(apiUrl)
            req = urlopen(apiUrl)
            res = req.read().decode() 
            temp = json.loads(res)
            self.xiaoqus[i]["lat"] = temp['result']['location']['lat']
            self.xiaoqus[i]["lng"] = temp['result']['location']['lng']
            self.xiaoqus[i]["precise"] = temp['result']['precise']
            self.xiaoqus[i]["confidence"] = temp['result']['confidence']
            self.xiaoqus[i]["comprehension"] = temp['result']['comprehension']
            self.xiaoqus[i]["level"] = temp['result']['level']
        return self.xiaoqus

    def write_csv(self,xiaoqus):
        df = pd.DataFrame.from_dict(self.xiaoqus, orient='columns')
        df.to_csv(self.city+self.county+'.csv',index = False,encoding="utf_8_sig")
    
    
if __name__ == "__main__": 
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
'Cookie': 'antipas=145M204676TL713539C97; uuid=db5afeb9-3098-4470-89bb-1dc454285b62; cityDomain=zhangzhou; clueSourceCode=%2A%2300; user_city_id=80; ganji_uuid=6283474678349984657438; sessionid=39d4b3ef-4a48-49c7-da02-9255c73b1379; lg=1; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1606212665; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22db5afeb9-3098-4470-89bb-1dc454285b62%22%2C%22ca_city%22%3A%22zhangzhou%22%2C%22sessionid%22%3A%2239d4b3ef-4a48-49c7-da02-9255c73b1379%22%7D; preTime=%7B%22last%22%3A1606212670%2C%22this%22%3A1606212663%2C%22pre%22%3A1606212663%7D; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1606212670'}
    window = tk.Tk()
    myapp = App(window) 
    window.mainloop()