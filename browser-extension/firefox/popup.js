// popup.js
document.getElementById('scanBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) return;

  const resultDiv = document.getElementById('result');
  resultDiv.textContent = "Scanning...";  // safe: plain text

  try {
    const response = await fetch("https://sit-say-par.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      resultDiv.textContent = "API Error: " + response.status;
      return;
    }

    const data = await response.json();
    const confidenceMap = {
      High: "မြင့်မား",
      Medium: "အလယ်အလတ်",
      Low: "နည်းပါး"
    };
    const confidenceLabel = confidenceMap[data.detection_confidence] || data.detection_confidence;

    // Clear resultDiv
    resultDiv.textContent = "";

    // Risk line
    const riskLine = document.createElement('p');
    riskLine.textContent = `Risk: ${data.risk_level} (${data.risk_score}/100)`;
    riskLine.className = data.risk_level.toLowerCase();
    resultDiv.appendChild(riskLine);

    // Confidence line
    const confLine = document.createElement('p');
    confLine.textContent = `စနစ်၏ စစ်ဆေးမှု သေချာမှု: ${confidenceLabel}`;
    confLine.className = `confidence-${data.detection_confidence.toLowerCase()}`;
    resultDiv.appendChild(confLine);

    // Explanation (first 5 lines)
    const explanationText = data.explanation.split('\n').slice(0, 5).join(' ');
    const explanationPara = document.createElement('small');
    explanationPara.textContent = explanationText;
    resultDiv.appendChild(explanationPara);

    // Contact email
    const hr = document.createElement('hr');
    hr.style.margin = '8px 0';
    resultDiv.appendChild(hr);

    const contactPara = document.createElement('small');
    contactPara.textContent = "📧 အကူအညီလိုအပ်ပါက: ";
    const emailLink = document.createElement('a');
    emailLink.href = "mailto:sitsaypar@gmail.com";
    emailLink.textContent = "sitsaypar@gmail.com";
    emailLink.style.color = "#007bff";
    contactPara.appendChild(emailLink);
    resultDiv.appendChild(contactPara);

  } catch (error) {
    resultDiv.textContent = "Error: " + error.message;
  }
});