from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controllers.application import ClienteController, AnimalController, VeterinarioController, ConsultaController
from controllers.auth_controller import AuthController
from models.cliente import Cliente
from models.animal import Animal
from models.veterinario import Veterinario
from models.consulta import Consulta
from models.usuario import Usuario
import uuid
from datetime import datetime 
from functools import wraps
from websocket_manager import socketio

routes = Blueprint("routes", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado():
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado() or not AuthController.is_admin():
            flash("Acesso negado. Apenas administradores podem acessar esta página.", "error")
            return redirect(url_for("routes.home"))
        return f(*args, **kwargs)
    return decorated_function

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        usuario = AuthController.autenticar(username, password)
        if usuario:
            AuthController.fazer_login(usuario)
            flash(f"Bem-vindo, {usuario.nome_completo}!", "success")
            return redirect(url_for("routes.home"))
        else:
            return render_template("login.html", error="Usuário ou senha incorretos.")
    
    return render_template("login.html")

@routes.route("/logout")
def logout():
    AuthController.fazer_logout()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("routes.login"))

@routes.route("/admin")
@login_required
@admin_required
def admin_panel():
    stats = {
        "total_clientes": len(ClienteController.listar()),
        "total_animais": len(AnimalController.listar()),
        "total_veterinarios": len(VeterinarioController.listar()),
        "total_consultas": len(ConsultaController.listar())
    }
    
    usuario = AuthController.usuario_atual()
    return render_template("admin.html", stats=stats, usuario=usuario, now=datetime.now())

@routes.route("/")
def home():
    return render_template("home.html", now=datetime.now())

@routes.route("/clientes")
@login_required
def listar_clientes():
    clientes = ClienteController.listar()
    return render_template("clientes.html", clientes=clientes)

@routes.route("/clientes/novo", methods=["GET"])
@login_required
def novo_cliente():
    return render_template("form_cliente.html", cliente=None, action_url=url_for("routes.adicionar_cliente"))

@routes.route("/clientes/adicionar", methods=["POST"])
@login_required
def adicionar_cliente():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    endereco = request.form["endereco"]
    novo_cliente = Cliente(str(uuid.uuid4()), nome, email, telefone, endereco)
    ClienteController.adicionar(novo_cliente)
    
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} adicionou um novo cliente: {nome}",
        "operation": "create",
        "entity": "cliente",
        "data": {"nome": nome, "email": email},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room='/')
    return redirect(url_for("routes.listar_clientes"))

@routes.route("/clientes/remover/<cliente_id>")
@login_required
def remover_cliente(cliente_id):
    clientes = ClienteController.listar()
    cliente = next((c for c in clientes if c["id"] == cliente_id), None)
    cliente_nome = cliente["nome"] if cliente else "Cliente"
    
    ClienteController.remover(cliente_id)
    
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} removeu o cliente: {cliente_nome}",
        "operation": "delete",
        "entity": "cliente",
        "data": {"id": cliente_id, "nome": cliente_nome},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room='/')
    return redirect(url_for("routes.listar_clientes"))
@routes.route("/clientes/editar/<cliente_id>", methods=["GET", "POST"])
@login_required
def editar_cliente(cliente_id):
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        cliente_atualizado = Cliente(cliente_id, nome, email, telefone, endereco)
        ClienteController.atualizar(cliente_atualizado)
        
        socketio.emit("crud_notification", {
            "message": f"{{session.get(\"username\", \"Usuário\")}} atualizou o cliente: {nome}",
            "operation": "update",
            "entity": "cliente",
            "data": {"id": cliente_id, "nome": nome, "email": email},
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": session.get("username", "Sistema")
        }, room='/')
        return redirect(url_for("routes.listar_clientes"))
    else:
        clientes = ClienteController.listar()
        cliente = next((c for c in clientes if c["id"] == cliente_id), None)
        if cliente is None:
            flash("Cliente não encontrado!", "error")
            return redirect(url_for("routes.listar_clientes"))
        cliente_obj = Cliente(cliente["id"], cliente["nome"], cliente["email"], cliente["telefone"], cliente["endereco"])
        action_url = url_for("routes.editar_cliente", cliente_id=cliente_id)
        return render_template("form_cliente.html", cliente=cliente_obj, action_url=action_url)

@routes.route("/animais")
@login_required
def listar_animais():
    animais = AnimalController.listar()
    return render_template("animais.html", animais=animais)

@routes.route("/animais/novo", methods=["GET"])
@login_required
def novo_animal():
    return render_template("form_animal.html", animal=None, action_url=url_for("routes.adicionar_animal"))

@routes.route("/animais/adicionar", methods=["POST"])
@login_required
def adicionar_animal():
    nome = request.form["nome"]
    especie = request.form["especie"]
    id_cliente = request.form["id_cliente"]
    raca = request.form["raca"]
    idade = int(request.form["idade"])
    peso = float(request.form["peso"])
    novo_animal = Animal(str(uuid.uuid4()), nome, especie, id_cliente, raca, idade, peso)
    AnimalController.adicionar(novo_animal)
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} adicionou um novo animal: {nome}",
        "operation": "create",
        "entity": "animal",
        "data": {"nome": nome, "especie": especie},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room='/')
    return redirect(url_for("routes.listar_animais"))

