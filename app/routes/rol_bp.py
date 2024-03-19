from flask import Blueprint
from ..controllers.rol_controller import RolController

rol_bp = Blueprint('rol_bp', __name__)

rol_bp.route('rol/<int:rol_id>', methods=['GET'])(RolController.get)
rol_bp.route('roles/', methods=['GET'])(RolController.get_all)
rol_bp.route('/rol/create', methods=['POST'])(RolController.create)
rol_bp.route('rol/update/<int:rol_id>', methods=['PUT'])(RolController.update)
rol_bp.route('rol/delete/<int:rol_id>', methods=['DELETE'])(RolController.delete)