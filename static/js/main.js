// Get the form element
const quizForm = document.querySelector('form');

// Attach an event listener to the form submission
quizForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the default form submission behavior

  // Get the user's answers from the form
  const formData = new FormData(quizForm);
  const userAnswers = {};
  for (const [question, answer] of formData) {
    userAnswers[question] = answer;
  }

  // Send an AJAX request to the server to get the quiz results
  fetch('/results', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userAnswers)
  })
  .then(response => response.json())
  .then(data => {
    // Update the results page with the user's score and feedback
    const resultsSection = document.querySelector('#results');
    resultsSection.innerHTML = `
      <p>You scored ${data.score} out of ${data.num_questions}.</p>
      <p>Your proficiency level is ${data.proficiency}.</p>
      <h2>Feedback</h2>
      <ul>
        ${Object.entries(data.results).map(([question, result]) => `<li>${question}: ${result}</li>`).join('')}
      </ul>
    `;
    resultsSection.classList.remove('hidden');
  })
  .catch(error => {
    console.error(error);
    alert('An error occurred while submitting your quiz. Please try again later.');
  });
});

