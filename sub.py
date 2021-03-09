from __all_models import *
from db_session import *


global_init("db.db")
session = create_session()

cats = (3, 1, 3, 2, 5, 4)
for index, job in enumerate(session.query(Jobs).all()):
    job.categories.clear()
    category = session.query(Category).filter(
        Category.id == cats[index]).first()
    job.categories.append(category)
session.commit()
