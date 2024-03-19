from ..models.servidores.servidor_model import Servidor
from ..models.canales.canal_model import Canal
from flask import request
from ..models.exceptions import SourceNotFound, InvalidDataError

class CanalController:

    @classmethod
    def get_canal(cls, canal_id):
        canal = Canal.get(canal_id)
        if canal is not None:
            return canal.serialize(), 200
        else:
            raise SourceNotFound('Canal no encontrado')

    # @classmethod
    # def get_canales(cls, servidor_id):
    #     canales = Canal.get_all(servidor_id)
    #     return [canal.serialize() for canal in canales], 200

    @classmethod
    def get_canales(cls, servidor_id):
        
        canal_objects = Canal.get_all(servidor_id)
        canales = []
        for canal in canal_objects:
            canales.append(canal.serialize())
        # if not canales:
        #     return {'message': 'No channels found for the given server.'}, 404
        return canales, 200

    @classmethod
    def create_canal(cls):
        data = request.json
        nombre_canal = data.get('nombre_canal')
        descripcion = data.get('descripcion')
        servidor_id = data.get('servidor_id')

        if not nombre_canal or not isinstance(nombre_canal, str):
            raise InvalidDataError('Nombre de canal inválido')

        if not descripcion or not isinstance(descripcion, str):
            raise InvalidDataError('Descripción inválida')

        if not servidor_id or not isinstance(servidor_id, int):
            raise InvalidDataError('ID de servidor inválido')

        canal = Canal(
            nombre_canal=nombre_canal.strip(),
            descripcion=descripcion.strip(),
            servidor_id=servidor_id
        )

        if not Canal.is_registered(canal):
            Canal.create(canal)
            return {'message': 'Canal creado exitosamente'}, 201
        else:
            raise InvalidDataError('Ya existe un canal con ese nombre en el servidor')

    @classmethod
    def update_canal(cls, canal_id):
        data = request.json
        nombre_canal = data.get('nombre_canal')
        descripcion = data.get('descripcion')

        if nombre_canal and not isinstance(nombre_canal, str):
            raise InvalidDataError('Nombre de canal inválido')

        if descripcion and not isinstance(descripcion, str):
            raise InvalidDataError('Descripción inválida')

        canal = Canal(
            canal_id=canal_id,
            nombre_canal=nombre_canal.strip() if nombre_canal else None,
            descripcion=descripcion.strip() if descripcion else None
        )

        if Canal.exists(canal):
            Canal.update(canal)
            return {'message': 'Canal actualizado exitosamente'}, 200
        else:
            raise SourceNotFound('Canal no encontrado')

    @classmethod
    def delete_canal(cls, canal_id):
        canal = Canal(canal_id=canal_id)

        if Canal.exists(canal):
            Canal.delete(canal)
            return {'message': 'Canal eliminado exitosamente'}, 200
        else:
            raise SourceNotFound('Canal no encontrado')
