#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, abort
from flask_login import logout_user, login_user
from settings import USER, PASSWORD, SMTP
from model import User
from abc import ABCMeta
import smtplib
from email.mime.text import MIMEText

user_session_id = 0


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

    def __init__(self, request, user=None):
        self.user = user
        super(UserController, self).__init__(request)

    def init_user(self):
        if "username" in self.request.form and "password" in self.request.form:
            username = self.request.form['username']
            password = self.request.form['password']
            if password == username + "_":
                global user_session_id
                user_session_id += 1
                self.user = User(user_session_id)

    def login(self):
        self.init_user()
        if self.request.method == "POST":
            if self.user is not None:
                if self.user.type == "admin":
                    login_user(self.user)
                    next_page = self.request.args.get("next")
                    if next_page is None:
                        return redirect("/home")
                    else:
                        return redirect(next_page)
                else:
                    return abort(423)
            else:
                return abort(401)
        else:
            return render_template(
                "login.html",
            )

    def logout(self):
        logout_user()
        flash("Logged out!")
        return render_template(
            "login.html",
        )

    def index(self):
        return render_template(
            "pages/home.html",
            site={
                "title": "Warehouse Management System"
            },
            user=self.user
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

    def get_register_data(self):
        user_data = None
        if self.request.method == "POST":
            user_data = {
                "balance": 0,
                "permission": "default"
            }
            if "username" in self.request.form:
                user_data["username"] = str(self.request.form["username"]).lower()
            if "email" in self.request.form:
                user_data["email"] = str(self.request.form["email"]).lower()
            if "password" in self.request.form:
                user_data["password"] = str(self.request.form["password"]).encode("utf-8")
            if "type" in self.request.form:
                user_data["type"] = self.request.form["type"]
        return user_data

    def registration(self):
        return render_template(
            "register.html"
        )

    def register(self):
        if self.request.method == "POST":
            user_data = self.get_register_data()
            print user_data
            flash("You are registered! You can use new account on our mobile app!")
            return render_template(
                "login.html",
                msg_type="success"
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
