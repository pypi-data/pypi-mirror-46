import os
import smtplib
import sys
import traceback
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


class Server:
    """
    用于实例化一个发邮件的服务器，并实现邮件发送。

    例如：
    import Server

    host = "xxx.com"
    sender = "username@xxx.com"
    username = "xxx"
    password = "xxx"

    s = server(host, sender, password, username)

    或者

    para_d = {
        'host': host,
        'sender': sender,
        'password': password,
        'username': '',
        'port': 25,
    }

    s = server(**para_d)

    s.sendmail('xxx@xx.com',subject='subject', contect='msg')

    s.close()
    """
    def __init__(self, host: str = None, sender: str = None, password: str = None,
                 username: str = None, port: int = 25,
                 **para_d):
        """
        :param host: 服务器地址
        :param sender: 发件人邮箱地址
        :param password: 登录密码
        :param username: 发件人昵称
        :param port: 端口，默认25
        :param para_d: para_d = {
                            'host': host,
                            'sender': sender,
                            'password': password,
                            'username': '',
                            'port': 25,
                            }
                字典类型传参
        """
        self.host = host if host else para_d.get('host')
        self.port = port if port else para_d.get('port', 25)
        self.sender = sender if sender else para_d.get('sender')
        self.username = username if username else para_d.get('sender') \
            if para_d.get('sender') else sender.split('@')[0]
        self.password = password if password else para_d.get('host')

        if not host:
            raise TypeError('请传入服务器地址')
        if not sender:
            raise TypeError('请传入发件邮箱')
        elif '@' not in sender:
            raise TypeError('发件邮箱不准确')
        else:
            pass
        if not password:
            raise TypeError('请传入密码')
        self.login()

    def login(self):
        """
        登录服务器，实例化一个邮箱
        :return: server对象
        """
        try:
            self._server = smtplib.SMTP(self.host, self.port)
            self._server.ehlo()
            self._server.starttls()
            self._server.ehlo()
            self._server.login(self.username, self.password)
        except smtplib.SMTPException as e:
            print(e)
            sys.exit('服务器认证失败')

    def close(self):
        """
        关闭和邮件服务器的连接
        :return:
        """
        self._server.close()

    def _print(self, e, *args, **kwargs):
        print(str(e), '\n',
              ', '.join([str(i) for i in args]), '\n',
              ', '.join([str(j) for j in kwargs.values()]))

    def send_mail(self, to, subject=None, content=None, cc=None, a=None, email_subtype='mixed', text_subtype='plain'):
        """

        :param to: 收件人，必须参数
        to 和 cc 都支持传输多个收件人，支持列表、元组、字符串，比如
        to = ['tom@xxx.com', 'lucy@xxx.com']
        或者
        to = ('tom@xxx.com', 'lucy@xxx.com')
        或者
        to = 'tom@xxx.com,lucy@xxx.com'
        邮件格式不对会报TypeError错。
        :param subject: （可选）主题，默认'未命名主题'
        :param content: （可选）内容，默认'未命名内容'
        :param cc:（可选） cc收件人，默认空

        :param a: （可选） 附件，文件不存在会报FileNotFoundError
        :param email_subtype: 邮件的类型，默认mixed， 可选'related','alternative'
        :param text_subtype: 文本的类型，默认'plain', 可选'html'
        :return: None
        """
        try:
            self._send_mail(to, subject, content, cc, a, email_subtype, text_subtype)
        except smtplib.SMTPException as e:
            print('发送失败~')
            exc = traceback.format_exc().split('\n')[-2]
            exc_tpye = exc.split(':', 1)[0]
            exc_info = exc.split(':', 1)[1]
            self._print(exc_tpye, exc_info)
            self.close()
        else:
            print('发送成功')
        finally:
            # 可用于记录日志
            pass

    def _send_mail(self, to, subject=None, content=None, cc=None, a=None,
                   email_subtype='mixed', text_subtype='plain', **kwargs):

        subject = subject if subject else '未命名主题'
        content = content if content else '未命名内容'
        msg = MIMEMultipart(_subtype=email_subtype)
        msg['Subject'] = subject
        msg['From'] = self.sender

        to_cc = []

        if isinstance(to, (list, tuple)):
            msg['To'] = ', '.join(to)
            to_cc.extend(list(to))
        elif isinstance(to, str):
            if len(to.split(',')) == 1 and '@' in to:
                msg['To'] = to
                to_cc.append(to)
            elif len(to.split(',')) > 1:
                for _to in to.split(','):
                    if '@' in _to:
                        pass
                    else:
                        raise TypeError('收件人 {} 格式不准确'.format(_to))
                else:
                    msg['To'] = to
                    to_cc.extend(to.split(','))
            else:
                raise TypeError('收件人格式不准确')
        else:
            raise TypeError('收件人地址不准确')

        if cc:
            if isinstance(cc, (list, tuple)):
                msg['cc'] = ', '.join(cc)
                to_cc.extend(list(cc))
            elif isinstance(cc, str):
                if len(cc.split(',')) == 1 and '@' in cc:
                    msg['cc'] = cc
                    to_cc.append(cc)
                elif len(cc.split(',')) > 1:
                    for _cc in cc.split(','):
                        if '@' in _cc:
                            pass
                        else:
                            raise TypeError('抄送收件人 {} 格式不准确'.format(_cc))
                    else:
                        msg['cc'] = cc
                        to_cc.extend(cc.split(','))
                else:
                    raise TypeError('抄送收件人格式不准确')
            else:
                raise TypeError('抄送收件人地址不准确')

        text = MIMEText(content, _subtype=text_subtype, _charset='utf-8')
        # plain html
        msg.attach(text)

        def attach(file, msg=msg):
            if not os.path.exists(file):
                raise FileNotFoundError('文件{}不存在～'.format(file))
            if not os.path.isfile(file):
                raise FileNotFoundError('目标{}不是一个文件'.format(file))
            file_name = file.split("/")[-1]
            with open(file, 'rb') as f:
                _a = f.read()
                part = MIMEApplication(_a)
                part.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(part)

        if a:
            if isinstance(a, (list, tuple)):
                for file in a:
                    attach(file)

            elif isinstance(a, str):
                if len(a.split(',')) == 1:
                    attach(a)
                elif len(a.split(',')) > 1:
                    for _a in a.split(','):
                        attach(_a)
                else:
                    raise TypeError('附件格式不准确')
            else:
                raise TypeError('附件格式不准确')

        self._server.sendmail(self.sender, to_cc, msg.as_string())


