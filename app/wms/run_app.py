from flask import Flask, redirect, request
from settings import DEBUG
from controllers import UserController

app = Flask(__name__)
app.secret_key = 'ThisIsMyGraduationWork:"WarehouseManagementSystem"'
app.template_folder = "files/templates"
app.static_folder = "files/static"
if DEBUG:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # turns off script caching


@app.route("/")
def index():
    return redirect("/home")


@app.route("/home", methods=["GET", "POST"])
def home():
    controller = UserController(request)
    return controller.index()


if __name__ == "__main__":
    app.run(debug=DEBUG)
