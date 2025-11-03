@echo off
chcp 65001 > nul
cls

echo ===================================================
echo          欢迎使用 GitHub 加速工具安装助手
===================================================
echo 正在下载 Watt Toolkit (原 Steam++):
echo 这是一款开源的 GitHub 加速工具，支持 Windows 系统
echo ===================================================

:: 创建下载目录
mkdir "%~dp0Watt_Toolkit" 2>nul
cd "%~dp0Watt_Toolkit"

:: 使用PowerShell下载最新的Watt Toolkit
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BeyondDimension/SteamTools/releases/latest/download/SteamTools.Client.Windows.zip' -OutFile 'SteamTools.zip'"

:: 检查下载是否成功
if not exist "SteamTools.zip" (
    echo 下载失败！尝试备用链接...
    powershell -Command "Invoke-WebRequest -Uri 'https://ghproxy.com/https://github.com/BeyondDimension/SteamTools/releases/latest/download/SteamTools.Client.Windows.zip' -OutFile 'SteamTools.zip'"
)

:: 再次检查
if not exist "SteamTools.zip" (
    echo 下载失败！请手动访问以下链接下载：
    echo https://github.com/BeyondDimension/SteamTools/releases/latest
echo 按任意键退出...
    pause
    exit /b 1
)

echo 下载成功！正在解压...

:: 解压文件
powershell -Command "Expand-Archive -Path 'SteamTools.zip' -DestinationPath '.' -Force"

echo 解压完成！正在启动 Watt Toolkit...

:: 启动应用程序
start SteamTools.exe

echo ===================================================
echo 🎉 Watt Toolkit 已成功启动！
echo 💡 使用说明：
echo 1. 在界面中找到 'GitHub' 加速选项
2. 点击 '启用加速' 按钮
3. 之后您的浏览器访问 GitHub 将自动加速
4. 也可以加速下载 GitHub 的资源
echo ===================================================
echo 按任意键退出...
pause