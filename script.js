document.getElementById('submitButton').addEventListener('click', () => {
    const text = document.getElementById('inputText').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('outputText').innerText = data.processed_text;
    })
    .catch(error => console.error('Ошибка:', error));
});
