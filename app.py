from flask import Flask, render_template
from __all_models import *
from db_session import global_init, create_session


app = Flask(__name__)
global_init("db.db")
session = create_session()


@app.route("/")
def works_log():
    query = session.query(Jobs, User).join(User)
    records = query.all()
    return render_template(
        "works_log.html", title="Журнал работ", records=records)


if __name__ == '__main__':
    app.run(debug=True)
