@echo off
echo 启动 hudong.py...
start python hudong.py

echo 启动 getDouyin 文件夹中的 main.py...
start cmd /c "cd getDouyin && .\venv\Scripts\activate && python main.py"
echo 互动脚本已启动。
pause