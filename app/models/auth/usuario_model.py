from ...database import DatabaseConnection
# from models.auth.rol_model import UsuarioRol
# from models.auth.status_model import UsuarioStatus
class Usuario:
    """Usuario model class"""
    

    def __init__(self, **kwargs):
        self.usuario_id = kwargs.get('usuario_id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.nombre_completo = kwargs.get('nombre_completo')
        self.email = kwargs.get('email')
        self.imagen_de_perfil = kwargs.get('imagen_de_perfil')
        self.rol_id = kwargs.get('rol_id')
        self.status_id = kwargs.get('status_id')
        
  
    @classmethod
    def is_registered(cls, usuario):
        query = "SELECT usuario_id FROM chatnet.usuarios WHERE email = %(email)s AND password = %(password)s;"
        params = usuario.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)
        if result is not None:
            return True
        return False
    
    def serialize(self):
        """Serialize object representation """
        
        return {
            "usuario_id": self.usuario_id,
            "username": self.username,
            "password": self.password,
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "imagen_de_perfil": self.imagen_de_perfil,
            # "rol": UsuarioRol.get(UsuarioRol(rol_id =self.rol_id)).serialize(),
            # "status": UsuarioStatus.get(UsuarioStatus(status_id= self.status_id)).serialize(),
            "rol": self.rol_id,
            "status": self.status_id
        }
    @classmethod
    def get(cls, usuario):
        query = """SELECT * FROM chatnet.usuarios 
        WHERE email = %(email)s OR usuario_id=%(usuario_id)s"""
        params = usuario.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
                usuario_id = result[0],
                username = result[1],
                password = result[2],
                nombre_completo = result[3],
                email = result[4],
                imagen_de_perfil = result[5],
                role_id = result[6],
                status_id = result[7]
            )
        return None
    @classmethod
    def getImg(cls, usuario_id):
        query = """SELECT imagen_de_perfil FROM chatnet.usuarios 
        WHERE usuario_id=%(usuario_id)s"""
        params = {'usuario_id': usuario_id}
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
               imagen_de_perfil = result[0]
              
            )
        return None
    @classmethod
    def update(cls, usuario):
        
        allowed_columns = {'username', 'password', 'nombre_completo', 'email', 'imagen_de_perfil'}
        query_parts = []
        params = []
        for key, value in usuario.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f"{key} = %s")
                params.append(value)
        params.append(usuario.usuario_id)

        query = "UPDATE chatnet.usuarios SET " + ", ".join(query_parts) + " WHERE usuario_id = %s"
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, usuario):
        query = "DELETE FROM chatnet.usuarios WHERE usuario_id = %s"
        params = usuario.usuario_id,
        DatabaseConnection.execute_query(query, params=params)
    @classmethod
    def create(cls, usuario):
        query = '''INSERT INTO chatnet.usuarios (username, password, nombre_completo, email,
                    imagen_de_perfil, rol_id, status_id) VALUES (%(username)s, %(password)s,
                     %(nombre_completo)s, %(email)s, %(imagen_de_perfil)s, %(rol_id)s, %(status_id)s)'''
        params = usuario.__dict__
        DatabaseConnection.execute_query(query, params=params)
    
    @classmethod
    def update(cls, usuario):
        allowed_columns = {'username',  'password', 'nombre_completo','email',
                           'imagen_de_perfil'}
        query_parts = []
        params = []
        for key, value in usuario.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f'{key} = %s')
                params.append(value)
        params.append(usuario.usuario_id)
        query = "UPDATE chatnet.usuarios SET " + ", ".join(query_parts) + " WHERE usuario_id = %s"
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM chatnet.usuarios'''
        result = DatabaseConnection.fetch_all(query)
        usuarios = []
        if result is not None:
            for res in result:
                usuarios.append(cls(
                usuario_id = res[0],
                username = res[1],
                password = res[2],
                nombre_completo = res[3],
                email = res[4],
                imagen_de_perfil = res[5],
                role_id = res[6],
                status_id = res[7]
                    ))
        return usuarios    