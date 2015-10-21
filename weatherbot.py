#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket,ssl,urllib
import sys,re,string
import ystockquote
import HTMLParser
reload(sys)  
sys.setdefaultencoding('utf8') 

network = 'irc.freenode.net'
#network = 'wolfe.freenode.net'
port = 6697
#channel = '#tuna'
channel = '#cafebabe'
ircnick = 'zbadbot'
appkey = '10003'
sign = 'b59bc3ef6191eb9f747dd4e83c99f2a4'
ircsocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc = ssl.wrap_socket(ircsocket)

bdebug = True

def debugprint(str):
    if bdebug:
        print str

def getweather(strsearch):
    debugprint( "Search weather: %s" % strsearch)
    #http://api.k780.com:88/?app=weather.today&weaid=%E6%B7%84%E5%B7%9D&appkey=&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=xml
    url = 'http://api.k780.com:88/?app=weather.today&format=xml&appkey=%s&sign=%s&weaid=%s' % (appkey, sign, strsearch)
    wp = urllib.urlopen(url)
    output = wp.read()
    debugprint(output)
    resweather = ''
    pattern = re.compile('<citynm>(.*?)</citynm>')
    match = pattern.search(output)
    if match:
        city = match.group(1)
        resweather = " %s 今日天气:" % city
    pattern = re.compile('<temp_curr>(.*?)</temp_curr>')
    match = pattern.search(output)
    if match:
        resweather = resweather + "当前温度" + match.group(1) + "摄氏度"
    pattern = re.compile('<temp_high>(.*?)</temp_high>')
    match = pattern.search(output)
    if match:
        resweather = resweather + ";最高温度" + match.group(1) + "摄氏度"
    pattern = re.compile('<temp_low>(.*?)</temp_low>')
    match = pattern.search(output)
    if match:
        resweather = resweather + ";最低温度" + match.group(1) + "摄氏度"
    return resweather
'''    pattern = re.compile('<wind>(.*?)</wind>')
    match = pattern.search(output)
    if match:
        city = match.group(1)
        print "City: %s" % city
    pattern = re.compile('<winp>(.*?)</winp>')
    match = pattern.search(output)
    if match:
        city = match.group(1)
        print "City: %s" % city
'''
'''
<wind>西北风</wind><winp>1级</winp><temp_high>22</temp_high><temp_low>12</temp_low><temp_curr>25</temp_curr>
'''

def getgeneralstock():
    url ='http://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sh000300,s_sz399415,s_sz399006'
    result = ''
    wp = urllib.urlopen(url)
    output = wp.read()

    pattern = re.compile("[\s\S]*?sh000001=\"(.*?),(.*?),[\s\S]*")
    match = pattern.match(output)
    if match:
        result = result + "%s : %s 。" % (pattern.match(output).group(1).decode('gb2312'), pattern.match(output).group(2))
    pattern = re.compile("[\s\S]*?sz399001=\"(.*?),(.*?),[\s\S]*")
    match = pattern.match(output)
    if match:
        result = result + "%s : %s 。" % (pattern.match(output).group(1).decode('gb2312'), pattern.match(output).group(2))
    pattern = re.compile("[\s\S]*?sh000300=\"(.*?),(.*?),[\s\S]*")
    match = pattern.match(output)
    if match:
        result = result + "%s : %s 。" % (pattern.match(output).group(1).decode('gb2312'), pattern.match(output).group(2))
    pattern = re.compile("[\s\S]*?sz399415=\"(.*?),(.*?),[\s\S]*")
    match = pattern.match(output)
    if match:
        result = result + "%s : %s 。" % (pattern.match(output).group(1).decode('gb2312'), pattern.match(output).group(2))
    pattern = re.compile("[\s\S]*?sz399006=\"(.*?),(.*?),[\s\S]*")
    match = pattern.match(output)
    if match:
        result = result + "%s : %s 。" % (pattern.match(output).group(1).decode('gb2312'), pattern.match(output).group(2))
    if result == '':
        return '数据获取失败'
    return result

