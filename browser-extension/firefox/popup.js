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

    if (!response.ok) {
      resultDiv.innerHTML = "API Error: " + response.status;
      return;
    }

    const data = await response.json();
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
      <hr style="margin: 8px 0;">
      <small>📧 အကူအညီလိုအပ်ပါက: <a href="mailto:sitsaypar@gmail.com" style="color:#007bff;">sitsaypar@gmail.com</a></small>
    `;
  } catch (error) {
    resultDiv.innerHTML = "Error: " + error.message;
  }
});