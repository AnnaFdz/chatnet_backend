from ...database import DatabaseConnection

class UsuarioRol:
    """UsuarioRolModel model class"""
    


    def __init__(self, **kwargs):
        self.rol_id = kwargs.get('rol_id')
        self.nombre_rol = kwargs.get('nombre_rol')

    def serialize(self):
        """Serialize object representation """
        
        return {
            "rol": self.rol_id,
            "nombre_rol": self.nombre_rol
        }
    @classmethod
    def get_rol(cls, rol):
        query = """SELECT rol_id, nombre_rol FROM chatnet.usuario_rol WHERE rol_id = %(rol_id)s"""
        params = rol.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return UsuarioRol(
                rol_id = result[0],
                nombre_rol = result[1]
            )
        return None
    @classmethod
    def get_roles(cls):
        query = '''SELECT * FROM chatnet.usuario_rol'''
        results = DatabaseConnection.fetch_all(query)
        roles = []
        if results is not None:
            for result in results:
                roles.append(cls(
                    rol_id=result[0],
                    nombre_rol=result[1]
                ))
        return roles
    
    @classmethod
    def create_rol(cls, rol):
        query = '''INSERT INTO chatnet.usuario_rol (nombre_rol)
                    VALUES (%(nombre_rol)s)'''
        params = rol.__dict__
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update_rol(cls, rol):
        allowed_columns = {'nombre_rol'}
        query_parts = []
        params = []
        for key, value in rol.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f'{key} = %s')
                params.append(value)
        params.append(rol.rol_id)
        query = "UPDATE chatnet.usuario_rol SET " + ", ".join(query_parts) + " WHERE rol_id = %s"
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete_rol(cls, rol):
        query = '''DELETE FROM chatnet.usuario_rol WHERE rol_id=%s'''
        params = rol.rol_id,
        DatabaseConnection.execute_query(query, params=params)    
    @classmethod
    def is_registered(cls, rol):
        query = '''SELECT rol_id FROM chatnet.usuario_rol\
                    WHERE nombre_rol=%(nombre_rol)s OR rol_id=%(rol_id)s'''
        params = rol.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)
        if result is not None:
            return True
        return False        