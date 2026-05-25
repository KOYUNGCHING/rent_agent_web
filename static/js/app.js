const areaForm = document.querySelector("#area-form");
const locationInput = document.querySelector("#location-input");
const quickButtons = document.querySelectorAll("[data-area]");
const chatbot = document.querySelector("#chatbot");
const chatPanel = document.querySelector("#chat-panel");
const chatToggle = document.querySelector("#chat-toggle");
const chatClose = document.querySelector("#chat-close");
const chatForm = document.querySelector("#chat-form");
const chatInput = document.querySelector("#chat-input");
const messages = document.querySelector("#messages");

function updateAreaCard(data) {
  document.querySelector("#area-title").textContent = `${data.area}附近`;
  document.querySelector("#area-district").textContent = data.district;
  document.querySelector("#traffic-score").textContent = data.traffic_score;
  document.querySelector("#weather-value").textContent = data.weather;
  document.querySelector("#rent-value").textContent = data.rent;
  document.querySelector("#air-value").textContent = data.air;
  document.querySelector("#area-summary").textContent = data.summary;
  document.querySelector("#report-time").textContent = `${data.generated_at} 更新`;
  const facilityList = document.querySelector("#facility-list");
  facilityList.replaceChildren();
  data.facilities.forEach((facility) => {
    const item = document.createElement("div");
    item.className = "facility";
    const icon = document.createElement("b");
    icon.textContent = facility.icon;
    const label = document.createElement("span");
    label.textContent = facility.name;
    const detail = document.createElement("small");
    detail.textContent = facility.detail;
    label.appendChild(detail);
    item.append(icon, label);
    facilityList.appendChild(item);
  });
}

async function analyzeArea(location) {
  const submitButton = areaForm.querySelector("button");
  const originalLabel = submitButton.innerHTML;
  submitButton.disabled = true;
  submitButton.textContent = "整理中...";
  try {
    const response = await fetch("/api/insight", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    updateAreaCard(result);
  } catch (error) {
    addMessage(error.message || "暫時無法整理區域資料，請稍後再試。", "bot");
    openChat();
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = originalLabel;
  }
}

areaForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const location = locationInput.value.trim();
  if (location) analyzeArea(location);
});

quickButtons.forEach((button) => {
  button.addEventListener("click", () => {
    locationInput.value = button.dataset.area;
    analyzeArea(button.dataset.area);
  });
});

function openChat() {
  chatbot.classList.add("open");
  chatPanel.setAttribute("aria-hidden", "false");
  chatToggle.setAttribute("aria-expanded", "true");
  chatInput.focus();
}

function closeChat() {
  chatbot.classList.remove("open");
  chatPanel.setAttribute("aria-hidden", "true");
  chatToggle.setAttribute("aria-expanded", "false");
}

function addMessage(text, role) {
  const bubble = document.createElement("div");
  bubble.className = `message ${role}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

async function askAssistant(message) {
  addMessage(message, "user");
  chatInput.value = "";
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const result = await response.json();
    addMessage(result.reply || result.error, "bot");
  } catch (error) {
    addMessage("目前連線不穩定，請稍後再問我一次。", "bot");
  }
}

chatToggle.addEventListener("click", openChat);
chatClose.addEventListener("click", closeChat);
chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (message) askAssistant(message);
});

document.querySelectorAll(".chat-suggestions button").forEach((button) => {
  button.addEventListener("click", () => askAssistant(button.textContent));
});
