#!/usr/bin/env python

import argparse
import atexit
import datetime
import smtplib
import sys
from email.mime.text import MIMEText
from typing import Union  # noqa

import peewee
import requests
import schema
import toml
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, abort, request
from pytimeparse import parse

try:
    from . import __version__
except ImportError:
    print("Could not import version. Ignore this error if running under debug mode.")
    __version__ = "x.x.x"


############
# Models


db = peewee.Proxy()


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Alert(BaseModel):
    alert_id = peewee.CharField()
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = ((("alert_id", "timestamp"), False),)


class Notification(BaseModel):
    alert_id = peewee.CharField(unique=True)
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = ((("alert_id", "timestamp"), False),)


def load_config(config_path: str) -> dict:
    try:
        configstr = open(config_path).read()
    except:  # noqa - We don't care *why* this failed.
        app.logger.error("Could not read configuration file %s." % config_path)
        sys.exit(1)

    channel_validation = [schema.And(schema.Use(lambda x: x.lower().strip()), schema.Or(*ALERTING_CHANNELS.keys()))]
    email_validation = schema.And(str, lambda x: "@" in x, error="Email address invalid.")
    s = schema.Schema(
        schema.And(
            schema.Use(toml.loads),
            {
                schema.Optional("config"): {schema.Optional("secret_key"): str},
                "alerting": {
                    schema.Optional("email"): {
                        "recipient_emails": [email_validation],
                        "from_addr": email_validation,
                        schema.Optional("hostname", default="localhost"): str,
                        schema.Optional("port", default=25): int,
                        schema.Optional("username", default=""): str,
                        schema.Optional("password", default=""): str,
                        schema.Optional("encryption", default="none"): schema.And(
                            schema.Use(lambda x: x.lower().strip()), schema.Or("none", "ssl", "starttls")
                        ),
                    },
                    schema.Optional("telegram"): {"chat_id": str, "apikey": str},
                },
                "alerts": {
                    schema.Optional("default_channels", default=["email"]): channel_validation,
                    str: {
                        "every": schema.And(
                            str,
                            schema.Use(parse),
                            schema.Use(lambda x: datetime.timedelta(seconds=x)),
                            error="Could not parse interval.",
                        ),
                        schema.Optional("recipient_emails", default=None): [email_validation],
                        schema.Optional("notify_every"): schema.And(
                            str,
                            schema.Use(parse),
                            schema.Use(lambda x: datetime.timedelta(seconds=x)),
                            error="Could not parse interval.",
                        ),
                        schema.Optional("channels"): channel_validation,
                    },
                },
            },
        )
    )
    try:
        config = s.validate(configstr)
    except schema.SchemaError as e:
        app.logger.error("Configuration error: %s" % str(e).replace("\n", " "))
        sys.exit(1)

    return config


############
# Utilities


def notify(subject: str, body: str, config: dict, alert_id: str) -> None:
    if "channels" in config["alerts"][alert_id]:
        channels = config["alerts"][alert_id]["channels"]
    else:
        channels = config["alerts"]["default_channels"]

    for channel_name in channels:
        notification_fn = ALERTING_CHANNELS[channel_name]
        notification_fn(subject, body, config["alerting"].get(channel_name, {}), config["alerts"][alert_id])


def notify_console(subject: str, body: str, config: dict, alert: dict) -> None:
    print(subject)


def notify_telegram(subject: str, body: str, config: dict, alert: dict) -> None:
    telegram_url = "https://api.telegram.org/bot{API}/sendMessage".format(API=config["apikey"])
    requests.get(telegram_url, params={"chat_id": config["chat_id"], "text": body})


def notify_email(subject: str, body: str, config: dict, alert: dict) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config["from_addr"]
    msg["To"] = ", ".join(config["recipient_emails"])

    from icecream import ic

    ic(alert)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    port = config["port"]
    encryption = config["encryption"].lower()
    if encryption == "ssl":
        s = smtplib.SMTP_SSL(host=config["hostname"], port=port)  # type: Union[smtplib.SMTP, smtplib.SMTP_SSL]
        s.ehlo()
    elif encryption == "starttls":
        s = smtplib.SMTP(host=config["hostname"], port=port)
        s.ehlo()
        s.starttls()
    else:
        s = smtplib.SMTP()
        s.connect(host=config["hostname"], port=port)

    if config["username"]:
        s.login(user=config["username"], password=config["password"])

    # Send to the alert's emails, if a list exists, or the default emails list.
    recipient_emails = alert["recipient_emails"] or config["recipient_emails"]
    ic(recipient_emails)
    s.sendmail(config["from_addr"], recipient_emails, msg.as_string())
    s.quit()


