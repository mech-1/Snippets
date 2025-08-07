const codeCount = document.getElementById('count');
const textArea = document.querySelector('textarea');

const numChars = textArea.value.length;
codeCount.textContent = `${numChars}/5000`;

textArea.addEventListener('input', () => {
    const numChars = textArea.value.length;
    codeCount.textContent = `${numChars}/5000`;
})