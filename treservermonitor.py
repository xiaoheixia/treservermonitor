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
    setname = sys.argv[1]
    monitorname = sys.argv[1].split(",")[3] + '_SERVER'
    iptmp = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
    ip = iptmp[iptmp.find(':')+1:iptmp.find('\n')]
    
    #获得时间变量
    today = datetime.date.today()
    dayago = '1'

    #进程监控
    for i in range(0,len(serverlist)):
        servername = serverlist[i].split(";")[0]
        serverdir = serverlist[i].split(";")[1].split("\n")[0]
        servernum = subprocess.Popen("ps -aux | grep -w "+servername+" | grep -v 'grep' | grep -v 'gdb' |grep -v 'vim' | grep -vE 'srm|rm|vim' | grep -v ' -v' | wc -l", shell=True,stdout=subprocess.PIPE).communicate()[0].split("\n")[0]
        msgtmp = ""+servername+"进程不存在，重启"+servername+"!"
        msg = msgtmp.decode('utf-8').encode('gb2312')
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if servernum == '1':
            os.system(""+home+"/tools/doss -s "+setname+" -i "+monitorname+" -v '0'")
            subprocess.Popen("echo "+str(now)+" "+ip+" "+servername+"进程存在，状态正常！>>"+home+"/logs/monitor.log."+str(today), shell=True,stdout=subprocess.PIPE).communicate()[0]
        else:
            #print "server core"
            os.system("sh "+serverdir+"/start.sh")
            os.system(""+home+"/tools/doss -s "+setname+" -i "+monitorname+" -v '1' -a "+msg+"")
            subprocess.Popen("echo "+str(now)+" "+ip+" "+servername+"进程不存在，已经尝试重新拉起！>>"+home+"/logs/monitor.log."+str(today), shell=True,stdout=subprocess.PIPE).communicate()[0]

    #日志清理
    subprocess.Popen("find "+home+"/logs/monitor* -mtime +"+dayago+" >>"+home+"/logs/logdel.log", shell=True,stdout=subprocess.PIPE).communicate()[0]
    delfile = open(""+home+"/logs/logdel.log",'r')
    dellist = delfile.readlines()
    for j in range(0,len(dellist)):
        rmfile = dellist[j].split("\n")[0]
        subprocess.Popen("bin/srm "+rmfile+"", shell=True,stdout=subprocess.PIPE).communicate()[0]
    delfile.close()
    subprocess.Popen(">"+home+"/logs/logdel.log", shell=True,stdout=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
    main(sys.argv)
