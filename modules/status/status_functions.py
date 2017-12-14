# coding: utf-8
import psutil
import subprocess
import socket
import os
import platform
import time
import datetime
from netifaces import interfaces, ifaddresses, AF_INET
from modules.webConfig import launch_process
from flask import current_app as app

def getProcess(LstProcName,cpumin):
    iter = psutil.process_iter()
    allprocesses = ListProcess(iter, cpumin)
    iter = psutil.process_iter()
    processes = getProcessStatus(LstProcName, iter)
    return allprocesses, processes


def getProcessStatus(LstProcName, iter):
    S = {}
    procs = []
    procsStatus = []
    # app.logger.debug('test %s' %LstProcName)
    for p in iter:
        try:
            p.dict = p.as_dict(['pid', 'memory_percent', 'cpu_percent',
                                'name', 'status','create_time'])
            procs.append(p.dict)
        except psutil.NoSuchProcess:
            app.logger.debug('error on p : %s' %p)
            pass
        except:
            app.logger.debug('unknown error on path %s' %path)
    for item in LstProcName:
        for name, path in LstProcName[item].items():
            try:
                procsStatus="OFF"
                lstPID = int(subprocess.check_output(["pidof",path]).replace('\n',''))
                # app.logger.debug('Info process %s   PID=%s' %(path,lstPID))
                for p in procs:
                    if p['pid'] == lstPID:
                        createTime = p['create_time']
                        createTime = datetime.datetime.fromtimestamp(createTime).strftime("%Y-%m-%d %H:%M:%S")
                        p['create_time'] = createTime
                        procsStatus = p
                        # app.logger.debug('procs %s' %procsStatus)
            except:
                pass
            S[item] = {'name' : name ,'lstPID': procsStatus}
    # app.logger.debug('retour=%s' %S)
    return S

def ListProcess(iter, cpumin=0):
    procs = []
    procs_status = {}
    item =0
    for p in iter:
        try:
            p.dict = p.as_dict(['pid','memory_percent','cpu_percent',
                                'name', 'status', 'create_time'])
            try:
                procs_status[p.dict['status']] += 1
            except KeyError:
                procs_status[p.dict['status']] = 1
        except psutil.NoSuchProcess:
            pass
        else:
            AddVal = True
            if cpumin > 0:
                if p.dict['cpu_percent'] <= cpumin:
                    AddVal = False
            if AddVal == True:    
                createTime = p.dict['create_time']
                createTime = datetime.datetime.fromtimestamp(createTime).strftime("%Y-%m-%d %H:%M:%S")
                p.dict['create_time'] = createTime
                item+=1
                procs.append(p.dict)
    # return processes sorted by CPU percent usage
    processes = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)
    return processes

def infoNetwork():
    Tab = psutil.net_io_counters(pernic=True)
    TabRet = {}

    for name in list(Tab.keys()):
        p = Tab[name]
        try:
            IP =  ifaddresses(name)[AF_INET][0]['addr']
        except:
            IP = ""
            pass
        TabRet[name] = {'ip' : IP, 'bytes_sent' : getDisplayValue(p.bytes_sent),'bytes_recv':getDisplayValue(p.bytes_recv),'bytes_sent_raw' : p.bytes_sent,'bytes_recv_raw': p.bytes_recv}        
    return TabRet
    
def getHostName():
    return socket.gethostname()

def getCpu():
    return psutil.cpu_times()

def getCpuPercent():
    cpu=getCpu()
    total= cpu.user + cpu.nice + cpu.system + cpu.idle + cpu.iowait + cpu.irq + cpu.softirq

    user = int(100*cpu.user / total)
    nice = int(100*cpu.nice / total)
    system = int(100*cpu.system / total)
    idle = int(100*cpu.idle / total)
    iowait =  int(100*cpu.iowait / total)
    irq = int(100*cpu.irq / total)
    softirq = int(100*cpu.softirq / total)

    return {'user':user,'nice':nice,'system':system,'idle':idle,'iowait':iowait,'irq':irq,'softirq':softirq }


def getNumCpu():
    return psutil.cpu_count()

def getCPUusage():
    return psutil.cpu_percent(percpu=True)

def getPartitions():
    return psutil.disk_partitions()    

def getDiskUsage(mountpoint):
    return psutil.disk_usage(mountpoint)

def getMemory():
    memory=psutil.virtual_memory()

    total = getDisplayValue(memory.total)
    available = getDisplayValue(memory.available)
    availableraw=memory.available
    
    used = getDisplayValue(memory.total-memory.available)
    usedraw = memory.total-memory.available
    free = getDisplayValue(memory.free)
    freeraw = memory.free
    percent = int(memory.percent)

    return {'total':total,'available':available,'availableraw':availableraw,'used':used,'usedraw':usedraw,'free':free,'freeraw':freeraw,'percent':percent} #,'buffers':buffers,'bufferraw':bufferraw,'swfree':swfree,'swtotal':swtotal,'swpercent':swpercent}
    
def getUptime(text=False):
    try:
        bt=int(time.time()-psutil.boot_time())
    except:
        bt=0
    if not text:
        return bt
    day=int(bt/86400)
    bt-=day*86400
    hour=int(bt/3600)
    bt-=hour*3600
    minute=int(bt/60)
    seconde=int(bt-minute*60)
    return "%i jours %i:%i:%i" % (day,hour,minute,seconde)


def getTemperature():
    if platform.system()[:3] == 'Win':
        return 42
    else:
        process = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        output, _error = process.communicate()
        return str(output.replace('temp=','')[:4])
    
def getCpuFrequency():
    ret = psutil.cpu_freq()
    return {'current':ret[0],'min':ret[1],'max':ret[2]}

def getDisplayValue(value):
    if value>(1024*1024*1024):
        return str(int(value/(1024*1024*1024)))+" Gb"
    if value>(1024*1024):
        return str(int(value/(1024*1024)))+" Mb"
    if value>(1024):
            return str(int(value/(1024)))+" kb"
    return str(int(value))+" b"

def getDiskSummary():
    summary=[]
    partitions=getPartitions()
    for partition in partitions:
        device=partition.device
        mountpoint=partition.mountpoint
        fstype=partition.fstype
        
        space=getDiskUsage(mountpoint)
        total= getDisplayValue(space.total)
        free = getDisplayValue(space.free)
        used = getDisplayValue(space.used)
        totalraw= space.total
        freeraw = space.free
        usedraw = space.used
        percent = int(space.percent)
        summary.append({ 'device':device,'mountpoint':mountpoint,'fstype':fstype,'total':total,'free':free,'used':used,'totalraw':totalraw,'freeraw':freeraw,'usedraw':usedraw,'percent':percent})

    return summary

def getLoadAvg():
    tab=os.getloadavg()
    return {'la1':tab[0],'la2':tab[1],'la3':tab[2]}

def getInfoVersion(LstInfos):
    LstInfosRet = []
    for key,info in LstInfos.items():
        for name,value in info.items():
            ret = launch_process(value)
            output = ret['output'].replace('\n','<br>')
            LstInfosRet.append({'name':name,'value':output})
    return LstInfosRet
