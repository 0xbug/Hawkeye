import smtplib
from email.header import Header
from email.mime.text import MIMEText
from config.database import setting_col, notice_col


class SMTPServer(object):
    def __init__(self, smtp_config):
        self.host = smtp_config.get('host')
        self.port = int(smtp_config.get('port'))
        self.tls = smtp_config.get('tls')
        self.username = smtp_config.get('username')
        self.password = smtp_config.get('password')
        try:
            if self.tls:
                self.smtp = smtplib.SMTP_SSL(self.host, self.port, timeout=300)
                print(self.tls)
                print("tls 已开启")
            else:
                self.smtp = smtplib.SMTP(self.host, self.port, timeout=300)
                print("tls 已关闭")

        except Exception as error:
            print(error)

    def login(self):
        try:
            self.smtp.login(self.username, self.password)
        except Exception as error:
            print(error)

    def sendmail(self, receivers, message):
        """

        :param receivers:
        :param message:
        :return:
        """
        message = message.as_string()
        self.smtp.sendmail(self.username, receivers, message)


def mail_notice(smtp_config, receivers, content):
    """
    :param receivers:
    :param smtp_config:
    :param content:
    :return:
    """

    message = MIMEText(content, _subtype='html', _charset='utf-8')
    message['From'] = Header('{}<{}>'.format(smtp_config.get('from'), smtp_config.get('username')))
    message['To'] = Header(','.join(receivers))
    message['Subject'] = Header('Github 监控邮件发送', 'utf-8')
    try:
        smtp = SMTPServer(smtp_config)
        smtp.login()
        smtp.sendmail(receivers, message)
        return True

    except smtplib.SMTPException as e:
        print("sendmail error:" + str(e))
        return False


if __name__ == '__main__':
    smtp_config = setting_col.find_one({'key': 'mail'})
    receivers = [data.get('mail') for data in notice_col.find({})]
    content = "这里是重要文档"

    print("===========================")
    print("Test email send function")
    print(smtp_config.get('host'))
    print(smtp_config.get('port'))
    print(smtp_config.get('tls'))
    print(smtp_config.get('from'))
    print("===========================")
    mail_notice(smtp_config, receivers, content)
