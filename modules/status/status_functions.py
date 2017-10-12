import psutil
import subprocess
import socket
import os
import platform
import time
import datetime
from netifaces import interfaces, ifaddresses, AF_INET
# from flask import Flask
# app = Flask(__name__)

def getProcess(LstProcName,cpumin):
    iter = psutil.process_iter()
    # app.logger.info('Asking authorization auth %s' %iter)
    allprocesses = ListProcess(iter, cpumin)
    processes = getProcessStatus(LstProcName, iter)
    return allprocesses, processes

def getProcessStatus(LstProcName, iter):
    S = {}
    procs = []
    for item in LstProcName:
        for name, path in LstProcName[item].items():
                try:
                    lstPID = int(subprocess.check_output(["pidof",path]).replace('\n',''))
                    # ****** Code non fonctionnel
                    for p in iter:
                        try:
                            p.dict = p.as_dict(['pid', 'memory_percent', 'cpu_percent',
                                                'name', 'status','create_time'])
                        except psutil.NoSuchProcess:
                            pass
                        else:
                            if p.dict['pid'] == lstPID:
                                createTime = p.dict['create_time']
                                createTime = datetime.datetime.fromtimestamp(createTime).strftime("%Y-%m-%d %H:%M:%S")
                                p.dict['create_time'] = createTime
                                procs.append(p.dict)
                    # ****** fin Code non fonctionnel
                    if not procs :
                        procs = lstPID
                except:
                    procs = ""
                    pass
                S[item] = {'name' : name ,'lstPID': procs}
    return S

def ListProcess(iter, cpumin=0):
    procs = []
    procs_status = {}
    item =0
    print('ListProcess : %s' %iter)
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
        IP =  ifaddresses(name)[AF_INET][0]['addr']
        TabRet[name] = {'ip' : IP, 'bytes_sent' : getDisplayValue(p.bytes_sent),'bytes_recv':getDisplayValue(p.bytes_recv)}
    return TabRet
    
def getHostName():
    return socket.gethostname()

# def getIP():
    # ip_list = []
    # for interface in interfaces():
        # try:
            # for interface in ifaddresses(interface)[AF_INET]:
                # if not interface['addr'].startswith("127."):
                    # ip_list.append(interface['addr'])
        # except:
            # pass
    # return ip_list

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
    cached=getDisplayValue(memory.cached)
    cachedraw=memory.cached

    used = getDisplayValue(memory.total-memory.available)
    usedraw = memory.total-memory.available
    percent = int(memory.percent)
    buffers = getDisplayValue(memory.buffers)
    bufferraw = memory.buffers
    free = getDisplayValue(memory.free)
    freeraw = memory.free
    memory=psutil.swap_memory()
    swtotal = getDisplayValue(memory.total)
    swused = getDisplayValue(memory.used)
    swpercent = int(memory.percent)
    swfree = getDisplayValue(memory.free)

    return {'cached':cached,'cachedraw':cachedraw,'usedraw':usedraw,'bufferraw':bufferraw,'freeraw':freeraw,'total':total,'available':available,'used':used,'percent':percent,'buffers':buffers,'free':free,'swfree':swfree,'swtotal':swtotal,'swpercent':swpercent}
    
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
    return "%id %ih %im %is" % (day,hour,minute,seconde)


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
    # return str(ret)

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
        percent = int(space.percent)
        summary.append({ 'device':device,'mountpoint':mountpoint,'fstype':fstype,'total':total,'free':free,'used':used,'percent':percent})

    return summary

def getLoadAvg():
    tab=os.getloadavg()
    return {'la1':tab[0],'la2':tab[1],'la3':tab[2]}
