from ...database import DatabaseConnection

class Canal:
    """Canal model class"""
    

    def __init__(self, **kwargs):
        self.canal_id = kwargs.get('canal_id')
        self.nombre_canal = kwargs.get('nombre_canal')
        self.descripcion = kwargs.get('descripcion')
        self.servidor_id = kwargs.get('servidor_id')

    @classmethod
    def create(cls, canal):
        query = """
            INSERT INTO chatnet.canales (nombre_canal, descripcion, servidor_id)
            VALUES (%(nombre_canal)s, %(descripcion)s, %(servidor_id)s);
        """
        params = canal.__dict__
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def get_all(cls, servidor_id):
        
        query = "SELECT * FROM chatnet.canales WHERE servidor_id = %(servidor_id)s;"
        params = {'servidor_id': servidor_id}
        results = DatabaseConnection.fetch_all(query, params=params)

        canales = []
        for result in results:
            canales.append(cls(
                canal_id=result[0],
                nombre_canal=result[1],
                descripcion = result[2],
                servidor_id=result[3]
            ))
        return canales        

    @classmethod
    def get(cls, canal_id):
        query = "SELECT * FROM chatnet.canales WHERE canal_id = %(canal_id)s;"
        params = {'canal_id': canal_id}
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
                canal_id=result[0],
                nombre_canal=result[1],
                descripcion = result[2],
                servidor_id=result[3]
            )
        return None

    def serialize(self):
        """Serialize object representation"""
        return {
            "canal_id": self.canal_id,
            "nombre_canal": self.nombre_canal,
            "descripcion": self.descripcion,
            "servidor_id": self.servidor_id
        }
    @classmethod
    def update(cls, canal):
        allowed_columns = {'nombre_canal', 'descripcion'}
        query_parts = []
        params = []
        for key, value in canal.__dict__.items():
            if key in allowed_columns and value is not None:
                query_parts.append(f"{key} = %s")
                params.append(value)
        params.append(canal.canal_id)

        query = "UPDATE chatnet.canales SET " + ", ".join(query_parts) + " WHERE canal_id = %s"
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, canal):
        query = "DELETE FROM chatnet.canales WHERE canal_id = %s"
        params = canal.canal_id,
        DatabaseConnection.execute_query(query, params=params)    
    @classmethod
    def is_registered(cls, canal):
        query = '''SELECT canal_id FROM chatnet.canales\
                    WHERE nombre_canal=%(nombre_canal)s OR canal_id=%(canal_id)s'''
        params = canal.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)
        if result is not None:
            return True
        return False