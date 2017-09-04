from flask import render_template, redirect, flash
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
            "me": "elmir_ide@mail.ru"
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
        # Create a text/plain message
        msg = MIMEText(message_data["message"])
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = message_data["subject"]
        msg['From'] = message_data["sender"]
        msg['To'] = message_data["me"]
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        try:
            message = "Name: {}\n" \
                      "Email: {}\n" \
                      "Subject: {}\n" \
                      "Message: \n{}"
            message.format(
                message_data["name"],
                message_data["sender"],
                message_data["subject"],
                message_data["message"]
            )
            s = smtplib.SMTP('smtp.mail.ru', 465)
            s.starttls()
            s.login("elmir_ide@mail.ru", "MAILRUqwedsazxc1997")
            s.sendmail(message_data["sender"], message_data["me"], message)
            s.quit()
            sending = "success"
        except:
            sending = "error"

        return render_template(
            "pages/feedback.html",
            site={
                "title": "Contact"
            },
            message=sending
        )
