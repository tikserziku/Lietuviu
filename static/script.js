document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const pasteButton = document.getElementById('pasteButton');
    const outputText = document.getElementById('outputText');
    const feedbackContainer = document.getElementById('feedbackContainer');
    const errorCount = document.getElementById('errorCount');

    const updateFeedbackStyle = (count) => {
        feedbackContainer.classList.remove('feedback-perfect', 'feedback-good', 'feedback-average', 'feedback-needs-work');
        
        if (count === 0) feedbackContainer.classList.add('feedback-perfect');
        else if (count <= 2) feedbackContainer.classList.add('feedback-good');
        else if (count <= 5) feedbackContainer.classList.add('feedback-average');
        else feedbackContainer.classList.add('feedback-needs-work');
    };

    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
        } catch (err) {
            feedbackContainer.innerText = '😅 Nepavyko įklijuoti teksto!';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
        }
    });

    submitButton.addEventListener('click', () => {
        const text = inputText.value;
        
        if (!text.trim()) {
            feedbackContainer.innerText = '😊 Įveskite tekstą!';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
            return;
        }
        
        submitButton.disabled = true;
        submitButton.textContent = 'Tikrinama...';
        feedbackContainer.classList.remove('show');
        errorCount.innerText = '';

        fetch('/process', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) throw new Error('Tinklo klaida');
            return response.json();
        })
        .then(data => {
            outputText.innerText = data.corrected_text;
            feedbackContainer.innerText = data.feedback;
            errorCount.innerText = `Klaidų skaičius: ${data.error_count}`;
            
            updateFeedbackStyle(data.error_count);
            feedbackContainer.classList.add('show');
        })
        .catch(error => {
            feedbackContainer.innerText = '😅 Klaida! Bandykite dar kartą! 🔄';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Tikrinti tekstą';
        });
    });
});
