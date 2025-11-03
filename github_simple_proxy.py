#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的GitHub代理工具
"""

import os
import sys
import ctypes
import time
import webbrowser
import winreg
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 设置标准输出编码
def setup_encoding():
    if hasattr(sys.stdout, 'buffer'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 检查管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 代理服务器列表
PROXIES = [
    ("阿里开发者代理", "47.96.154.23:80"),
    ("阿里CDN代理", "47.104.190.217:80"),
    ("阿里杭州节点", "115.236.96.13:80"),
    ("阿里北京节点", "118.190.205.16:80"),
]

# GitHub页面
GITHUB_DEVICE_LOGIN = "https://github.com/login/device"
GITHUB_DEVICE_CONFIRM = "https://github.com/login/device/confirmation"

# 测试代理连接
def test_proxy(proxy):
    print(f"测试代理: {proxy}")
    
    # 设置环境变量
    os.environ["http_proxy"] = f"http://{proxy}"
    os.environ["https_proxy"] = f"http://{proxy}"
    
    try:
        start_time = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # 测试连接
        print(f"正在连接GitHub...")
        req = Request(GITHUB_DEVICE_LOGIN, headers=headers)
        with urlopen(req, timeout=10) as response:
            status_code = response.status
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            print(f"连接成功!")
            print(f"状态码: {status_code}")
            print(f"响应时间: {response_time:.2f} ms")
            
            # 清除环境变量
            if "http_proxy" in os.environ:
                del os.environ["http_proxy"]
            if "https_proxy" in os.environ:
                del os.environ["https_proxy"]
            
            return True, response_time
    
    except Exception as e:
        print(f"连接失败: {str(e)}")
        
    # 清除环境变量
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        del os.environ["https_proxy"]
    
    return False, 0

# 测试所有代理
def test_all_proxies():
    print("\n开始测试所有代理服务器...")
    print("-" * 50)
    
    working_proxies = []
    
    for name, proxy in PROXIES:
        print(f"\n[{name}]")
        success, response_time = test_proxy(proxy)
        
        if success:
            working_proxies.append((name, proxy, response_time))
    
    print("\n" + "-" * 50)
    print(f"测试完成! 找到 {len(working_proxies)} 个可用代理")
    
    if working_proxies:
        print("\n可用代理列表:")
        for i, (name, proxy, time_ms) in enumerate(working_proxies, 1):
            print(f"{i}. {name} ({proxy}) - {time_ms:.2f} ms")
    
    return working_proxies

# 设置系统代理
def set_system_proxy(proxy):
    print(f"\n设置系统代理: {proxy}")
    
    try:
        # 设置IE代理
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_SET_VALUE
        )
        
        # 启用代理
        winreg.SetValueEx(reg_key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        # 设置代理服务器
        winreg.SetValueEx(reg_key, "ProxyServer", 0, winreg.REG_SZ, proxy)
        # 设置不使用代理的地址
        winreg.SetValueEx(reg_key, "ProxyOverride", 0, winreg.REG_SZ, "<local>")
        winreg.CloseKey(reg_key)
        
        # 刷新系统代理设置
        ctypes.windll.Wininet.InternetSetOptionW(0, 37, 0, 0)
        ctypes.windll.Wininet.InternetSetOptionW(0, 39, 0, 0)
        
        print("代理设置成功!")
        return True
    except Exception as e:
        print(f"设置代理失败: {str(e)}")
        return False

# 禁用系统代理
def disable_system_proxy():
    print("\n禁用系统代理...")
    
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(reg_key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(reg_key)
        
        # 刷新系统代理设置
        ctypes.windll.Wininet.InternetSetOptionW(0, 37, 0, 0)
        ctypes.windll.Wininet.InternetSetOptionW(0, 39, 0, 0)
        
        print("代理已禁用!")
        return True
    except Exception as e:
        print(f"禁用代理失败: {str(e)}")
        return False

# 打开GitHub页面
def open_github():
    print("\n打开GitHub设备登录页面...")
    webbrowser.open(GITHUB_DEVICE_LOGIN)
    webbrowser.open(GITHUB_DEVICE_CONFIRM)

# 主菜单
def main_menu():
    while True:
        print("\n===== GitHub代理工具 =====")
        print("1. 测试所有代理服务器")
        print("2. 设置系统代理")
        print("3. 禁用系统代理")
        print("4. 打开GitHub设备登录页面")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-4): ")
        
        if choice == "1":
            test_all_proxies()
        elif choice == "2":
            if not is_admin():
                print("需要管理员权限来设置系统代理!")
                input("请右键以管理员身份运行此脚本。按Enter键继续...")
                continue
                
            proxy = input("请输入代理地址 (例如: 123.45.67.89:80): ")
            if proxy:
                set_system_proxy(proxy)
        elif choice == "3":
            if not is_admin():
                print("需要管理员权限来禁用系统代理!")
                input("请右键以管理员身份运行此脚本。按Enter键继续...")
                continue
            
            disable_system_proxy()
        elif choice == "4":
            open_github()
        elif choice == "0":
            print("\n感谢使用，再见!")
            break
        else:
            print("无效的选择，请重试")
        
        input("\n按Enter键继续...")

# 主程序
def main():
    setup_encoding()
    
    print("欢迎使用GitHub代理工具")
    print("此工具帮助您通过代理访问GitHub网站")
    
    if not is_admin():
        print("\n注意: 当前未以管理员权限运行")
        print("设置/禁用系统代理功能需要管理员权限")
    
    main_menu()

if __name__ == "__main__":
    main()