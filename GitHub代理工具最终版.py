#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub代理工具 - 最终版
"""

import os
import sys
import ctypes
import time
import webbrowser
import winreg
import subprocess
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

# 以管理员身份运行
def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            ' '.join(sys.argv),
            None,
            1
        )
        return True
    except:
        return False

# 扩展的代理服务器列表
PROXIES = [
    ("阿里开发者代理1", "47.96.154.23:80"),
    ("阿里CDN代理1", "47.104.190.217:80"),
    ("阿里杭州节点1", "115.236.96.13:80"),
    ("阿里北京节点1", "118.190.205.16:80"),
    ("阿里开发者代理2", "47.96.123.185:80"),
    ("阿里CDN代理2", "47.104.76.11:80"),
    ("阿里深圳节点", "47.106.136.125:80"),
    ("阿里上海节点", "47.101.204.225:80"),
]

# GitHub页面
GITHUB_DEVICE_LOGIN = "https://github.com/login/device"
GITHUB_DEVICE_CONFIRM = "https://github.com/login/device/confirmation"
GITHUB_MAIN = "https://github.com"

# 测试代理连接（优化版）
def test_proxy(proxy):
    print(f"测试代理: {proxy}")
    
    # 保存原始代理设置
    orig_http_proxy = os.environ.get("http_proxy")
    orig_https_proxy = os.environ.get("https_proxy")
    
    try:
        # 设置临时环境变量
        os.environ["http_proxy"] = f"http://{proxy}"
        os.environ["https_proxy"] = f"http://{proxy}"
        
        start_time = time.time()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        
        # 先测试连接到简单的网站
        print(f"正在测试连接...")
        test_url = "http://www.baidu.com"
        req = Request(test_url, headers=headers)
        with urlopen(req, timeout=8) as response:
            test_time = (time.time() - start_time) * 1000
            print(f"基础连接成功! 响应时间: {test_time:.2f} ms")
        
        # 再测试GitHub
        print(f"正在连接GitHub设备登录页面...")
        req = Request(GITHUB_DEVICE_LOGIN, headers=headers)
        with urlopen(req, timeout=10) as response:
            status_code = response.status
            content_length = response.getheader('Content-Length', '未知')
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            print(f"✅ GitHub连接成功!")
            print(f"  状态码: {status_code}")
            print(f"  内容大小: {content_length} 字节")
            print(f"  总响应时间: {response_time:.2f} ms")
            
            return True, response_time
    
    except HTTPError as e:
        print(f"⚠️  HTTP错误但能连接: 状态码 {e.code}")
        # 即使有HTTP错误，也视为可以连接
        try:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            print(f"  响应时间: {response_time:.2f} ms")
            return True, response_time
        except:
            print(f"  无法获取响应时间")
            return True, 9999
    except URLError as e:
        print(f"❌ 连接失败: URL错误 - {str(e)}")
    except TimeoutError:
        print(f"❌ 连接失败: 超时")
    except Exception as e:
        print(f"❌ 连接失败: 未知错误 - {str(e)}")
    
    finally:
        # 恢复原始代理设置
        if orig_http_proxy is not None:
            os.environ["http_proxy"] = orig_http_proxy
        elif "http_proxy" in os.environ:
            del os.environ["http_proxy"]
            
        if orig_https_proxy is not None:
            os.environ["https_proxy"] = orig_https_proxy
        elif "https_proxy" in os.environ:
            del os.environ["https_proxy"]
    
    return False, 0

# 测试所有代理（带进度显示）
def test_all_proxies():
    print("\n🚀 开始测试所有代理服务器...")
    print("=" * 60)
    
    working_proxies = []
    total_proxies = len(PROXIES)
    
    for i, (name, proxy) in enumerate(PROXIES, 1):
        print(f"\n🔍 测试 {i}/{total_proxies}: {name}")
        success, response_time = test_proxy(proxy)
        
        if success:
            working_proxies.append((name, proxy, response_time))
            print(f"✅ [{i}/{total_proxies}] {name} 可用")
        else:
            print(f"❌ [{i}/{total_proxies}] {name} 不可用")
    
    print("\n" + "=" * 60)
    print(f"📊 测试完成! 找到 {len(working_proxies)} 个可用代理")
    
    if working_proxies:
        # 按响应时间排序
        working_proxies.sort(key=lambda x: x[2])
        
        print("\n🏆 可用代理列表（按速度排序）:")
        for i, (name, proxy, time_ms) in enumerate(working_proxies, 1):
            speed_status = "🚀" if time_ms < 500 else "⚡" if time_ms < 1000 else "⏱️"
            print(f"{i}. {speed_status} {name} ({proxy}) - {time_ms:.2f} ms")
        
        best_name, best_proxy, best_time = working_proxies[0]
        print(f"\n🥇 最佳推荐代理: {best_name} ({best_proxy}) - {best_time:.2f} ms")
    else:
        print("\n❌ 没有找到可用的代理服务器")
        print("💡 建议:")
        print("  1. 检查网络连接")
        print("  2. 尝试手动添加其他代理")
        print("  3. 考虑使用商业VPN服务")
    
    return working_proxies

# 设置系统代理（增强版）
def set_system_proxy(proxy):
    print(f"\n🔧 设置系统代理: {proxy}")
    
    if not is_admin():
        print("⚠️ 需要管理员权限来设置系统代理")
        print("正在尝试以管理员身份重新运行...")
        if run_as_admin():
            sys.exit(0)
        else:
            print("❌ 无法获取管理员权限")
            return False
    
    try:
        # 设置IE代理（其他浏览器通常使用IE设置）
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
        
        print("✅ 系统代理设置成功!")
        print("💡 提示: 请清除浏览器缓存后访问GitHub")
        return True
    except Exception as e:
        print(f"❌ 设置代理失败: {str(e)}")
        print("💡 尝试手动设置浏览器代理")
        return False

# 禁用系统代理
def disable_system_proxy():
    print("\n🔄 禁用系统代理...")
    
    if not is_admin():
        print("⚠️ 需要管理员权限来禁用系统代理")
        print("正在尝试以管理员身份重新运行...")
        if run_as_admin():
            sys.exit(0)
        else:
            print("❌ 无法获取管理员权限")
            return False
    
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
        
        print("✅ 系统代理已禁用!")
        return True
    except Exception as e:
        print(f"❌ 禁用代理失败: {str(e)}")
        return False

# 打开GitHub关键页面
def open_github_pages():
    print("\n🌐 正在打开GitHub关键页面...")
    print("1. GitHub设备登录页面")
    print("2. GitHub设备确认页面")
    print("3. GitHub主页")
    
    webbrowser.open(GITHUB_DEVICE_LOGIN)
    time.sleep(1)  # 短暂延迟避免浏览器阻塞
    webbrowser.open(GITHUB_DEVICE_CONFIRM)
    time.sleep(1)
    webbrowser.open(GITHUB_MAIN)
    
    print("✅ 所有页面已在浏览器中打开")

# 显示浏览器代理设置指南
def show_browser_guide():
    print("\n📖 浏览器代理设置指南:")
    print("=" * 60)
    print("\n🔷 Chrome浏览器:")
    print("1. 点击右上角三个点 > 设置")
    print("2. 搜索'代理' > 打开您计算机的代理设置")
    print("3. 在Windows设置中手动配置代理")
    print("   - 地址: 输入代理IP")
    print("   - 端口: 输入代理端口")
    print("4. 点击'保存'")
    
    print("\n🔷 Firefox浏览器:")
    print("1. 打开Firefox > 选项 > 常规")
    print("2. 滚动到底部 > 网络设置 > 设置")
    print("3. 选择'手动配置代理'")
    print("4. HTTP代理: 输入代理IP")
    print("5. 端口: 输入代理端口")
    print("6. 勾选'为HTTPS使用相同代理'")
    print("7. 点击'确定'")
    
    print("\n🔷 Edge浏览器:")
    print("1. 点击右上角三个点 > 设置")
    print("2. 系统 > 代理")
    print("3. 开启'使用代理服务器'")
    print("4. 输入地址和端口")
    print("5. 点击'保存'")
    print("\n" + "=" * 60)

# 显示使用帮助
def show_help():
    print("\n❓ GitHub代理工具使用帮助")
    print("=" * 60)
    print("\n🔍 功能说明:")
    print("1. 测试代理: 自动测试多个代理服务器的连接状态")
    print("2. 设置代理: 配置系统全局代理设置")
    print("3. 禁用代理: 关闭系统代理设置")
    print("4. 打开GitHub: 快速访问GitHub关键页面")
    print("5. 浏览器指南: 查看各浏览器代理设置方法")
    
    print("\n💡 常见问题:")
    print("Q: 为什么需要管理员权限?")
    print("A: 修改系统代理设置需要管理员权限才能确保生效")
    
    print("\nQ: 代理设置后仍无法访问怎么办?")
    print("A: 请尝试清除浏览器缓存和Cookie，或重启浏览器")
    
    print("\nQ: 所有代理都不可用怎么办?")
    print("A: 代理服务器可能已更新，请尝试其他网络环境或商业VPN")
    
    print("\n⚠️ 注意事项:")
    print("- 代理服务器可能随时变化，请定期测试")
    print("- 使用代理时请注意网络安全")
    print("- 不要在代理环境下输入敏感信息")
    print("\n" + "=" * 60)

# 网络连接检测
def check_network_connection():
    print("\n🌐 正在检测网络连接...")
    try:
        # 测试基本连接
        test_url = "http://www.baidu.com"
        with urlopen(test_url, timeout=5):
            print("✅ 基础网络连接正常")
            return True
    except:
        print("❌ 基础网络连接失败")
        print("💡 请检查您的网络连接后重试")
        return False

# 主菜单
def main_menu():
    while True:
        print("\n" + "=" * 60)
        print("          🚀 GitHub代理工具 🚀")
        print("=" * 60)
        print("1. 🧪 测试所有代理服务器")
        print("2. ⚙️  手动设置代理服务器")
        print("3. 🔄 禁用系统代理")
        print("4. 🌐 打开GitHub关键页面")
        print("5. 📖 浏览器代理设置指南")
        print("6. ❓ 查看使用帮助")
        print("0. 🚪 退出")
        print("=" * 60)
        
        choice = input("\n请输入选择 (0-6): ").strip()
        
        if choice == "1":
            if not check_network_connection():
                input("\n按Enter键继续...")
                continue
            working_proxies = test_all_proxies()
            
            if working_proxies:
                use_best = input("\n是否使用最佳代理? (y/n): ").lower()
                if use_best == 'y':
                    best_name, best_proxy, _ = working_proxies[0]
                    set_system_proxy(best_proxy)
        
        elif choice == "2":
            proxy = input("\n请输入代理地址 (格式: IP:端口，如 123.45.67.89:80): ").strip()
            if proxy and ':' in proxy:
                set_system_proxy(proxy)
            else:
                print("❌ 无效的代理格式，请重试")
        
        elif choice == "3":
            disable_system_proxy()
        
        elif choice == "4":
            open_github_pages()
        
        elif choice == "5":
            show_browser_guide()
        
        elif choice == "6":
            show_help()
        
        elif choice == "0":
            print("\n👋 感谢使用GitHub代理工具！")
            print("💡 记得在不需要时禁用代理")
            break
        
        else:
            print("❌ 无效的选择，请输入0-6之间的数字")
        
        input("\n按Enter键继续...")

# 主程序
def main():
    setup_encoding()
    
    print("🎉 欢迎使用GitHub代理工具")
    print("🛠️  专业版 v1.0")
    print("🔒 安全可靠的GitHub访问解决方案")
    
    if not is_admin():
        print("\n⚠️  当前未以管理员权限运行")
        print("   部分功能（如设置系统代理）需要管理员权限")
        print("   建议右键点击脚本 > 以管理员身份运行")
    
    main_menu()

# 程序入口
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🔴 程序被用户中断")
    except Exception as e:
        print(f"\n\n❌ 程序遇到错误: {str(e)}")
    finally:
        print("\n💾 程序已退出")
        input("按Enter键关闭窗口...")