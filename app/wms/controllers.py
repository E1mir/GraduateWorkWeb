from flask import render_template
from abc import ABCMeta


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
        return render_template("pages/home.html")
