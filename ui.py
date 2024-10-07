import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QListWidget, QStackedWidget, QComboBox, QMessageBox, QTextEdit, QFrame, QGroupBox

from PyQt5.QtWebEngineWidgets import QWebEngineView
import qdarkgraystyle
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess, Qt
from qt_material import apply_stylesheet
from PyQt5 import QtWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

  # 创建主布局
        central_widget = QWidget()  # 创建中央小部件
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # 定义主布局，并将其设置为中央小部件的布局
        self.setWindowTitle('数字人互动系统')
        self.setWindowIcon(QIcon('icons/logo.png')) 
        # 创建侧边菜单
        self.menu_list = QListWidget()
        self.menu_list.setFixedWidth(200)  # 增加侧边栏的宽度
        self.menu_list.setStyleSheet
        

        # 添加侧边栏菜单项并附加图标
        self.menu_list.addItem(QListWidgetItem(QIcon("icons/home.png"), "数字人生成"))
        self.menu_list.addItem(QListWidgetItem(QIcon("icons/human.png"), "数字人训练"))
        self.menu_list.addItem(QListWidgetItem(QIcon("icons/audio.png"), "音频模型训练"))
        self.menu_list.addItem(QListWidgetItem(QIcon("icons/clone.png"), "音频克隆"))
        self.menu_list.addItem(QListWidgetItem(QIcon("icons/ai.png"), "AI互动大模型训练"))
  # 响应侧边栏选项切换
        self.menu_list.currentRowChanged.connect(self.display_page)
        # 创建窗口容器（QStackedWidget）
        self.stack = QStackedWidget()

        # 添加页面
        self.stack.addWidget(self.create_home_page())  # 主窗口
        self.stack.addWidget(DigitalHumanTraining())  # 数字人训练页面
        self.stack.addWidget(self.create_audio_model_training_page())  # 音频模型训练页面
        self.stack.addWidget(self.create_audio_cloning_page())  # 音频克隆页面
        self.stack.addWidget(self.start_ai_model_training_page())  # ai训练

        # 将侧边菜单和窗口容器添加到主布局
        main_layout.addWidget(self.menu_list, 1)
        main_layout.addWidget(self.stack, 4)

        # 创建一个中央窗口来容纳主布局
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
         # 右侧状态栏
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)

        # 添加左侧菜单、窗口区域、右侧状态栏
        main_layout.addWidget(self.menu_list, 1)
        main_layout.addWidget(self.stack, 4)
        main_layout.addWidget(self.status_display, 2)

        # QProcess 处理
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def handle_stdout(self):
        """捕获标准输出"""
        data = self.process.readAllStandardOutput()
        text = data.data().decode()
        self.status_display.append(text)

    def handle_stderr(self):
        """捕获标准错误输出"""
        data = self.process.readAllStandardError()
        text = data.data().decode()
        self.status_display.append(f"<span style='color:red'>{text}</span>")

    def process_finished(self):
        """进程结束时显示"""
        self.status_display.append("进程结束。")

    def start_process(self, command):
        """启动进程，并捕获输出"""
        self.status_display.append(f"正在运行: {command}")
        self.process.start(command)

    def display_page(self, index):
        """切换显示不同的页面"""
        self.stack.setCurrentIndex(index)

    def create_home_page(self):
        """创建主窗口页面"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)  # 增加组件之间的间距

        # 使用 QGroupBox 创建模块分隔
        live_url_group = QGroupBox("")
        live_url_layout = QVBoxLayout()
        label_url = QLabel('请输入抖音直播间的 链接:')
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("输入抖音直播间的链接")
        button_change_url = QPushButton('确定更改 直播间链接')
        button_change_url.clicked.connect(lambda: self.change_live_url(self.input_url.text()))

        live_url_layout.addWidget(label_url)
        live_url_layout.addWidget(self.input_url)
        live_url_layout.addWidget(button_change_url)
        live_url_group.setLayout(live_url_layout)

        # 创建分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # 将所有模块添加到布局
        layout.addWidget(live_url_group)
        layout.addWidget(separator)

        # 添加数字人模型选择模块
        model_label = QLabel('选择数字人模型:', self)
        self.model_dropdown = QComboBox(self)
        self.load_model_dropdown()  # 加载模型列表
        confirm_button = QPushButton('确认选择模型', self)
        confirm_button.clicked.connect(self.on_model_selected)

        # 添加模型选择模块到布局
        layout.addWidget(model_label)
        layout.addWidget(self.model_dropdown)
        layout.addWidget(confirm_button)

        # 文本生成模块
        text_group = QGroupBox("文本生成")
        text_layout = QVBoxLayout()
        text_input_label = QLabel('直接输入文字生成数字人:')
        self.text_input = QTextEdit()
        button_generate_text = QPushButton('确认生成')
        button_generate_text.clicked.connect(lambda: self.generate_ai_reply_text(self.text_input.toPlainText()))

        text_layout.addWidget(text_input_label)
        text_layout.addWidget(self.text_input)
        text_layout.addWidget(button_generate_text)
        text_group.setLayout(text_layout)

        layout.addWidget(text_group)

         # 启动按钮
        button_layout = QHBoxLayout()
        self.button_start_digital_human = QPushButton('启动数字人')
        self.button_start_digital_human.clicked.connect(self.start_digital_human)  # 绑定启动数字人的功能
        self.button_start_interactive_system = QPushButton('启动互动系统')
        self.button_start_interactive_system.clicked.connect(self.start_interactive_system)  # 绑定启动互动系统的功能

        button_layout.addWidget(self.button_start_digital_human)
        button_layout.addWidget(self.button_start_interactive_system)

        layout.addLayout(button_layout)
        page.setLayout(layout)
        return page
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

# setup stylesheet
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())



    def load_model_dropdown(self):
        """加载 video_data 文件夹中的所有子文件夹到下拉菜单"""
        video_data_path = os.path.join('DH_live-main', 'video_data')
        if os.path.exists(video_data_path):
            model_folders = [f for f in os.listdir(video_data_path) if os.path.isdir(os.path.join(video_data_path, f))]
            self.model_dropdown.addItems(model_folders)  # 将子文件夹名称加入下拉菜单
        else:
            QMessageBox.warning(self, "错误", f"未找到路径: {video_data_path}")

    def on_model_selected(self):
        """当用户点击确认按钮时，更新 DH_live-main/jiankong.py 中的 moxing_file 变量"""
        selected_model = self.model_dropdown.currentText()
        if selected_model:
            jiankong_path = os.path.join('DH_live-main', 'jiankong.py')
            if os.path.exists(jiankong_path):
                try:
                    with open(jiankong_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()

                    with open(jiankong_path, 'w', encoding='utf-8') as file:
                        for line in lines:
                            if line.startswith("moxing_file"):
                                file.write(f'moxing_file = "{selected_model}"\n')
                            else:
                                file.write(line)

                    QMessageBox.information(self, "成功", f"已确认选择模型并更新: {selected_model}")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"更新 jiankong.py 失败: {str(e)}")
            else:
                QMessageBox.warning(self, "错误", "未找到 jiankong.py 文件")

    def change_live_url(self, new_url):
        """修改 config.py 中的 LIVE_URL 变量"""
        if new_url:
            try:
                config_path = os.path.join('getDouyin', 'config.py')  # config.py 的路径
                with open(config_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                with open(config_path, 'w', encoding='utf-8') as file:
                    for line in lines:
                        if line.startswith("LIVE_URL"):
                            file.write(f'LIVE_URL = "{new_url}"\n')
                        else:
                            file.write(line)

                QMessageBox.information(self, "提示", "直播间链接 已成功更改")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"修改失败: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "请输入有效的直播间链接")

    def generate_ai_reply_text(self, user_input_text):
        """生成文字到 ai_reply.txt 文件"""
        if user_input_text.strip():
            try:
                ai_reply_file_path = os.path.join('GPT-SoVITS-v2', 'ai_reply.txt')
                with open(ai_reply_file_path, 'w', encoding='utf-8') as file:
                    file.write(user_input_text)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"更新 ai_reply.txt 失败: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "请输入内容以更新 ai_reply.txt")

    def start_digital_human(self):
        """启动数字人"""
        try:
            bat_path = os.path.abspath('yunxing.bat')  # 获取 yunxing.bat 的绝对路径
            print(f"准备启动数字人，执行文件路径: {bat_path}")  # 调试信息
            if os.path.exists(bat_path):
                print(f"文件 {bat_path} 存在，正在启动...")
                subprocess.Popen(['call', bat_path], shell=True)
                QMessageBox.information(self, "提示", "数字人已启动")
            else:
                print(f"文件 {bat_path} 不存在")
                QMessageBox.critical(self, "错误", f"启动失败：未找到 {bat_path}")
        except Exception as e:
            print(f"启动数字人失败: {e}")
            QMessageBox.critical(self, "错误", f"启动数字人失败: {str(e)}")

    def start_interactive_system(self):
        """启动互动系统，要求输入直播间链接"""
        live_url = self.input_url.text().strip()
        if live_url:
            try:
                bat_path = os.path.abspath('yunxinghudong.bat')  # 获取 yunxinghudong.bat 的绝对路径
                print(f"准备启动互动系统，执行文件路径: {bat_path}")  # 调试信息
                if os.path.exists(bat_path):
                    print(f"文件 {bat_path} 存在，正在启动...")
                    subprocess.Popen(['start', bat_path], shell=True)
                    QMessageBox.information(self, "提示", "互动系统已启动")
                else:
                    print(f"文件 {bat_path} 不存在")
                    QMessageBox.critical(self, "错误", f"启动失败：未找到 {bat_path}")
            except Exception as e:
                print(f"启动互动系统失败: {e}")
                QMessageBox.critical(self, "错误", f"启动互动系统失败: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "请先输入直播间链接")


    def create_audio_model_training_page(self):
        """创建音频模型训练页面"""
        page = QWidget()
        layout = QVBoxLayout()

        # 添加启动音频模型训练按钮
        self.start_audio_training_button = QPushButton('启动音频模型训练', self)
        self.start_audio_training_button.clicked.connect(self.start_audio_model_training)

        # 添加浏览器窗口
        self.web_view = QWebEngineView(self)

        layout.addWidget(self.start_audio_training_button)
        layout.addWidget(self.web_view)
        page.setLayout(layout)
        return page

    def start_audio_model_training(self):
        """启动音频模型训练并在窗口中显示 Web UI"""
        try:
            # 构造 go-webui.bat 的绝对路径
            bat_path = os.path.abspath(os.path.join('GPT-SoVITS-v2', 'go-webui.bat'))

            # 检查 go-webui.bat 文件是否存在
            if os.path.exists(bat_path):
                # 启动 go-webui.bat，并确保工作目录是 GPT-SoVITS-v2
                subprocess.Popen(['start', bat_path], shell=True, cwd=os.path.dirname(bat_path))

                # 打开本地运行的 Web UI
                self.web_view.setUrl(QUrl("http://localhost:9874/"))
            else:
                QMessageBox.critical(self, "错误", f"未找到批处理文件: {bat_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动音频模型训练失败: {str(e)}")

    def create_audio_cloning_page(self):
        """创建音频克隆页面（暂时为空白）"""
        page = QWidget()
        layout = QVBoxLayout()
         # 添加启动音频模型训练按钮
        self.start_audio_training_button = QPushButton('启动音频克隆', self)
        self.start_audio_training_button.clicked.connect(self.start_audio_model)

        # 添加浏览器窗口
        self.web_view = QWebEngineView(self)

        layout.addWidget(self.start_audio_training_button)
        layout.addWidget(self.web_view)
        page.setLayout(layout)
        return page

    def create_audio_cloning_page(self):
        """创建音频克隆页面"""
        page = QWidget()
        layout = QVBoxLayout()

        # 添加启动音频模型训练按钮
        self.start_audio_training_button = QPushButton('启动音频克隆', self)
        self.start_audio_training_button.clicked.connect(self.start_audio_model)

        # 添加浏览器窗口，用于显示网页内容
        self.audio_web_view = QWebEngineView(self)

        # 布局中添加按钮和浏览器视图
        layout.addWidget(self.start_audio_training_button)
        layout.addWidget(self.audio_web_view, stretch=1)
        page.setLayout(layout)
        return page

    def start_audio_model(self):
        """启动音频模型训练并在窗口中显示 Web UI"""
        try:
            bat_path = os.path.abspath(os.path.join('GPT-SoVITS-v2', 'tuili.bat'))

            if os.path.exists(bat_path):
                subprocess.Popen(bat_path, shell=True, cwd=os.path.dirname(bat_path))
                self.audio_web_view.setUrl(QUrl("http://localhost:9872/"))  # 加载音频克隆的网页
            else:
                QMessageBox.critical(self, "错误", f"未找到批处理文件: {bat_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动音频克隆失败: {str(e)}")

    def start_ai_model_training_page(self):
        """创建AI模型训练页面"""
        page = QWidget()
        layout = QVBoxLayout()

        # 添加启动 AI 模型训练按钮
        self.start_ai_training_button = QPushButton('启动 AI 模型训练', self)
        self.start_ai_training_button.clicked.connect(self.start_ai_model_training)

        # 添加浏览器窗口，用于显示网页内容
        self.ai_web_view = QWebEngineView(self)

        # 布局中添加按钮和浏览器视图
        layout.addWidget(self.start_ai_training_button)
        layout.addWidget(self.ai_web_view, stretch=1)
        page.setLayout(layout)
        return page

    def start_ai_model_training(self):
         # 获取当前脚本的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
          # 将相对路径 'maxkb' 转换为绝对路径
        data_path = os.path.join(current_dir, 'maxkb')
        abs_data_path = os.path.abspath(data_path)
        """启动 Docker 中的 maxkb 容器并在浏览器中显示页面"""
        try:
            result = subprocess.run(["docker", "ps", "-a", "-q", "-f", "name=maxkb"], capture_output=True, text=True)
            container_id = result.stdout.strip()

            if container_id:
                subprocess.run(["docker", "start", "maxkb"], check=True)
            else:
                subprocess.run([
                "docker", "run", "-d", "--name=maxkb", "-p", "8080:8080",
                "-v", f"{abs_data_path}:/var/lib/postgresql/data",
                "1panel/maxkb"
            ], check=True)

            # 更新状态并加载网页
            self.ai_web_view.setHtml("<h3>正在启动 maxkb 服务，请稍候...</h3>")
            QTimer.singleShot(5000, self.load_maxkb_webpage)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "错误", f"启动容器时出错: {str(e)}")

    def load_maxkb_webpage(self):
        """加载 maxkb 容器的 Web 界面"""
        self.ai_web_view.setUrl(QUrl("http://localhost:8080"))  # 加载 AI 模型训练的网页


class DigitalHumanTraining(QWidget):
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.new_video_path = None
        self.dh_name = None

        # 创建标签、按钮和输入框
        self.upload_label = QLabel('', self)  # 显示上传状态
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("请输入数字人名称")
        self.button_train = QPushButton('训练', self)
        self.button_train.setEnabled(False)  # 禁用训练按钮直到上传视频
        self.button_train.clicked.connect(self.run_training)

        # 视频上传按钮
        self.button_upload = QPushButton('上传视频', self)
        self.button_upload.clicked.connect(self.show_video_upload)

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(QLabel('数字人训练页面', self))
        layout.addWidget(self.button_upload)
        layout.addWidget(self.upload_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.button_train)

        self.setLayout(layout)

    def show_video_upload(self):
        """显示文件选择对话框，上传视频"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("视频文件 (*.mp4 *.avi *.mov)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.video_path = selected_file
            self.upload_label.setText(f"已上传视频: {self.video_path}")
            self.button_train.setEnabled(True)  # 启用训练按钮

    def run_training(self):
        """运行训练脚本"""
        self.dh_name = self.name_input.text().strip()
        if not self.dh_name:
            self.upload_label.setText("请先输入数字人名称")
            return

        yuan_folder = os.path.abspath(os.path.join('DH_live-main', 'yuan'))
        if not os.path.exists(yuan_folder):
            os.makedirs(yuan_folder)

        video_extension = os.path.splitext(self.video_path)[1]
        new_video_name = f"{self.dh_name}{video_extension}"
        self.new_video_path = os.path.join(yuan_folder, new_video_name)

        try:
            shutil.copy(self.video_path, self.new_video_path)
            self.upload_label.setText(f"视频已重命名并复制到: {self.new_video_path}")
        except Exception as e:
            self.upload_label.setText(f"视频复制失败: {str(e)}")
            return

        xunlian_path = os.path.abspath(os.path.join('DH_live-main', 'xunlian.py'))
        if not os.path.exists(xunlian_path):
            self.upload_label.setText(f"错误：找不到文件 {xunlian_path}")
            return

        try:
            with open(xunlian_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open(xunlian_path, 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.startswith("video_file"):
                        file.write(f'video_file = "yuan/{new_video_name}"\n')
                    else:
                        file.write(line)

            bat_path = os.path.abspath('shipinxunlian.bat')
            if os.path.exists(bat_path):
                subprocess.Popen(bat_path, shell=True)
                self.upload_label.setText(f'训练已启动，正在使用视频: {self.new_video_path}')
            else:
                self.upload_label.setText(f'错误：找不到文件 {bat_path}')
        except Exception as e:
            self.upload_label.setText(f'训练启动失败: {str(e)}')


# 创建应用
app = QApplication(sys.argv)

# 创建主窗口
window = MainWindow()
window.show()

# 运行应用
sys.exit(app.exec_())
