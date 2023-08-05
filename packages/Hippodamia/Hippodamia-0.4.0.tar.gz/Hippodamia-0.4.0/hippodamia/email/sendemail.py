import smtplib
from email.mime.text import MIMEText
from pelops.logging.mylogger import get_child


class SendEmail:
    """
    Classic publish to email implementation.

    config yaml entries:

    email:
            address: smtp.zoho.com  # url of smtp server
            port: 465  # port of smtp server
            from: name123@sender123.com  # sender email address
            credentials-file: ~/credentials.yaml  # a yaml config file with one root entry as described below

    credentials yaml file:

    monitoringservice:
        email:
            config:
                username: username  # username for smtp server
                password: password  # password for smtp server
    """
    _counter = None
    _config = None
    _address = None  # url of smtp server
    _port = None  # port of smtp server
    _username = None  # username for smtp server
    _password = None  # password for smtp server
    _from = None  # sender email address

    def __init__(self, config, logger):
        """
        Constructor

        :param config: yaml config structure
        :param logger: logger instance from the parent. a child will be spawned
        """
        self._config = config
        self._logger = get_child(logger, self.__class__.__name__)
        self._logger.info("__init__")
        self._logger.debug("__init__: {}".format(self._config))
        self._address = self._config["address"]
        self._port = self._config["port"]
        self._username = self._config["username"]
        self._password = self._config["password"]
        self._from = self._config["from"]

        if not self._test_connection():
            self._logger.error("connection test failed")
            raise RuntimeError("connection test failed")
        else:
            self._logger.debug("connection test success")
        self._counter = 0

    def _test_connection(self):
        try:
            server = smtplib.SMTP_SSL(host=self._address, port=self._port)
            server.set_debuglevel(0)
            server.login(self._username, self._password)
            server.noop()
            server.quit()
            return True
        except smtplib.SMTPException as exception:
            self._logger.error("test_connection - failed: {}.".format(exception))
        return False

    def send_message(self, subject, message, to):
        self._logger.info("send_message - to: {}, subject: {}, lem(message): {}".format(to, subject, len(message)))
        msg = MIMEText(message, 'html')
        if isinstance(to, str):
            _to = [to]
        else:
            _to = to

        msg['To'] = ', '.join(_to)
        msg['From'] = self._from
        msg['Subject'] = subject

        try:
            server = smtplib.SMTP_SSL(host=self._address, port=self._port)
            server.set_debuglevel(0)
            server.login(self._username, self._password)
            server.send_message(msg)
        except smtplib.SMTPException as exception:
            self._logger.error("send_message - failed: {}.".format(exception))
            raise

        server.quit()
        self._counter += 1

    def get_stats(self):
        stats = {
            "count": self._counter,
            "address": self._address,
            "port": self._port,
            "from": self._from
        }
        return stats
