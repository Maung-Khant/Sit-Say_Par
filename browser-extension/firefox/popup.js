// popup.js
document.getElementById('scanBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) return;

  const resultDiv = document.getElementById('result');
  resultDiv.textContent = "Scanning...";  // Safe text assignment

  try {
    const response = await fetch("https://sit-say-par.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const data = await response.json();

    // Clear previous content
    resultDiv.innerHTML = "";

    // Create risk level element
    const riskSpan = document.createElement('span');
    riskSpan.className = `score level-${data.risk_level.toLowerCase()}`;
    riskSpan.textContent = `${data.risk_level} (${data.risk_score}/100)`;

    // Create explanation paragraph
    const explanationP = document.createElement('p');
    explanationP.textContent = data.explanation.split('\n').slice(0,3).join(' ');

    // Append to result
    resultDiv.appendChild(document.createTextNode("Risk: "));
    resultDiv.appendChild(riskSpan);
    resultDiv.appendChild(document.createElement('br'));
    resultDiv.appendChild(explanationP);

  } catch (error) {
    resultDiv.textContent = "Error: " + error.message;
  }
});