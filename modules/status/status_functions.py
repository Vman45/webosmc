import psutil
import subprocess
import socket
import os
import time
import datetime
from netifaces import interfaces, ifaddresses, AF_INET

def getProcessStatus(LstProcName):
    S = {}
    for item in LstProcName:
        for name, path in LstProcName[item].items():
                try:
                    lstPID = subprocess.check_output(["pidof",path])
                except:
                    lstPID = ""
                    pass
                S[item] = {'name' : name ,'lstPID': lstPID}
    return S

def ListProcess(cpumin=0):
    S = {}
    iter = psutil.process_iter()
    if cpumin > 0:
        pslist = psutil.get_process_list()
        iter = filter( process.get_cpu_percent() > cpumin, pslist )
    item =0
    for p in iter:
        S[item] = p.as_dict(attrs=['name','pid','cpu_times','cpu_percent','create_time','status'])
        S[item]['create_time'] = datetime.datetime.fromtimestamp(S[item]['create_time']).strftime("%Y-%m-%d %H:%M:%S")
        item+=1
        # with p.oneshot():
        #   S[item] = {'name' : p.name ,'PID': p.pid(),'cpu_times':p.cpu_times(),'cpu_percent':p.cpu_percent(),'create_time':p.create_time(), 'status': p.status()}
    return S

def infoNetwork():
    return  psutil.net_io_counters(pernic=True)
    # {'lo': snetio(bytes_sent=547971, bytes_recv=547971, packets_sent=5075, packets_recv=5075, errin=0, errout=0, dropin=0, dropout=0),
    # 'wlan0': snetio(bytes_sent=13921765, bytes_recv=62162574, packets_sent=79097, packets_recv=89648, errin=0, errout=0, dropin=0, dropout=0)}
    
def getHostName():
    return socket.gethostname()

def getIP():
    ip_list = []
    for interface in interfaces():
        try:
            for interface in ifaddresses(interface)[AF_INET]:
                if not interface['addr'].startswith("127."):
                    ip_list.append(interface['addr'])
        except:
            pass
    return ip_list

#    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]

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
    process = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _error = process.communicate()
    return str(output.replace('temp=','')[:4])
    
    # ret = psutil.cpu_temperature()
    # return str(ret)
    
def getCpuFrequency():
    ret = psutil.cpu_freq()
    return str(ret)

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
