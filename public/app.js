async function loadSnapshot() {
  const response = await fetch("./data/dashboard_snapshot.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Snapshot load failed: ${response.status}`);
  }
  return response.json();
}

function textNode(value) {
  return document.createTextNode(value || "");
}

function renderBoundaries(items) {
  const target = document.getElementById("boundaries");
  target.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.appendChild(textNode(item));
    target.appendChild(li);
  });
}

function renderCommands(commands) {
  const target = document.getElementById("commands");
  target.innerHTML = "";
  commands.forEach((command) => {
    const code = document.createElement("code");
    code.textContent = command;
    target.appendChild(code);
  });
}

function renderIntegrations(env) {
  const target = document.getElementById("integrationState");
  target.innerHTML = "";
  env.forEach((item) => {
    const row = document.createElement("div");
    row.className = "kv";
    const key = document.createElement("span");
    key.textContent = item.name;
    const value = document.createElement("span");
    value.textContent = item.present ? `present (${item.length})` : "not set";
    row.append(key, value);
    target.appendChild(row);
  });
}

function renderProblems(snapshot) {
  const fits = new Map(snapshot.biopharma.candidate_lanes.map((lane) => [lane.title, lane.fit]));
  const target = document.getElementById("problemStatements");
  target.innerHTML = "";
  snapshot.biopharma.problem_statements.forEach((statement) => {
    const card = document.createElement("article");
    card.className = "lane-card";
    const num = document.createElement("div");
    num.className = "num";
    num.textContent = statement.id;
    const title = document.createElement("h3");
    title.textContent = statement.title;
    const description = document.createElement("p");
    description.textContent = statement.description;
    const fit = document.createElement("div");
    fit.className = "fit";
    fit.textContent = fits.get(statement.title) || "Needs lane mapping.";
    card.append(num, title, description, fit);
    target.appendChild(card);
  });
}

function renderDocs(docs) {
  const target = document.getElementById("docs");
  target.innerHTML = "";
  docs.forEach((doc) => {
    const row = document.createElement("article");
    row.className = "doc-row";
    const section = document.createElement("strong");
    section.textContent = doc.section;
    const summary = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = doc.title;
    const description = document.createElement("p");
    description.textContent = doc.description || doc.url;
    summary.append(title, description);
    const link = document.createElement("a");
    link.href = doc.url;
    link.textContent = "Open";
    link.target = "_blank";
    link.rel = "noreferrer";
    row.append(section, summary, link);
    target.appendChild(row);
  });
}

loadSnapshot()
  .then((snapshot) => {
    document.getElementById("generatedAt").textContent = `Updated ${new Date(
      snapshot.generated_at,
    ).toLocaleString()}`;
    document.getElementById("strandsSummary").textContent = snapshot.strands.summary;
    renderBoundaries(snapshot.project.boundaries);
    renderCommands(snapshot.strands.install_commands);
    renderIntegrations(snapshot.integrations.env);
    renderProblems(snapshot);
    renderDocs(snapshot.strands.selected_docs);
  })
  .catch((error) => {
    document.getElementById("generatedAt").textContent = error.message;
  });

