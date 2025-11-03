#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub VPN代理配置工具
"""

import os
import sys
import subprocess
import ctypes
import time
import webbrowser
import winreg
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

class VPNProxyTool:
    """VPN代理工具类"""
    
    # GitHub设备登录页面
    GITHUB_DEVICE_LOGIN = "https://github.com/login/device"
    GITHUB_DEVICE_CONFIRM = "https://github.com/login/device/confirmation"
    
    # 推荐的代理服务器列表
    RECOMMENDED_PROXIES = [
        ("阿里开发者代理", "47.96.154.23:80"),
        ("阿里CDN代理", "47.104.190.217:80"),
        ("阿里杭州节点", "115.236.96.13:80"),
        ("阿里北京节点", "118.190.205.16:80"),
    ]
    
    @staticmethod
    def is_admin():
        """检查是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def run_as_admin():
        """以管理员权限重新运行程序"""
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            ' '.join(sys.argv),
            None,
            1
        )
    
    @staticmethod
    def set_browser_proxy(proxy):
        """设置浏览器代理"""
        print(f"设置浏览器代理: {proxy}")
        
        try:
            # 设置IE代理（其他浏览器通常会使用IE的代理设置）
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
            
            print("✓ 浏览器代理设置成功")
            return True
        except Exception as e:
            print(f"✗ 设置代理失败: {str(e)}")
            return False
    
    @staticmethod
    def disable_browser_proxy():
        """禁用浏览器代理"""
        print("禁用浏览器代理...")
        
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
            
            print("✓ 浏览器代理已禁用")
            return True
        except Exception as e:
            print(f"✗ 禁用代理失败: {str(e)}")
            return False
    
    @staticmethod
    def test_proxy(proxy):
        """测试代理连接"""
        print(f"测试代理: {proxy}")
        
        # 设置测试环境
        os.environ["http_proxy"] = f"http://{proxy}"
        os.environ["https_proxy"] = f"http://{proxy}"
        
        try:
            start_time = time.time()
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            # 测试GitHub设备登录页面
            print(f"正在连接: {VPNProxyTool.GITHUB_DEVICE_LOGIN}")
            req = Request(VPNProxyTool.GITHUB_DEVICE_LOGIN, headers=headers)
            with urlopen(req, timeout=10) as response:
                status_code = response.status
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                print(f"✓ 连接成功!")
                print(f"  状态码: {status_code}")
                print(f"  响应时间: {response_time:.2f} ms")
                
                # 清除环境变量
                if "http_proxy" in os.environ:
                    del os.environ["http_proxy"]
                if "https_proxy" in os.environ:
                    del os.environ["https_proxy"]
                
                return True, response_time
        
        except URLError as e:
            print(f"✗ 连接错误: {str(e)}")
        except HTTPError as e:
            # HTTP错误但能连接，也视为有效代理
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            print(f"⚠️  HTTP错误但能连接: {e.code}")
            print(f"  响应时间: {response_time:.2f} ms")
            
            # 清除环境变量
            if "http_proxy" in os.environ:
                del os.environ["http_proxy"]
            if "https_proxy" in os.environ:
                del os.environ["https_proxy"]
            
            return True, response_time
        except Exception as e:
            print(f"✗ 未知错误: {str(e)}")
        
        # 清除环境变量
        if "http_proxy" in os.environ:
            del os.environ["http_proxy"]
        if "https_proxy" in os.environ:
            del os.environ["https_proxy"]
        
        return False, 0
    
    @staticmethod
    def test_all_proxies():
        """测试所有推荐代理"""
        print("\n正在测试所有推荐代理...")
        print("=" * 60)
        
        best_proxy = None
        best_name = ""
        best_time = float('inf')
        working_proxies = []
        
        for name, proxy in VPNProxyTool.RECOMMENDED_PROXIES:
            print(f"\n测试: {name} ({proxy})")
            success, response_time = VPNProxyTool.test_proxy(proxy)
            
            if success:
                working_proxies.append((name, proxy, response_time))
                if response_time < best_time:
                    best_time = response_time
                    best_proxy = proxy
                    best_name = name
        
        print("\n" + "=" * 60)
        print(f"测试完成! 找到 {len(working_proxies)} 个可用代理")
        
        if working_proxies:
            print("\n可用代理列表:")
            for i, (name, proxy, time_ms) in enumerate(working_proxies, 1):
                print(f"{i}. {name} ({proxy}) - {time_ms:.2f} ms")
            
            if best_proxy:
                print(f"\n✅ 最佳代理: {best_name} ({best_proxy}) - {best_time:.2f} ms")
        
        return best_proxy, best_name, working_proxies
    
    @staticmethod
    def open_github_pages():
        """打开GitHub页面"""
        print("\n打开GitHub关键页面...")
        webbrowser.open(VPNProxyTool.GITHUB_DEVICE_LOGIN)
        webbrowser.open(VPNProxyTool.GITHUB_DEVICE_CONFIRM)
        webbrowser.open("https://github.com")
    
    @staticmethod
    def create_firefox_profile():
        """创建Firefox代理配置文件"""
        print("\n创建Firefox代理配置指南:")
        print("1. 打开Firefox浏览器")
        print("2. 输入 about:profiles 并回车")
        print("3. 点击 '创建新配置文件'，按照向导操作")
        print("4. 切换到新配置文件")
        print("5. 输入 about:preferences#general 并回车")
        print("6. 滚动到底部，点击 '网络设置'")
        print("7. 选择 '手动配置代理'")
        print("8. HTTP代理: 输入代理IP")
        print("9. 端口: 输入代理端口")
        print("10. 勾选 '为HTTPS使用相同代理'")
        print("11. 点击 '确定' 保存设置")
    
    @staticmethod
    def show_proxy_help():
        """显示代理使用帮助"""
        print("\n=== 代理使用帮助 ===")
        print("1. 如果代理设置后仍无法访问，请尝试以下操作:")
        print("   - 清除浏览器缓存和Cookie")
        print("   - 重启浏览器")
        print("   - 尝试使用不同的浏览器")
        print("")
        print("2. 代理可能会定期变化，如无法使用请重新测试")
        print("")
        print("3. 如果所有推荐代理都不可用:")
        print("   - 尝试使用其他网络环境")
        print("   - 联系网络管理员")
        print("   - 考虑使用商业VPN服务")
        

