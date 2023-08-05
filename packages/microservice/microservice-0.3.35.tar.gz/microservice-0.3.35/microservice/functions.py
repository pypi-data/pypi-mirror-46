import itertools
import logging
import os
import platform
import socket
from email.mime.text import MIMEText
from hashlib import md5
from smtplib import SMTP_SSL, SMTP
from time import perf_counter as pc

import requests
from asgiref.sync import sync_to_async
from telebot import TeleBot

try:
    import boto3
except ImportError:
    boto3 = None

from .exceptions import InternalError

import cfg


class TelegramReporter:
    last_error = None
    bot = TeleBot(cfg.app.telegram_bot_token)
    host = socket.gethostbyname_ex(socket.gethostname())
    addr = os.environ.get('REMOTE_ADDR', "")

    @staticmethod
    def telegram_error(traceback, info=None):
        """
        Отправляет сообщение в телеграм с ошибкой на сервере
        :param traceback: list of error lines
        """
        config = cfg.app.telegram_reporter.get(platform.node())
        if not config:
            logging.warning("Telegram reporter: Unknown host, can't send message")
        else:
            text = (
                "<b>Error on {name}, node: {host}, {addr}</b>\n"
                "{log}\n"
                "<pre>{body}</pre>\n"
                "<b>Token:</b> {token}\n"
                "<pre>{traceback}</pre>"
            ).format(
                name=config["name"],
                host=TelegramReporter.host,
                addr=TelegramReporter.addr,
                log=info["log"],
                body=info["body"],
                token=info["token"],
                traceback="".join(traceback).replace("<", "").replace(">", ""),
            )
            logging.info("Sending error from node {} to chat {}".format(config["name"], config["chat_id"]))
            if text != TelegramReporter.last_error:
                TelegramReporter.last_error = text
                TelegramReporter.bot.send_message(config["chat_id"], text, parse_mode="html")

    @staticmethod
    def send_message(chat_id, message, only_prod=False, ignore_tests=True, footer=True):
        if ignore_tests and TelegramReporter.host[0].startswith("runner"):
            return
        if only_prod and "Production" not in TelegramReporter.host[0]:
            return
        if footer:
            message = (
                "{}\n"
                "<b>Host:</b> {}, {} "
                "<b>DB:</b> {} "
            ).format(message, TelegramReporter.host, TelegramReporter.addr, cfg.db.host)
        TelegramReporter.bot.send_message(chat_id, message, disable_web_page_preview=True, parse_mode="html")

    @staticmethod
    @sync_to_async
    def send_async(chat_id, message, only_prod=False, ignore_tests=True, footer=False):
        TelegramReporter.send_message(chat_id, message, only_prod=only_prod, ignore_tests=ignore_tests, footer=footer)

    @staticmethod
    def send_picture(chat_id, link):
        TelegramReporter.bot.send_photo(chat_id, link)


def send_mail_smtp(to, text, subject, type="plain", sentry=None):
    # send mail via smtp host
    if cfg.app.smtp_ssl:
        smtp = SMTP_SSL(cfg.app.smtp_host, port=cfg.app.smtp_port)
        smtp.login(cfg.app.smtp_login, cfg.app.smtp_password)
    else:
        smtp = SMTP(cfg.app.smtp_host, port=cfg.app.smtp_port)

    msg = MIMEText(text or "", _subtype=type)
    msg["Subject"] = subject
    msg["From"] = cfg.app.smtp_from
    msg["To"] = to

    recpts = smtp.sendmail(cfg.app.support_email, to, msg.as_string())
    smtp.quit()

    if sentry:
        for addr in to:
            sentry.captureMessage("email is sent",
                                  level=logging.INFO if addr in recpts else logging.WARNING,
                                  tags={"email": addr})

    return len(recpts) > 0


def send_mail_aws(to, text, subject, type="plain", sentry=None):
    # send mail via amazon ses
    client = boto3.client('ses', region_name=cfg.aws.email_region_name, aws_access_key_id=cfg.aws.email_key,
                          aws_secret_access_key=cfg.aws.email_secret)
    if type == "plain":
        message = {"Text": {"Charset": "utf-8", "Data": text}}
    else:
        message = {"Html": {"Charset": "utf-8", "Data": text}}
    _to = to if isinstance(to, (list, tuple)) else [to]
    response = client.send_email(Destination={"ToAddresses": _to},
                                 Message={"Subject": {"Charset": "utf-8", "Data": subject}, "Body": message},
                                 Source=cfg.app.smtp_from)
    response_level_ok = 200 <= response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500) < 400

    if sentry:
        for addr in _to:
            sentry.captureMessage("email is sent",
                                  level=logging.INFO if response_level_ok else logging.WARNING,
                                  extra={"response": response}, tags={"email": addr})

    return response_level_ok


send_mail = None
if cfg.app.send_mail == "smtp":
    send_mail = send_mail_smtp
elif cfg.app.send_mail == "aws":
    send_mail = send_mail_aws
    if boto3 is None:
        raise InternalError("Please, install boto3 to use Amazon SES")
else:
    raise NotImplementedError("Unknow send_mail method")


@sync_to_async
def send_mail_async(*args, **kwargs):
    return send_mail(*args, **kwargs)


def chunks(iterable, n):
    """
    Разделить итератор на куски по n элементов
    :param iterable: итератор
    :param n: количество элементов в куске
    """
    it = iterable
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


# def extract_results(results, *args, **kwargs):
#     """
#     Извлечь список из результатов пиви или эластика
#     :param extra_attrs: аттрибуты из результата, которые надо включить в словарь (peewee)
#     :param results: ответ эластика или пиви
#     :return: list
#     """
#     if len(results) > 0:
#         lst = [x.dict(*args, **kwargs) for x in results]
#     else:
#         lst = []
#     return lst
#
#
# def extract_one(results, *args, **kwargs):
#     for x in results:
#         return x.dict(*args, **kwargs)
#     return None


async def location(ip):
    if cfg.app.ipstack_api_key:
        country = requests.request("GET", "http://api.ipstack.com/{}?access_key={}".format(ip, cfg.app.ipstack_api_key)).json()
    else:
        country = {}
    return country


async def gravatar(email):
    digest = md5(email.lower().encode("utf-8")).hexdigest()
    return "https://www.gravatar.com/avatar/{}?d=retro&s={}".format(digest, 500)


class DummyAtomic:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *kwargs):
        pass


def check_atomic(obj, atomize=True):
    if obj and atomize is True:
        return obj.atomic()
    else:
        return DummyAtomic()


class Timer:
    def __init__(self):
        self.start_time = pc()
        self.mark = pc()
        self.counter = 0

    def step(self, step="Step"):
        from_prev = pc() - self.mark
        from_start = pc() - self.start_time
        logging.debug("Step {} {}: {:.3f} from prev step, {:.3f} from start".format(self.counter, step, from_prev*1000, from_start*1000))
        self.mark = pc()
        self.counter += 1
