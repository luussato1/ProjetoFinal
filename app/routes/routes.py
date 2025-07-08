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

routes = Blueprint('routes', __name__)

# Decorator para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado():
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado() or not AuthController.is_admin():
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('routes.home'))
        return f(*args, **kwargs)
    return decorated_function

# Rotas de autenticação
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = AuthController.autenticar(username, password)
        if usuario:
            AuthController.fazer_login(usuario)
            flash(f'Bem-vindo, {usuario.nome_completo}!', 'success')
            return redirect(url_for('routes.home'))
        else:
            return render_template('login.html', error='Usuário ou senha incorretos.')
    
    return render_template('login.html')

@routes.route('/logout')
def logout():
    AuthController.fazer_logout()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('routes.login'))

@routes.route('/admin')
@login_required
@admin_required
def admin_panel():
    # Estatísticas do sistema
    stats = {
        'total_clientes': len(ClienteController.listar()),
        'total_animais': len(AnimalController.listar()),
        'total_veterinarios': len(VeterinarioController.listar()),
        'total_consultas': len(ConsultaController.listar())
    }
    
    usuario = AuthController.usuario_atual()
    return render_template('admin.html', stats=stats, usuario=usuario, now=datetime.now())

@routes.route('/')
def home():
    return render_template("home.html", now=datetime.now())

# Rotas de clientes (protegidas)
@routes.route('/clientes')
@login_required
def listar_clientes():
    clientes = ClienteController.listar()
    return render_template('clientes.html', clientes=clientes)

@routes.route('/clientes/novo', methods=['GET'])
@login_required
def novo_cliente():
    return render_template('form_cliente.html', cliente=None, action_url=url_for('routes.adicionar_cliente'))

@routes.route('/clientes/adicionar', methods=['POST'])
@login_required
def adicionar_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    endereco = request.form['endereco']
    novo_cliente = Cliente(str(uuid.uuid4()), nome, email, telefone, endereco)
    ClienteController.adicionar(novo_cliente)
    flash('Cliente adicionado com sucesso!', 'success')
    return redirect(url_for('routes.listar_clientes'))

@routes.route('/clientes/remover/<cliente_id>')
@login_required
def remover_cliente(cliente_id):
    ClienteController.remover(cliente_id)
    flash('Cliente removido com sucesso!', 'success')
    return redirect(url_for('routes.listar_clientes'))

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
        flash("Cliente atualizado com sucesso!", "success")
        return redirect(url_for("routes.listar_clientes"))
    else:
        clientes = ClienteController.listar()
        cliente = next((c for c in clientes if c["id"] == cliente_id), None)
        if cliente is None:
            flash("Cliente não encontrado!", "error")
            return redirect(url_for("routes.listar_clientes"))
        action_url = url_for("routes.editar_cliente", cliente_id=cliente_id)
        return render_template("form_cliente.html", cliente=cliente, action_url=action_url)

# Rotas de animais (protegidas)
@routes.route('/animais')
@login_required
def listar_animais():
    animais = AnimalController.listar()
    return render_template('animais.html', animais=animais)

@routes.route('/animais/novo', methods=['GET'])
@login_required
def novo_animal():
    return render_template('form_animal.html', animal=None, action_url=url_for('routes.adicionar_animal'))

@routes.route('/animais/adicionar', methods=['POST'])
@login_required
def adicionar_animal():
    nome = request.form['nome']
    especie = request.form['especie']
    id_cliente = request.form['id_cliente']
    raca = request.form['raca']
    idade = int(request.form['idade'])
    peso = float(request.form['peso'])
    novo_animal = Animal(str(uuid.uuid4()), nome, especie, id_cliente, raca, idade, peso)
    AnimalController.adicionar(novo_animal)
    flash('Animal adicionado com sucesso!', 'success')
    return redirect(url_for('routes.listar_animais'))

@routes.route('/animais/remover/<animal_id>')
@login_required
def remover_animal(animal_id):
    AnimalController.remover(animal_id)
    flash('Animal removido com sucesso!', 'success')
    return redirect(url_for('routes.listar_animais'))

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
        flash("Animal atualizado com sucesso!", "success")
        return redirect(url_for("routes.listar_animais"))
    else:
        animais = AnimalController.listar()
        animal = next((a for a in animais if a["id"] == animal_id), None)
        if animal is None:
            flash("Animal não encontrado!", "error")
            return redirect(url_for("routes.listar_animais"))
        action_url = url_for("routes.editar_animal", animal_id=animal_id)
        return render_template("form_animal.html", animal=animal, action_url=action_url)

# Rotas de veterinários (protegidas)
@routes.route('/veterinarios')
@login_required
def listar_veterinarios():
    veterinarios = VeterinarioController.listar()
    return render_template('veterinarios.html', veterinarios=veterinarios)

