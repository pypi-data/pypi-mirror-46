# -*- coding: UTF-8 -*-
import platform,os,time,re,requests,shadowsocks

class changeip(object):
    def __init__(self,server_ip, server_port, server_password, server_method):
        self.ip,self.port,self.password,self.method = server_ip,server_port,server_password,server_method
        self.os_type = platform.system()
        self.path = 'C:/ss-hzy'
        if self.os_type == 'Linux':
            self.path = '/opt/ss-hzy'
        self.download()
        self.dochange()
        print("change ip to {}".format(self.ip))

    def download(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        file_list = ['Shadowsocks.exe','gui-tpl.json','ss-local.json']
        for filename in file_list:
            file = self.path +'/'+ filename
            if not os.path.exists(file):
                url = 'http://47.107.168.51/ssclient/'+filename
                r = requests.get(url)
                with open(file, "wb") as code:
                    code.write(r.content)

    def start_exe(self,exe_file_path):  # 启动程序,等待10秒
        # win32api.ShellExecute(0, 'open', exe_file_path, '', '', 1)
        os.startfile(exe_file_path)
        time.sleep(5)  # 等待程序完全开启

    def quit_exe(self,exe_file_name):#关闭程序,等待10秒
        os.popen("taskkill /F /IM "+exe_file_name)
        time.sleep(5)#等待程序完全关闭

    def start_window(self):#Windows下切换IP
        self.quit_exe("Shadowsocks.exe")
        tfile = open(self.path+"/gui-tpl.json","r")
        config_file = open(self.path+"/gui-config.json","w")
        for line in tfile.readlines():
            server_ip_req = re.compile('server\W+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            server_port_req = re.compile('server_port\W+(\d+)')
            server_password_req = re.compile('password\W+"(.*?)"')
            server_method_req = re.compile('method\W+"(.*?)"')
            if server_ip_req.findall(line):
                line = line.replace(str(server_ip_req.findall(line)[0]), str(self.ip))
            if server_port_req.findall(line):
                line = line.replace(str(server_port_req.findall(line)[0]), str(self.port))
            if server_password_req.findall(line):
                line = line.replace(str(server_password_req.findall(line)[0]), str(self.password))
            if server_method_req.findall(line):
                line = line.replace(str(server_method_req.findall(line)[0]), str(self.method))
            config_file.write(line)
        config_file.close()
        tfile.close()
        self.start_exe(self.path+ '/Shadowsocks.exe')

    def start_linux(self):#Linux系统切换IP
        cur_path = os.getcwd()
        configfile = self.path + '/ss-local.json'
        os.system('sslocal -c {} -d stop'.format(configfile))
        file_data = ''
        with open(self.path+'/ss-local.json','r',encoding='utf-8') as f:
            for line in f:
                server_ip_req = re.compile('server\W+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                server_port_req = re.compile('server_port\W+(\d+)')
                server_password_req = re.compile('password\W+"(.*?)"')
                server_method_req = re.compile('method\W+"(.*?)"')
                if server_ip_req.findall(line):
                    line = line.replace(str(server_ip_req.findall(line)[0]), str(self.ip))
                if server_port_req.findall(line):
                    line = line.replace(str(server_port_req.findall(line)[0]), str(self.port))
                if server_password_req.findall(line):
                    line = line.replace(str(server_password_req.findall(line)[0]), str(self.password))
                if server_method_req.findall(line):
                    line = line.replace(str(server_method_req.findall(line)[0]), str(self.method))
                file_data += line
        with open(self.path+'/ss-local.json', 'w', encoding='utf-8') as f:
            f.write(file_data)

        os.system('sslocal -c {} -d start'.format(configfile))
        os.system('export http_proxy="127.0.0.1:8118"')
        os.system('export https_proxy="127.0.0.1:8118"')

    def dochange(self):#判断系统切换IP
        if self.os_type=="Windows":#Windows系统
            self.start_window()
        elif self.os_type=="Linux":#Linux系统
            self.start_linux()

if __name__ == '__main__':
    server_ip, server_port, server_password, server_method = '144.34.147.67','39877','TEK63B','aes-256-cfb'
    changeip(server_ip, server_port, server_password, server_method)

