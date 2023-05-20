from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_localizacion(self, localizacion1_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_localizacion, localizacion1_name)
            for row in result:
                print("Created localizacion between: {l1}".format(l1=row['l1']))

    @staticmethod
    def _create_and_return_localizacion(tx, localizacion1_name):
        query = (
            "CREATE (l1:Localizacion { name: $localizacion1_name }) "
            "RETURN l1"
        )
        result = tx.run(query, localizacion1_name=localizacion1_name)
        try:
            return [{"l1": row["l1"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def get_equipo(self, equipo):
        with self.driver.session() as session:
            result = session.execute_write(self._get_equipo, equipo)
            print(result)
            return result

    @staticmethod
    def _get_equipo(tx, equipo):
        result = tx.run(f"""
        MATCH (:Equipo {{id: $equipo}})-->(problema:Problema)
            CALL {{
                WITH problema
                MATCH (problema)-[r]->(solucion:Solucion)
                RETURN solucion, r
            }}
        RETURN solucion, problema
        """, equipo=equipo)
        nodes = []
        for line in result:
            nodes.append({
                'solucion': dict(dict(line)['solucion']),
                'problema': dict(dict(line)['problema'])
            })
        return nodes


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://76838788.databases.neo4j.io"
    user = "neo4j"
    password = "urfpim_kxVWH5LgUxt0M1NcEVRhgyPTd9W5ZXjoRQMQ"
    app = App(uri, user, password)
    app.get_equipo(571)
    app.close()