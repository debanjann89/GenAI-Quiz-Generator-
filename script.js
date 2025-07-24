document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('quiz-form');
    const generateBtn = document.getElementById('generate-btn');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('quiz-results');

    form.addEventListener('submit', async(event) => {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        // Get form data
        const sourceText = document.getElementById('source-text').value;
        const numQuestions = document.getElementById('num-questions').value;
        const difficulty = document.getElementById('difficulty').value;

        if (sourceText.trim() === '') {
            alert('Please paste some text to generate a quiz.');
            return;
        }

        // Show loader and hide previous results
        loader.classList.remove('hidden');
        resultsContainer.innerHTML = '';
        generateBtn.disabled = true;

        try {
            // Send data to our Flask backend
            const response = await fetch('/generate-quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source_text: sourceText,
                    num_questions: numQuestions,
                    difficulty: difficulty,
                }),
            });

            if (!response.ok) {
                throw new Error(`An error occurred: ${response.statusText}`);
            }

            const data = await response.json();
            displayQuiz(data.quiz);

        } catch (error) {
            resultsContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        } finally {
            // Hide loader and re-enable button
            loader.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    function displayQuiz(questions) {
        if (!questions || questions.length === 0) {
            resultsContainer.innerHTML = '<p>No quiz could be generated. Try different text or settings.</p>';
            return;
        }

        questions.forEach(q => {
            const card = document.createElement('div');
            card.className = 'question-card';

            let optionsHTML = '';
            if (q.question_type === 'Multiple Choice') {
                optionsHTML = '<div class="options">';
                q.options.forEach(option => {
                    const isCorrect = option === q.correct_answer;
                    optionsHTML += `<label><input type="radio" name="q${q.question_number}" disabled ${isCorrect ? 'checked' : ''}> ${option}</label>`;
                });
                optionsHTML += '</div>';
            } else { // True/False
                optionsHTML = `<p>Answer: ${q.correct_answer}</p>`;
            }

            card.innerHTML = `
                <h3>Q${q.question_number}: ${q.question_text}</h3>
                ${optionsHTML}
                <p class="explanation"><strong>Explanation:</strong> ${q.explanation}</p>
            `;
            resultsContainer.appendChild(card);
        });
    }
});