import flask
from flask import Flask,request,render_template
from flask.ext.cas import CAS
from flask.ext.cas import login_required
from qqbot import QQBotSlot as qqbotslot, RunBot
import configparser
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import multiprocessing
from werkzeug.utils import secure_filename
from chatterbot.storage.sqlalchemy_storage import SQLAlchemyDatabaseAdapter
import os,logging

app = Flask(__name__)
cas = CAS(app, '/cas')
app.secret_key = "xpms"
cp = configparser.SafeConfigParser()
cp.read('chatbot.conf')

cas_server = cp.get('chatbot', 'cas_server')
app.config['CAS_SERVER'] = cas_server
app.config['CAS_AFTER_LOGIN'] = 'login'
app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
app.config['CAS_VALIDATE_ROUTE'] = '/cas/serviceValidate'

logging.basicConfig(level=logging.INFO)

@app.route('/')
@login_required
def route_root():
    return "success"


@app.route('/chatbot/train',methods=[ 'POST'])
@login_required
def route_train():
    if (Train()):
        return "训练成功"
    else:
        return "训练失败"


UPLOAD_FOLDER = 'static/datas'
@app.route('/chatbot/upload', methods=[ 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename) #获取一个安全的文件名，且仅仅支持ascii字符；
        if os.path.exists(os.path.join(UPLOAD_FOLDER, fname)):
            os.remove(os.path.join(UPLOAD_FOLDER, fname))
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        return '上传成功'

@app.route('/chatbot/main', methods=['GET'])
@login_required
def main():
    if request.method == 'GET':
        return render_template('main.html')


chatbot = ChatBot("myBot", storage_adapter='chatterbot.storage.SQLAlchemyDatabaseAdapter', database="xp", read_only=True)
#response chat
@qqbotslot
def onQQMessage(bot, contact, member, content):
    # buddy私聊   group群聊
    if(contact.ctype == 'buddy'):
        bot.SendTo(contact, str(chatbot.get_response(content)))
    elif(contact.ctype == 'group'):
        if '@ME' in content:
            bot.SendTo(contact, str(chatbot.get_response(content)))


#train data
def Train():
    try:
        trainbot = ChatBot("trainbot", storage_adapter='chatterbot.storage.SQLAlchemyDatabaseAdapter', database="xp",drop_create=True)
        trainbot.set_trainer(ChatterBotCorpusTrainer)
        trainbot.train(
            "./static/datas/"
        )
        return True
    except KeyboardInterrupt:
        return False

#start flask server
def startServer():
    try:
        host = cp.get('chatbot', 'host')
        port = int(cp.get('chatbot', 'port'))
        print("Server started on" + host + ":" + str(port))
        app.run(host, port, debug=True)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=RunBot, )
    p2 = multiprocessing.Process(target=startServer, )
    p2.start()
    p1.start()