@routes.route('/veterinarios/novo', methods=['GET'])
@login_required
def novo_veterinario():
    return render_template('form_veterinario.html', veterinario=None, action_url=url_for('routes.adicionar_veterinario'))

@routes.route('/veterinarios/adicionar', methods=['POST'])
@login_required
def adicionar_veterinario():
    nome = request.form['nome']
    crmv = request.form['crmv']
    especialidade = request.form['especialidade']
    telefone = request.form['telefone']
    email = request.form['email']
    novo_veterinario = Veterinario(str(uuid.uuid4()), nome, crmv, especialidade, telefone, email)
    VeterinarioController.adicionar(novo_veterinario)
    flash('Veterinário adicionado com sucesso!', 'success')
    return redirect(url_for('routes.listar_veterinarios'))

@routes.route('/veterinarios/remover/<veterinario_id>')
@login_required
def remover_veterinario(veterinario_id):
    VeterinarioController.remover(veterinario_id)
    flash('Veterinário removido com sucesso!', 'success')
    return redirect(url_for('routes.listar_veterinarios'))

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
        flash("Veterinário atualizado com sucesso!", "success")
        return redirect(url_for("routes.listar_veterinarios"))
    else:
        veterinarios = VeterinarioController.listar()
        veterinario = next((v for v in veterinarios if v["id"] == veterinario_id), None)
        if veterinario is None:
            flash("Veterinário não encontrado!", "error")
            return redirect(url_for("routes.listar_veterinarios"))
        action_url = url_for("routes.editar_veterinario", veterinario_id=veterinario_id)
        return render_template("form_veterinario.html", veterinario=veterinario, action_url=action_url)

# Rotas de consultas (protegidas)
@routes.route('/consultas')
@login_required
def listar_consultas():
    consultas = ConsultaController.listar()
    return render_template('consultas.html', consultas=consultas)

@routes.route('/consultas/novo', methods=['GET'])
@login_required
def nova_consulta():
    return render_template('form_consulta.html', consulta=None, action_url=url_for('routes.adicionar_consulta'))

@routes.route('/consultas/adicionar', methods=['POST'])
@login_required
def adicionar_consulta():
    id_animal = request.form['id_animal']
    id_veterinario = request.form['id_veterinario']
    data_consulta_str = request.form['data_consulta']
    data_consulta = datetime.strptime(data_consulta_str, '%Y-%m-%dT%H:%M') if data_consulta_str else None
    motivo = request.form['motivo']
    diagnostico = request.form['diagnostico']
    tratamento = request.form['tratamento']
    observacoes = request.form['observacoes']
    valor = float(request.form['valor']) if request.form['valor'] else 0.0
    nova_consulta = Consulta(str(uuid.uuid4()), id_animal, id_veterinario, data_consulta, motivo, diagnostico, tratamento, observacoes, valor)
    ConsultaController.adicionar(nova_consulta)
    flash('Consulta adicionada com sucesso!', 'success')
    return redirect(url_for('routes.listar_consultas'))

@routes.route('/consultas/remover/<consulta_id>')
@login_required
def remover_consulta(consulta_id):
    ConsultaController.remover(consulta_id)
    flash('Consulta removida com sucesso!', 'success')
    return redirect(url_for('routes.listar_consultas'))

@routes.route("/consultas/editar/<consulta_id>", methods=["GET", "POST"])
@login_required
def editar_consulta(consulta_id):
    if request.method == "POST":
        id_animal = request.form["id_animal"]
        id_veterinario = request.form["id_veterinario"]
        data_consulta_str = request.form["data_consulta"]
        data_consulta = datetime.strptime(data_consulta_str, "%Y-%m-%dT%H:%M") if data_consulta_str else None
        motivo = request.form["motivo"]
        diagnostico = request.form["diagnostico"]
        tratamento = request.form["tratamento"]
        observacoes = request.form["observacoes"]
        valor = float(request.form["valor"]) if request.form["valor"] else 0.0
        consulta_atualizada = Consulta(consulta_id, id_animal, id_veterinario, data_consulta, motivo, diagnostico, tratamento, observacoes, valor)
        ConsultaController.atualizar(consulta_atualizada)
        flash("Consulta atualizada com sucesso!", "success")
        return redirect(url_for("routes.listar_consultas"))
    else:
        consultas = ConsultaController.listar()
        consulta = next((c for c in consultas if c["id"] == consulta_id), None)
        if consulta is None:
            flash("Consulta não encontrada!", "error")
            return redirect(url_for("routes.listar_consultas"))
        # Format data_consulta for the datetime-local input
        if consulta and "data_consulta" in consulta and consulta["data_consulta"]:
            consulta["data_consulta"] = datetime.fromisoformat(consulta["data_consulta"]).strftime("%Y-%m-%dT%H:%M")
        action_url = url_for("routes.editar_consulta", consulta_id=consulta_id)
        return render_template("form_consulta.html", consulta=consulta, action_url=action_url)


