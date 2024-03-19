from ..models.auth.usuario_model import Usuario
from flask import request, session, send_file, send_from_directory
from ..models.exceptions import SourceNotFound, InvalidDataError
import base64
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/app/static/uploads'


class UserController:
    @classmethod
    def login(cls):
        data = request.json
        usuario = Usuario(
            email = data.get('email'),
            password = data.get('password')
        )
        if Usuario.is_registered(usuario):
            usuario = Usuario.get(usuario) # obtener todos los datos del usuario en un nuevo obj usuario
            session['email'] = data.get('email')
            user = Usuario.get(Usuario(email = session.get('email')))
            session['usuario_id'] = user.usuario_id
            return {"usuario_id": usuario.usuario_id, "email": usuario.email}, 200
        return {"message": "Usuario o contraseña incorrectos"}, 401
    
    @classmethod
    def logout(cls):
        session.pop('email', None)
        return {"message": "Sesión cerrada"}, 200

    @classmethod
    def show_profile(cls):
        email = session.get('email')
        usuario = Usuario.get(Usuario(email = email))
        if usuario is None:
            return {"message": "Usuario no encontrado"}, 404
        else:
            return usuario.serialize(), 200

    @classmethod
    def img(cls):
        email = session.get('email')
        usuario = Usuario.get(Usuario(email = email))
        # print(usuario.imagen_de_perfil)
        # return send_from_directory("./stataic/uploads/", usuario.imagen_de_perfil)
        if usuario is None:
            return {"message": "Usuario no encontrado"}, 404
        else:
            #"static/uploads/" + usuario.imagen_de_perfil)
            # "./static/uploads/avatar1.png"
            ruta = os.path.join("./static/uploads/", usuario.imagen_de_perfil)
            
            #return send_file(ruta, mimetype='image/png')
            if ruta:
                #print("si existe", usuario.imagen_de_perfil)
                return send_file(ruta, mimetype='image/png')
            else:
                #print("no existe", os.path.join("./static/uploads/", usuario.imagen_de_perfil))
                return send_file("./static/default/profile.png", mimetype='image/png')

    @classmethod
    def img_user(cls, usuario_id):
       
        img = Usuario.getImg(usuario_id)

        # print('usuario de img user', usuario)

        if img is None:
            return {"message": "Usuario no encontrado"}, 404
        else:
            ruta = os.path.join(os.path.abspath("./app/static/uploads/"), img.imagen_de_perfil)
            # print('ruta: img serv', ruta)

            if os.path.exists(ruta):
                return send_file(ruta, mimetype='image/png'), 200
            else:
                default_image_path = os.path.abspath("./app/static/default/profile.png")
                return send_file(default_image_path, mimetype='image/png'), 200
              
    @classmethod
    def create(cls):
        data = request.json
        if data.get('username') is not None:
            if isinstance(data.get('username'), str):
                data['username'] = data.get('username').strip()
            else:
                raise InvalidDataError('Debe ingresar una cadena de caracteres para el nombre de usuario')
        else:
            raise InvalidDataError('El nombre de usuario es obligatorio')
        if data.get('password') is not None:
            if len(data.get('password'))>=5:
                data['password'] = data.get('password').strip()
            else:
                raise InvalidDataError('La contraseña debe tener al menos 5 caracteres')
        else:
            raise InvalidDataError('La contraseña es obligatoria')
        if data.get('nombre_completo') is not None:
            if isinstance(data.get('nombre_completo'), str):
                data['nombre_completo'] = data.get('nombre_completo').strip()
            else:
                raise InvalidDataError('Ingrese una cadena valida para el nombre')
        else:
            raise InvalidDataError('El nombre es obligatorio')
        if data.get('email') is not None:
            if isinstance(data.get('email'), str):
                data['email'] = data.get('email').strip()
            else:
                raise InvalidDataError('Ingrese una direccion de mail valida')
        else:
            raise InvalidDataError('El email es obligatorio')
        data['imagen_de_perfil'] = 'app\static\default\profile.png'
        data['rol_id'] = 1
        data['status_id'] = 1
        
        
        usuario = Usuario(**data)
        if not Usuario.is_registered(usuario):
            Usuario.create(usuario)
            return {'message': 'Usuario creado exitosamente'}, 201
        else:
            return {'message': 'Ya existe un usuario con esos datos'}, 400
      
   

    @classmethod
    def update(cls, usuario_id):
        data = request.form.to_dict()
        if data.get('username') is not None:
            if isinstance(data.get('username'), str):
                data['username'] = data.get('username').strip()
            else:
                raise InvalidDataError('Debe ingresar una cadena de caracteres para el nombre de usuario')
        if data.get('password') is not None:
            if len(data.get('password')) >= 5:
                data['password'] = data.get('password').strip()
            else:
                raise InvalidDataError('La contraseña debe tener al menos 5 caracteres')
        if data.get('nombre_completo') is not None:
            if isinstance(data.get('nombre_completo'), str):
                data['nombre_completo'] = data.get('nombre_completo').strip()
            else:
                raise InvalidDataError('Ingrese una cadena válida para el nombre completo')
        if data.get('email') is not None:
            if isinstance(data.get('email'), str):
                data['email'] = data.get('email').strip()
            else:
                raise InvalidDataError('Ingrese una dirección de correo válida')

        if 'imagen_de_perfil' in request.files:
            imagen_de_perfil = request.files['imagen_de_perfil']
            if imagen_de_perfil and allowed_file(imagen_de_perfil.filename):
                filename = secure_filename(imagen_de_perfil.filename)
                imagen_de_perfil.save(os.path.join("app/static/uploads", filename))
                               
                data['imagen_de_perfil'] = filename

        data['usuario_id'] = usuario_id
        usuario = Usuario(**data)
        if Usuario.is_registered(usuario):
            Usuario.update(usuario)
            if data.get('email') is not None:
                session['email'] = data.get('email')
            return {'message': 'Usuario actualizado exitosamente'}, 201
        else:
            raise SourceNotFound('No existe un usuario con esos datos')
        
    @classmethod
    def get_all(cls):
        usuario_objects = Usuario.get_all()
        usuarios = []
        for usuario in usuario_objects:
            usuarios.append(usuario.serialize())
        return usuarios, 200
    @classmethod
    def get(cls, usuario_id):
        usuario = Usuario.get(Usuario(usuario_id = usuario_id))
        # print('us',usuario)
        if usuario is not None:
            return usuario.serialize(), 200
        else:
            raise SourceNotFound('Usuario no encontrado')
        
    @classmethod
    def delete(cls, usuario_id):
        usuario = Usuario(usuario_id=usuario_id)
        if Usuario.is_registered(usuario):
            Usuario.delete(usuario)
            return {'message': 'Usuario eliminado correctamente'}, 204
        raise SourceNotFound('Usuario no encontrado')  

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# def allowed_file(filename):
#     return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
