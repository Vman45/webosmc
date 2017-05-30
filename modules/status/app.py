# coding: utf-8
import modules.status.status_functions as status_functions
import json

def get_status(LstProcName):
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

    cpufrequency=status_functions.getCpuFrequency()+" Mhz"
    
    for d in disk:
        if d['mountpoint']=='/':
            freespace=d['free']

    uptime=status_functions.getUptime(True)
    ip = str(status_functions.getIP()) + '\n' +  str(status_functions.infoNetwork())
    processes = status_functions.getProcessStatus(LstProcName)
    allprocesses = status_functions.ListProcess()
    content={'allprocesses':allprocesses,'processes':processes,'freespace':freespace,'cpufrequency':cpufrequency,'uptime':uptime,'loadavg':loadavg,'ip':ip,'hostname':hostname,'cpu':cpu,'numcpu':numcpu,'cpuusage':cpuusage,'disk':disk,'temperature':temperature,'memory':memory}	
    return content