document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('math-input');
    const solveBtn = document.getElementById('solve-btn');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const mainResult = document.getElementById('main-result');
    const derivativeResult = document.getElementById('derivative-result');
    const integralResult = document.getElementById('integral-result');
    const solutionsResult = document.getElementById('solutions-result');

    const solve = async () => {
        const expression = input.value.trim();
        if (!expression) return;

        // Show loading, hide results
        loading.classList.remove('hidden');
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression }),
            });

            const data = await response.json();

            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            // Update LaTeX content
            mainResult.innerHTML = `\\[ ${data.latex} \\]`;
            derivativeResult.innerHTML = data.details.derivative ? `\\[ ${data.details.derivative} \\]` : 'N/A';
            integralResult.innerHTML = data.details.integral ? `\\[ ${data.details.integral} \\]` : 'N/A';
            solutionsResult.innerHTML = data.details.solutions ? `\\[ ${data.details.solutions} \\]` : 'N/A';

            // Trigger MathJax re-render
            if (window.MathJax) {
                MathJax.typesetPromise();
            }

            // Show results
            resultContainer.classList.remove('hidden');
        } catch (err) {
            console.error(err);
            alert('Failed to connect to the server.');
        } finally {
            loading.classList.add('hidden');
        }
    };

    solveBtn.addEventListener('click', solve);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') solve();
    });
});
