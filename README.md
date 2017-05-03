# qqchatbot
一个python版flask web项目,同时也对接了CAS单点登录,简单集成chatterbot和qqbot的智能聊天机器人,存储使用sqlite3。提供了上传文件,训练文件的接口.

使用框架 智能回复:https://github.com/gunthercox/ChatterBot 的项目


smartqq: https://github.com/pandolia/qqbot

python 版本3.x


使用说明：

pip install chatterbot


pip install qqbot


pip install flask


pip install flask-cas


pip install sqlalchemy


执行：python flaskMain.py -u qq号
