from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from __all_models import *
from db_session import global_init, create_session
from forms import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "strong_password"
login_manager = LoginManager(app)
login_manager.login_view = "login"
global_init("db.db")
session = create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/")
def works_log():
    query = session.query(Jobs, User).join(User)
    records = query.all()
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
    print(current_user.id)
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


if __name__ == '__main__':
    app.run(debug=True)
