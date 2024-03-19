from ..models.auth.rol_model import UsuarioRol
from flask import request
from ..models.exceptions import InvalidDataError  # Asegúrate de que esta importación sea correcta.

class RolController:

    @classmethod
    def get(cls, rol_id):
        rol = UsuarioRol.get(UsuarioRol(rol_id=rol_id))
        if rol is not None:
            return rol.serialize(), 200
        return {'message': 'Rol no encontrado'}, 404
    
    @classmethod
    def get_all(cls):
        rol_objects = UsuarioRol.get_all()
        roles = []
        for rol in rol_objects:
            roles.append(rol.serialize())
        return roles, 200
    
    @classmethod
    def create(cls):
        data = request.json
        rol = UsuarioRol(**data)
        try:
            if not UsuarioRol.is_registered(rol):
                UsuarioRol.create(rol)
                return {'message': 'Rol creado con éxito'}, 201
            else:
                raise InvalidDataError('Ya existe un rol con ese nombre')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
    
    @classmethod
    def update(cls, rol_id):
        data = request.json
        data['rol_id'] = rol_id
        rol = UsuarioRol(**data)
        try:
            if UsuarioRol.is_registered(rol):
                UsuarioRol.update(rol)
                return {'message': 'Rol modificado con éxito'}, 201
            else:
                raise InvalidDataError('Rol no encontrado')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
    
    @classmethod
    def delete(cls, rol_id):
        rol = UsuarioRol(rol_id=rol_id)
        try:
            if UsuarioRol.is_registered(rol):
                UsuarioRol.delete(rol)
                return {'message': 'Rol eliminado correctamente'}, 204
            else:
                raise InvalidDataError('Rol no encontrado')
        except InvalidDataError as e:
            return {'message': str(e)}, 400
