# 🐾 PETBUS - Sistema Veterinário BMVC

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 📋 Descrição

Sistema veterinário completo desenvolvido em **Flask** seguindo o padrão **BMVC** (Business Model View Controller) para gerenciamento eficiente de clínicas veterinárias. O sistema oferece uma interface moderna e intuitiva para controle de clientes, animais, veterinários e consultas.

## 📋 Funcionalidades Implementadas

### ✅ Requisitos do Nível 3 da BMVC

- **CRUD Completo**: Operações Create, Read, Update, Delete para todos os modelos
- **Sistema de Login**: Autenticação de usuários com controle de sessão
- **Controle de Acesso**: Páginas protegidas e área administrativa restrita
- **Páginas HTML/TPL**: Templates funcionais com design responsivo
- **CSS e JS Ativos**: Estilos e scripts JavaScript plenamente funcionais

### 🏗️ Arquitetura BMVC

- **Models**: Cliente, Animal, Veterinário, Consulta, Usuário
- **Views**: Templates HTML com Jinja2
- **Controllers**: Lógica de negócio e manipulação de dados
- **Business**: Regras de negócio e validações

### 🔐 Sistema de Autenticação

- Login com usuário e senha
- Controle de sessões
- Proteção de rotas
- Área administrativa para administradores
- Logout seguro

### 📊 Modelos de Dados

1. **Cliente**: Nome, email, telefone, endereço
2. **Animal**: Nome, espécie, raça, idade, peso, cliente proprietário
3. **Veterinário**: Nome, CRMV, especialidade, telefone, email
4. **Consulta**: Animal, veterinário, data, motivo, diagnóstico, tratamento, observações, valor
5. **Usuário**: Username, senha (hash), email, nome completo, permissões

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Windows PowerShell ou Terminal

### Instalação e Execução

1. **Clone ou baixe o projeto**:
   ```powershell
   # Se usando git
   git clone <url-do-repositorio>
   # Ou baixe e extraia o arquivo ZIP
   ```

2. **Navegue até o diretório do projeto**:
   ```powershell
   cd "c:\Users\lu1zi\Desktop\bmvc_projeto\bmvc_projeto\bmvc_projeto"
   ```

3. **Instale as dependências** (recomendado criar um ambiente virtual):

   ```powershell
   # Criar ambiente virtual (opcional, mas recomendado)
   python -m venv venv
   
   # Ativar ambiente virtual
   .\venv\Scripts\Activate.ps1
   
   # Instalar dependências do arquivo requirements.txt
   pip install -r requirements.txt
   
   # OU instalar Flask manualmente
   pip install flask
   ```

4. **Execute a aplicação**:
   ```powershell
   cd app
   python app.py
   ```

5. **Acesse no navegador**:

   ```
   http://127.0.0.1:5000
   ```

### ⚠️ Solução de Problemas

- **Erro de execução de scripts**: Se houver erro com PowerShell, execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **Módulo Flask não encontrado**: Certifique-se de que o Flask está instalado:
  ```powershell
  pip install flask
  ```

## 👤 Usuários de Teste

### 🔑 Administrador

- **Usuário**: `admin`
- **Senha**: `admin`
- **Permissões**: Acesso total ao sistema e área administrativa

### 👨‍⚕️ Veterinário

- **Usuário**: `veterinario`
- **Senha**: `secret123`
- **Permissões**: Acesso às funcionalidades do sistema

## 🎯 Funcionalidades por Módulo

### 🏠 Página Inicial

- Apresentação do sistema
- Botão para exibir nomes dos desenvolvedores
- Acesso ao login

### 👥 Gestão de Clientes

- Listar todos os clientes
- Adicionar novo cliente
- Editar dados do cliente
- Excluir cliente
- Validações de formulário

### 🐕 Gestão de Animais

- Cadastro completo de animais
- Vinculação com clientes
- Controle de dados veterinários
- CRUD completo

### 👨‍⚕️ Gestão de Veterinários

- Cadastro de profissionais
- Controle de CRMV e especialidades
- Dados de contato

### 📋 Gestão de Consultas

- Agendamento de consultas
- Vinculação animal-veterinário
- Registro de diagnósticos e tratamentos
- Controle de valores

### 🔐 Área Administrativa

- Dashboard com estatísticas
- Acesso restrito a administradores
- Visão geral do sistema
- Ações administrativas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: JSON (para desenvolvimento)
- **Autenticação**: Flask Sessions
- **Validações**: JavaScript + Python
- **Design**: CSS responsivo com tema personalizado

## ✨ Melhorias Implementadas

### 🎨 CSS Avançado

- Design responsivo
- Animações e transições
- Tema consistente com cores personalizadas
- Componentes visuais modernos

### ⚡ JavaScript Funcional

- Validação de formulários em tempo real
- Máscaras para telefone
- Confirmações de exclusão
- Mensagens de feedback
- Auto-focus em campos
- Contador de caracteres

### 🎯 UX/UI

- Navegação intuitiva
- Mensagens de sucesso/erro
- Design mobile-friendly
- Feedback visual para ações

## 📁 Estrutura do Projeto

```text
bmvc_projeto/
├── app/
│   ├── models/          # Modelos de dados
│   ├── views/html/      # Templates HTML
│   ├── controllers/     # Controladores
│   ├── routes/          # Rotas da aplicação
│   ├── static/
│   │   ├── css/         # Estilos CSS
│   │   ├── js/          # Scripts JavaScript
│   │   └── images/      # Imagens do sistema
│   └── app.py           # Aplicação principal
├── data/
│   └── db.json          # Banco de dados JSON
└── README.md            # Documentação
```

## 👨‍💻 Desenvolvedores

- **Arthur Luiz**
- **Luiz Henrique**

## 📋 Observações para Apresentação

- Sistema completo e funcional
- Todos os requisitos do Nível 3 implementados
- CRUD testado e validado
- Sistema de login operacional
- CSS e JavaScript ativos e funcionais
- Pronto para demonstração em vídeo

## 📝 Funcionalidades Principais

- ✅ **CRUD Completo** para todos os modelos
- ✅ **Sistema de Autenticação** com controle de sessão
- ✅ **Interface Responsiva** com design moderno
- ✅ **Validações** em tempo real
- ✅ **Área Administrativa** restrita
- ✅ **Banco de Dados** em JSON para simplicidade

## 🔄 Fluxo do Sistema

1. **Login** → Autenticação do usuário
2. **Dashboard** → Visão geral do sistema
3. **Gestão** → CRUD de clientes, animais, veterinários
4. **Consultas** → Agendamento e controle
5. **Admin** → Área administrativa (apenas admin)

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se o Python 3.11+ está instalado
2. Certifique-se de que o Flask está instalado
3. Execute o sistema a partir do diretório correto
4. Acesse via <http://127.0.0.1:5000>

---

### 🏆 Projeto desenvolvido para a disciplina BMVC - Nível 3

**Status**: ✅ Concluído e funcional  
**Última atualização**: Janeiro 2025