@routes.route("/animais/remover/<animal_id>")
@login_required
def remover_animal(animal_id):
    animais = AnimalController.listar()
    animal = next((a for a in animais if a["id"] == animal_id), None)
    animal_nome = animal["nome"] if animal else "Animal"

    AnimalController.remover(animal_id)
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} removeu o animal: {animal_nome}",
        "operation": "delete",
        "entity": "animal",
        "data": {"id": animal_id, "nome": animal_nome},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room="/")
    return redirect(url_for("routes.listar_animais"))

@routes.route("/animais/editar/<animal_id>", methods=["GET", "POST"])
@login_required
def editar_animal(animal_id):
    if request.method == "POST":
        nome = request.form["nome"]
        especie = request.form["especie"]
        id_cliente = request.form["id_cliente"]
        raca = request.form["raca"]
        idade = int(request.form["idade"])
        peso = float(request.form["peso"])
        animal_atualizado = Animal(animal_id, nome, especie, id_cliente, raca, idade, peso)
        AnimalController.atualizar(animal_atualizado)
        socketio.emit("crud_notification", {
            "message": f"{{session.get(\"username\", \"Usuário\")}} atualizou o animal: {nome}",
            "operation": "update",
            "entity": "animal",
            "data": {"id": animal_id, "nome": nome, "especie": especie},
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": session.get("username", "Sistema")
        }, room="/")
        return redirect(url_for("routes.listar_animais"))
    else:
        animais = AnimalController.listar()
        animal = next((a for a in animais if a["id"] == animal_id), None)
        if animal is None:
            flash("Animal não encontrado!", "error")
            return redirect(url_for("routes.listar_animais"))
        action_url = url_for("routes.editar_animal", animal_id=animal_id)
        return render_template("form_animal.html", animal=animal, action_url=action_url)

@routes.route("/veterinarios")
@login_required
def listar_veterinarios():
    veterinarios = VeterinarioController.listar()
    return render_template("veterinarios.html", veterinarios=veterinarios)

@routes.route("/veterinarios/novo", methods=["GET"])
@login_required
def novo_veterinario():
    return render_template("form_veterinario.html", veterinario=None, action_url=url_for("routes.adicionar_veterinario"))

@routes.route("/veterinarios/adicionar", methods=["POST"])
@login_required
def adicionar_veterinario():
    nome = request.form["nome"]
    crmv = request.form["crmv"]
    especialidade = request.form["especialidade"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    novo_veterinario = Veterinario(str(uuid.uuid4()), nome, crmv, especialidade, telefone, email)
    VeterinarioController.adicionar(novo_veterinario)
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} adicionou um novo veterinário: {nome}",
        "operation": "create",
        "entity": "veterinario",
        "data": {"nome": nome, "crmv": crmv},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room="/")
    flash("Veterinário adicionado com sucesso!", "success")
    return redirect(url_for("routes.listar_veterinarios"))

@routes.route("/veterinarios/remover/<veterinario_id>")
@login_required
def remover_veterinario(veterinario_id):
    veterinarios = VeterinarioController.listar()
    veterinario = next((v for v in veterinarios if v["id"] == veterinario_id), None)
    veterinario_nome = veterinario["nome"] if veterinario else "Veterinário"

    VeterinarioController.remover(veterinario_id)
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} removeu o veterinário: {veterinario_nome}",
        "operation": "delete",
        "entity": "veterinario",
        "data": {"id": veterinario_id, "nome": veterinario_nome},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
    }, room="/")
    return redirect(url_for("routes.listar_veterinarios"))

