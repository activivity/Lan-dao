@echo off
echo 启动 jianting.py...
start python jianting.py

echo 启动 GPT-SoVITS-v2 文件夹中的 推理_并行.bat...
start cmd /c "cd GPT-SoVITS-v2 && call tuili.bat"

echo 启动 DH_live 文件夹中的 jiankong.py...
start cmd /k "cd DH_live-main && call jiankong.bat"

echo 数字人脚本已启动。
pause
