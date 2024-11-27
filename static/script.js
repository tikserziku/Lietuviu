document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const pasteButton = document.getElementById('pasteButton');
    const outputText = document.getElementById('outputText');
    const feedbackContainer = document.getElementById('feedbackContainer');
    const errorCount = document.getElementById('errorCount');

    const updateFeedbackStyle = (count) => {
        feedbackContainer.classList.remove('feedback-perfect', 'feedback-good', 'feedback-average', 'feedback-needs-work');
        
        if (count === 0) {
            feedbackContainer.classList.add('feedback-perfect');
        } else if (count <= 2) {
            feedbackContainer.classList.add('feedback-good');
        } else if (count <= 5) {
            feedbackContainer.classList.add('feedback-average');
        } else {
            feedbackContainer.classList.add('feedback-needs-work');
        }
    };

    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
        } catch (err) {
            console.error('Nepavyko įklijuoti teksto:', err);
            feedbackContainer.innerText = '😅 Nepavyko įklijuoti teksto. Įsitikinkite, kad suteikėte leidimą prieigai prie mainų srities.';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
        }
    });

    submitButton.addEventListener('click', () => {
        const text = inputText.value;
        
        if (!text.trim()) {
            feedbackContainer.innerText = '😊 Prašome įvesti tekstą tikrinimui!';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
            return;
        }
        
        submitButton.disabled = true;
        submitButton.textContent = 'Tikrinama...';
        outputText.innerText = 'Vyksta teksto analizė...';
        feedbackContainer.classList.remove('show');

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) throw new Error('Tinklo klaida');
            return response.json();
        })
        .then(data => {
            outputText.innerText = data.corrected_text;
            feedbackContainer.innerText = data.feedback;
            errorCount.innerText = `Rasta klaidų: ${data.error_count}`;
            
            updateFeedbackStyle(data.error_count);
            feedbackContainer.classList.add('show');
        })
        .catch(error => {
            console.error('Klaida:', error);
            feedbackContainer.innerText = '😅 Įvyko klaida! Bandyk dar kartą! 🔄';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Tikrinti';
        });
    });
});
