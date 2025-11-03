@echo off

:: 强制使用UTF-8编码
chcp 65001 > nul
cls

:: 直接运行Python脚本
python "GitHub代理工具最终版.py"

:: 完成后暂停
pause