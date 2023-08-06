#!/usr/bin/python
import requests
import cookielib
import time
import json
import os

import logging
logger = logging.getLogger("neterra.py")

from urllib2 import HTTPPasswordMgr
from cookielib import CookieJar
from telnetlib import theNULL

#to disable warnings related to https certificates verification
import urllib3
urllib3.disable_warnings()

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

from bs4 import BeautifulSoup



class NeterraProxy(object):

    def __init__(self, username, password, app_dir):
        self.username = username
        self.password = password
        #self.cookieJar = cookielib.CookieJar()
        self.session = requests.Session()
        self.expireTime = 0
        self.app_dir = app_dir
        #client 
        script_dir = os.path.dirname(__file__)
        self.channelsJson = json.load(open(script_dir + '/channels.json'))
    

        
    def checkAuthentication(self):
        now = int(time.time() * 1000)
        if now > self.expireTime:
            self.authenticate2()
    
    def authenticate2(self):
        token = ""
        logged = False
        self.session.cookies.clear()
        url="https://www.neterra.tv/sign-in"
        try:
            r = self.session.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            logger.info(soup)
            element = soup.find(attrs={"name" : "_token"})
            token = element["value"]
        except requests.exceptions.RequestException as err:
            logger.exception("message")
            sys.exit(1)

        formBody = {"username": self.username, \
                    "password": self.password, \
                    "_token": token}
        try:
            r2 = self.session.post(url, data = formBody)
            logged = self.username in r2.content
        except requests.exceptions.RequestException as err:
            logger.exception("message")
            sys.exit(1)   

        if logged:
            self.expiretime = int(time.time() * 1000) + 28800000
        return logged

    def authenticate(self):
        logger.info('authenticating...')
        logged = False
        self.session.cookies.clear()
        url = "http://www.neterra.tv/user/login_page"
        formBody = {"login_username": self.username, \
                    "login_password": self.password, \
                    "login" : "1", \
                    "login_type" : "1"}
        try:
            r = self.session.post(url, data = formBody) #the session now contains the cookies provided in .cookies
            logged = "var LOGGED = '1'" in r.content
        except requests.exceptions.RequestException as err:
            logger.exception("message")
            sys.exit(1)
            
        if logged:
            self.expiretime = int(time.time() * 1000) + 28800000
        return logged
    
    def getM3U82(self):
        r = self.session.get('https://www.neterra.tv/live')
        soup = BeautifulSoup(r.content, 'html.parser')
        channelsPlaylistElement = soup.find("ul",{"class" : "playlist-items"})
        
        from cStringIO import StringIO
        sb = StringIO()
        sb.write("#EXTM3U\n")

        for li in channelsPlaylistElement.findAll('li', attrs={'class': None}):
            channel = li.find('a', {"class" : "playlist-item"})
            chanName = channel.attrs["title"]
            chanId = li.find("div", {"class" : "js-pl-favorite playlist-item__favorite"}) \
                                    .attrs["data-id"]
            if chanId in self.channelsJson:
                tvgId = self.channelsJson[chanId]["tvg-id"]
                tvgName = self.channelsJson[chanId]["tvg-name"]
                group = self.channelsJson[chanId]["group"]
                logo = self.channelsJson[chanId]["logo"]
                #print chanName + " : " + tvgId
            else:
                tvgId = ""
                tvgName = ""
                group = ""
                logo = ""
                #print chanName + " : not found"
            chdata = u"#EXTINF:-1 tvg-id=\"{0}\" tvg-name=\"{1}\" tvg-logo=\"{2}\" group-title=\"{3}\", {4} \n " \
                            .format(tvgId, tvgName,logo, group, chanName)
            link = "http://{0}/playlist.m3u8?ch={1}\n" \
                            .format(self.host, chanId)
            sb.write(chdata.encode("utf-8"))
            sb.write(link)     

        return sb.getvalue() 
    
    def getM3U8(self):
        r = self.session.get('http://www.neterra.tv/content/live')
        import json
        from cStringIO import StringIO
        sb = StringIO()
        sb.write("#EXTM3U\n")
        for channel in r.json()['tv_choice_result']:
            #issues_name = channel[0]['issues_name'].encode("utf-8")
            issues_name = channel[0]['issues_name']
            issues_id = channel[0]['issues_id']
            tvg_id = channel[0]['product_epg_media_id']
            tvg_name = channel[0]['media_file_tag']
            tvg_logo = channel[0]['product_big_pic']
            group_id = channel[0]['product_group_id']
            chdata = u"#EXTINF:-1 tvg-id=\"{0}\" tvg-name=\"{1}\" tvg-logo=\"{2}\" group-id=\"{3}\",{4} \n " \
                            .format(tvg_id, tvg_name,'', group_id, issues_name)
            link = "http://{0}/playlist.m3u8?ch={1}&name={2}\n".format(self.host, issues_id, tvg_name)
            sb.write(chdata.encode("utf-8"))
            sb.write(link)
        
        # import io
        # with io.open('playlist.m3u8', 'w', encoding='utf8') as text_file:
        #     text_file.write(unicode(str(sb)))
        
        return sb.getvalue()     

    def __getStream2(self, chanId):
        self.checkAuthentication()
        playUrl = "https://www.neterra.tv/live/play/" + str(chanId)
        sr = self.session.get(playUrl)
        return sr.json()

    def __getStream(self, issueId):
        self.checkAuthentication()
        data = {'issue_id':issueId, 'quality':'0', 'type':'live'}
        sr = self.session.post('http://www.neterra.tv/content/get_stream', data=data)
        
        # playLinkJson = sr.json()
        # import json, io
        # with io.open('playLinkJson.json','w',encoding="utf-8") as outfile:
        #     outfile.write(unicode(json.dumps(playLinkJson, ensure_ascii=False)))
        
        return sr.json()

    def getPlayLink2(self, chanId):
        playLinkJson=self.__getStream2(chanId)
        import json, io
        # with io.open(self.script_dir + '/playLinkJson.json','w',encoding="utf-8") as outfile:
        #      outfile.write(unicode(json.dumps(playLinkJson, ensure_ascii=False)))
        link = playLinkJson["link"]
        #link = playLinkJson["url"]["play"]
        return link


    def getPlayLink(self, issueId):
        playLinkJson = self.__getStream(issueId)
        raw_link = playLinkJson['play_link']
        # #Cleanup DVR features in live stream that were causing problems for some channels
        # clean_link = raw_link.replace(':443','').replace('DVR&','').replace('/dvr','/live')
        # return clean_link
        return raw_link



