from flask import Blueprint
from ..controllers.canal_controller import CanalController

canal_bp = Blueprint('canal_bp', __name__)

canal_bp.route('/crear', methods=['POST'])(CanalController.create_canal)
canal_bp.route('/canal/<int:canal_id>', methods=['GET'])(CanalController.get_canal)
# canal_bp.route('/canales', methods=['GET'])(CanalController.get_canales)
canal_bp.route('/canales/<int:servidor_id>', methods=['GET'])(CanalController.get_canales)
canal_bp.route('/update/<int:canal_id>', methods=['PUT'])(CanalController.update_canal)
canal_bp.route('/delete/<int:canal_id>', methods=['DELETE'])(CanalController.delete_canal)