def getsinastock(strsearch):
    if strsearch == '':
        strsearch = 'GOOG'
    currencysign = '￥'
    debugprint( "Search sina stock: %s" % strsearch )
    url =''
    pgb = re.compile('([A-Za-z]*)$')
    psh = re.compile('.*(60\d{4}).*')
    psz = re.compile('.*([0|3]0\d{4}).*')
    resultpos = 4
    if strsearch.lower().find("tuna") != -1:
        resstock = "Jack MA bought 68kg TUNA with CNY 38888!"
        return resstock
    match = pgb.match(strsearch)
    if match:
        strsearch = match.group(1)
        url = "http://hq.sinajs.cn/?list=gb_%s" % strsearch.lower()
        currencysign = '$'
        resultpos = 2
    match = psh.match(strsearch)
    if match:
        strsearch = match.group(1)
        url = "http://hq.sinajs.cn/?list=sh%s" % strsearch
        currencysign = '￥'
        resultpos = 4
    match = psz.match(strsearch)
    if match:
        strsearch = match.group(1)
        url = "http://hq.sinajs.cn/?list=sz%s" % strsearch
        currencysign = '￥'
        resultpos = 4
    if url == '':
        return "代码'%s'不存在" % strsearch
    wp = urllib.urlopen(url)
    output = wp.read()
    #print output
    resstock = ''
    pattern = re.compile("=\"(.*?),(.*?),(.*?),(.*?),")
    match = pattern.search(output)
    if match:
        resstock = " %s 当前股价:%s%s" % (match.group(1).decode('gb2312'), currencysign, match.group(resultpos))
    return resstock

def getyahoostock(strsearch):
    stockall = ystockquote.get_all(strsearch)
    company = stockall["notes"]
    price = stockall["last_trade_price"]
    pattern = re.compile("<b>(.*?)<")
    match = pattern.search(price)
    if match:
        price = match.group(1)
    resstock = " %s当前股价:$%s" % (company, price)
    return resstock

def getstockold(strsearch):
    if strsearch == '':
        strsearch = 'GOOG'
    print "Search stock: %s" % strsearch
    #url = 'http://api.k780.com:88/?app=weather.today&format=xml&appkey=%s&sign=%s&weaid=%s' % (appkey, sign, strsearch)
    url = 'https://finance.yahoo.com/q?s=%s' % strsearch
    wp = urllib.urlopen(url)
    output = wp.read()
    #print output
    resstock = ''
    stockname = strsearch.upper()
    #pattern = re.compile("<title>%s: Summary for (.*?)- Yahoo! Finance</title>" % stockname)
    pattern = re.compile("title\"><h2>(.*?)[(]%s[)]</h2>" % stockname)
    match = pattern.search(output)
    if match:
        stockname = match.group(1)
    pattern = re.compile("yfs_l84_%s\">(.*?)</span>" % strsearch.upper())
    match = pattern.search(output)
    if match:
        resstock = " %s当前股价:$%s" % (stockname,match.group(1))
    return resstock

def getrhbz(rhbz):
    h = HTMLParser.HTMLParser()
    if rhbz == '':
        return ''
    print "Search rhbz %s" % rhbz
    url = 'https://bugzilla.redhat.com/show_bug.cgi?id=%s' % rhbz
    wp = urllib.urlopen(url)
    output = wp.read()
    bugtitle = ''
    pattern = re.compile("title>(.*?)</title>")
    match = pattern.search(output)
    if match:
        bugtitle = h.unescape(match.group(1)) + " " + url
    return bugtitle

def matchcmd(str,cmd):
    clist = []
    prefix = ['.', '!', '/','！','。', ':.', ':!', ':/',':！',':。']
    for i in prefix:
        clist.append("%s%s" % (i,cmd) )
    if str in clist:
        debugprint ( "!%s command matched" % cmd )
        return True
    return False

def regexbot(spatt, starget):
    if (spatt != '' and starget != ''):
        pattern = re.compile(spatt)
        match = pattern.search(starget)
        if match:
            return match.groups()
        return ''

