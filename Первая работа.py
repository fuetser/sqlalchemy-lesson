from datetime import datetime
from __all_models import *
from db_session import global_init, create_session


def main():
    global_init("db.db")
    session = create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.now()
    job.is_finished = False
    session.add(job)
    session.commit()


if __name__ == '__main__':
    main()
