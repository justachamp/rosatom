import csv

import orjson
from fastapi import FastAPI, Form, Request
from fastapi.responses import ORJSONResponse
from uvicorn import Config, Server

import department_classification as dpc
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates/")
app = FastAPI(default_response_class=ORJSONResponse)


@app.post("/", status_code=200)
async def assign_task(request: Request):
    deps = {}
    with open('data/departments.csv', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        [deps.update({rows['department_id']: rows}) for rows in csv_reader]
        del csv_reader
        f.close()
    form = await request.form()
    return templates.TemplateResponse('index.html', context={'request': request, 'result': deps[str(dpc.predict_department(form.get('task')))]['department_name']})


@app.get("/", status_code=200)
async def get_tasks(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request, 'result': ''})


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
