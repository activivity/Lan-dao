

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re

# 创建 ChromeOptions 对象，启用日志记录功能
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")  # 开启开发者工具（可选）
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # 启用性能日志

# 使用 webdriver_manager 管理 ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 打开直播间页面
driver.get("https://live.douyin.com/211374705237")  # 替换为直播间链接

# 等待页面加载
time.sleep(5)  # 根据实际需要调整

# 切换到 iframe，如果页面使用了嵌套的 iframe
iframe = driver.find_element(By.TAG_NAME, 'iframe')  # 使用新的 API
driver.switch_to.frame(iframe)

# 等待页面加载
time.sleep(5)

# 获取性能日志
logs = driver.get_log("performance")

# 查找 WebSocket 连接地址
websocket_url = None
for log in logs:
    message = log["message"]
    if "Network.webSocketCreated" in message:
        # 尝试从日志中提取 WebSocket 地址
        ws_match = re.search(r'"url":"(ws://[^\s"]+|wss://[^\s"]+)"', message)
        if ws_match:
            websocket_url = ws_match.group(1)
            break

if websocket_url:
    print(f"WebSocket 连接地址: {websocket_url}")
else:
    print("未找到 WebSocket 地址")

# 切换回主页面
driver.switch_to.default_content()

# 关闭浏览器
driver.quit()
