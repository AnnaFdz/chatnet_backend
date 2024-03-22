from ...database import DatabaseConnection

class Servidor:
    """Servidor model class"""
    

    def __init__(self, **kwargs):
        self.servidor_id = kwargs.get('servidor_id')
        self.nombre_servidor = kwargs.get('nombre_servidor')
        self.descripcion = kwargs.get('descripcion')
        self.imagen_servidor = kwargs.get('imagen_servidor')
        self.creador_id = kwargs.get('creador_id')
        

    @classmethod
    def create(cls, servidor):
        query = """
            INSERT INTO chatnet.servidores (nombre_servidor, descripcion, imagen_servidor, creador_id)
            VALUES (%(nombre_servidor)s, %(descripcion)s, %(imagen_servidor)s, %(creador_id)s);
        """
        # params = servidor.__dict__
        params = {
            'nombre_servidor': servidor.nombre_servidor,
            'descripcion': servidor.descripcion,
            'imagen_servidor': servidor.imagen_servidor,
            'creador_id': servidor.creador_id
        }
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def create_usuarios(cls, usuario_id, servidor_id):
        query = '''
            INSERT INTO chatnet.usuarios_servidores (usuario_id, servidor_id)
            VALUES (%(usuario_id)s, %(servidor_id)s)
        '''
        params = {
            'usuario_id': usuario_id,
            'servidor_id': servidor_id
        }
        DatabaseConnection.execute_query(query, params=params)

    # @classmethod
    # def get(cls, servidor_id):
    #     query = "SELECT * FROM chatnet.servidores WHERE servidor_id = %(servidor_id)s;"
    #     params = {'servidor_id': servidor_id}
    #     result = DatabaseConnection.fetch_one(query, params=params)

    #     if result is not None:
    #         return cls(
    #             servidor_id=result[0],
    #             nombre_servidor=result[1],
    #             descripcion=result[2],
    #             imagen_servidor=result[3],
    #             creador_id=result[4]
                
    #         )
    #     return None
    @classmethod
    def get(cls, servidor):
        query = '''SELECT * FROM chatnet.servidores\
                    WHERE servidor_id=%(servidor_id)s OR nombre_servidor=%(nombre_servidor)s'''
        # query = '''SELECT * FROM chatnet.servidores\
        #     WHERE (servidor_id=%(servidor_id)s AND nombre_servidor IS NULL) OR nombre_servidor=%(nombre_servidor)s'''

        params = servidor.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)
        
        if result is not None:
            return cls(
                servidor_id=result[0],
                nombre_servidor=result[1],
                descripcion=result[2],
                imagen_servidor=result[3],
                creador_id=result[4]
                
            )
        
        return None
    @classmethod
    def getImg(cls, nombre_servidor):
        query = '''SELECT imagen_servidor FROM chatnet.servidores\
                    WHERE nombre_servidor=%(nombre_servidor)s'''
        # query = '''SELECT * FROM chatnet.servidores\
        #     WHERE (servidor_id=%(servidor_id)s AND nombre_servidor IS NULL) OR nombre_servidor=%(nombre_servidor)s'''

        params = {'nombre_servidor': nombre_servidor}
        result = DatabaseConnection.fetch_one(query, params=params)
        
        if result is not None:
            return cls(
                imagen_servidor=result[0]
                
                
            )
        
        return None
    @classmethod
    def get_all(cls):
        
        query = """SELECT * FROM chatnet.servidores"""
        results = DatabaseConnection.fetch_all(query)

        servidores = []
        if results is not None:
            for result in results:
                # print("mostrar todo ",result)
                servidores.append(cls(
                    servidor_id=result[0],
                    nombre_servidor=result[1],
                    descripcion=result[2],
                    imagen_servidor=result[3],
                    creador_id=result[4]
                                      ))
        return servidores
    
    def serialize(self):
        """Serialize object representation"""
        return {
            "servidor_id": self.servidor_id,
            "nombre_servidor": self.nombre_servidor,
            "descripcion": self.descripcion,
            "imagen_servidor": self.imagen_servidor,
            "creador_id": self.creador_id,
            
        }
    @classmethod
    def update(cls, servidor):
        allowed_columns = {'nombre_servidor', 'descripcion', 'imagen_servidor'}
        query_parts = []
        params = []
        for key, value in servidor.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f"{key} = %s")
                params.append(value)
        params.append(servidor.servidor_id)

        query = "UPDATE chatnet.servidores SET " + ", ".join(query_parts) + " WHERE servidor_id = %s"
        DatabaseConnection.execute_query(query, params=params)
    
    @classmethod
    def delete(cls, servidor):
        query = "DELETE FROM chatnet.servidores WHERE servidor_id = %s"
        params = servidor.servidor_id,
        DatabaseConnection.execute_query(query, params=params)
    @classmethod
    def delete_servidor_usuario(cls, servidor_id, usuario_id):
        query = '''DELETE FROM chatnet.usuarios_servidores 
                    WHERE usuario_id=%s AND servidor_id=%s'''
        
        params = usuario_id, servidor_id
        DatabaseConnection.execute_query(query, params=params)
    
    # @classmethod
    # def create_usuarios(cls, usuario_id, servidor_id):
    #     query = '''INSERT INTO chatnet.usuarios_servidores (usuario_id, servidor_id)
    #                 VALUES (%s, %s)'''
    #     params = (usuario_id, servidor_id)
    #     DatabaseConnection.execute_query(query, params=params)

    # @classmethod
    # def get_usuarios(cls, usuario):
    #     query = '''SELECT s.* FROM chatnet.usuarios_servidores us
    #                 INNER JOIN chatnet.servidores s
    #                 ON us.servidor_id = s.servidor_id
    #                 WHERE us.usuario_id=%s'''
    #     params = usuario,
    #     result = DatabaseConnection.fetch_all(query, params=params)
    #     usuarios = []
    #     if result is not None:
    #         for item in result:
    #             usuarios.append(cls(
    #                     servidor_id = item[0],
    #                     nombre_servidor = item[1],
    #                     descripcion = item[2],
    #                     imagen_servidor = item[3],
    #                     creador_id = item[4]
    #                 ))
    #     return usuarios

    @classmethod
    def get_usuarios(cls, usuario):
        query = '''
            SELECT s.servidor_id, s.nombre_servidor, s.descripcion, s.imagen_servidor, s.creador_id
            FROM chatnet.usuarios_servidores us
            INNER JOIN chatnet.servidores s ON us.servidor_id = s.servidor_id
            WHERE us.usuario_id = %s
        '''
        params = (usuario,)
        result = DatabaseConnection.fetch_all(query, params=params)
        
        usuarios = []

        if result is not None:
            for item in result:
                usuarios.append(cls(
                    servidor_id=item[0],
                    nombre_servidor=item[1],
                    descripcion=item[2],
                    imagen_servidor=item[3],
                    creador_id=item[4]
                ))

        return usuarios

    @classmethod
    def exist_usuarios(cls, usuario, servidor):
        query = '''SELECT * from chatnet.usuarios_servidores 
                    WHERE usuario_id=%s AND servidor_id=%s'''
        params = usuario, servidor
        result = DatabaseConnection.fetch_one(query, params=params)
        if result is not None:
            return True
        return False
    # @classmethod
    # def is_registered(cls, servidor):
    #     query = '''SELECT servidor_id FROM chatnet.servidores\
    #                 WHERE nombre_servidor=%(nombre_servidor)s OR servidor_id=%(servidor_id)s'''
    #     params = servidor.__dict__
    #     result = DatabaseConnection.fetch_one(query, params=params)
    #     if result is not None:
    #         return True
    #     return False    
    @classmethod
    def is_registered(cls, servidor):
        query = "SELECT servidor_id FROM chatnet.servidores WHERE nombre_servidor = %(nombre_servidor)s OR servidor_id = %(servidor_id)s"
        params = {
            'nombre_servidor': servidor.nombre_servidor,
            'servidor_id': servidor.servidor_id
        }
        result = DatabaseConnection.fetch_one(query, params=params)
        return result is not None
    @classmethod
    def buscar_servidores(cls, nombre_servidor):
        # Perform a database query to find servers that match the search query
        # Include the number of registered users for each server in the result
        # Return a list of dictionaries containing server information

        # Example:
        query = '''
            SELECT us.usuario_id 
            FROM chatnet.servidores s
            LEFT JOIN chatnet.usuarios_servidores us ON s.servidor_id = us.servidor_id
            WHERE s.nombre_servidor LIKE %s
            
        '''

        params = ["%" + nombre_servidor + "%"]

        query_result = DatabaseConnection.fetch_all(query, params=params)

        users = []
        for row in query_result:
            users.append({
                
                "usuario_id": row[0]
            })

        # return servers
        # num_users = [users['num_users'] for users in users]
        return users
            
    @classmethod
    def get_all_by_name(cls, servidor):
        query = '''SELECT * FROM chatnet.servidores
                    WHERE LOWER(nombre_servidor)=%s'''
        
        params = servidor,
        results = DatabaseConnection.fetch_all(query, params=params)
        servidores = []
        if results is not None:
            for result in results:
                servidores.append(cls(
                        servidor_id = result[0],
                        nombre_servidor = result[1],
                        descripcion = result[2],
                        imagen_servidor = result[3],
                        creador_id = result[4]
                    ))
        return servidores
