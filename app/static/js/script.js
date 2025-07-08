document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade original dos nomes dos desenvolvedores
    const showNameButton = document.getElementById('show-name-btn');
    const nameDisplay = document.getElementById('name-display');

    if (showNameButton && nameDisplay) {
        showNameButton.addEventListener('click', function() {
            const myName = "Arthur Luiz e Luiz Henrique";
            nameDisplay.textContent = `Nossos nomes são: ${myName}`;
            nameDisplay.style.color = '#D4748F';
            nameDisplay.style.fontWeight = 'bold';
            nameDisplay.style.marginTop = '10px';
        });
    }

    // Validação de formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('input[required], select[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                    field.style.backgroundColor = '#ffeaea';
                } else {
                    field.style.borderColor = '#ffcad4';
                    field.style.backgroundColor = 'white';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showMessage('Por favor, preencha todos os campos obrigatórios.', 'error');
            }
        });
    });

    // Confirmação para exclusão
    const deleteLinks = document.querySelectorAll('a[href*="/remover/"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });

    // Função para mostrar mensagens
    function showMessage(text, type = 'info') {
        const existingMessage = document.querySelector('.message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(message, container.firstChild);
            
            // Remove a mensagem após 5 segundos
            setTimeout(() => {
                message.remove();
            }, 5000);
        }
    }

    // Máscara para telefone
    const phoneInputs = document.querySelectorAll('input[name="telefone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                if (value.length < 14) {
                    value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
                }
                e.target.value = value;
            }
        });
    });

    // Validação de email
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function(e) {
            const email = e.target.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email && !emailRegex.test(email)) {
                e.target.style.borderColor = '#e74c3c';
                showMessage('Por favor, insira um email válido.', 'error');
            } else {
                e.target.style.borderColor = '#ffcad4';
            }
        });
    });

    // Animação suave para links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // Auto-focus no primeiro campo dos formulários
    const firstInput = document.querySelector('form input:first-of-type');
    if (firstInput) {
        firstInput.focus();
    }

    // Contador de caracteres para campos de texto longos
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.style.textAlign = 'right';
            counter.style.fontSize = '0.8em';
            counter.style.color = '#666';
            counter.style.marginTop = '5px';
            
            textarea.parentNode.appendChild(counter);
            
            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} caracteres restantes`;
                
                if (remaining < 50) {
                    counter.style.color = '#e74c3c';
                } else {
                    counter.style.color = '#666';
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter();
        }
    });
});