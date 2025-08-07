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

const alertsBox = document.getElementById("alertsFixedContainer");
setTimeout(closeMessages, 2000);