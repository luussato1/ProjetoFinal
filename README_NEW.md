# 🐾 PETBUS 2.0 - Sistema Veterinário com WebSocket

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real%20Time-4CAF50?style=for-the-badge&logo=websocket&logoColor=white)](https://socket.io)

---

## 👨‍💻 **DESENVOLVEDORES**

| **Desenvolvedor** | **Matrícula** |
|-------------------|---------------|
| **Luiz Henrique Pessato da Mota** | 232028428 |
| **Arthur Luiz Silva Guedes** | 231028675 |

---

## 📋 **DESCRIÇÃO**

**PETBUS 2.0** é um sistema web para gestão de clínicas veterinárias que permite o controle completo de clientes, animais, veterinários e consultas. O sistema oferece uma interface moderna com atualizações em tempo real através de WebSocket, facilitando o dia a dia das clínicas veterinárias.

### 🎯 **Para que serve:**
- **Cadastro de Clientes**: Gerenciar dados dos proprietários dos animais
- **Registro de Pets**: Controlar informações dos animais (peso, idade, raça, etc.)
- **Gestão de Veterinários**: Cadastrar profissionais com CRMV e especialidades
- **Agendamento**: Marcar e controlar consultas veterinárias
- **Dashboard**: Visualizar estatísticas e atividades em tempo real
- **Chat**: Comunicação instantânea entre usuários do sistema

**Objetivo Acadêmico**: Projeto desenvolvido para a disciplina de **Orientação a Objetos**.

---

## 🚀 **FUNCIONALIDADES**

### 🔐 **Sistema de Login**
- Autenticação segura com usuário e senha
- Controle de sessões e níveis de acesso
- Área administrativa restrita

### 📊 **Gestão Completa (CRUD)**
- **Clientes**: Cadastro dos proprietários dos animais
- **Animais**: Registro completo dos pets (nome, espécie, peso, idade)
- **Veterinários**: Cadastro profissional com CRMV e especialidades
- **Consultas**: Agendamento e prontuário eletrônico

### ⚡ **Recursos em Tempo Real**
- Dashboard com estatísticas atualizadas automaticamente
- Notificações instantâneas para todas as operações
- Chat entre usuários conectados
- Sincronização entre múltiplas sessões

---

## 💻 **TECNOLOGIAS**

- **Python 3.11+** + **Flask** - Backend
- **WebSocket** (Flask-SocketIO) - Tempo real
- **HTML5/CSS3/JavaScript** - Frontend responsivo
- **JSON** - Banco de dados simples

---

## 🏃‍♂️ **COMO EXECUTAR**

```powershell
# 1. Instalar dependências
pip install flask flask-socketio

# 2. Executar
cd app
python app.py

# 3. Acessar: http://127.0.0.1:5000
```

### 👤 **Usuários para Teste**
| Usuário | Senha | Tipo |
|---------|-------|------|
| `admin` | `admin` | Administrador |
| `veterinario` | `secret123` | Usuário comum |

---

## 📁 **ESTRUTURA DO PROJETO**

```
PETBUS2.0/
├── app/
│   ├── controllers/    # Lógica de negócio
│   ├── models/        # Modelos de dados
│   ├── views/html/    # Templates HTML
│   ├── routes/        # Rotas da aplicação
│   ├── static/        # CSS, JS, imagens
│   └── app.py         # Aplicação principal
└── data/
    └── db.json        # Banco de dados
```

---

**Projeto desenvolvido para disciplina de Orientação a Objetos**  
**Data**: Julho 2025  
**Status**: Funcional  

---

*Sistema PETBUS 2.0 - Gestão Veterinária com WebSocket*
