document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const pasteButton = document.getElementById('pasteButton');
    const outputText = document.getElementById('outputText');

    // Функция для вставки текста из буфера обмена
    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
        } catch (err) {
            console.error('Nepavyko įklijuoti teksto:', err);
            outputText.innerText = 'Nepavyko įklijuoti teksto. Įsitikinkite, kad suteikėte leidimą prieigai prie mainų srities.';
        }
    });

    submitButton.addEventListener('click', () => {
        const text = inputText.value;
        
        if (!text.trim()) {
            outputText.innerText = 'Prašome įvesti tekstą tikrinimui';
            return;
        }
        
        submitButton.disabled = true;
        submitButton.textContent = 'Tikrinama...';
        outputText.innerText = 'Vyksta teksto analizė...';

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Tinklo klaida');
            }
            return response.json();
        })
        .then(data => {
            outputText.innerText = data.processed_text;
        })
        .catch(error => {
            console.error('Klaida:', error);
            outputText.innerText = 'Įvyko klaida apdorojant tekstą. Bandykite dar kartą vėliau.';
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Tikrinti';
        });
    });
});