def main():
    print("欢迎使用GitHub VPN代理工具")
    print("此工具帮助您通过VPN代理访问GitHub网站")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 自动测试并使用最佳代理")
        print("2. 显示所有可用代理")
        print("3. 禁用代理")
        print("4. 立即访问GitHub设备登录页面")
        print("5. Firefox浏览器代理配置指南")
        print("6. 查看代理使用帮助")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-6): ")
        
        if choice == "1":
            best_proxy, best_name, _ = VPNProxyTool.test_all_proxies()
            
            if best_proxy:
                print(f"\n正在应用最佳代理: {best_name} ({best_proxy})")
                if not VPNProxyTool.is_admin():
                    print("需要管理员权限来设置系统代理")
                    VPNProxyTool.run_as_admin()
                    sys.exit(0)
                
                if VPNProxyTool.set_browser_proxy(best_proxy):
                    input("\n代理设置成功！按Enter键打开GitHub...")
                    VPNProxyTool.open_github_pages()
        
        elif choice == "2":
            _, _, working_proxies = VPNProxyTool.test_all_proxies()
            
            if working_proxies:
                proxy_choice = input("\n请选择要使用的代理编号 (0取消): ")
                try:
                    idx = int(proxy_choice) - 1
                    if 0 <= idx < len(working_proxies):
                        selected_name, selected_proxy, _ = working_proxies[idx]
                        print(f"\n正在应用选择的代理: {selected_name} ({selected_proxy})")
                        
                        if not VPNProxyTool.is_admin():
                            print("需要管理员权限来设置系统代理")
                            VPNProxyTool.run_as_admin()
                            sys.exit(0)
                        
                        if VPNProxyTool.set_browser_proxy(selected_proxy):
                            input("\n代理设置成功！按Enter键继续...")
                except ValueError:
                    pass
        
        elif choice == "3":
            if not VPNProxyTool.is_admin():
                print("需要管理员权限来禁用代理")
                VPNProxyTool.run_as_admin()
                sys.exit(0)
            
            VPNProxyTool.disable_browser_proxy()
            input("\n按Enter键继续...")
        
        elif choice == "4":
            VPNProxyTool.open_github_pages()
        
        elif choice == "5":
            VPNProxyTool.create_firefox_profile()
            input("\n按Enter键继续...")
        
        elif choice == "6":
            VPNProxyTool.show_proxy_help()
            input("\n按Enter键继续...")
        
        elif choice == "0":
            print("\n感谢使用，再见！")
            break
        
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    # 确保编码正确
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 如果不是以管理员权限运行，提示用户
    if not VPNProxyTool.is_admin():
        print("⚠️  当前未以管理员权限运行")
        print("某些功能（如设置系统代理）需要管理员权限")
        print("建议右键点击脚本并选择'以管理员身份运行'")
        print("")
    
    main()