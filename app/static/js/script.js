document.addEventListener('DOMContentLoaded', function() {
    initPageTransitions();
    initFormValidation();
    initLoadingStates();
    initTooltips();
    initWebSocketTracking();
    
    function initPageTransitions() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    }
    
    function initLoadingStates() {
        const buttons = document.querySelectorAll('.btn:not(.btn-logout)');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (this.closest('form')) {
                    this.innerHTML = '<span>⏳ Processando...</span>';
                    this.disabled = true;
                    
                    setTimeout(() => {
                        this.disabled = false;
                        this.innerHTML = this.dataset.originalText || 'Enviar';
                    }, 3000);
                }
            });
        });
    }
    
    function initTooltips() {
        const adminBtns = document.querySelectorAll('.admin-btn, .quick-btn');
        adminBtns.forEach(btn => {
            btn.setAttribute('title', 'Clique para acessar esta funcionalidade');
        });
    }

    const showNameButton = document.getElementById('show-name-btn');
    const nameDisplay = document.getElementById('name-display');

    if (showNameButton && nameDisplay) {
        showNameButton.addEventListener('click', function() {
            const myName = "Arthur Luiz e Luiz Henrique";
            nameDisplay.textContent = `Nossos nomes são: ${myName}`;
            nameDisplay.style.color = '#667eea';
            nameDisplay.style.fontWeight = 'bold';
            nameDisplay.style.marginTop = '10px';
        });
    }

    function initFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const requiredFields = form.querySelectorAll('input[required], select[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    field.classList.remove('error');
                    
                    if (!field.value.trim()) {
                        isValid = false;
                        field.style.borderColor = '#e74c3c';
                        field.style.backgroundColor = '#ffeaea';
                    } else {
                        field.style.borderColor = '#667eea';
                        field.style.backgroundColor = 'white';
                    }
                });
            
                if (!isValid) {
                    e.preventDefault();
                    showMessage('Por favor, preencha todos os campos obrigatórios.', 'error');
                }
            });
        });
    }

    const deleteLinks = document.querySelectorAll('a[href*="/remover/"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });

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
            
            setTimeout(() => {
                message.remove();
            }, 5000);
        }
    }

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

    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    const firstInput = document.querySelector('form input:first-of-type');
    if (firstInput) {
        firstInput.focus();
    }

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
    
    function initWebSocketTracking() {
        const currentPath = window.location.pathname;
        let entityType = null;
        
        if (currentPath.includes('/clientes')) {
            entityType = 'clientes';
        } else if (currentPath.includes('/animais')) {
            entityType = 'animais';
        } else if (currentPath.includes('/veterinarios')) {
            entityType = 'veterinarios';
        } else if (currentPath.includes('/consultas')) {
            entityType = 'consultas';
        }
        
        if (entityType && typeof socket !== 'undefined') {
            setInterval(() => {
                requestDataUpdate(entityType);
            }, 30000);
        }
    }
});

if (typeof io !== 'undefined') {
    const socket = io();
    
    socket.on('connect', function() {
        socket.emit('join', {room: 'general'});
    });
    
    socket.on('crud_notification', function(data) {
        showRealtimeNotification(data);
    });
    
    socket.on('system_alert', function(data) {
        showSystemAlert(data);
    });
    
    function showRealtimeNotification(data) {
        const notification = document.createElement('div');
        notification.className = 'realtime-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <strong>${data.user}</strong> ${data.message}
                <span class="notification-time">${data.timestamp}</span>
            </div>
        `;
        
        if (!document.getElementById('realtime-notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'realtime-notification-styles';
            styles.textContent = `
                .realtime-notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #2196F3;
                    color: white;
                    padding: 15px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    z-index: 10000;
                    max-width: 350px;
                    animation: slideInRight 0.3s ease-out;
                }
                
                .realtime-notification.create {
                    background: #4CAF50;
                }
                
                .realtime-notification.update {
                    background: #FF9800;
                }
                
                .realtime-notification.delete {
                    background: #f44336;
                }
                
                .notification-content {
                    font-size: 14px;
                    line-height: 1.4;
                }
                
                .notification-time {
                    display: block;
                    font-size: 12px;
                    opacity: 0.8;
                    margin-top: 5px;
                }
                
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(styles);
        }
        
        if (data.operation) {
            notification.classList.add(data.operation);
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
        
        notification.addEventListener('click', function() {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }
    
    function showSystemAlert(data) {
        alert(`[${data.timestamp}] ${data.message}`);
    }
    
    function trackUserActivity(activityType, page) {
        socket.emit('user_activity', {
            activity_type: activityType,
            page: page || window.location.pathname
        });
    }
}

function requestDataUpdate(entityType) {
    if (typeof socket !== 'undefined' && socket.connected) {
        socket.emit('request_data_update', {entity_type: entityType});
    }
}
