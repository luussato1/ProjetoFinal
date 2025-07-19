from flask_socketio import SocketIO

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app)




@socketio.on('send_message')
def handle_send_message(data):
    from flask import session
    from datetime import datetime
    data["username"] = session.get("username", "Anônimo")
    data["timestamp"] = datetime.now().strftime("%H:%M:%S")
    socketio.emit("new_message", data, room=data["room"])

@socketio.on('join')
def on_join(data):
    from flask_socketio import join_room
    from flask import session
    username = session.get('username', 'Anônimo')
    room = data['room']
    join_room(room)
    socketio.emit('new_message', {'username': 'Sistema', 'message': f'{username} entrou na sala.', 'room': room}, room=room)

@socketio.on('disconnect')
def test_disconnect():
    from flask import session
    from flask_socketio import rooms
    username = session.get('username', 'Anônimo')
    for room in rooms():
        if room != session.sid:
            socketio.emit('new_message', {'username': 'Sistema', 'message': f'{username} saiu da sala.', 'room': room}, room=room)

@socketio.on('system_notification')
def handle_system_notification(data):
    socketio.emit('crud_notification', data, broadcast=True)

@socketio.on('request_data_update')
def handle_request_data_update(data):
    from controllers.application import ClienteController, AnimalController, VeterinarioController, ConsultaController
    entity_type = data.get('entity_type')
    if entity_type == 'clientes':
        count = len(ClienteController.listar())
    elif entity_type == 'animais':
        count = len(AnimalController.listar())
    elif entity_type == 'veterinarios':
        count = len(VeterinarioController.listar())
    elif entity_type == 'consultas':
        count = len(ConsultaController.listar())
    else:
        count = 0
    socketio.emit('data_update', {'entity_type': entity_type, 'data': {'length': count}})

