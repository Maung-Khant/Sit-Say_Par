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

    // Confidence mapping
    const confidenceMap = {
      High: "မြင့်မား",
      Medium: "အလယ်အလတ်",
      Low: "နည်းပါး"
    };
    const confidenceLabel = confidenceMap[data.detection_confidence] || data.detection_confidence;

    resultDiv.innerHTML = `
      <strong>Risk:</strong> <span class="${data.risk_level.toLowerCase()}">${data.risk_level}</span> (${data.risk_score}/100)<br>
      <strong>စနစ်၏ စစ်ဆေးမှု သေချာမှု:</strong> <span class="confidence-${data.detection_confidence.toLowerCase()}">${confidenceLabel}</span><br>
      <small>${data.explanation.split('\n').slice(0,5).join('<br>')}</small>
    `;
  } catch (error) {
    resultDiv.innerHTML = "Error: " + error.message;
  }
});