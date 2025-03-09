from flask import Flask, request, render_template, redirect, session, make_response

from user import create_user_table, User

import secrets

create_user_table()
app = Flask("main")
app.secret_key = secrets.token_hex(32)

@app.route("/")
def recomend_page():
    response = make_response('hello world')  # создание объекта ответа
    response.set_cookie('cookie_name', 'cookie_value', 3600)
    return response

@app.route("/registration", methods=["POST", "GET"])
def register_page():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")


        user = User.get_user_by_username(username)
        if user:
            return render_template(
                "register.html", error="Пользователь с таким ником уже есть"
            )

        if password != confirm_password:
            return render_template(
                "register.html", error="Пароли не совпадают"
            )

        User.create(username, password)
        session["username"] = username
        return redirect('/')

@app.route("/profile/<int:id>")
def profile_page(id):
    pass

@app.route("/subscribes")
def subscribes_page():
    pass


@app.route("/music")
def music_page():
    pass

@app.route("/quit")
def quit_page():
    pass

app.run(host='0.0.0.0', port=8080, debug=True)
