import csv

import orjson
from fastapi import Body, FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn import Config, Server

import department_classification as dpc
from schema import Task

app = FastAPI(default_response_class=ORJSONResponse)


@app.post("/tasks", status_code=201)
def assign_task(body: Task = Body(...)):
    resp = {"department_id": dpc.predict_department(body.task)}
    return orjson.dumps(resp)


@app.get("/tasks", status_code=200)
def get_tasks():
    data = []
    with open('data/tasks.csv', encoding='utf-8') as f:
        tasks = csv.DictReader(f)
        [data.append(rows) for rows in tasks]
        return orjson.dumps(data)


@app.get("/departments", status_code=200)
def get_departments():
    data = []
    with open('data/departments.csv', encoding='utf-8') as f:
        tasks = csv.DictReader(f)
        [data.append(rows) for rows in tasks]
        return orjson.dumps(data)


@app.get("/employees", status_code=200)
def get_employees():
    data = []
    with open('data/employees.csv', encoding='utf-8') as f:
        tasks = csv.DictReader(f)
        [data.append(rows) for rows in tasks]
        return orjson.dumps(data)


if __name__ == "__main__":
    server = Server(Config(app, ))
    server.run()
