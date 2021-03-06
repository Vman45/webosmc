# coding: utf-8
import modules.status.status_functions as status_functions
import modules.status.phone_home as phone_home
import json

def get_status(LstProcName,cpumin,RechVersion,LstIPs):
    cpu=status_functions.getCpuPercent()
    numcpu=status_functions.getNumCpu()
    cpuusage=status_functions.getCPUusage()
    average=0
    count=0
    for i in cpuusage:
        average+=i
        count+=1
    average=int(average/count)
    cpuusage={'average':average,'values':cpuusage}
    disk=status_functions.getDiskSummary()
    temperature=status_functions.getTemperature()
    memory=status_functions.getMemory()

    loadavg=status_functions.getLoadAvg()	
    hostname=status_functions.getHostName()

    cpufrequency=status_functions.getCpuFrequency()
    
    for d in disk:
        if d['mountpoint']=='/':
            freespace=d['free']

    uptime=status_functions.getUptime(True)
    ip = {'detail':status_functions.infoNetwork()}
    allprocesses, processes = status_functions.getProcess(LstProcName,cpumin)
    InfoVersion = status_functions.getInfoVersion(RechVersion)
    Statuts_Phone = phone_home.returnState(LstIPs)
    content={'InfoVersion':InfoVersion,'allprocesses':allprocesses,'processes':processes,'freespace':freespace,'cpufrequency':cpufrequency,'uptime':uptime,'loadavg':loadavg,'ip':ip,'hostname':hostname,'cpu':cpu,'numcpu':numcpu,'cpuusage':cpuusage,'disk':disk,'temperature':temperature,'memory':memory,'Statuts_Phone':Statuts_Phone}	
    return content
