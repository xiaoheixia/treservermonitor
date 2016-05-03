#!/usr/bin/env python
#coding:UTF-8
import os
import sys
import subprocess
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

def main(argv):
    #获取当前目录
    home = os.getcwd()
    conffile = '/conf/pmon.conf'
    f = open(""+home+"/"+conffile+"",'r')

    #获取SERVER清单
    serverlist = f.readlines()
    f.close()
    
    #获取删除几天前的日志
    #使用find命令，+1表示1*24+24以前，+0表示0*24+24以前，1表示1*24+24到24之间，0表示0*24+24到0之间，-1表示0*24+24以内，甚至未来时间
    dayago = sys.argv[1]
    #daydel = datetime.date.today() - datetime.timedelta(days=dayago)
    #print daydel 

    for i in range(0,len(serverlist)):
        dir = os.path.expanduser('~')
        servername = serverlist[i].split(";")[0]
        serverdir = ""+dir+"/"+servername+"/log/"
        shelldir = ""+dir+"/"+servername+"/shell/png*"
        subprocess.Popen("find "+serverdir+" -mtime +"+dayago+" >>"+home+"/logs/del.log", shell=True,stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen("find "+shelldir+" -mtime +"+dayago+" >>"+home+"/logs/del.log", shell=True,stdout=subprocess.PIPE).communicate()[0]
        delfile = open(""+home+"/logs/del.log",'r')
        dellist = delfile.readlines()
        for j in range(0,len(dellist)):
            rmfile = dellist[j].split("\n")[0]
            subprocess.Popen("bin/srm "+rmfile+"", shell=True,stdout=subprocess.PIPE).communicate()[0]
        delfile.close()
        subprocess.Popen(">"+home+"/logs/del.log", shell=True,stdout=subprocess.PIPE).communicate()[0]

if __name__ == '__main__':
    main(sys.argv)
