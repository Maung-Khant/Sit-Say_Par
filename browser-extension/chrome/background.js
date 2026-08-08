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

async function fetchResult(url) {
  try {
    const response = await fetch("https://sit-say-par.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/icon48.png",
      title: "Sit-Say Par Result",
      message: `Risk: ${data.risk_level} (${data.risk_score}/100)\n${data.explanation.split('\n').slice(0,2).join(' ')}...`,
      requireInteraction: true
    });
  } catch (error) {
    console.error("Error scanning URL:", error);
  }
}
