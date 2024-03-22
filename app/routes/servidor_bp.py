from flask import Blueprint
from ..controllers.servidor_controller import ServidorController

servidor_bp = Blueprint('servidor_bp', __name__)

servidor_bp.route('/crear', methods=['POST'])(ServidorController.create_servidor)
servidor_bp.route('/<nombre_servidor>', methods=['GET'])(ServidorController.get_servidor)
servidor_bp.route('/servidores', methods=['GET'])(ServidorController.get_servidores)
servidor_bp.route('/update/<int:servidor_id>', methods=['POST'])(ServidorController.update_servidor)
servidor_bp.route('/<int:servidor_id>', methods=['DELETE'])(ServidorController.delete_servidor)
servidor_bp.route('/usuario_servidor', methods=['POST'])(ServidorController.add_userio_servidor)
servidor_bp.route('/usuario_servidor', methods=['GET'])(ServidorController.get_usuarios)
servidor_bp.route('/img', methods=['GET'])(ServidorController.img) 
servidor_bp.route('/imgserv/<string:nombre_servidor>', methods=['GET'])(ServidorController.img_serv) 
# servidor_bp.route('/buscar_uxs', methods=['GET'])(ServidorController.buscar_servidores)
servidor_bp.route('/buscar/<string:nombre_servidor>', methods=['GET'])(ServidorController.get_all_by_name)
servidor_bp.route('/remover_usuario/<int:servidor_id>/<int:usuario_id>', methods=['DELETE'])(ServidorController.delete_servidor_usuario)