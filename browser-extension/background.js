// background.js
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "scanWithSitSayPar",
    title: "Scan with Sit-Say Par",
    contexts: ["link", "selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  let url = info.linkUrl || info.selectionText;
  if (url) {
    url = url.trim();
    fetchResult(url);
  }
});

// Listen for messages from popup (not used now, but kept for future)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyzeUrl") {
    fetchResult(request.url).then(sendResponse);
    return true;
  }
});

async function fetchResult(url) {
  try {
    const response = await fetch("https://sit-say-par.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    // Show notification
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/icon48.png",
      title: "Sit-Say Par Result",
      message: `Risk: ${data.risk_level} (${data.risk_score}/100)\n${data.explanation.split('\n').slice(0,2).join(' ')}...`,
      requireInteraction: true
    });
    return data;
  } catch (error) {
    console.error("Error scanning URL:", error);
    return { error: "Scan failed" };
  }
}