ALERTING_CHANNELS = {"console": notify_console, "email": notify_email, "telegram": notify_telegram}


def check_and_notify_broken(
    alert_id: str,
    interval: datetime.timedelta,
    notification_interval: datetime.timedelta,
    config: dict,
    last_checkin_time: datetime.datetime,
) -> None:
    notification, created = Notification.get_or_create(alert_id=alert_id)

    app.logger.info(
        "Checking alert %s: %s, %s, %s"
        % (alert_id, interval, notification_interval, datetime.datetime.now() - notification.timestamp)
    )

    if not created and datetime.datetime.now() - notification.timestamp < notification_interval:
        # If we've already sent a notification within the interval, abort.
        return

    app.logger.info("Notifying that %s broke...", alert_id)
    if created:
        subject = 'Caduceus: Alert "%s" is failing.' % alert_id
    else:
        subject = 'Caduceus: Alert "%s" is still failing.' % alert_id

    body = """Hello!,
Your alert named "%s" is failing to check in. It is configured to check
in every %s, but it hasn't checked in for longer than that.

We last saw this alert on %s. you should look into why it hasn't worked.

Thanks,
Caduceus
""" % (
        alert_id,
        interval,
        last_checkin_time,
    )
    notify(subject, body, config, alert_id)
    notification.timestamp = datetime.datetime.now()
    notification.save()


def check_and_notify_fixed(alert_id: str, config: dict) -> None:
    notifications = list(Notification.select().where(Notification.alert_id == alert_id))
    if not notifications:
        return

    app.logger.info("Notifying that %s is reporting again...", alert_id)
    notify(
        "Caduceus: Alert %s is reporting again." % alert_id,
        """Hello!,
%s is reporting again. All is well.

Thanks,
Caduceus
"""
        % (alert_id,),
        config,
        alert_id,
    )

    # Delete the old notification, as we don't need it any more.
    notifications[0].delete_instance()


############
# Views


app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome."


@app.route("/reset/<alert_id>/")
def reset(alert_id):
    """
    Reset one of the alerts.
    """
    if alert_id not in app.config["CONFIG"]["alerts"]:
        abort(404)

    secret = app.config["CONFIG"]["config"].get("secret_key", "")

    if request.args.get("key", "") and not secret:
        return (
            "The server is not configured to use a secret key. If you did set one,"
            " please double-check your configuration."
        )

    if secret and request.args.get("key", "") != secret:
        abort(404)

    Alert.create(alert_id=alert_id)

    check_and_notify_fixed(alert_id, app.config["CONFIG"])

    return "Alert reset."


def cron():
    with app.app_context():
        alerts = app.config["CONFIG"]["alerts"]
        now = datetime.datetime.now()
        for alert_id, config in alerts.items():
            if alert_id == "default_channels":
                # This isn't an actual alert, rather a setting.
                continue
            last_checkin = Alert.select().where(Alert.alert_id == alert_id).order_by(Alert.timestamp.desc()).limit(1)
            if last_checkin:
                last_checkin_time = last_checkin[0].timestamp
            else:
                # This means that there has been no checkin yet.
                last_checkin_time = app.config["STARTUP_TIME"]

            interval = config["every"]
            if now - last_checkin_time > interval:
                # We haven't seen this in the required interval.
                check_and_notify_broken(
                    alert_id, interval, config.get("notify_every", interval), app.config["CONFIG"], last_checkin_time
                )


def startup(args):
    db.initialize(peewee.SqliteDatabase(args.db))
    db.connect()
    db.create_tables([Alert, Notification])

    config = load_config(args.config)
    app.config["CONFIG"] = config
    app.config["STARTUP_TIME"] = datetime.datetime.now()

    # Delete alerts from the database that are no longer in the config.
    alert_ids = list(config["alerts"].keys())
    Alert.delete().where(Alert.alert_id.not_in(alert_ids)).execute()
    Notification.delete().where(Notification.alert_id.not_in(alert_ids)).execute()

    start_scheduler()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(id="cron_job", func=cron, trigger=IntervalTrigger(seconds=10), replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())


def main():
    parser = argparse.ArgumentParser(description="Notify when scheduled tasks didn't run")
    parser.add_argument("--version", action="version", version="%(prog)s " + str(__version__))

    parser.add_argument(
        "-b", "--db", metavar="DATABASE", default="database.sqlite3", help="The path to the database file"
    )
    parser.add_argument(
        "-c", "--config", metavar="CONFIG", default="caduceus.toml", help="The path to the configuration file"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-i", "--host", type=str, help="The hostname/IP to listen on")
    parser.add_argument("-p", "--port", type=int, help="The port to listen on")

    args = parser.parse_args()
    startup(args)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
