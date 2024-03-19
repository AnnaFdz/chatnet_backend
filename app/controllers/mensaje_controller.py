from ..models.mensajes.mensaje_model import Mensaje
from flask import request, session
from ..models.exceptions import SourceNotFound, InvalidDataError
from datetime import datetime

class MensajeController:

    @classmethod
    def get_mensaje(cls, mensaje_id):
        mensaje = Mensaje.get(Mensaje(mensaje_id=mensaje_id))
        if mensaje is not None:
            return mensaje.serialize(), 200
        else:
            raise SourceNotFound('Mensaje no encontrado')

    @classmethod
    def get_mensajes(cls, canal_id):
        mensaje_objects = Mensaje.get_all(canal_id)
        mensajes = []
        for mensaje in mensaje_objects:
            mensajes.append(mensaje.serialize())
        return mensajes, 200

    @classmethod
    def create_mensaje(cls):
        data = request.json
        print(data)
        data['usuario_id'] = session.get('usuario_id')  
        data['fecha_hora'] = datetime.now()
        mensaje= Mensaje(**data)
        
        Mensaje.create(mensaje)
        return {'message': 'Mensaje creado con éxito'}, 201

    @classmethod
    def update_mensaje(cls, mensaje_id):
        data = request.json
        data['mensaje_id'] = mensaje_id 
        mensaje = Mensaje(**data)
        mensaje_existente = Mensaje.get(mensaje_id)  
        if mensaje_existente:
            mensaje.contenido_mensaje = data.get('contenido_mensaje', mensaje_existente.contenido_mensaje)
            mensaje.fecha_hora = data.get('fecha_hora', mensaje_existente.fecha_hora)
            mensaje.usuario_id = data.get('usuario_id', mensaje_existente.usuario_id)  
            mensaje.canal_id = data.get('canal_id', mensaje_existente.canal_id)

            Mensaje.update(mensaje)
            return {"message": "Mensaje actualizado exitosamente"}, 200
        else:
            raise SourceNotFound('Mensaje no encontrado')

    @classmethod
    def delete_mensaje(cls, mensaje_id):
        print(mensaje_id)
        mensaje = Mensaje.get(mensaje_id)  
        if mensaje:
            Mensaje.delete(mensaje)
            return {"message": "Mensaje eliminado exitosamente"}, 200
        raise SourceNotFound('Mensaje no encontrado')

