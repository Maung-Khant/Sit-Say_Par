// popup.js
document.getElementById('scanBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) return;

  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = "Scanning...";

  try {
    const response = await fetch("https://sit-say-par.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    resultDiv.innerHTML = `
      <strong>Risk:</strong> <span class="${data.risk_level.toLowerCase()}">${data.risk_level}</span> (${data.risk_score}/100)<br>
      <small>${data.explanation.split('\n').slice(0,3).join('<br>')}</small>
    `;
  } catch (error) {
    resultDiv.innerHTML = "Error: " + error.message;
  }
});
