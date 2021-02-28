from __all_models import *
from db_session import global_init, create_session


def main():
    global_init("db.db")
    session = create_session()
    members = [
        {
            "surname": "Scott",
            "name": "Ridley",
            "age": 21,
            "position": "captain",
            "speciality": "research engineer",
            "address": "module_1",
            "email": "scott_chief@mars.org"
        },
        {
            "surname": "Weer",
            "name": "Andy",
            "age": 26,
            "position": "pilot",
            "speciality": "engineer",
            "address": "module_2",
            "email": "weer_andy@mars.org"
        },
        {
            "surname": "Watny",
            "name": "Mark",
            "age": 23,
            "position": "researcher",
            "speciality": "doctor",
            "address": "module_1",
            "email": "watny_mark@mars.org"
        },
        {
            "surname": "Bean",
            "name": "Shawn",
            "age": 30,
            "position": "eco techic",
            "speciality": "engineer",
            "address": "module_3",
            "email": "bean_shawn@mars.org"
        },
    ]
    for member in members:
        user = User()
        user.surname = member["surname"]
        user.name = member["name"]
        user.age = member["age"]
        user.position = member["position"]
        user.speciality = member["speciality"]
        user.address = member["address"]
        user.email = member["email"]
        session.add(user)
    session.commit()


if __name__ == '__main__':
    main()
