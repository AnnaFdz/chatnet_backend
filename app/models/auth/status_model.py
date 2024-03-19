from ...database import DatabaseConnection

class UsuarioStatus:
    """UsuarioStatusModel model class"""
    

    def __init__(self, **kwargs):
        self.status_id = kwargs.get('status_id')
        self.nombre_status = kwargs.get('nombre_status')

    def serialize(self):
        """Serialize object representation """
        
        return {
            "status": self.status_id,
            "nombre_status": self.nombre_status
        }
    @classmethod
    def get(cls, status):
        query = """SELECT status_id, nombre_status FROM chatnet.usuario.status WHERE status_id = %(status_id)s"""
        params = status.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return UsuarioStatus(
                status_id = result[0],
                nombre_status = result[1]
            )
        return None