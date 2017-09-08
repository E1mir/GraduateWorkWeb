from flask import Flask, redirect, request, flash
from flask_login import login_required, LoginManager
from model import User
from settings import DEBUG
from controllers import UserController, StaticPageController, ServiceController

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.secret_key = 'ThisIsMyGraduationWork:"WarehouseManagementSystem"'
app.template_folder = "files/templates"
app.static_folder = "files/static"
if DEBUG:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # turns off script caching


@app.route("/")
def index():
    return redirect("/home")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    controller = UserController(request)
    return controller.index()


@app.route("/login", methods=["GET", "POST"])
def login():
    controller = UserController(request)
    return controller.login()


@app.route("/register", methods=["GET", "POST"])
def register():
    controller = StaticPageController(request)
    return controller.register()


@app.route("/contact", methods=["GET", "POST"])
def contact():
    controller = StaticPageController(request)
    return controller.contact()


@app.route("/send", methods=["GET", "POST"])
def send_feedback():
    controller = ServiceController(request)
    return controller.send_feedback()


@app.route("/logout")
@login_required
def logout():
    controller = UserController(request)
    return controller.logout()


@app.errorhandler(401)
def page_not_found(e):
    flash("Username or password incorrect")
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


if __name__ == "__main__":
    app.run(debug=DEBUG)
