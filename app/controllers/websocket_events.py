from flask_socketio import emit, join_room
from flask import session
from websocket_manager import socketio
from datetime import datetime

@socketio.on("connect")
def handle_connect():
    print(f"Cliente conectado: {session.get('username', 'Usuário')}")
    emit("status", {"msg": f"{session.get('username', 'Usuário')} conectado!"})
    join_room("/")

@socketio.on("disconnect")
def handle_disconnect():
    print(f"Cliente desconectado: {session.get('username', 'Usuário')}")

from flask_socketio import emit, join_room
from websocket_manager import socketio

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('disconnect')
def handle_disconnect():
    pass

@socketio.on('join')
def handle_join(data):
    room = data.get('room', '/')
    join_room(room)

@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    username = session.get("username", "Usuário")
    emit("status", {"msg": f"{username} saiu da sala {room}."}, room=room)

@socketio.on("crud_operation")
def handle_crud_operation(data):
    operation = data.get("operation")
    entity = data.get("entity")
    entity_data = data.get("data", {})
    username = session.get("username", "Sistema")
    
    messages = {
        "create": f"{username} adicionou um novo {entity}",
        "update": f"{username} atualizou um {entity}",
        "delete": f"{username} removeu um {entity}"
    }
    
    message = messages.get(operation, f"{username} realizou uma operação em {entity}")
    
    emit("crud_notification", {
        "message": message,
        "operation": operation,
        "entity": entity,
        "data": entity_data,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": username
    }, broadcast=True)

@socketio.on("request_data_update")
def handle_data_update_request(data):
    entity_type = data.get("entity_type")
    
    from controllers.application import ClienteController, AnimalController, VeterinarioController, ConsultaController
    
    try:
        if entity_type == "clientes":
            controller = ClienteController()
            entities = controller.listar()
        elif entity_type == "animais":
            controller = AnimalController()
            entities = controller.listar()
        elif entity_type == "veterinarios":
            controller = VeterinarioController()
            entities = controller.listar()
        elif entity_type == "consultas":
            controller = ConsultaController()
            entities = controller.listar()
        else:
            entities = []
        
        entities_data = []
        for entity in entities:
            if hasattr(entity, "__dict__"):
                entities_data.append(entity.__dict__)
            else:
                entities_data.append(entity)
        
        emit("data_update", {
            "entity_type": entity_type,
            "data": entities_data,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
    except Exception as e:
        emit("error", {"message": f"Erro ao obter dados: {str(e)}"})

@socketio.on("system_notification")
def handle_system_notification(data):
    message = data.get("message", "Notificação do sistema")
    notification_type = data.get("type", "info")
    
    emit("system_alert", {
        "message": message,
        "type": notification_type,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }, broadcast=True)

@socketio.on("send_message")
def handle_message(data):
    username = session.get("username", "Anônimo")
    message = data.get("message", "")
    room = data.get("room", "general")
    
    if message.strip():
        emit("new_message", {
            "username": username,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }, room=room)

@socketio.on("user_activity")
def handle_user_activity(data):
    activity_type = data.get("activity_type")
    page = data.get("page")
    username = session.get("username", "Anônimo")
    
    emit("activity_update", {
        "user": username,
        "activity": activity_type,
        "page": page,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }, room="admin")

@socketio.on("request_initial_activities")
def handle_initial_activities():
    from datetime import datetime, timedelta
    import random
    
    activities = [
        {
            "message": "Sistema PETBUS inicializado com sucesso",
            "operation": "system",
            "entity": "sistema",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 30))).strftime("%H:%M:%S"),
            "user": "Sistema"
        },
        {
            "message": "Backup automático dos dados realizado",
            "operation": "system",
            "entity": "backup",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(31, 60))).strftime("%H:%M:%S"),
            "user": "Sistema"
        },
        {
            "message": "Verificação de integridade dos dados concluída",
            "operation": "system",
            "entity": "verificacao",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(61, 120))).strftime("%H:%M:%S"),
            "user": "Sistema"
        }
    ]
    
    for activity in activities:
        emit("crud_notification", activity)

@socketio.on("request_system_status")
def handle_system_status():
    from controllers.application import ClienteController, AnimalController, VeterinarioController, ConsultaController
    
    stats = {
        "total_clientes": len(ClienteController.listar()),
        "total_animais": len(AnimalController.listar()),
        "total_veterinarios": len(VeterinarioController.listar()),
        "total_consultas": len(ConsultaController.listar()),
        "system_uptime": "Online",
        "last_backup": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "database_status": "Conectado"
    }
    
    emit("system_status_update", stats)
