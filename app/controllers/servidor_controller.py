from ..models.servidores.servidor_model import Servidor
from ..models.auth.usuario_model import Usuario
from ..controllers.usuario_controller import UserController
from flask import request, session, send_file
from ..models.exceptions import SourceNotFound, InvalidDataError
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/app/static/uploads'

class ServidorController:

    @classmethod
    def get_servidores(cls):
        servidor_objects = Servidor.get_all()
        servidores = []
        for servidor in servidor_objects:
            servidores.append(servidor.serialize())
        return servidores, 200
    @classmethod
    def buscar_servidores(query):
        # query = request.args.get('query')

        if query:
            servers = Servidor.buscar_servidores(query)
            return servers
        else:
            return ({"message": "Por favor ingresar busqueda"}), 400
    @classmethod
    def get_all_by_name(cls, nombre_servidor):
        server_objects = Servidor.get_all_by_name(nombre_servidor)
        num_users=Servidor.buscar_servidores(nombre_servidor)
        allUsers=UserController.get_all()
        # print('num_users get', num_users)
        servidores = []
        for servidor in server_objects:
            
            servidores.append(servidor.serialize())
            
        return ({'servidores':servidores, 'num_users': num_users, 'allUsers': allUsers}), 200



    
    @classmethod
    def create_servidor(cls):
        data = request.json
        if data.get('nombre_servidor') is not None:
            if isinstance(data.get('nombre_servidor'), str):
                data['nombre_servidor'] = data.get('nombre_servidor').strip()
            else:
                raise InvalidDataError('Ingrese un nombre válido para el servidor')
        else:
            raise InvalidDataError('El nombre del servidor es obligatorio')
        
        if data.get('descripcion') is not None:
            data['descripcion'] = data.get('descripcion').strip()
        session['nombre_servidor'] = data.get('nombre_servidor')
        data['creador_id'] = session.get('usuario_id')
        
        # print("Creador ID from session:", data['creador_id'])
        # print("nombre servidor from session:", session['nombre_servidor'] )
        data['imagen_servidor'] = 'server.png'

        servidor = Servidor(**data)

        if not Servidor.is_registered(servidor):
            Servidor.create(servidor)

            serv = Servidor.get(Servidor(nombre_servidor=session.get('nombre_servidor')))
            # print("nombre servidor from session - serv:", serv )

            uid = session.get('usuario_id')
            # print("Creador ID from session - uid:", uid)
            Servidor.create_usuarios(uid, serv.servidor_id)

            return {'message': 'Servidor creado con éxito'}, 201
        else:
            raise InvalidDataError('Ya existe un servidor con ese nombre')


    @classmethod
    def add_userio_servidor(cls):
        data = request.json
        serv = Servidor.get(Servidor(nombre_servidor=data.get('nombre_servidor')))
        uid = session.get('usuario_id')
        if not Servidor.exist_usuarios(uid, serv.servidor_id):
            Servidor.create_usuarios(uid, serv.servidor_id)
            return {'message': 'Relación creada con éxito'}, 201
        else:
            raise InvalidDataError('El usuario ya pertenece al servidor')
        
    @classmethod
    def get_usuarios(cls):
        usuario = session.get('usuario_id')
        usuarios_servidores_objects = Servidor.get_usuarios(usuario)
        usuarios_servidores = []
        for item in usuarios_servidores_objects:
            usuarios_servidores.append(item.serialize())
        return usuarios_servidores, 200
    @classmethod
    def img(cls):
        nombre_servidor = session.get('nombre_servidor')
        # print('nombre_servidor img', nombre_servidor)
        if nombre_servidor is None:
            return {"message": "Nombre de servidor no proporcionado"}, 400
        # print('servidor_id', servidor_id)
        #print('nombre_servidor', nombre_servidor)
        servidor = Servidor.get(Servidor(nombre_servidor= nombre_servidor))
        
        #servidor = Servidor.get(Servidor(server))
        # servidor = Servidor.get(Servidor(nombre_servidor=session.get('nombre_servidor')))
        # print('servidor de img',servidor)
        
        
        # print(usuario.imagen_de_perfil)
        # print(servidor.imagen_servidor)
        # return send_from_directory("./stataic/uploads/", usuario.imagen_de_perfil)
    
        
        if servidor is None:
            return {"message": "Servidor no encontrado"}, 404
        else:
            #"static/uploads/" + servidor.imagen_servidor)
            # "./static/uploads/avatar1.png"
            # ruta = os.path.join("./static/uploads/", servidor.imagen_servidor)
            ruta = os.path.join(os.path.abspath("./app/static/uploads/"), servidor.imagen_servidor)
            # print('ruta: img', ruta)
            #return send_file(ruta, mimetype='image/png')
            # if ruta:
            if os.path.exists(ruta):
                #print("si existe", server.imagen_servidor)
                return send_file(ruta, mimetype='image/png')
            else:
                #print("no existe", os.path.join("./static/uploads/", usuario.imagen_de_perfil)) server.png
                # return send_file("./static/default/server.png", mimetype='image/png')
                return send_file(os.path.abspath("./app/static/default/server.png"), mimetype='image/png')
    # @classmethod
    # def img_serv(cls, nombre_servidor):
    #     # nombre_servidor = session.get('nombre_servidor')
    #     print('nombre_servidor img_serv', nombre_servidor)
    #     if nombre_servidor is None:
    #         return {"message": "Nombre de servidor no proporcionado"}, 400
    #     servidor = Servidor.get(Servidor(nombre_servidor= nombre_servidor))
        
    #     print('servidor de img serv',servidor)
        
    #     if servidor is None:
    #         return {"message": "Servidor no encontrado"}, 404
    #     else:
            
    #         ruta = os.path.join(os.path.abspath("./app/static/uploads/"), servidor.imagen_servidor)
    #         print('ruta: img serv', ruta)
            
    #         if os.path.exists(ruta):
                
    #             return send_file(ruta, mimetype='image/png')
    #         else:
                
    #             return send_file(os.path.abspath("./app/static/default/server.png"), mimetype='image/png')     

    # @classmethod
    # def img_serv(cls, nombre_servidor):
    #     # print('nombre_servidor img_serv', nombre_servidor)

    #     # if nombre_servidor is None:
    #     #     return {"message": "Nombre de servidor no proporcionado"}, 400

    #     # Servidor.get returns a Servidor instance
    #     #servidor = Servidor.get(Servidor(nombre_servidor=nombre_servidor))

    #      # Create an instance of Servidor with the provided nombre_servidor
    #     servidor_instance = Servidor(nombre_servidor=nombre_servidor)

    #     # Call the get method with the Servidor instance
    #     servidor = Servidor.get(servidor_instance)

    #     # print('servidor de img serv', servidor)

    #     if servidor is None:
    #         return {"message": "Servidor no encontrado"}, 404
    #     else:
    #         ruta = os.path.join(os.path.abspath("./app/static/uploads/"), servidor.imagen_servidor)
    #         # print('ruta: img serv', ruta)

    #         if os.path.exists(ruta):
    #             return send_file(ruta, mimetype='image/png'), 200
    #         else:
    #             default_image_path = os.path.abspath("./app/static/default/server.png")
    #             return send_file(default_image_path, mimetype='image/png'), 200
    @classmethod
    def img_serv(cls, nombre_servidor):
        # print('nombre_servidor img_serv', nombre_servidor)

        # if nombre_servidor is None:
        #     return {"message": "Nombre de servidor no proporcionado"}, 400

        # Servidor.get returns a Servidor instance
        #servidor = Servidor.get(Servidor(nombre_servidor=nombre_servidor))

         # Create an instance of Servidor with the provided nombre_servidor
        

        # Call the get method with the Servidor instance
        img = Servidor.getImg(nombre_servidor)
        
        # print('servidor de img serv', servidor)

        if img is None:
            return {"message": "Servidor no encontrado"}, 404
        else:
            ruta = os.path.join(os.path.abspath("./app/static/uploads/"), img.imagen_servidor)
            # print('ruta: img serv', ruta)

            if os.path.exists(ruta):
                return send_file(ruta, mimetype='image/png'), 200
            else:
                default_image_path = os.path.abspath("./app/static/default/server.png")
                return send_file(default_image_path, mimetype='image/png'), 200                               
    @classmethod
    def update_servidor(cls, servidor_id):
        # data = request.json
        data = request.form.to_dict()
        data['servidor_id'] = servidor_id
        if data.get('nombre_servidor') is not None:
            if isinstance(data.get('nombre_servidor'), str):
                    data['nombre_servidor'] = data.get('nombre_servidor').strip()
            else:
                    raise InvalidDataError('Debe ingresar una cadena de caracteres para el nombre del servidor')
        
        if data.get('descripcion') is not None:
            if isinstance(data.get('descripcion'), str):
                data['descripcion'] = data.get('descripcion').strip()
            else:
                raise InvalidDataError('Ingrese una cadena válida para la descripcion del servidor')
        

        if 'imagen_servidor' in request.files:
            imagen_servidor = request.files['imagen_servidor']
            if imagen_servidor and allowed_file(imagen_servidor.filename):
                filename = secure_filename(imagen_servidor.filename)
                imagen_servidor.save(os.path.join("./app/static/uploads", filename))
                               
                data['imagen_servidor'] = filename
        servidor = Servidor(**data)
        if Servidor.is_registered(servidor):
            Servidor.update(servidor)
            return {'message': 'Servidor modificado con éxito'}, 201
        else:
            raise SourceNotFound('Servidor no encontrado')
        
    @classmethod
    def delete_servidor(cls, servidor_id):
        servidor = Servidor(servidor_id=servidor_id)
        if Servidor.is_registered(servidor):
            Servidor.delete(servidor)
            return {'message': 'Servidor eliminado correctamente'}, 204
        else:
            raise SourceNotFound('Servidor no encontrado')
        
    @classmethod
    def get_servidor(cls, nombre_servidor):
        # servidor_id = session.get('servidor_id')
        # print('nombre_servidor metodo get_servidor', nombre_servidor)
        # Create an instance of Servidor with the provided nombre_servidor
        servidor_instance = Servidor(nombre_servidor=nombre_servidor)

        # Call the get method with the Servidor instance
        servidor = Servidor.get(servidor_instance)
        allUsers=UserController.get_all()
        if servidor is not None:
            # print('servidor get servidor', servidor)
            session['servidor_id'] = servidor.servidor_id
            session['nombre_servidor'] = servidor.nombre_servidor
            # print('servidor_id session metodo get_servidor', session['servidor_id'], session['nombre_servidor'])
            servidor = servidor.serialize()
            return {"servidor":servidor, "allUsers":allUsers}, 200
            # ,{"servidor_id": servidor.servidor_id, "nombre_servidor": servidor.nombre_servidor}
        else:
            raise SourceNotFound('Servidor no encontrado')
    # @classmethod
    # def get_servidor(cls, nombre_servidor):
    #     print('nombre_servidor metodo get_servidor', nombre_servidor)
        
    #     # Create an instance of Servidor with the provided nombre_servidor
    #     servidor_instance = Servidor(nombre_servidor=nombre_servidor)

    #     # Call the get method with the Servidor instance
    #     servidor = Servidor.get(servidor_instance)
        
    #     if servidor is not None:
    #         session['servidor_id'] = servidor.servidor_id
    #         session['nombre_servidor'] = servidor.nombre_servidor
    #         print('servidor_id session metodo get_servidor', session['servidor_id'], session['nombre_servidor'])
            
    #         # Combine the information into a single dictionary
    #         combined_info = {
    #             "servidor_id": servidor.servidor_id,
    #             "nombre_servidor": servidor.nombre_servidor,
    #             "serialized_info": servidor.serialize(),
    #         }

    #         return combined_info, 200
    #     else:
    #         raise SourceNotFound('Servidor no encontrado')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# def allowed_file(filename):
#     return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS