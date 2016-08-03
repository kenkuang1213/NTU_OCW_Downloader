#!/usr/bin/env python
#coding:utf-8
import argparse
import mechanize
from progressbar import ProgressBar,Percentage, Bar
import re
import random
import sys
from BeautifulSoup import BeautifulSoup
import Queue as queue
# strUrl= "http://ocw.aca.ntu.edu.tw/ntu-ocw/index.php/ocw/cou/102S116"
class Downloader:
    br = mechanize.Browser()
    def __init__(self, strurl):
        self.br.set_handle_robots(False) # ignore robots
        self.br.open(strurl)

    def findVideo(self):
        br=self.br
        for link in br.links(url_regex='.mp4'):
            br.follow_link(link)
            # br.follow_link(link).read(512)
            # print link.url
            br.response()
            self.file_name = re.findall("filename=\"(.*)\"",br.response().info()['Content-Disposition'])[0]
            self.file_size = int(br.response().info()['Content-Length'])
            self.download_url=link
    def downloadVideo(self):
        f = open(self.file_name, 'wb')
        bar=ProgressBar(widgets=[Percentage(), Bar()], maxval=self.file_size).start()
        # print self.download_url
        # self.br.follow_link(self.download_url)
        target=self.br.response()
        MB=1024*1024
        for i in range(0,self.file_size,MB):
            buffer = target.read(MB)
            f.write(buffer)
            bar.update(i)
        if self.file_size % MB >0 :
            buffer = target.read(self.file_size%MB)
            f.write(buffer)
        bar.finish()
        f.close()
    def close():
        br.close()

if __name__=='__main__':
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    # parser = argparse.ArgumentParser()
    # parser.add_argument('username',nargs=1)
    # parser.add_argument('password',nargs=1)
    # args=parser.parse_args()
    dw=Downloader('http://ocw.aca.ntu.edu.tw/ntu-ocw/index.php/ocw/cou/102S116/1')
    dw.findVideo()
    dw.downloadVideo()
    dw.close()
