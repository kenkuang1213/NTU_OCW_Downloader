#!/usr/bin/env python
# coding:utf-8
import argparse
import mechanize
from progressbar import ProgressBar, Percentage, Bar
import re
from BeautifulSoup import BeautifulSoup


class Downloader:
    br = mechanize.Browser()

    def __init__(self, strurl):
        self.br.set_handle_robots(False)  # ignore robots
        self.br.open(strurl)

    def findVideo(self):
        br = self.br
        return list(br.links(url_regex='.mp4'))[0]

    def downloadVideo(self, link):
        br = self.br
        br.follow_link(link)
        file_name = re.findall(
            "filename=\"(.*)\"",
            br.response().info()['Content-Disposition'])[0]
        file_size = int(br.response().info()['Content-Length'])
        f = open(file_name, 'wb')
        bar = ProgressBar(
            widgets=[
                Percentage(),
                Bar()],
            maxval=file_size).start()
        # print self.download_url
        # self.br.follow_link(self.download_url)
        target = br.response()
        print "Downloading " + file_name
        MB = 1024*1024
        for i in range(0, file_size, MB):
            buffer = target.read(MB)
            f.write(buffer)
            bar.update(i)
        if file_size % MB > 0:
            buffer = target.read(file_size % MB)
            f.write(buffer)
        bar.finish()
        f.close()

    def close(self):
        self.br.close()


class ClassFinder:
    br = mechanize.Browser()

    def __init__(self, strurl):
        self.br.set_handle_robots(False)  # ignore robots
        self.br.open(strurl)
        self.strulr = strurl

    def findCourse(self):
        br = self.br
        s = BeautifulSoup(br.response().get_data())
        divs = s.findAll(
            'div', {
                "class": "AccordionPanelTab", "style": "cursor: pointer;"})
        courses = []
        for i in divs:
            courses.append(
                re.findall(
                    "location.href=\'(.*)\'",
                    i['onclick'])[0].encode(
                    'ascii',
                    "ignore"))
        return courses

    def close(self):
        self.br.close()

    def __exit__(self, type, msg, traceback):
        self.close()
        return False

    def __enter__(self):
        return self
if __name__ == '__main__':
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs=1)
    # parser.add_argument('password',nargs=1)
    args = parser.parse_args()
    with ClassFinder(args.url[0]) as cf:
        courses = cf.findCourse()
        for cr in courses:
            dw = Downloader(str(cr))
            link = dw.findVideo()
            dw.downloadVideo(link)
            dw.close()
