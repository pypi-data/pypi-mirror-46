# -*- coding: UTF-8 -*-
import platform,os,time,re

def start_exe(exe_file_path):  # 启动程序,等待10秒
    # win32api.ShellExecute(0, 'open', exe_file_path, '', '', 1)
    os.startfile(exe_file_path)
    time.sleep(3)  # 等待程序完全开启

def quit_exe(exe_file_name):#关闭程序,等待10秒
    os.popen("taskkill /F /IM "+exe_file_name)
    time.sleep(3)#等待程序完全关闭

def start_shadowsocks(server_ip, server_port, server_password, server_method):#Windows下切换IP
    #将新IP写入配置文件
    quit_exe("Shadowsocks.exe")  # 关闭vpn程序
    print("启动Shadowsocks ")
    f1 = open("vpn/gui-config-tpl.json","r")
    f2 = open("vpn/gui-config.json","w")
    for line in f1.readlines():
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
        f2.write(line)
    f1.close()
    f2.close()
    cur_path = os.getcwd()
    os.startfile(cur_path+'/vpn/Shadowsocks.exe')
    time.sleep(10)  # 等待程序完全开启

def start_ssr(server_ip, server_port, server_password, server_method):#Linux系统切换IP
    file_data = ''
    with open('/opt/shadowsocksr/user_config.json','r',encoding='utf-8') as f:
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
    with open('/opt/shadowsocksr/user_config.json', 'w', encoding='utf-8') as f:
        f.write(file_data)
    os.system('export http_proxy="127.0.0.1:8118"')
    os.system('export https_proxy="127.0.0.1:8118"')
    os.system('sh /opt/runing.sh')


def dochange(server_ip, server_port, server_password, server_method):#判断系统切换IP
    if platform.system()=="Windows":#Windows系统
        start_shadowsocks(server_ip, server_port, server_password, server_method)  # Windows下切换IP
    elif platform.system()=="Linux":#Linux系统
        start_ssr(server_ip, server_port, server_password, server_method)  # Linux系统切换IP


if __name__ == '__main__':
    server_ip, server_port, server_password, server_method = '144.34.147.67','39877','TEK63B','aes-256-cfb'
    dochange(server_ip, server_port, server_password, server_method)