import pyqrcode, os, sys, time, smtplib, requests, dns.resolver


def qrcode(text, Format):
    pyqrcode.create('%s'%text).svg('%s.%s'%(text, Format), scale=8)

def timeNow():
    return '%s:%s:%s'%(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)

def dateNow():
    return '%s/%s/%s'%(time.localtime().tm_mday ,time.localtime().tm_mon ,time.localtime().tm_year)

def sendgmail(username, password, to, text):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('%s'%username, '%s'%password)
    server.sendmail('%s'%username, '%s'%to, "%s"%text)
    server.close()

def myip():
    resp = requests.get('https://httpbin.org/ip').json()['origin']
    return resp[:resp.find(',')]

def dns(url):
    for server in dns.resolver.query('%s'%url,'NS'):
        return server.target
