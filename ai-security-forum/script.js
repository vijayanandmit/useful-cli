const seedThreads = [
  {
    title: "Prompt injection guardrails for customer support copilots",
    topic: "Prompt Injection",
    risk: "High",
    summary: "What layered controls actually reduce real-world exploit success without harming completion quality?",
    replies: 18
  },
  {
    title: "SOC2 evidence mapping for model governance controls",
    topic: "Model Governance",
    risk: "Medium",
    summary: "Looking for practical mapping from policy statements to observable telemetry and audit artifacts.",
    replies: 11
  },
  {
    title: "Detecting PII leakage in generated summaries",
    topic: "Data Leakage",
    risk: "Critical",
    summary: "Need lightweight checks before outbound messages hit users in our healthcare chatbot workflow.",
    replies: 27
  },
  {
    title: "Package signing strategy for local AI agent plugins",
    topic: "Supply Chain",
    risk: "Medium",
    summary: "Comparing Sigstore-style provenance with private key signing for internal extension ecosystems.",
    replies: 8
  }
];

const state = {
  threads: [...seedThreads],
  topic: "All",
  risk: "All",
  query: ""
};

const topicList = document.getElementById("topicList");
const riskList = document.getElementById("riskList");
const threadFeed = document.getElementById("threadFeed");
const threadCount = document.getElementById("threadCount");
const replyCount = document.getElementById("replyCount");
const searchInput = document.getElementById("searchInput");
const newThreadBtn = document.getElementById("newThreadBtn");
const threadDialog = document.getElementById("threadDialog");
const threadForm = document.getElementById("threadForm");
const cancelBtn = document.getElementById("cancelBtn");

function uniqueValues(key) {
  return [...new Set(state.threads.map((thread) => thread[key]))];
}

function buildChips(container, values, selected, onClick) {
  container.innerHTML = "";
  ["All", ...values].forEach((value) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = `chip ${value === selected ? "active" : ""}`;
    button.textContent = value;
    button.addEventListener("click", () => onClick(value));
    item.appendChild(button);
    container.appendChild(item);
  });
}

function matchesFilter(thread) {
  const matchesTopic = state.topic === "All" || thread.topic === state.topic;
  const matchesRisk = state.risk === "All" || thread.risk === state.risk;
  const query = state.query.trim().toLowerCase();
  const matchesQuery = !query || `${thread.title} ${thread.summary} ${thread.topic} ${thread.risk}`.toLowerCase().includes(query);
  return matchesTopic && matchesRisk && matchesQuery;
}

function riskClass(risk) {
  return ["Critical", "High"].includes(risk) ? `risk-${risk.toLowerCase()}` : "";
}

function renderThreads() {
  const visible = state.threads.filter(matchesFilter);
  threadFeed.innerHTML = "";

  if (!visible.length) {
    threadFeed.innerHTML = "<p>No threads match your filters.</p>";
  }

  visible.forEach((thread) => {
    const article = document.createElement("article");
    article.className = "thread-card";
    article.innerHTML = `
      <h3>${thread.title}</h3>
      <div class="thread-meta">
        <span class="pill">${thread.topic}</span>
        <span class="pill ${riskClass(thread.risk)}">${thread.risk} Risk</span>
        <span>${thread.replies} replies</span>
      </div>
      <p>${thread.summary}</p>
    `;
    threadFeed.appendChild(article);
  });

  threadCount.textContent = String(state.threads.length);
  replyCount.textContent = String(state.threads.reduce((acc, thread) => acc + thread.replies, 0));
}

function renderFilters() {
  buildChips(topicList, uniqueValues("topic"), state.topic, (value) => {
    state.topic = value;
    renderThreads();
    renderFilters();
  });
  buildChips(riskList, uniqueValues("risk"), state.risk, (value) => {
    state.risk = value;
    renderThreads();
    renderFilters();
  });
}

searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderThreads();
});

newThreadBtn.addEventListener("click", () => threadDialog.showModal());
cancelBtn.addEventListener("click", () => threadDialog.close());

threadForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(threadForm);
  state.threads.unshift({
    title: String(formData.get("title")),
    topic: String(formData.get("topic")),
    risk: String(formData.get("risk")),
    summary: String(formData.get("summary")),
    replies: 0
  });
  threadForm.reset();
  threadDialog.close();
  renderFilters();
  renderThreads();
});

renderFilters();
renderThreads();
