from ..models.auth.status_model import UsuarioStatus
from flask import request
from ..models.exceptions import InvalidDataError  
class StatusController:

    @classmethod
    def get(cls, status_id):
        status = UsuarioStatus.get(UsuarioStatus(status_id=status_id))
        if status is not None:
            return status.serialize(), 200
        return {'message': 'Status no encontrado'}, 404
    
    @classmethod
    def get_all(cls):
        status_objects = UsuarioStatus.get_all()
        statuss = []
        for status in status_objects:
            statuss.append(status.serialize())
        return statuss, 200
    
    @classmethod
    def create(cls):
        data = request.json
        status = UsuarioStatus(**data)
        try:
            if not UsuarioStatus.is_registered(status):
                UsuarioStatus.create(status)
                return {'message': 'Status creado con éxito'}, 201
            else:
                raise InvalidDataError('Ya existe un status con ese nombre')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
    
    @classmethod
    def update(cls, status_id):
        data = request.json
        data['status_id'] = status_id
        status = UsuarioStatus(**data)
        try:
            if UsuarioStatus.is_registered(status):
                UsuarioStatus.update(status)
                return {'message': 'Status modificado con éxito'}, 201
            else:
                raise InvalidDataError('Status no encontrado')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
    
    @classmethod
    def delete(cls, status_id):
        status = UsuarioStatus(status_id=status_id)
        try:
            if UsuarioStatus.is_registered(status):
                UsuarioStatus.delete(status)
                return {'message': 'Status eliminado correctamente'}, 204
            else:
                raise InvalidDataError('Status no encontrado')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