@routes.route("/veterinarios/editar/<veterinario_id>", methods=["GET", "POST"])
@login_required
def editar_veterinario(veterinario_id):
    if request.method == "POST":
        nome = request.form["nome"]
        crmv = request.form["crmv"]
        especialidade = request.form["especialidade"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        veterinario_atualizado = Veterinario(veterinario_id, nome, crmv, especialidade, telefone, email)
        VeterinarioController.atualizar(veterinario_atualizado)
        socketio.emit("crud_notification", {
            "message": f"{{session.get(\"username\", \"Usuário\")}} atualizou o veterinário: {nome}",
            "operation": "update",
            "entity": "veterinario",
            "data": {"id": veterinario_id, "nome": nome, "crmv": crmv},
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": session.get("username", "Sistema")
        }, room="/")
        return redirect(url_for("routes.listar_veterinarios"))
    else:
        veterinarios = VeterinarioController.listar()
        veterinario = next((v for v in veterinarios if v["id"] == veterinario_id), None)
        if veterinario is None:
            flash("Veterinário não encontrado!", "error")
            return redirect(url_for("routes.listar_veterinarios"))
        action_url = url_for("routes.editar_veterinario", veterinario_id=veterinario_id)
        return render_template("form_veterinario.html", veterinario=veterinario, action_url=action_url)

@routes.route("/consultas")
@login_required
def listar_consultas():
    consultas = ConsultaController.listar()
    return render_template("consultas.html", consultas=consultas)

@routes.route("/consultas/nova", methods=["GET"])
@login_required
def nova_consulta():
    return render_template("form_consulta.html", consulta=None, action_url=url_for("routes.adicionar_consulta"))

@routes.route("/consultas/adicionar", methods=["POST"])
@login_required
def adicionar_consulta():
    id_animal = request.form["id_animal"]
    id_veterinario = request.form["id_veterinario"]
    data_consulta = request.form["data_consulta"]
    motivo = request.form["motivo"]
    diagnostico = request.form["diagnostico"]
    tratamento = request.form["tratamento"]
    observacoes = request.form["observacoes"]
    valor = float(request.form["valor"])
    nova_consulta = Consulta(str(uuid.uuid4()), id_animal, id_veterinario, data_consulta, motivo, diagnostico, tratamento, observacoes, valor)
    ConsultaController.adicionar(nova_consulta)
    
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} adicionou uma nova consulta",
        "operation": "create",
        "entity": "consulta",
        "data": {"id_animal": id_animal, "id_veterinario": id_veterinario},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room='/')
    return redirect(url_for("routes.listar_consultas"))

@routes.route("/consultas/remover/<consulta_id>")
@login_required
def remover_consulta(consulta_id):
    consultas = ConsultaController.listar()
    consulta = next((c for c in consultas if c["id"] == consulta_id), None)
    consulta_info = f"Consulta {consulta_id[:8]}" if consulta else "Consulta"
    
    ConsultaController.remover(consulta_id)
    
    socketio.emit("crud_notification", {
        "message": f"{{session.get(\"username\", \"Usuário\")}} removeu uma consulta",
        "operation": "delete",
        "entity": "consulta",
        "data": {"id": consulta_id},
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
        }, room='/')
    return redirect(url_for("routes.listar_consultas"))

@routes.route("/consultas/editar/<consulta_id>", methods=["GET", "POST"])
@login_required
def editar_consulta(consulta_id):
    if request.method == "POST":
        id_animal = request.form["id_animal"]
        id_veterinario = request.form["id_veterinario"]
        data_consulta = request.form["data_consulta"]
        motivo = request.form["motivo"]
        diagnostico = request.form["diagnostico"]
        tratamento = request.form["tratamento"]
        observacoes = request.form["observacoes"]
        valor = float(request.form["valor"])
        consulta_atualizada = Consulta(consulta_id, id_animal, id_veterinario, data_consulta, motivo, diagnostico, tratamento, observacoes, valor)
        ConsultaController.atualizar(consulta_atualizada)
        
        socketio.emit("crud_notification", {
            "message": f"{{session.get(\"username\", \"Usuário\")}} atualizou uma consulta",
            "operation": "update",
            "entity": "consulta",
            "data": {"id": consulta_id, "id_animal": id_animal},
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": session.get("username", "Sistema")
        }, room='/')
        return redirect(url_for("routes.listar_consultas"))
    else:
        consultas = ConsultaController.listar()
        consulta = next((c for c in consultas if c["id"] == consulta_id), None)
        if consulta is None:
            flash("Consulta não encontrada!", "error")
            return redirect(url_for("routes.listar_consultas"))
        action_url = url_for("routes.editar_consulta", consulta_id=consulta_id)
        return render_template("form_consulta.html", consulta=consulta, action_url=action_url)

@routes.route("/dashboard_realtime")
@login_required
def dashboard_realtime():
    from datetime import datetime, timedelta
    
    stats = {
        "total_clientes": len(ClienteController.listar()),
        "total_animais": len(AnimalController.listar()),
        "total_veterinarios": len(VeterinarioController.listar()),
        "total_consultas": len(ConsultaController.listar())
    }
    
    usuario = AuthController.usuario_atual()
    
    initial_activities = [
        {
            "time": datetime.now().strftime('%H:%M:%S'),
            "text": "Dashboard carregado com sucesso",
            "user": "Sistema",
            "type": "system"
        },
        {
            "time": (datetime.now() - timedelta(minutes=5)).strftime('%H:%M:%S'),
            "text": f"Logou no sistema",
            "user": usuario.get('username', 'Usuário') if usuario else 'Usuário',
            "type": "info"
        },
        {
            "time": (datetime.now() - timedelta(minutes=15)).strftime('%H:%M:%S'),
            "text": "Monitoramento em tempo real ativo",
            "user": "Sistema",
            "type": "system"
        }
    ]
    
    socketio.emit("system_notification", {
        "message": f"{usuario.get('username', 'Usuário') if usuario else 'Usuário'} acessou o dashboard em tempo real",
        "type": "info",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": session.get("username", "Sistema")
    }, room="/")
    
    return render_template("realtime_dashboard.html", stats=stats, usuario=usuario, initial_activities=initial_activities)