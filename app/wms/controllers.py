#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from settings import USER, PASSWORD, SMTP
from abc import ABCMeta
import smtplib
from email.mime.text import MIMEText


class Controller(object):
    """
        Base controller class
        :ivar request: web requests
    """
    __metaclass__ = ABCMeta

    def __init__(self, request):
        self.request = request


class UserController(Controller):
    """
        Controller for users
    """

    def __init__(self, request):
        super(UserController, self).__init__(request)

    def index(self):
        return render_template(
            "pages/home.html",
            site={
                "title": "Warehouse Management System"
            }
        )


class StaticPageController(Controller):
    """
        Controller for static page likes About or Contact
    """

    def __init__(self, request):
        super(StaticPageController, self).__init__(request)

    def contact(self):
        return render_template(
            "pages/feedback.html",
            site={
                "title": "Contact"
            }
        )


class ServiceController(Controller):
    def __init__(self, request):
        super(ServiceController, self).__init__(request)

    def get_form_data(self):
        form_data = {
            "me": USER
        }
        if "userName" in self.request.form:
            form_data["user_name"] = self.request.form["userName"]
        if "userEmail" in self.request.form:
            form_data["sender"] = self.request.form["userEmail"]
        if "userMessage" in self.request.form:
            form_data["message"] = self.request.form["userMessage"]
        if "userSubject" in self.request.form:
            form_data["subject"] = self.request.form["userSubject"]
        return form_data

    def send_feedback(self):
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        message_data = self.get_form_data()

        # Send the message via our own SMTP server, but don't include the
        # envelope header.

        message = "Name: {0}\nSender: {1}\nSubject: {2}\nMessage:\n\n{3}".format(
            message_data["user_name"].encode('utf-8'),
            message_data["sender"].encode('utf-8'),
            message_data["subject"].encode('utf-8'),
            message_data["message"].encode('utf-8')
        )
        # Create a text/plain message
        msg = MIMEText(message)
        msg['Subject'] = message_data["subject"]
        msg['From'] = message_data["me"]
        msg['To'] = message_data["me"]
        session = smtplib.SMTP(SMTP["HOST"], SMTP["PORT"])
        session.starttls()
        session.login(user=USER, password=PASSWORD)
        session.sendmail(message_data["me"], message_data["me"], msg.as_string())
        session.quit()
        return "success"
