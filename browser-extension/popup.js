document.getElementById('scanBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) return;
  
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = "Scanning...";
  
  // Send message to background to call API (or call directly if host permissions allow)
  chrome.runtime.sendMessage({ action: "analyzeUrl", url: url }, (response) => {
    if (response.error) {
      resultDiv.innerHTML = "Error: " + response.error;
    } else {
      resultDiv.innerHTML = `
        <strong>Risk:</strong> <span class="${response.risk_level.toLowerCase()}">${response.risk_level}</span> (${response.risk_score}/100)<br>
        <small>${response.explanation.split('\n').slice(0,3).join('<br>')}</small>
      `;
    }
  });
});
