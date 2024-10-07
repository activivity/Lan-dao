import os
import time
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 获取脚本所在目录的路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义监听的文件夹路径和目标文件夹路径
source_folder = os.path.abspath(os.path.join(script_dir, 'GPT-SoVITS-v2', '音频输出'))
destination_folder = os.path.abspath(os.path.join(script_dir, 'DH_live-main', "audio"))

# 确保目标文件夹存在
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 定义事件处理器类
class AudioFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.wav', '.mp3')):
            print(f"检测到文件修改: {event.src_path}")
            time.sleep(2)  # 确保文件写入完成
            self.convert_audio_bitrate(event.src_path)

    def convert_audio_bitrate(self, src_path):
        file_name = os.path.basename(src_path)
        destination_path = os.path.join(destination_folder, file_name)
        temp_file = os.path.join(destination_folder, "temp_" + file_name)
        
        print(f"正在将文件 {src_path} 转换为 256 kbps, 16kHz 采样率, 单声道 16 位...")
        command = [
            ffmpeg_path, '-i', src_path, 
            '-b:a', '256k', '-ar', '16000', '-ac', '1', '-sample_fmt', 's16', temp_file
        ]
        try:
            subprocess.run(command, check=True)
            shutil.move(temp_file, destination_path)
            print(f"已将文件 {src_path} 转换并复制到: {destination_path}")
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg转换失败: {e}")

# 获取ffmpeg路径
ffmpeg_path = os.path.join(script_dir, "ffmpeg","ffmpeg-master-latest-win64-gpl", "bin", 'ffmpeg.exe')

# 创建观察者
event_handler = AudioFileHandler()
observer = Observer()
observer.schedule(event_handler, path=source_folder, recursive=True)

try:
    print(f"开始监听文件夹: {source_folder}")
    observer.start()
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("停止监听...")
    observer.stop()

observer.join()
