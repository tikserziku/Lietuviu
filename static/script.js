document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const pasteButton = document.getElementById('pasteButton');
    const outputText = document.getElementById('outputText');
    const feedbackContainer = document.getElementById('feedbackContainer');
    const errorCount = document.getElementById('errorCount');

    const updateFeedbackStyle = (count) => {
        feedbackContainer.classList.remove('feedback-perfect', 'feedback-good', 'feedback-average', 'feedback-needs-work');
        feedbackContainer.classList.remove('show');
        
        if (count === 0) {
            feedbackContainer.classList.add('feedback-perfect');
            // Показываем сообщение об успехе только на короткое время
            feedbackContainer.classList.add('show');
            setTimeout(() => {
                feedbackContainer.classList.remove('show');
            }, 3000);
        } else {
            if (count <= 2) feedbackContainer.classList.add('feedback-good');
            else if (count <= 5) feedbackContainer.classList.add('feedback-average');
            else feedbackContainer.classList.add('feedback-needs-work');
            feedbackContainer.classList.add('show');
        }
    };

    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
            // Очищаем предыдущие результаты при вставке нового текста
            outputText.innerText = '';
            feedbackContainer.classList.remove('show');
            errorCount.innerText = '';
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
        outputText.innerText = 'Analizuojama...';

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
            
            if (data.error_count > 0) {
                feedbackContainer.innerText = data.feedback;
                errorCount.innerText = `Klaidų skaičius: ${data.error_count}`;
                updateFeedbackStyle(data.error_count);
            } else {
                // Показываем краткое сообщение об успехе
                feedbackContainer.innerText = "🌟 Puiku! Tekstas parašytas be klaidų! ⭐";
                errorCount.innerText = "Klaidų nerasta";
                updateFeedbackStyle(0);
            }
        })
        .catch(error => {
            console.error('Klaida:', error);
            feedbackContainer.innerText = '😅 Klaida! Bandykite dar kartą! 🔄';
            feedbackContainer.classList.add('show', 'feedback-needs-work');
            outputText.innerText = '';
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Tikrinti tekstą';
        });
    });
});
