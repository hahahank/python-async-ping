
import time
import asyncio
#import subprocess
import platform
import re

ping_result={}

async def ping(host):
    global ping_result
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    command = "ping {0} 1  {1}".format(param, host)
    proc = await asyncio.create_subprocess_shell(
        command,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    regex = re.compile(r'icmp_seq=1 ttl=\d+ time=')
    if(regex.search(str(stdout))):
        print(command, " OK")
        ping_result[host] = True
    else:
        print(command, " Not Found")
        ping_result[host] = False
    return

def genIPRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range


if __name__ == "__main__":
    start = time.time()
    ip_range_start = "172.32.3.1"
    ip_range_end = "172.32.3.254"
    iprange = genIPRange(ip_range_start,ip_range_end)
    ping_task = [ping(ip) for ip in iprange]
    asyncio.run(asyncio.wait(ping_task))
    print(ping_result)
    print(f"time: {time.time() - start} (s)")
