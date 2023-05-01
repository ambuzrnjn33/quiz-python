const form = document.querySelector('form');
const resultContainer = document.querySelector('#result-container');
console.log(resultContainer);

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const data = {};

  for (const [key, value] of formData.entries()) {
    data[key] = value;
  }

  fetch('/results', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  
  .then(response => response.text())
  .then(response => {
    console.log(response);
    resultContainer.innerHTML = response;
  })

//  .then(response => response.json())
//  .then(response => {
//    console.log(response);

//    // Display the results on the page
//    if (resultContainer) {
//      resultContainer.innerHTML = `
//        <p>Score: ${response.score.toFixed(1)} / ${response.num_questions}</p>
//        <p>Proficiency: ${response.proficiency}</p>
//        <ul>
//          ${Object.keys(response.results).map(question => `
//            <li>
//              ${question}: ${response.results[question]}
//            </li>
//          `).join('')}
//        </ul>
//      `;
//    }
//  })
  .catch(error => {
    console.error(error);
    // Display an error message on the page
    if (resultContainer) {
      resultContainer.innerHTML = '<p>An error occurred while submitting your quiz. Please try again later.</p>';
    }
  });
});

