from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from twitter_api import get_user_details, get_nonfollowers_list

app = application = Flask(__name__)
app.secret_key = "super secret 123"
app.config["SESSION_TYPE"] = "filesystem"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/list', methods=['POST'])
def list():
    screen_name = request.values['twitter_handle'].strip()
    if not screen_name:
        return redirect(url_for("home"))
    user_info =  get_user_details(screen_name)
    if "nonfollowers" not in session:
        session["nonfollowers"] = get_nonfollowers_list(screen_name)

    nonfollowers = session["nonfollowers"]
    return render_template("list.html", nonfollowers=nonfollowers, user_info=user_info)


if __name__ == "__main__":
    app.run(debug=True)
