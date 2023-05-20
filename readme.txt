En este archivo se explica cada uno de los archivos aqui presentes y como conectarse a la DB que se encuentra actualmente corriendo en AuraDB

* KB.CSV y nombres.csv hacen referencia a los datos que fueron entregados directamente por Darnel

* main.csv es la primera versión de la conexión de la API a Neo4j con la que se comuicara el UI que utilizaran los stakeholders

* data_loader.ipynb es un notebook en el cual se encuentra como conectarse con Neo4j y el preprocesamiento de los datos con el que se insertan los datos.

Para conectarse a a la db se recomienda usar Python usando el sigente codigo:

from neo4j import GraphDatabase
uri = "neo4j+s://76838788.databases.neo4j.io"
user = "neo4j"
password = "urfpim_kxVWH5LgUxt0M1NcEVRhgyPTd9W5ZXjoRQMQ"
driver = GraphDatabase.driver(uri, auth=(user, password))

Y para hacer queries usar el siguiente codigo.

with driver.session() as session:
    info = session.run(query)

Donde query es un string con la query a ejecutar