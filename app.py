import urllib.parse
import xml.etree.ElementTree
from flask import Flask, render_template, redirect, abort, request, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from __all_models import *
from api import api
from db_session import global_init, create_session
from forms import *


def get_coords(toponym: str):
    url = "http://geocode-maps.yandex.ru/1.x/?"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "xml",
        "geocode": toponym,
    }
    responce = requests.get(url, params=params)
    tree = xml.etree.ElementTree.XML(responce.text)
    return tree.findtext(".//{*}pos").replace(" ", ",")


def get_image_url(coords: str):
    url = "https://static-maps.yandex.ru/1.x/?"
    params = {
        "ll": coords,
        "l": "sat",
        "z": "13"
    }
    data = urllib.parse.urlencode(params)
    return f"{url}{data}"


app = Flask(__name__)
app.config["SECRET_KEY"] = "strong_password"
app.register_blueprint(api)
login_manager = LoginManager(app)
login_manager.login_view = "login"
global_init("db.db")
session = create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/")
def works_log():
    records = session.query(Jobs, User).join(User).all()
    return render_template("works_log.html", title="Журнал работ",
                           records=records, current_user=current_user)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.login.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(team_leader=form.team_leader.data, job=form.job.data,
                   work_size=form.work_size.data,
                   collaborators=form.collaborators.data,
                   is_finished=form.is_finished.data)
        session.add(job)
        session.commit()
        return redirect("/")
    return render_template("add_job.html", title="Добавить работу", form=form)


@app.route("/job/<int:job_id>", methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    if request.method == "GET":
        job = session.query(Jobs).filter(
            Jobs.id == job_id,
            (Jobs.team_leader == current_user.id) | (current_user.id == 1)
        ).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("add_job.html", title="Изменить работу", form=form,
                           job_id=job_id, delete=True)


@app.route("/deljob/<int:job_id>")
@login_required
def delete_job(job_id):
    job = session.query(Jobs).filter(
        Jobs.id == job_id,
        (Jobs.team_leader == current_user.id) | (current_user.id == 1)
    ).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/departments")
def departments():
    records = session.query(Department, User).join(User).all()
    return render_template("departments.html", title="List of Departments",
                           records=records, current_user=current_user)


@app.route("/adddepartment", methods=["GET", "POST"])
def add_department():
    form = DepartmantForm()
    if form.validate_on_submit():
        dep = Department(title=form.title.data, chief=form.chief.data,
                         members=form.members.data, email=form.email.data)
        session.add(dep)
        session.commit()
        return redirect(url_for("departments"))
    return render_template(
        "add_department.html", title="Add Department", form=form)


@app.route("/department/<int:dep_id>", methods=['GET', 'POST'])
@login_required
def edit_department(dep_id):
    form = DepartmantForm()
    if request.method == "GET":
        dep = session.query(Department).filter(
            Department.id == dep_id,
            (Department.chief == current_user.id) | (current_user.id == 1)
        ).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        dep = session.query(Department).filter(Department.id == dep_id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect(url_for("departments"))
        else:
            abort(404)
    return render_template("add_department.html", title="Изменить работу",
                           form=form, delete=True, dep_id=dep_id)


@app.route("/deldepartment/<int:dep_id>")
@login_required
def delete_department(dep_id):
    dep = session.query(Department).filter(
        Department.id == dep_id,
        (Department.chief == current_user.id) | (current_user.id == 1)
    ).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect(url_for("departments"))


@app.route("/users_show/<int:user_id>")
def show_users_hometown(user_id):
    resp = requests.get(f"http://localhost:5000/api/users/{user_id}")
    if not resp.ok:
        abort(404)
    user = resp.json().get("users")[0]
    url = get_image_url(get_coords(user["city_from"]))
    return render_template(
        "nostalgy.html", title="Hometown", image_url=url, user=user)


if __name__ == '__main__':
    app.run(debug=True)
