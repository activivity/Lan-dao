@echo off
REM 切换到当前目录中的 DH_live-main 文件夹
cd /d "%~dp0DH_live-main"

REM 激活 Conda 环境
call conda activate dh_live

REM 运行 xunlian.py 脚本
python xunlian.py

REM 暂停以防止窗口自动关闭
pause
