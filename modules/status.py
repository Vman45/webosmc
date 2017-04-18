import status_functions
import json

def get_status():
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

    cpufrequency=str(status_functions.getCpuFrequency()/1000000)+" Mhz"
    
    for d in disk:
        if d['mountpoint']=='/':
            freespace=d['free']

    uptime=status_functions.getUptime(True)
    ip = status_functions.getIP()
    content={'freespace':freespace,'cpufrequency':cpufrequency,'uptime':uptime,'loadavg':loadavg,'ip':ip,'hostname':hostname,'cpu':cpu,'numcpu':numcpu,'cpuusage':cpuusage,'disk':disk,'temperature':temperature,'memory':memory}	
    return json.dumps(content)
    #if http_context.suburl=='getinfo' :
    #    return WebStructure.HttpContext(statuscode=200,content=json.dumps(content), template=None, mimetype='text/html')
    #return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')
