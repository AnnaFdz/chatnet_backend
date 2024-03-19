from flask import Blueprint
from ..controllers.mensaje_controller import MensajeController

mensaje_bp = Blueprint('mensaje_bp', __name__)


mensaje_bp.route('/crear', methods=['POST'])(MensajeController.create_mensaje)
mensaje_bp.route('/<int:mensaje_id>', methods=['GET'])(MensajeController.get_mensaje)

mensaje_bp.route('/mensajes/<int:canal_id>', methods=['GET'])(MensajeController.get_mensajes)
mensaje_bp.route('/update/<int:mensaje_id>', methods=['PUT'])(MensajeController.update_mensaje)
mensaje_bp.route('/delete/<int:mensaje_id>', methods=['DELETE'])(MensajeController.delete_mensaje)
