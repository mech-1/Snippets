function closeMessage() {
    const message = alertsBox.querySelector('div');
    message.remove();
}


function closeMessages() {
    const messages = alertsBox.querySelectorAll('div');
    let step = 600;
    let messageNum = 1;
    for (let message of messages) {
        setTimeout(closeMessage, messageNum * step);
        messageNum++;
    }
}

// <div className="alert alert-warning alert-dismissible fade show" role="alert">
//     Доработать закрытие сообщений по таймеру
//     <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>
// </div>

function sendMessage(text, type = 'info') {
    const message = document.createElement('div');
    message.classList.add('alert', 'alert-dismissible', 'fade', 'show');
    message.classList.add(`alert-${type}`);
    message.setAttribute('role', 'alert');
    message.innerHTML = `${text} <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>`;
    alertsBox.appendChild(message);
    setTimeout(closeMessages, 2000);
}

function sendMessageToDjango(message, level = 'info') {
    fetch('/send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
        },
        body: JSON.stringify({message: message, level: level, url: window.location.href, path: window.location.pathname})
    })
        .then(response => response.json())
        .then(data => {
            console.log('Message sent:', data);
        })
        .catch(error => console.error('Error:', error));
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const alertsBox = document.getElementById("alertsFixedContainer");
setTimeout(closeMessages, 2000);