from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models.profesor_clasesModel import Profesor_clases_model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from config.db import Session
from models.profesor_clasesModel import Profesor_clases_model
from models.clasesModel import Clases_model
from models.nivelesModel import Niveles_model


class Profesor_clases_services:
    def __init__(self) -> None:
        self.db = Session()
        #db para que cada vez que se ejecute ese servicio se envíe una sesión a la base de datos
        #ya puedo acceder a la base de datos desde otros métodos

    # CONSULTAR TODAS LAS RELACIONES 'PROFESOR - CLASE - NIVEL' POR ID_CLASE_PROFESOR
    def consultar_profesor_clases(self):
        result = self.db.query(Profesor_clases_model).all()
        # Obtengo todos los datos Profesor_clases_model y los guardo en la variable result.
        if not result:
        # Si no se encuentra la relación de profesor clase y nivel, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación 'profesor - clase - nivel 'no encontrada") 
        return  result


    # CONSULTAR UNA RELACIÓN 'PROFESOR - CLASE - NIVEL' POR ID_CLASE_PROFESOR
    def consultar_profesor_clase_nivel_por_id(self, id):
        result = self.db.query(Profesor_clases_model).filter(Profesor_clases_model.id_clase_profesor == id).first()
        # Obtengo los datos del profesor que quiero consultar filtrando por nombre.
        # Obtengo los del primero que encuentre y los guardo en la variable result.
        if not result:
            # Si no se encuentra el alumno, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación 'profesor - clase - nivel 'no encontrada") 
        return  result


    # CONSULTAR UNA RELACIÓN 'PROFESOR - CLASE - NIVEL' POR ID_CLASE_PROFESOR
    def consultar_profesor_clase_nivel_por_nombre_clase(self, nombre):
        query = f"""SELECT profesores_clases.id_clase_profesor, clases.nombre_clase, niveles.nombre_nivel, profesores.nombre_profesor
                    FROM profesores_clases
                    JOIN clases
                    ON clases.id_clase = profesores_clases.clase_id
                    JOIN niveles
                    ON niveles.id_nivel = profesores_clases.nivel_id
                    JOIN profesores
                    ON profesores.id_profesor = profesores_clases.profesor_id
                    WHERE clases.nombre_clase = '{nombre}'"""

        result = self.db.execute(text(query)).fetchall()
        result_dicts = [{'id':row[0],  'nombre de clase':row[1],  'nivel':row[2], 'profesor':row[3]}  for row in result]

        # Obtengo los datos del profesor que quiero consultar filtrando por nombre.
        # Obtengo los del primero que encuentre y los guardo en la variable result.
        if not result:
                 # Si no se encuentra el profesor, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error.
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación 'profesor - clase - nivel 'no encontrada")
        return result_dicts


        # CONSULTAR UNA RELACIÓN 'PROFESOR - CLASE - NIVEL' POR ID_CLASE_PROFESOR
    def consultar_profesor_clase_nivel_por_nombre_profesor(self, nombre):

        query = f"""SELECT profesores.nombre_profesor, clases.nombre_clase, niveles.nombre_nivel
                FROM profesores_clases
                JOIN clases
                ON clases.id_clase = profesores_clases.clase_id
                JOIN niveles
                ON niveles.id_nivel = profesores_clases.nivel_id
                JOIN profesores
                ON profesores.id_profesor = profesores_clases.profesor_id
                WHERE profesores.nombre_profesor = '{nombre}'"""

        result = self.db.execute(text(query)).fetchall()
        result_dicts = [{'profesor':row[0],  'nombre de clase':row[1],  'nivel':row[2]}  for row in result]

            # Obtengo los datos del profesor que quiero consultar filtrando por nombre.
            # Obtengo los del primero que encuentre y los guardo en la variable result.
        if not result:
                 # Si no se encuentra el profesor, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación 'profesor - clase -nivel ' no encontrada")
        return result_dicts

    # AGREGAR UNA RELACIÓN 'PROFESOR - CLASE - NIVEL'
    def agregar_profesor_clase_nivel(self, data):

        nuevo_profesor_clase = Profesor_clases_model(**data.dict())
        #Le envío el nuevo profesor
        self.db.add(nuevo_profesor_clase)
        #Hago el commit para que se actualice
        self.db.commit()
        return f"Se agregó la nueva relación 'profesor -clase - nivel' {nuevo_profesor_clase} correctamente"



    # EDITAR UNA RELACIÓN 'PROFESOR - CLASE - NIVEL'
    def editar_profesor_clase_nivel(self, id: int, data):

        profesor_clase = self.db.query(Profesor_clases_model).filter(Profesor_clases_model.id_clase_profesor == id).first()
        if not profesor_clase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación 'profesor - clase -nivel'  no encontrada")

        profesor_clase.clase_id = data.clase_id
        profesor_clase.profesor_id = data.profesor_id
        profesor_clase.nivel_id = data.nivel_id
        self.db.commit()

        return {"message": "Relación 'profesor - clase -nivel' actualizada correctamente"}


    # BORRAR UNA RELACIÓN RELACIÓN 'PROFESOR - CLASE - NIVEL'
    def borrar_profesor_clase_nivel(self, id: int):

        profesor_clase = self.db.query(Profesor_clases_model).filter(Profesor_clases_model.id_clase_profesor == id).first()
        if not profesor_clase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ninguna relación 'profesor - clase -nivel' con ese id")
        self.db.query(Profesor_clases_model).filter(Profesor_clases_model.id_clase_profesor == id).delete()
        self.db.commit()
        return

