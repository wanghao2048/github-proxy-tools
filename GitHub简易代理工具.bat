@echo off
chcp 65001 > nul

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境！
    echo 请先安装Python 3.6或更高版本
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo ======================================
echo         GitHub简易代理工具
 echo ======================================

:: 运行Python代理工具
python "github_simple_proxy.py"

echo. 
echo 程序已完成运行
echo. 
pause
exit /b 0