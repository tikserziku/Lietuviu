document.getElementById('submitButton').addEventListener('click', () => {
    const text = document.getElementById('inputText').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorInfo => Promise.reject(errorInfo));
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('outputText').innerText = data.processed_text;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('outputText').innerText = 'Произошла ошибка при обработке запроса.';
    });
});
