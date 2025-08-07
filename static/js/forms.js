const codeCount = document.getElementById('count');
const textArea = document.querySelector('textarea[name="code"]');
const maxlength = textArea.getAttribute("maxlength");

const formDataKey = 'FormDataDraft';
const autosaveDraftInterval = 15000;
const numChars = textArea.value.length;
codeCount.textContent = `${numChars}/${maxlength}`;

const name = document.querySelector('input[name="name"]');
const lang = document.querySelector('select[name="lang"]');
const code = document.querySelector('textarea[name="code"]');

textArea.addEventListener('input', () => {
    const numChars = textArea.value.length;
    codeCount.textContent = `${numChars}/${maxlength}`;
})

// 1. Сохранение данных формы (по таймеру)
function saveDraft() {
    const formData = {
        name: name.value,
        lang: lang.value,
        code: code.value,
    }
    // sendMessage("Данные формы сохранены");
    // save form if not empty
    for (const element of Object.values(formData)) {
        if (element.length !== 0) {
            localStorage.setItem(formDataKey, JSON.stringify(formData));
            break;
        }
    }
}

setInterval(saveDraft, autosaveDraftInterval);

// 2. Восстановление (localStorage --> form)
function restoreDraft(){
    const data = localStorage.getItem(formDataKey);
    const formData = JSON.parse(data);
    name.value = formData.name;
    lang.value = formData.lang;
    code.value = formData.code;
}

// Проверка данных формы
function checkDraft(){
    const data = localStorage.getItem(formDataKey);
    console.log(JSON.parse(data));
    if (data){
        if (confirm('Восстановить данные формы?')){
            restoreDraft();
        }
        localStorage.removeItem(formDataKey);
    }
}

document.addEventListener('DOMContentLoaded', function (){
    checkDraft();
})