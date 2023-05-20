from fastapi import FastAPI
from main import App
import datetime
from mangum import Mangum


app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {'message': 'hello'}


@app.get("/problems/{equipo}")
async def get_top_problems(equipo):
    problems_with_solutions = get_neo4j_data(int(equipo))
    problems_with_solutions.sort(key=lambda x: datetime.datetime.strptime(x['solucion']['inicio_intervencion'][:-4],
                                                                          "%Y-%m-%d %H:%M:%S").timestamp(),
                                 reverse=True)
    problems = []
    descs = []
    for problem in list(map(lambda x: x['problema'], problems_with_solutions)):
        if problem['descripcion'] not in descs:
            descs.append(problem['descripcion'])
            problems.append(problem)

    for p in problems:
        p['soluciones'] = get_soluciones_problema(problems_with_solutions, p['descripcion'])
    return problems


def get_neo4j_data(equipo):
    uri = "neo4j+s://76838788.databases.neo4j.io"
    user = "neo4j"
    password = "urfpim_kxVWH5LgUxt0M1NcEVRhgyPTd9W5ZXjoRQMQ"
    db = App(uri, user, password)
    nodes = db.get_equipo(equipo)
    print(nodes)
    db.close()
    return nodes

def get_soluciones_problema(problems_with_solutions, desc):
    soluciones = []
    for p in problems_with_solutions:
        if desc == p['problema']['descripcion']:
            soluciones.append(p['solucion'])
    return soluciones
