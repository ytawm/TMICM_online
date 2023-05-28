import os
# import shutil
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from flask import Flask, render_template, flash, request, redirect, session
from prediction import Voting
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
# V = Voting(model1='models/model2.pth', model2='models/model4.pth', model3='models/model5.pth')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('if_logged', None)
    flash('退出')
    return redirect('/')


def predict_result(img_path):
    V = Voting(model1='models/model2.pth', model2='models/model4.pth', model3='models/model5.pth')
    pred_label = V.predict(img_path)
    pred_info = '该图像的类别是：' + str(pred_label)
    return str(pred_label), ["预测结果：", pred_info, os.path.basename(img_path), ""]


@app.route('/', methods=['POST', 'GET'])
def index():
    show_email = False
    img_paths = None
    if request.method == 'POST':
        if 'button1' in request.form:
            f = request.files['file']
            if f.filename != '':
                f.save("tmp/" + secure_filename(f.filename))
                img_path = "tmp/" + f.filename.replace(' ', '_').replace('(', '').replace(')', '')
                # shutil.copy(img_path, 'static')
                pred_label, prediction = predict_result(img_path)
                print('pred_label:', pred_label)
                if pred_label == 'malignant':
                    show_email = True
                else:
                    show_email = False
                os.remove(img_path)

                return render_template('index.html', prediction=prediction, show_email=show_email)

            else:
                return render_template('index.html', prediction=['预测结果：', '亲，你确定你上传图像了吗？', '', ''],
                                       show_email=show_email)

        if 'button2' in request.form:
            email_content = request.form['content']
            print('email_content:', email_content, img_paths)
            # sent_email(email_content)
            show_email = True
            # ["预测结果：", "邮件发送成功...", str(os.path.basename(img_paths)), str(email_content)]
            return render_template('index.html', prediction=["预测结果：", str(email_content) + "。该邮件发送成功...", "",
                                                             str(email_content)], show_email=show_email)

    return render_template('index.html', prediction=['预测结果：', '请选择一张图片...', '', ''], show_email=show_email)


def sent_email(email_content):
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "2318622235@qq.com"  # 用户名
    mail_pass = "KPIMQMFJIRJUGXWF"  # 获取授权码
    sender = 'wang_ruiqi_ssisp@163.com'  # 发件人账号
    receivers = ['wang_ruiqi_ssisp@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    send_content = email_content
    message = MIMEText(send_content, 'plain', 'utf-8')  # 第一个参数为邮件内容,第二个设置文本格式，第三个设置编码
    message['From'] = Header("发件人", 'utf-8')  # 发件人
    message['To'] = Header("收件人", 'utf-8')  # 收件人

    subject = '图像识别结果分析'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    app.run(debug=True)
