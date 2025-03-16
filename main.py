from flask import Flask, request, render_template, redirect, session, make_response

from user import create_user_table, User
from video import create_video_table, Video

import secrets



create_user_table()
create_video_table()
app = Flask("main")
app.secret_key = secrets.token_hex(32)

@app.route("/")
def recomend_page():
    videos = Video.get_all()
    username = session.get("username", None)
    user = None
    if username:
        user = User.get_user_by_username(username)

    return render_template("index.html", videos=videos, user=user)

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

@app.route("/profile", methods=["POST", "GET"])
def profile_page():
    username = session.get("username")

    user = User.get_user_by_username(username)

    if not username:
         return redirect("/login")

    if request.method == "GET":
        videos = Video.get_by_author(user.id)
        return render_template("profile.html", user=user, videos=videos)
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        file_name = request.files["file_name"]

        file_name.save(f"static/uploads/{file_name.filename}")

        Video.create(title, text, file_name.filename, user.id)
        return redirect('/profile')
@app.route("/profile/<int:id>")
def unknow_profile_page(id):
    pass


@app.route("/login", methods=["POST", "GET"])
def login_page():
    user_session = session.get("username")
    print(user_session)

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = User.get_user_by_username(username)
        if not user:
            return render_template("login.html", error="Неправльный логин или пароль.")

        if user.password == password:
            session["username"] = username
            return redirect('/')
        else:
            return render_template("login.html", error="Неправильный логин или пароль.")

@app.route("/subscribes")
def subscribes_page():
    pass


@app.route("/music")
def music_page():
    pass

@app.route("/quit")
def quit_page():
    del session["username"]
    return redirect('/login')

app.run(host='0.0.0.0', port=8080, debug=True)
