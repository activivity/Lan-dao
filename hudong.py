import requests
import json
import time
import os
import subprocess

# 基本配置
base_url = "http://localhost:8080/api"
headers = {
    "Authorization": "application-dba757fef57ede5eb74eb97b35dd33f5",  # 替换为你的 API Key
    "Content-Type": "application/json"
}

# 启动 Docker Desktop
def start_docker_desktop():
    try:
        if os.name == 'nt':  # 如果是 Windows 系统
            print("尝试启动 Docker Desktop...")
            subprocess.run(["start", "Docker Desktop"], shell=True)
            time.sleep(10)  # 等待 Docker 启动
            print("Docker Desktop 启动中，等待初始化完成...")
            # 等待一段时间以确保 Docker 完全启动
            for _ in range(10):  # 尝试 10 次，每次等待 5 秒
                result = subprocess.run(["docker", "info"], capture_output=True, text=True)
                if "Cannot connect to the Docker daemon" not in result.stderr:
                    print("Docker 已启动。")
                    return True
                time.sleep(5)
            print("无法连接 Docker Daemon，请检查 Docker Desktop 是否成功启动。")
            return False
        else:
            print("非 Windows 系统，请手动启动 Docker。")
            return False
    except Exception as e:
        print(f"启动 Docker Desktop 时出错: {e}")
        return False

# 启动 Docker 容器或使用已有的容器
def start_docker_and_maxkb():
    try:
        # 检查 Docker Desktop 是否已经启动
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if "Cannot connect to the Docker daemon" in result.stderr:
            print("Docker Desktop 没有运行，正在尝试启动 Docker Desktop...")
            if not start_docker_desktop():
                return False

        return manage_container()  # 调用管理 Docker 容器的函数
    except subprocess.CalledProcessError as e:
        print(f"启动 Docker 或容器时出错: {e}")
        return False


def manage_container():
    try:
        # 获取当前脚本的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 将相对路径 'maxkb' 转换为绝对路径
        data_path = os.path.join(current_dir, 'maxkb')
        abs_data_path = os.path.abspath(data_path)

        # 检查是否已经存在名为 maxkb 的容器
        result = subprocess.run(["docker", "ps", "-a", "-q", "-f", "name=maxkb"], capture_output=True, text=True)
        container_id = result.stdout.strip()

        if container_id:
            # 容器已存在，检查是否在运行
            running_result = subprocess.run(["docker", "ps", "-q", "-f", "name=maxkb"], capture_output=True, text=True)
            if running_result.stdout.strip():
                print("maxkb 容器已在运行中。")
            else:
                print("正在启动已存在的 maxkb 容器...")
                subprocess.run(["docker", "start", "maxkb"], check=True)
                print("maxkb 容器启动成功。")
        else:
            # 容器不存在，创建一个新容器，挂载相对路径下的 maxkb 目录
            print("maxkb 容器不存在，正在创建并启动新容器...")
            subprocess.run([
                "docker", "run", "-d", "--name=maxkb", "-p", "8080:8080",
                "-v", f"{abs_data_path}:/var/lib/postgresql/data",
                "1panel/maxkb"
            ], check=True)
            print("maxkb 容器创建并启动成功。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"启动 Docker 或 maxkb 容器时出错: {e}")
        return False
# 获取应用信息
def get_application_info():
    url = f"{base_url}/application/profile"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("获取应用信息成功:", response.json())
        return response.json()  # 返回应用信息
    else:
        print(f"获取应用信息失败，状态码: {response.status_code}, 响应: {response.text}")
        return None

# 打开会话
def open_chat(application_id):
    url = f"{base_url}/application/{application_id}/chat/open"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("会话开启成功:", response.json())
        return response.json().get("data")  # 获取 chat_id
    else:
        print(f"打开会话失败，状态码: {response.status_code}, 响应: {response.text}")
        return None

# 发送消息并处理回复，将回复保存到txt文件
def send_message(chat_id, message):
    url = f"{base_url}/application/chat_message/{chat_id}"

    # 在弹幕前加上指定的前导文字
    full_message = "下面是一场直播的弹幕，请对弹幕信息进行回答，使用中文回答，不需要说用户名，说公屏上看到有位宝子问，只对弹幕内容回复，请使用中文回答，不要回答表情: " + message

    data = {
        "message": full_message,
        "re_chat": False,
        "stream": True
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.text.splitlines()
        full_reply = ""
        for line in response_data:
            try:
                chunk = line.strip().split(": ", 1)[-1]  # 获取数据块
                if chunk:
                    content_data = json.loads(chunk)
                    full_reply += content_data.get("content", "")
                    if content_data.get("is_end"):
                        print("模型回复:", full_reply)
                        save_reply_to_file(full_reply)
                        break
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}")
                print(f"无法解析的内容: {line}")
    else:
        print(f"发送消息失败，状态码: {response.status_code}, 响应: {response.text}")

# 保存 AI 回复到 txt 文件
def save_reply_to_file(reply):
    file_path = "GPT-SoVITS-v2/ai_reply.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(reply)
    print(f"AI 的回复已保存到 {file_path}")

# 监控 danmu.txt 文件
def watch_danmu_file(chat_id, file_path):
    last_modify_time = os.path.getmtime(file_path)
    while True:
        current_modify_time = os.path.getmtime(file_path)
        if current_modify_time != last_modify_time:
            with open(file_path, 'r', encoding='utf-8') as file:
                danmu_message = file.read().strip()
                if danmu_message:
                    print(f"文件更新，发送新弹幕: {danmu_message}")
                    send_message(chat_id, danmu_message)
            last_modify_time = current_modify_time
        time.sleep(1)

# 主流程
def main():
    if start_docker_and_maxkb():  # 确保 Docker 和 maxkb_new 容器已经启动
        application_info = get_application_info()
        if application_info:
            application_id = application_info.get("data", {}).get("id")
            if application_id:
                chat_id = open_chat(application_id)
                if chat_id:
                    # 初始发送弹幕
                    file_path = "getDouyin/danmu.txt"  # 弹幕文件路径
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            danmu_message = file.read().strip()
                            if danmu_message:
                                send_message(chat_id, danmu_message)
                    # 开始监控文件变化
                    watch_danmu_file(chat_id, file_path)

if __name__ == "__main__":
    main()
