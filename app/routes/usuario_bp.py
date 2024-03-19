from flask import Blueprint
from ..controllers.usuario_controller import UserController
usuario_bp = Blueprint('usuario_bp', __name__)
usuario_bp.route('/login', methods=['POST'])(UserController.login)
usuario_bp.route('/profile', methods=['GET'])(UserController.show_profile)
usuario_bp.route('/logout', methods=['GET'])(UserController.logout)
usuario_bp.route('/create', methods=['POST'])(UserController.create)
usuario_bp.route('/', methods=['GET'])(UserController.get_all)
usuario_bp.route('/update/<int:usuario_id>', methods=['POST'])(UserController.update)
usuario_bp.route('/delete/<int:usuario_id>', methods=['DELETE'])(UserController.delete)
usuario_bp.route('/img', methods=['GET'])(UserController.img)
usuario_bp.route('/img_user/<int:usuario_id>', methods=['GET'])(UserController.img_user)
usuario_bp.route('/<int:usuario_id>', methods=['GET'])(UserController.get)