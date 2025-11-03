@echo off
chcp 65001 > nul

set "SCRIPT_NAME=阿里代理配置工具.py"

echo ===================================================================
echo                阿里代理访问GitHub工具 v1.0
setlocal enabledelayedexpansion

:: 检查Python是否安装
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境！
    echo 请先安装Python 3.6或更高版本
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

:: 创建Python配置脚本
echo 创建配置工具...
( echo #!/usr/bin/env python3
  echo # -*- coding: utf-8 -*-
  echo """
  echo 阿里代理访问GitHub配置工具
  echo """
  echo 
  echo import os
  echo import sys
  echo import subprocess
  echo import ctypes
  echo import time
  echo import webbrowser
  echo import winreg
  echo 
  echo class ProxyConfig:
  echo     """代理配置类"""
  echo     
  echo     # 阿里公共代理服务器列表 (示例，实际使用时请替换为有效代理)
  echo     ALI_PROXIES = {
  echo         "阿里云开发者代理": "47.96.154.23:80",
  echo         "阿里CDN代理": "47.104.190.217:80",
  echo         "阿里杭州节点": "115.236.96.13:80",
  echo         "阿里北京节点": "118.190.205.16:80"
  echo     }
  echo     
  echo     # GitHub相关域名
  echo     GITHUB_DOMAINS = [
  echo         "github.com",
  echo         "www.github.com",
  echo         "api.github.com",
  echo         "raw.githubusercontent.com",
  echo         "assets-cdn.github.com",
  echo         "avatars.githubusercontent.com",
  echo         "githubstatus.com",
  echo         "githubusercontent.com"
  echo     ]
  echo     
  echo     @staticmethod
  echo     def is_admin():
  echo         """检查是否以管理员权限运行"""
  echo         try:
  echo             return ctypes.windll.shell32.IsUserAnAdmin()
  echo         except:
  echo             return False
  echo     
  echo     @staticmethod
  echo     def run_as_admin():
  echo         """以管理员权限重新运行程序"""
  echo         ctypes.windll.shell32.ShellExecuteW(
  echo             None,
  echo             "runas",
  echo             sys.executable,
  echo             ' '.join([sys.argv[0]] + sys.argv[1:]),
  echo             None,
  echo             1
  echo         )
  echo     
  echo     @staticmethod
  def set_proxy(proxy_address):
  echo         """设置系统代理"""
  echo         print(f"正在设置代理: {proxy_address}")
  echo         
  echo         # 设置HTTP代理
  echo         reg_key = winreg.OpenKey(
  echo             winreg.HKEY_CURRENT_USER,
  echo             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
  echo             0,
  echo             winreg.KEY_SET_VALUE
  echo         )
  echo         
  echo         # 启用代理
  echo         winreg.SetValueEx(reg_key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
  echo         # 设置HTTP代理
  echo         winreg.SetValueEx(reg_key, "ProxyServer", 0, winreg.REG_SZ, proxy_address)
  echo         # 设置代理排除列表（本地地址不使用代理）
  echo         winreg.SetValueEx(reg_key, "ProxyOverride", 0, winreg.REG_SZ, "<local>")
  echo         winreg.CloseKey(reg_key)
  echo         
  echo         print("代理设置成功！")
  echo         ProxyConfig.refresh_browser()
  echo     
  echo     @staticmethod
  def disable_proxy():
  echo         """禁用系统代理"""
  echo         print("正在禁用代理...")
  echo         
  echo         reg_key = winreg.OpenKey(
  echo             winreg.HKEY_CURRENT_USER,
  echo             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
  echo             0,
  echo             winreg.KEY_SET_VALUE
  echo         )
  echo         
  echo         winreg.SetValueEx(reg_key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
  echo         winreg.CloseKey(reg_key)
  echo         
  echo         print("代理已禁用！")
  echo         ProxyConfig.refresh_browser()
  echo     
  echo     @staticmethod
  def test_connection(proxy_address):
  echo         """测试代理连接"""
  echo         print(f"\n测试代理连接: {proxy_address}")
  echo         print("=" * 60)
  echo         
  echo         try:
  echo             # 设置临时环境变量用于测试
  echo             env = os.environ.copy()
  echo             env["http_proxy"] = f"http://{proxy_address}"
  echo             env["https_proxy"] = f"http://{proxy_address}"
  echo             
  echo             # 测试GitHub连接
  echo             print("测试连接 GitHub.com...")
  echo             result = subprocess.run(
  echo                 ["curl", "-s", "-o", "NUL", "-w", "%%{http_code}", "https://github.com"],
  echo                 env=env,
  echo                 capture_output=True,
  echo                 text=True,
  echo                 timeout=10
  echo             )
  echo             
  echo             if result.returncode == 0 and result.stdout.strip():  
  echo                 print(f"✓ GitHub.com 连接成功! 状态码: {result.stdout.strip()}")
  echo                 return True
  echo             else:
  echo                 print(f"✗ GitHub.com 连接失败! 返回码: {result.returncode}")
  echo                 return False
  echo         except subprocess.TimeoutExpired:
  echo             print("✗ 连接超时")
  echo             return False
  echo         except Exception as e:
  echo             print(f"✗ 测试出错: {str(e)}")
  echo             return False
  echo     
  echo     @staticmethod
  def refresh_browser():
  echo         """刷新浏览器设置"""
  echo         print("\n刷新浏览器代理设置...")
  echo         # 通知系统代理设置已更改
  echo         try:
  echo             ctypes.windll.Wininet.InternetSetOptionW(0, 37, 0, 0)  # INTERNET_OPTION_SETTINGS_CHANGED
  echo             ctypes.windll.Wininet.InternetSetOptionW(0, 39, 0, 0)  # INTERNET_OPTION_REFRESH
  echo         except:
  echo             pass
  echo     
  echo     @staticmethod
  def open_github():
  echo         """打开GitHub网站"""
  echo         print("\n打开GitHub官方网站...")
  echo         webbrowser.open("https://github.com")
  echo         webbrowser.open("https://github.com/login/device")
  echo     
  echo     @staticmethod
  def show_current_settings():
  echo         """显示当前代理设置"""
  echo         print("\n当前代理设置:")
  echo         print("=" * 60)
  echo         
  echo         try:
  echo             reg_key = winreg.OpenKey(
  echo                 winreg.HKEY_CURRENT_USER,
  echo                 r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
  echo                 0,
  echo                 winreg.KEY_READ
  echo             )
  echo             
  echo             enabled = winreg.QueryValueEx(reg_key, "ProxyEnable")[0]
  echo             server = winreg.QueryValueEx(reg_key, "ProxyServer")[0] if "ProxyServer" in [winreg.EnumValue(reg_key, i)[0] for i in range(winreg.QueryInfoKey(reg_key)[1])] else "未设置"
  echo             
  echo             print(f"代理状态: {'已启用' if enabled else '已禁用'}")
  echo             print(f"代理服务器: {server}")
  echo             
  echo             winreg.CloseKey(reg_key)
  echo         except Exception as e:
  echo             print(f"无法读取代理设置: {str(e)}")
  echo 
  echo def main():
  echo     """主函数"""
  echo     print("欢迎使用阿里代理访问GitHub工具")
  echo     print("=" * 60)
  echo     
  echo     # 显示当前设置
  echo     ProxyConfig.show_current_settings()
  echo     
  echo     while True:
  echo         print("\n请选择操作:")
  echo         print("1. 测试并选择阿里代理服务器")
  echo         print("2. 启用自动推荐代理")
  echo         print("3. 手动输入代理服务器")
  echo         print("4. 禁用代理")
  echo         print("5. 立即访问GitHub")
  echo         print("0. 退出")
  echo         
  echo         choice = input("\n请输入选择 (0-5): ")
  echo         
  echo         if choice == "1":
  echo             # 测试所有代理
  echo             print("\n正在测试所有阿里代理服务器...")
  echo             best_proxy = None
  echo             best_time = float('inf')
  echo             
  echo             for name, address in ProxyConfig.ALI_PROXIES.items():
  echo                 print(f"\n测试: {name} ({address})")
  echo                 start_time = time.time()
  echo                 success = ProxyConfig.test_connection(address)
  echo                 end_time = time.time()
  echo                 
  echo                 if success:
  echo                     response_time = (end_time - start_time) * 1000
  echo                     print(f"响应时间: {response_time:.2f} ms")
  echo                     
  echo                     if response_time < best_time:
  echo                         best_time = response_time
  echo                         best_proxy = (name, address)
  echo             
  echo             if best_proxy:
  echo                 print(f"\n最佳代理: {best_proxy[0]} ({best_proxy[1]})")
  echo                 print(f"响应时间: {best_time:.2f} ms")
  echo                 
  echo                 use_it = input("\n是否使用此代理? (y/n): ")
  echo                 if use_it.lower() == 'y':
  echo                     if not ProxyConfig.is_admin():
  echo                         print("需要管理员权限来设置代理")
  echo                         ProxyConfig.run_as_admin()
  echo                         sys.exit(0)
  echo                     ProxyConfig.set_proxy(best_proxy[1])
  echo             else:
  echo                 print("\n所有代理测试失败，请检查网络连接或尝试手动输入")
  echo         
  echo         elif choice == "2":
  echo             # 使用推荐代理
  echo             recommended = "47.96.154.23:80"  # 阿里云开发者代理
  echo             print(f"\n使用推荐代理: {recommended}")
  echo             
  echo             if ProxyConfig.test_connection(recommended):
  echo                 use_it = input("\n代理测试成功，是否使用? (y/n): ")
  echo                 if use_it.lower() == 'y':
  echo                     if not ProxyConfig.is_admin():
  echo                         print("需要管理员权限来设置代理")
  echo                         ProxyConfig.run_as_admin()
  echo                         sys.exit(0)
  echo                     ProxyConfig.set_proxy(recommended)
  echo         
  echo         elif choice == "3":
  echo             # 手动输入
  echo             custom_proxy = input("\n请输入代理服务器地址 (格式: ip:端口): ")
  echo             if custom_proxy:
  echo                 if ProxyConfig.test_connection(custom_proxy):
  echo                     use_it = input("\n代理测试成功，是否使用? (y/n): ")
  echo                     if use_it.lower() == 'y':
  echo                         if not ProxyConfig.is_admin():
  echo                             print("需要管理员权限来设置代理")
  echo                             ProxyConfig.run_as_admin()
  echo                             sys.exit(0)
  echo                         ProxyConfig.set_proxy(custom_proxy)
  echo         
  echo         elif choice == "4":
  echo             # 禁用代理
  echo             if not ProxyConfig.is_admin():
  echo                 print("需要管理员权限来禁用代理")
  echo                 ProxyConfig.run_as_admin()
  echo                 sys.exit(0)
  echo             ProxyConfig.disable_proxy()
  echo         
  echo         elif choice == "5":
  echo             # 打开GitHub
  echo             ProxyConfig.open_github()
  echo         
  echo         elif choice == "0":
  echo             print("\n感谢使用，再见！")
  echo             break
  echo         
  echo         else:
  echo             print("无效选择，请重试")
  echo         
  echo         input("\n按Enter键继续...")
  echo 
  echo if __name__ == "__main__":
  echo     # 检查是否安装了curl
  echo     try:
  echo         subprocess.run(["curl", "--version"], capture_output=True, check=True)
  echo     except:
  echo         print("注意: 未找到curl工具，某些网络测试功能可能受限")
  echo         print("建议安装curl以获得最佳体验")
  echo         input("按Enter键继续...")
  echo     
  echo     # 如果命令行参数中包含"--set-proxy"，则直接设置代理
  echo     if len(sys.argv) > 1 and sys.argv[1] == "--set-proxy" and len(sys.argv) > 2:
  echo         if ProxyConfig.is_admin():
  echo             ProxyConfig.set_proxy(sys.argv[2])
  echo         else:
  echo             print("需要管理员权限")
  echo             sys.exit(1)
  echo     else:
  echo         main()
) > "%SCRIPT_NAME%"

:: 检查是否需要管理员权限
NET SESSION >nul 2>&1
set ADMIN=%errorLevel%

:: 运行Python脚本
if %ADMIN% EQU 0 (
    echo 以管理员权限运行配置工具...
    python "%SCRIPT_NAME%"
) else (
    echo 以普通用户权限运行配置工具...
    echo 注意: 某些功能（如设置系统代理）需要管理员权限
    python "%SCRIPT_NAME%"
)

:: 清理临时文件
del "%SCRIPT_NAME%" >nul 2>&1

echo. 
echo 工具已完成运行
pause
exit /b 0