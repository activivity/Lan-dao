通过MaxKB容器训练直播互动模型，具备智能互动能力，通过微调预训练的语言模型来适应特定的直播场景需求，提升数字人的交互体验。基于TTS和Wav2lip开发语音克隆和唇形同步算法，通过预训练数字人模型的方式压缩生成时间，并根据多模态数据（如表情、语言等）进行微调，优化模型的计算性能，保证数字人在高并发环境下的实时响应，使数字人交互速度达到实时交互水平（5s）。

使用逻辑
三种启动模式
1 只启动数字人系统。
首先在数字人模型切换下拉框中选择要使用的数字人模型，并点击确认更换数字人模型。然后点击主界面里的启动数字人系统按钮，初始化tts算法和唇形替换算法。然后可以把想要生成的文案输入到输入框内，点击确定生成数字人，程序会开始运行。生成出来的视频会保存在
2 只启动互动系统
首先在主界面顶部输入要进行ai互动的直播间链接（一般是自己的直播间链接），然后点击主界面的中的启动互动系统按钮，启动互动系统。程序会实时爬取直播间内观众的弹幕信息，并调用本地大模型进行智能回复（本地大模型可以根据直播间内容，商品信息等做微调训练）
3 同时启动互动系统和数字人生成系统
按照上面的步骤同时启用互动系统和数字人生成系统。程序会自动爬取直播间弹幕，并调用本地大模型进行智能回复，回复的内容会作为文本输入，生成实时回复的数字人视频。
