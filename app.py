from flask import Flask, render_template, redirect
from werkzeug.security import generate_password_hash
from __all_models import *
from db_session import global_init, create_session
from forms import RegisterForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "strong_password"
global_init("db.db")
session = create_session()


@app.route("/")
def works_log():
    query = session.query(Jobs, User).join(User)
    records = query.all()
    return render_template(
        "works_log.html", title="Журнал работ", records=records)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.login.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.hashed_password = generate_password_hash(form.password.data)
        user.address = form.address.data
        session.add(user)
        session.commit()
        return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


if __name__ == '__main__':
    app.run(debug=True)
