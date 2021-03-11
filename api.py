from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from __all_models import *
from db_session import global_init, create_session


api = Blueprint("api", __name__, url_prefix="/api")
jobs_fields = ("id", "team_leader", "job", "work_size", "collaborators",
               "start_date", "end_date", "is_finished")
jobs_short_fields = ('job', 'team_leader', 'work_size', 'collaborators',
                     'is_finished', 'id')
users_fields = ("id", "surname", "name", "age", "position", "speciality",
                "address", "email", "password")
global_init("db.db")
session = create_session()


@api.route("/jobs")
def get_jobs():
    jobs = session.query(Jobs).all()
    return jsonify({
        "jobs": [job.to_dict(only=jobs_fields) for job in jobs]
    })


@api.route("/jobs", methods=["POST"])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in jobs_short_fields):
        return jsonify({'error': 'Bad request'})
    elif session.query(Jobs).get(request.json["id"]) is not None:
        return jsonify({"error": "Id already exists"})
    job = Jobs(**request.json)
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/jobs", methods=["DELETE"])
def delete_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif "id" not in request.json:
        return jsonify({"error": "Bad request"})
    job = session.query(Jobs).get(request.json["id"])
    if not job:
        return jsonify({"error": "No job found"})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/jobs", methods=["PUT"])
def edit_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in jobs_short_fields) or "id" not in request.json:
        return jsonify({'error': 'Bad request'})
    job = session.query(Jobs).get(request.json["id"])
    if not job:
        return jsonify({"error": "No job found"})
    for key in request.json:
        setattr(job, key, request.json[key])
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/jobs/<int:job_id>")
def get_job_by_id(job_id):
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({"error": "Not found"})
    return jsonify({
        "jobs": [job.to_dict(only=jobs_fields)]
    })


@api.route("/users")
def get_users():
    users = session.query(User).all()
    return jsonify({
        "users": [user.to_dict() for user in users]
    })


@api.route("/users", methods=["POST"])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in users_fields):
        return jsonify({'error': 'Bad request'})
    elif session.query(User).get(request.json["id"]) is not None:
        return jsonify({"error": "Id already exists"})
    request.json["hashed_password"] = generate_password_hash(
        request.json.pop("password"))
    user = User(**request.json)
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/users", methods=["DELETE"])
def delete_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif "id" not in request.json:
        return jsonify({"error": "Bad request"})
    user = session.query(User).get(request.json["id"])
    if not user:
        return jsonify({"error": "No user found"})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/users", methods=["PUT"])
def edit_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in users_fields) or "id" not in request.json:
        return jsonify({'error': 'Bad request'})
    user = session.query(User).get(request.json["id"])
    if not user:
        return jsonify({"error": "No user found"})
    for key in request.json:
        setattr(user, key, request.json[key])
    session.commit()
    return jsonify({'success': 'OK'})


@api.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "Not found"})
    return jsonify({
        "users": [user.to_dict()]
    })
