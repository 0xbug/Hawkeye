import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SMTPServer(object):
    def __init__(self, smtp_config):
        self.host = smtp_config.get('host')
        self.port = int(smtp_config.get('port'))
        self.tls = smtp_config.get('tls')
        self.username = smtp_config.get('username')
        self.password = smtp_config.get('password')
        try:
            if self.tls:
                self.smtp = smtplib.SMTP(self.host, self.port, timeout=300)
            else:
                self.smtp = smtplib.SMTP_SSL(self.host, self.port, timeout=300)
        except Exception as error:
            print(error)

    def login(self):
        try:
            if self.tls:
                self.smtp.starttls()
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
    message['From'] = Header('{}<{}>'.format(smtp_config.get('from'), smtp_config.get('username')), 'utf-8')
    message['To'] = Header(';'.join(receivers), 'utf-8')
    message['Subject'] = Header('[GitHub] 监控告警', 'utf-8')
    try:
        smtp = SMTPServer(smtp_config)
        print('login')
        smtp.login()
        smtp.sendmail(receivers, message)
        return True

    except smtplib.SMTPException:
        return False
