
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket,ssl,urllib,os
import sys,re,string
import ystockquote
import HTMLParser
reload(sys)  
sys.setdefaultencoding('utf8') 

def rhbzsearch(keyword):
    url = 'https://bugzilla.redhat.com/buglist.cgi?order=bug_id DESC&quicksearch=%s' % keyword
    wp = urllib.urlopen(url)
    output = wp.read()
    pattern = re.compile('<tr id=\"(.*?)</tr>',re.DOTALL)
    statuspattern = re.compile('bz_status_(.*?) ')
    bugpattern = re.compile('<a href=\"show_bug.cgi\?id=([0-9]*)\">(.*?)</a>')
    res = ''
    i = 0
    match = pattern.findall(output)
    for tritem in match:
        i = i + 1
        bugstatus = statuspattern.search(tritem).group(1)
        bugid = bugpattern.search(tritem).group(1)
        bugtitle = bugpattern.search(tritem).group(2)
        #res = res + bugstatus.strip() + ' ' + bugid.strip() + ' ' + bugtitle.strip() + ';\n'
        res = res + '<a href="https://bugzilla.redhat.com/show_bug.cgi?id=' + bugid.strip() + '">' + bugstatus.strip() + '&nbsp; ' + bugid.strip() + '&nbsp; ' + bugtitle.strip() + '<br />'
        if i>= 5:
            return res
    return res

def kernelsearch(keyword):
    url = 'https://bugzilla.kernel.org/buglist.cgi?order=bug_id DESC&quicksearch=%s' % keyword
    wp = urllib.urlopen(url)
    output = wp.read()
    pattern = re.compile('<tr id=\"(.*?)</tr>',re.DOTALL)
    statuspattern = re.compile('bz_([A-Z]*) ')
    bugpattern = re.compile('<a href=\"show_bug.cgi\?id=([0-9]*)\">(?![0-9]{1,})(.*?)</a>')
    res = ''
    i = 0
    match = pattern.findall(output)
    for tritem in match:
        i = i + 1
        bugstatus = statuspattern.search(tritem).group(1)
        bugid = bugpattern.search(tritem).group(1)
        bugtitle = bugpattern.search(tritem).group(2)
        #res = res + bugstatus.strip() + ' ' + bugid.strip() + ' ' + bugtitle.strip() + ';\n'
        res = res + '<a href="https://bugzilla.kernel.org/show_bug.cgi?id=' + bugid.strip() + '">' + bugstatus.strip() + '&nbsp; ' + bugid.strip() + '&nbsp; ' + bugtitle.strip() + '<br />'
        if i>= 5:
            return res
    return res
def savetohtml(keyword,content):
    if os.path.exists("bughtml"):
        pass
    else:
        os.mkdir("bughtml")
    filename = "bughtml/%s.html" % keyword 
    file_object = open(filename, 'w')
    file_object.write(content)
    file_object.close( )
    return 'http://192.168.211.6/bugsearch/%s.html' % keyword
