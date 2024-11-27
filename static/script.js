document.getElementById('submitButton').addEventListener('click', () => {
    const text = document.getElementById('inputText').value;
    const button = document.getElementById('submitButton');
    const outputText = document.getElementById('outputText');
    
    // Disable button and show loading state
    button.disabled = true;
    button.textContent = 'Обработка...';
    outputText.innerText = 'Подождите, текст обрабатывается...';

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        outputText.innerText = data.processed_text;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        outputText.innerText = 'Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.';
    })
    .finally(() => {
        // Re-enable button and restore original text
        button.disabled = false;
        button.textContent = 'Проверить';
    });
});
