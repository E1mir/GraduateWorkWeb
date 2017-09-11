from flask import Flask, redirect, request, flash
from flask_login import login_required, LoginManager
from model import User
from settings import DEBUG, TEMPLATE_FOLDER, STATIC_FOLDER, S_KEY
from controllers import UserController, StaticPageController, ServiceController

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "alert-danger"
app.secret_key = S_KEY
app.template_folder = TEMPLATE_FOLDER
app.static_folder = STATIC_FOLDER
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


@app.route("/accounts", methods=["GET", "POST"])
@login_required
def accounts():
    controller = UserController(request)
    return controller.accounts()


@app.route("/login", methods=["GET", "POST"])
def login():
    controller = StaticPageController(request)
    return controller.login()


@app.route("/signIn", methods=["GET", "POST"])
def sign_in():
    controller = UserController(request)
    return controller.login()


@app.route("/registration", methods=["GET", "POST"])
def registration():
    controller = StaticPageController(request)
    return controller.registration()


@app.route("/register", methods=["GET", "POST"])
def register():
    controller = ServiceController(request)
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


'''Error handlers'''


@app.errorhandler(401)
def page_not_found(e):
    message = str(e).split(":")[1].rstrip()
    flash(message, 'alert-danger')
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


if __name__ == "__main__":
    app.run(debug=DEBUG)