def dataparse(ircdata):
    dataparts = string.split(ircdata)
    if bdebug:
        print dataparts
    offset = 0
    iCMD = 3
    iPARAM = 4
    if dataparts[0].find(':teleboto!') != -1:
        offset = 1
    if (len(dataparts) >= iPARAM+offset+1 and dataparts[iPARAM+offset] == ircnick and matchcmd(dataparts[iCMD+offset], "bug")):
        irc.send ( u'PRIVMSG %s : 跪了，膝盖中了一箭。。\r\n' % dataparts[2])
        irc.send ( u'PART %s\r\n' % dataparts[2] )
    elif (len(dataparts) >= iPARAM+offset+1 and dataparts[iPARAM+offset] == ircnick and matchcmd(dataparts[iCMD+offset], "halt")):
        irc.send ( u'PRIVMSG %s : 谁动了我的电源。。\r\n' % dataparts[2])
        irc.send ( u'PART %s\r\n' % dataparts[2])
        irc.send ( 'QUIT\r\n' )
        exit(0)
    elif len(dataparts) >= iPARAM+offset+1 and matchcmd(dataparts[iCMD+offset], "join"):
        irc.send ( 'JOIN %s\r\n' % dataparts[iPARAM+offset])
    elif len(dataparts) >= iPARAM+offset+1 and matchcmd(dataparts[iCMD+offset], "weather"):
        weather = getweather(dataparts[iPARAM])
        if weather != '':
            irc.send ( 'PRIVMSG %s : %s\r\n' % (dataparts[2],weather))
        else:
            weather = '这个城市是在火星么？'
            irc.send ( 'PRIVMSG %s : %s\r\n' % (dataparts[2],weather))
    elif len(dataparts) == iPARAM+offset and matchcmd(dataparts[iCMD+offset], "help"):
        irc.send ( 'PRIVMSG %s : * !weather <city>: show the weather of the given city, CHN only; !bug %s: Kick me away; !join <channel>: Invite me to a IRC channel, IRC only;!regex <pattern> <words>: test regular expressions in Python, space is not supported ;!stock <stockcode>: get the price of the stock, or general stock if no param passed.\r\n' % (dataparts[2], ircnick) )
    elif len(dataparts) >= iPARAM+offset and matchcmd(dataparts[iCMD+offset], "bot"):
        irc.send ( 'PRIVMSG %s :喵，是在叫我嘛？\r\n' % dataparts[2] )
    elif len(dataparts) >= iPARAM+offset and matchcmd(dataparts[iCMD+offset], "stock"):
        if len(dataparts)>= iPARAM+offset+1 :
            stock = getsinastock(dataparts[iPARAM+offset])
        else:
            stock = getgeneralstock()
        if stock != '':
            irc.send ( 'PRIVMSG %s : %s\r\n' % (dataparts[2],stock))
    elif len(dataparts) >= iPARAM+offset+2 and matchcmd(dataparts[iCMD+offset], "regex"):
        regexresult = regexbot(dataparts[iPARAM+offset], dataparts[iPARAM+offset+1])
        if regexresult == '':
            regexresult = '匹配失败'
        irc.send ( 'PRIVMSG %s : %s\r\n' % (dataparts[2],regexresult))
    elif len(dataparts) >= iPARAM+offset+1 and matchcmd(dataparts[iCMD+offset], "rhbz"):
        bugtitle = getrhbz(dataparts[iPARAM])
        if bugtitle != '':
            irc.send ( 'PRIVMSG %s : %s\r\n' % (dataparts[2],bugtitle))

def main():
    irc.connect ( ( network, port ) )
    print irc.recv ( 4096 )
    irc.send ( 'NICK %s\r\n' % ircnick )
    irc.send ( 'USER %s %s %s :Python IRC\r\n' % (ircnick, ircnick, ircnick))
    irc.send ( 'JOIN %s\r\n' % channel )
    irc.send ( 'PRIVMSG %s :喵喵~.\r\n' % channel )
    while True:
        data = irc.recv ( 4096 )
        datap = string.split(data)
        print len(datap)
        if data.find ( 'PING' ) != -1:
            irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
        elif ((len(datap)>=4) and (datap[0].find ( ircnick ) == -1 and datap[0].find ( 'MeowBot' ) == -1)):
            dataparse(data)

        #print data
if __name__ == '__main__':
    main()
