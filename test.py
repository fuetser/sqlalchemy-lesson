import pytest
import requests


users_url = "http://localhost:5000/api/users"
jobs_url = "http://localhost:5000/api/jobs"


def test_all_jobs():
    resp = requests.get(jobs_url)
    if resp.ok:
        assert len(resp.json().get("jobs", [])) > 0, "Wrong amount of jobs"


def test_one_job():
    resp = requests.get(f"{jobs_url}/1")
    if resp.ok:
        json = resp.json()
        assert len(json.get("jobs", [])) > 0 and json["jobs"][0].get("job", "") != "", "Wrong answer"


def test_wrong_id():
    resp = requests.get(f"{jobs_url}/1000")
    if resp.ok:
        assert resp.json().get("error") is not None, "Wrong error message"


def test_string_request():
    resp = requests.get(f"{jobs_url}/string")
    assert resp.status_code == 404, "Wrong status code"


# правильные данные для запроса
correct_json = {
    'job': 'test',
    'team_leader': 1,
    'work_size': 20,
    'collaborators': '1, 2, 10, 23',
    'is_finished': 0,
    'id': 10
}


def test_correct_post_request():
    resp = requests.post(jobs_url, json=correct_json)
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_new_job_apperance():
    resp = requests.get(jobs_url)
    if resp.ok:
        if len((jobs := resp.json().get("jobs"))): 
            assert jobs[-1].get("id", -1) == correct_json["id"], "New job hasn't been added"
    # сравнение id добавленной нами записи с id последней записи, котрую возвращает api


def test_incorrect_request1():
    # запрос без данных
    resp = requests.post(jobs_url)
    if resp.ok:
        assert resp.json().get("error") == "Empty request", "Wrong responce"


def test_incorrect_request2():
    # запрос не со всеми ключами
    correct_json.pop("id")
    resp = requests.post(jobs_url, json=correct_json)
    if resp.ok:
        assert resp.json().get("error") == "Bad request", "Wrong responce"


def test_incorrect_request3():
    # запрос с существующим id
    correct_json["id"] = 1
    resp = requests.post(jobs_url, json=correct_json)
    if resp.ok:
        assert resp.json().get("error") == "Id already exists", "Wrong responce"


id_to_delete = 13


def test_correct__delete_request():
    resp = requests.delete(jobs_url, json={"id": id_to_delete})
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_job_deletion():
    resp = requests.get(jobs_url)
    if resp.ok:
        assert resp.json()["jobs"][-1]["id"] != id_to_delete, "Job hasn't been deleted"


def test_request_without_json():
    resp = requests.delete(jobs_url)
    if resp.ok:
        assert resp.json().get("error") == "Empty request", "Wrong responce"


def test_request_without_id_key():
    resp = requests.delete(
        jobs_url, json={"key1": "val1", "key2": "val2", "key3": "val3"})
    if resp.ok:
        assert resp.json().get("error") == "Bad request", "Wrong responce"


def test_request_with_invalid_id():
    resp = requests.delete(jobs_url, json={"id": 9999})
    if resp.ok:
        assert resp.json().get("error") == "No job found", "Wrong responce"


def test_changing_one_param():
    json = {
        'id': 7,
        "job": "Some new title"
    }
    resp = requests.put(jobs_url, json=json)
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_changing_several_params():
    json = {
        'id': 7,
        "team_leader": 3,
        "collaborators": "67, 68, 69",
        "work_size": 50
    }
    resp = requests.put(jobs_url, json=json)
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_changes_apperance():
    resp = requests.get(f"{jobs_url}/7")
    if resp.ok:
        assert resp.json().get("jobs")[0]["team_leader"] == 3, "Jobs hasn't been changed"


def test_empty_request():
    resp = requests.put(jobs_url)
    if resp.ok:
        assert resp.json().get("error") == "Empty request", "Wrong responce"


def test_request_without_required_params():
    resp = requests.put(jobs_url, json={"k1": "v1", "k2": "v2", "k3": "v3"})
    if resp.ok:
        assert resp.json().get("error") == "Bad request", "Wrong responce"


def test_request_wtih_invalid_id():
    resp = requests.put(jobs_url, json={"id": 999, "job": "New awesome title"})
    if resp.ok:
        assert resp.json().get("error") == "No job found", "Wrong responce"


def test_adding_user():
    json = {
        "id": 5,
        "name": "test",
        "surname": "user",
        "age": 20,
        "position": "engineer",
        "speciality": "pilot",
        "address": "module_2",
        "email": "test@mars.org",
        "password": "password"
    }
    resp = requests.post(users_url, json=json)
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_editing_user():
    json = {
        "id": 5,
        "name": "new",
        "surname": "name",
    }
    resp = requests.put(users_url, json=json)
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


def test_deleting_user():
    resp = requests.delete(users_url, json={"id": 5})
    if resp.ok:
        assert resp.json().get("success") is not None, "Wrong responce"


if __name__ == '__main__':
    pytest.main([__file__])
