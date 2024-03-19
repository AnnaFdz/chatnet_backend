from ...database import DatabaseConnection

class Mensaje:
    """Mensaje model class"""
    

    def __init__(self, **kwargs):
        self.mensaje_id = kwargs.get('mensaje_id')
        self.contenido_mensaje = kwargs.get('contenido_mensaje')
        self.fecha_hora = kwargs.get('fecha_hora')
        self.usuario_id = kwargs.get('usuario_id')
        self.canal_id = kwargs.get('canal_id')

    @classmethod
    def create(cls, mensaje):
        query = """
            INSERT INTO chatnet.mensajes (contenido_mensaje, fecha_hora, usuario_id, canal_id)
            VALUES (%(contenido_mensaje)s, %(fecha_hora)s, %(usuario_id)s, %(canal_id)s);
        """
        params = mensaje.__dict__
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def get_all(cls, canal_id):
        query = "SELECT * FROM chatnet.mensajes WHERE canal_id = %(canal_id)s;"
        params = {'canal_id': canal_id}
        results = DatabaseConnection.fetch_all(query, params=params)

        mensajes = []
        for result in results:
            mensajes.append(cls(
                mensaje_id=result[0],
                contenido_mensaje=result[1],
                fecha_hora=result[2],
                usuario_id=result[3],
                canal_id=result[4]
            ))
        return mensajes

    @classmethod
    def get(cls, mensaje_id):
        query = "SELECT * FROM chatnet.mensajes WHERE mensaje_id = %(mensaje_id)s;"
        params = {'mensaje_id': mensaje_id}
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
                mensaje_id=result[0],
                contenido_mensaje=result[1],
                fecha_hora=result[2],
                usuario_id=result[3],
                canal_id=result[4]
            )
        return None

    def serialize(self):
        """Serialize object representation"""
        return {
            "mensaje_id": self.mensaje_id,
            "contenido_mensaje": self.contenido_mensaje,
            "fecha_hora": self.fecha_hora,
            "usuario_id": self.usuario_id,
            "canal_id": self.canal_id
        }
    @classmethod
    def update(cls, mensaje):
        allowed_columns = {'contenido_mensaje', 'fecha_hora', 'usuario_id', 'canal_id'}
        query_parts = []
        params = []
        for key, value in mensaje.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f"{key} = %s")
                params.append(value)
        params.append(mensaje.mensaje_id)

        query = "UPDATE chatnet.mensajes SET " + ", ".join(query_parts) + " WHERE mensaje_id = %s"
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, mensaje):
        query = "DELETE FROM chatnet.mensajes WHERE mensaje_id = %s"
        params = mensaje.mensaje_id,
        DatabaseConnection.execute_query(query, params=params)        