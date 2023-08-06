# -*- coding: UTF-8 -*-
import platform,os,time,re,requests,shadowsocks

path = 'ssr'
if not os.path.exists(path):
    os.mkdir(path)
file_list = ['Shadowsocks.exe','gui-config.json','ss-local.json']
for filename in file_list:
    file = path +'/'+ filename
    if not os.path.exists(file):
        url = 'http://47.107.168.51/ssclient/'+filename
        r = requests.get(url)
        with open(file, "wb") as code:
            code.write(r.content)


def start_exe(exe_file_path):  # 启动程序,等待10秒
    # win32api.ShellExecute(0, 'open', exe_file_path, '', '', 1)
    os.startfile(exe_file_path)
    time.sleep(3)  # 等待程序完全开启

def quit_exe(exe_file_name):#关闭程序,等待10秒
    os.popen("taskkill /F /IM "+exe_file_name)
    time.sleep(3)#等待程序完全关闭

def start_window(server_ip, server_port, server_password, server_method):#Windows下切换IP
    quit_exe("Shadowsocks.exe")
    config_file = open(path+"/gui-config.json","w")
    for line in config_file.readlines():
        server_ip_req = re.compile('server\W+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        server_port_req = re.compile('server_port\W+(\d+)')
        server_password_req = re.compile('password\W+"(.*?)"')
        server_method_req = re.compile('method\W+"(.*?)"')
        if server_ip_req.findall(line):
            line = line.replace(str(server_ip_req.findall(line)[0]), str(server_ip))
        if server_port_req.findall(line):
            line = line.replace(str(server_port_req.findall(line)[0]), str(server_port))
        if server_password_req.findall(line):
            line = line.replace(str(server_password_req.findall(line)[0]), str(server_password))
        if server_method_req.findall(line):
            line = line.replace(str(server_method_req.findall(line)[0]), str(server_method))
        config_file.write(line)
    config_file.close()
    cur_path = os.getcwd()
    #os.startfile(cur_path+'/vpn/Shadowsocks.exe')
    os.startfile(path + '/Shadowsocks.exe')
    time.sleep(10)  # 等待程序完全开启

def start_linux(server_ip, server_port, server_password, server_method):#Linux系统切换IP
    file_data = ''
    with open(path+'/ss-local.json','r',encoding='utf-8') as f:
        for line in f:
            server_ip_req = re.compile('server\W+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            server_port_req = re.compile('server_port\W+(\d+)')
            server_password_req = re.compile('password\W+"(.*?)"')
            server_method_req = re.compile('method\W+"(.*?)"')
            if server_ip_req.findall(line):
                line = line.replace(str(server_ip_req.findall(line)[0]), str(server_ip))
            if server_port_req.findall(line):
                line = line.replace(str(server_port_req.findall(line)[0]), str(server_port))
            if server_password_req.findall(line):
                line = line.replace(str(server_password_req.findall(line)[0]), str(server_password))
            if server_method_req.findall(line):
                line = line.replace(str(server_method_req.findall(line)[0]), str(server_method))
            file_data += line
    with open(path+'/ss-local.json', 'w', encoding='utf-8') as f:
        f.write(file_data)
    os.system('export http_proxy="127.0.0.1:8118"')
    os.system('export https_proxy="127.0.0.1:8118"')
    os.system('sslocal -c shadowsocks.json -d start')


def dochange(server_ip, server_port, server_password, server_method):#判断系统切换IP
    print("切换客户端代理IP ")
    if platform.system()=="Windows":#Windows系统
        start_window(server_ip, server_port, server_password, server_method)  # Windows下切换IP
    elif platform.system()=="Linux":#Linux系统
        start_linux(server_ip, server_port, server_password, server_method)  # Linux系统切换IP


if __name__ == '__main__':
    server_ip, server_port, server_password, server_method = '144.34.147.67','39877','TEK63B','aes-256-cfb'
    dochange(server_ip, server_port, server_password, server_method)
