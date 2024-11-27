document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const pasteButton = document.getElementById('pasteButton');
    const outputText = document.getElementById('outputText');
    const feedbackContainer = document.getElementById('feedbackContainer');
    const errorDetails = document.getElementById('errorDetails');

    const updateFeedbackStyle = (count) => {
        feedbackContainer.classList.remove('feedback-perfect', 'feedback-good', 'feedback-average', 'feedback-needs-work');
        feedbackContainer.classList.add('show');
        
        if (count === 0) feedbackContainer.classList.add('feedback-perfect');
        else if (count <= 2) feedbackContainer.classList.add('feedback-good');
        else if (count <= 5) feedbackContainer.classList.add('feedback-average');
        else feedbackContainer.classList.add('feedback-needs-work');
    };

    const displayResults = (data) => {
        outputText.innerText = data.corrected_text;
        feedbackContainer.innerText = data.feedback;
        
        if (data.error_count > 0) {
            errorDetails.innerHTML = `Rastos klaidos (${data.error_count}):
                ${data.errors_found ? '<br>' + data.errors_found.join('<br>') : ''}`;
            errorDetails.classList.add('show');
        } else {
            errorDetails.classList.remove('show');
        }
        
        updateFeedbackStyle(data.error_count);
    };

    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
            clearResults();
        } catch (err) {
            showError('Nepavyko įklijuoti teksto!');
        }
    });

    const clearResults = () => {
        outputText.innerText = '';
        feedbackContainer.classList.remove('show');
        errorDetails.classList.remove('show');
    };

    const showError = (message) => {
        feedbackContainer.innerText = `😅 ${message}`;
        feedbackContainer.classList.add('show', 'feedback-needs-work');
    };

    submitButton.addEventListener('click', () => {
        const text = inputText.value.trim();
        
        if (!text) {
            showError('Įveskite tekstą!');
            return;
        }
        
        submitButton.disabled = true;
        submitButton.textContent = 'Tikrinama...';
        clearResults();

        fetch('/process', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) throw new Error('Tinklo klaida');
            return response.json();
        })
        .then(displayResults)
        .catch(error => {
            console.error('Klaida:', error);
            showError('Įvyko klaida! Bandykite dar kartą!');
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Tikrinti tekstą';
        });
    });
});
