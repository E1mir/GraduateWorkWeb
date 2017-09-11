#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, abort
from flask_login import logout_user, login_user
from settings import USER, PASSWORD, SMTP
from model import User, DatabaseConnector, StorageAccountModel, StorageTypeModel, WMSAccountsModel, WMSTypesModel, \
    encrypt_pass
from abc import ABCMeta
import smtplib
from email.mime.text import MIMEText


class Storage(object):
    def __init__(self):
        self.storage = DatabaseConnector("wms")

    def get_all_users(self):
        users = self.storage.collection("accounts").find({}).sort("permission")
        for account in users:
            yield StorageAccountModel(account)

    def log_in(self, username, password):
        account = self.storage.collection("accounts").find_one({"$or": [{"username": username}, {"email": username}]})
        if account["password"] != password:
            return abort(401)
        else:
            return User(account["_id"], account["permission"])

    def register(self, obj):
        self.storage.insert("accounts", obj)
        return "registered"

    def check_unique(self, user):
        username = self.storage.collection("accounts").count({"username": user["username"]})
        email = self.storage.collection("accounts").count({"email": user["email"]})
        if username > 0:
            return "Username"
        elif email > 0:
            return "Email"
        else:
            return "Unique"

    def get_types(self):
        types = self.storage.collection("types").find({})
        for account_type in types:
            yield StorageTypeModel(account_type)


class Controller(object):
    """
        Base controller class
        :ivar request: web requests
    """
    __metaclass__ = ABCMeta

    def __init__(self, request):
        self.storage = Storage()
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
            username = str(self.request.form["username"]).lower()
            password = encrypt_pass(str(self.request.form['password']).encode("utf-8"))
            self.user = self.storage.log_in(username, password)

    def login(self):
        self.init_user()
        if self.user is not None:
            if self.user.permission == "admin":
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

    def accounts(self):
        permissions = ["admin", "default"]
        types = self.storage.get_types()
        get_accounts = self.storage.get_all_users()
        model = WMSAccountsModel()
        model.types = types
        model.permissions = permissions
        model.accounts = get_accounts
        return render_template(
            "account/accounts.html",
            site={
                "title": "WMS Accounts"
            },
            model=model
        )

    @staticmethod
    def logout():
        logout_user()
        flash("Logged out!", 'alert-warning')
        return render_template(
            "login.html",
        )

    def index(self):
        return render_template(
            "account/home.html",
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

    @staticmethod
    def contact():
        return render_template(
            "feedback.html",
            site={
                "title": "Contact"
            }
        )

    def registration(self):
        model = WMSTypesModel()
        model.types = self.storage.get_types()
        return render_template(
            "register.html",
            model=model
        )

    @staticmethod
    def login():
        return render_template(
            "login.html"
        )


class ServiceController(Controller):
    def __init__(self, request):
        super(ServiceController, self).__init__(request)

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
                user_data["password"] = encrypt_pass(str(self.request.form["password"]).encode("utf-8"))
            if "type" in self.request.form:
                user_data["type"] = self.request.form["type"]
        return user_data

    def register(self):
        if self.request.method == "POST":
            user_data = self.get_register_data()
            check_u_data = self.storage.check_unique(user_data)
            if check_u_data != "Username" and check_u_data != "Email":
                self.storage.register(user_data)
                flash("You are registered! But you can use new account only in our mobile app!", 'alert-warning')
                return redirect("/login")
            else:
                flash("{} has been already taken!".format(check_u_data), 'alert-danger')
                return redirect("/registration")

    def get_feedback_data(self):
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
        message_data = self.get_feedback_data()

        message = "Name: {0}\nSender: {1}\nSubject: {2}\nMessage:\n\n{3}".format(
            message_data["user_name"].encode('utf-8'),
            message_data["sender"].encode('utf-8'),
            message_data["subject"].encode('utf-8'),
            message_data["message"].encode('utf-8')
        )
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
