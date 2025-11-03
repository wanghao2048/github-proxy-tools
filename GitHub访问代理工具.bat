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

echo ===================================================================
echo                  GitHub访问代理工具 v1.0
echo ===================================================================
echo 
echo 正在启动代理配置工具...
echo 请稍候...
echo 

:: 运行Python代理配置工具
python "github_proxy_tool.py"

echo. 
echo 工具已完成运行
echo 注意：如果遇到代理连接问题，可能是因为代理服务器已经失效
echo 请尝试其他代理或联系网络管理员
echo. 
pause
exit /b 0