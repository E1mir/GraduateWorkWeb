#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, abort
from flask_login import logout_user, login_user
from settings import USER, PASSWORD, SMTP, PERMISSIONS
from model import User, DatabaseConnector, StorageAccountModel, StorageTypeModel, StorageGoodsModel, WMSAccountsModel, \
    WMSTypesModel, WMSWarehouseModel, encrypt_pass
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
        if account is not None:
            if account["password"].encode('utf-8') != password:
                return None
            else:
                return User(account["_id"], account["permission"])
        else:
            return None

    def register(self, obj):
        self.storage.insert("accounts", obj)
        return "registered"

    def edit_user(self, username, edited_user):
        self.storage.save("accounts", {"username": username}, edited_user)
        return "edited"

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
        types = self.storage.collection("types").find({}).sort("name", 1)
        for account_type in types:
            yield StorageTypeModel(account_type)

    def add_new_type(self, new_type):
        if self.storage.count_by_query("types", {"name": new_type["name"]}) == 0:
            self.storage.insert("types", new_type)
            return "Success"
        else:
            return "Exist"

    def get_goods(self):
        goods = self.storage.collection("warehouse").find({}).sort("type", 1)
        for product in goods:
            yield StorageGoodsModel(product)

    def add_product(self, new_product):
        if self.storage.count_by_query("warehouse", {"name": new_product["name"]}) == 0:
            self.storage.insert("warehouse", new_product)
            return "Success"
        else:
            return "Exist"

    def edit_product(self, name, updated_product):
        if name != updated_product["name"]:
            if self.storage.count_by_query("warehouse", {"name": updated_product["name"]}) == 1:
                return "Denied"
        self.storage.save("warehouse", {"name": name}, updated_product)
        return "Edited"


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
            password = encrypt_pass(str(self.request.form['password'].encode('utf-8')))
            self.user = self.storage.log_in(username, password)

    def login(self):
        self.init_user()
        if self.user is not None:
            if self.user.permission == "admin":
                login_user(self.user)
                next_page = self.request.args.get("next")
                if next_page is None:
                    return redirect("/admin/home")
                else:
                    return redirect(next_page)
            else:
                return abort(401, "Access denied! You don't have permission!")
        else:
            return abort(401, "Username or password incorrect!")

    def accounts(self):
        types = self.storage.get_types()
        get_accounts = self.storage.get_all_users()
        model = WMSAccountsModel()
        model.types = types
        model.permissions = PERMISSIONS
        model.accounts = get_accounts
        return render_template(
            "account/accounts.html",
            site={
                "title": "WMS Accounts"
            },
            model=model
        )

    def types(self):
        types = self.storage.get_types()
        model = WMSTypesModel()
        model.types = types
        return render_template(
            "account/types.html",
            site={
                "title": "WMS Types"
            },
            model=model
        )

    def warehouse(self):
        goods = self.storage.get_goods()
        types = self.storage.get_types()
        model = WMSWarehouseModel()
        model.warehouse = goods
        model.types = list(types)
        return render_template(
            "account/warehouse.html",
            site={
                "title": "WMS Warehouse"
            },
            model=model
        )

    def orders(self):
        return render_template(
            "account/orders.html",
            site={
                "title": "WMS Orders"
            }
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
                "balance": 0.0,
                "permission": "default"
            }
            if "username" in self.request.form:
                user_data["username"] = str(self.request.form["username"]).lower()
            if "email" in self.request.form:
                user_data["email"] = str(self.request.form["email"]).lower()
            if "shopName" in self.request.form:
                user_data["shop_name"] = str(self.request.form["shopName"]).capitalize()
            if "password" in self.request.form:
                user_data["password"] = encrypt_pass(str(self.request.form["password"].encode("utf-8")))
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

    def get_type_data(self):
        type_data = None
        if self.request.method == "POST":
            if "name" in self.request.form:
                type_data = {}
                name = str(self.request.form["name"]).rstrip().capitalize()
                if name != "":
                    type_data["name"] = name
                    return type_data
                else:
                    return None
        return type_data

    def add_type(self):
        new_type_data = self.get_type_data()
        if new_type_data is None:
            flash("Field is empty!", "alert-danger")
            return redirect("/admin/types")
        status = self.storage.add_new_type(new_type_data)
        if status == "Success":
            flash("Type {} added".format(new_type_data["name"]), "alert-success")
            return redirect("/admin/types")
        if status == "Exist":
            flash("Type {} already exist!".format(new_type_data["name"]), "alert-warning")
            return redirect("/admin/types")
        flash("Something went wrong!", "alert-danger")
        return redirect("/admin/types")

    def get_product_data(self):
        product_data = None
        if self.request.method == "POST":
            product_data = {
                "description": "",
                "count": 0
            }
            try:
                product_data["name"] = str(self.request.form["name"]).rstrip().capitalize()
                product_data["type"] = str(self.request.form["type"]).rstrip().capitalize()
                product_data["price"] = float(self.request.form["price"])
            except:
                return None
        return product_data

    def add_product(self):
        new_product_data = self.get_product_data()
        status = self.storage.add_product(new_product_data)
        if status == "Success":
            flash("{} added!".format(new_product_data["name"]), "alert-success")
            return redirect("/admin/warehouse")
        if status == "Exist":
            flash("Product {} already exist!".format(new_product_data["name"]), "alert-warning")
            return redirect("/admin/warehouse")
        else:
            flash("Something went wrong!", "alert-danger")
            return redirect("/admin/warehouse")

    def get_edited_user_data(self):
        updated_data = {}
        if self.request.method == "POST":
            updated_data["username"] = str(self.request.form["username"]).lower()
            updated_data["shop_name"] = str(self.request.form["shopName"]).capitalize()
            updated_data["type"] = self.request.form["type"]
            updated_data["balance"] = float(self.request.form["balance"])
            updated_data["permission"] = self.request.form["permission"]
        return updated_data

    def edit_account(self, username):
        edited_user = self.get_edited_user_data()
        status = self.storage.edit_user(username, edited_user)
        model = WMSAccountsModel()
        model.accounts = self.storage.get_all_users()
        model.types = self.storage.get_types()
        model.permissions = PERMISSIONS
        if status == "edited":
            return render_template(
                "tables/accounts.table.html",
                model=model
            )
        else:
            raise Exception("User not Found!")

    def get_edited_product_data(self):
        product_data = {}
        if self.request.method == "POST":
            product_data["name"] = str(self.request.form["name"]).capitalize()
            product_data["type"] = str(self.request.form["type"]).capitalize()
            product_data["price"] = float(self.request.form["price"])
            if "description" in self.request.form:
                product_data["description"] = self.request.form["description"]
            if "count" in self.request.form:
                product_data["count"] = int(self.request.form["count"])
        return product_data

    def edit_product(self, name):
        edited_product = self.get_edited_product_data()
        status = self.storage.edit_product(name, edited_product)
        model = WMSWarehouseModel()
        model.warehouse = self.storage.get_goods()
        model.types = self.storage.get_types()
        if status == "Edited":
            return render_template(
                "tables/warehouse.table.html",
                model=model
            )
        else:
            return "Product name should be same or unique!!"

    def get_feedback_data(self):
        feedback_data = {
            "me": USER
        }
        if "userName" in self.request.form:
            feedback_data["user_name"] = self.request.form["userName"]
        if "userEmail" in self.request.form:
            feedback_data["sender"] = self.request.form["userEmail"]
        if "userMessage" in self.request.form:
            feedback_data["message"] = self.request.form["userMessage"]
        if "userSubject" in self.request.form:
            feedback_data["subject"] = self.request.form["userSubject"]
        return feedback_data

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
