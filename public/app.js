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

function renderOpenAIAgent(status) {
  const target = document.getElementById("openaiAgent");
  target.innerHTML = "";
  if (!status) {
    const p = document.createElement("p");
    p.textContent = "Not run yet. Use npm run agent:openai, then npm run pull:data.";
    target.appendChild(p);
    return;
  }
  [
    ["Status", status.status],
    ["Provider", status.provider],
    ["Model", status.model_id],
    ["Key", status.api_key_present ? "present" : "not set"],
    ["Generated", new Date(status.generated_at).toLocaleString()],
  ].forEach(([label, value]) => {
    const row = document.createElement("div");
    row.className = "kv";
    const key = document.createElement("span");
    key.textContent = label;
    const val = document.createElement("span");
    val.textContent = value || "";
    row.append(key, val);
    target.appendChild(row);
  });
  const output = document.createElement("p");
  output.className = "agent-output";
  output.textContent = status.output || status.note || status.error || "";
  target.appendChild(output);
}

function renderBrightData(status) {
  const target = document.getElementById("brightData");
  target.innerHTML = "";
  if (!status) {
    const p = document.createElement("p");
    p.textContent = "Not checked yet. Use npm run status:brightdata, then npm run pull:data.";
    target.appendChild(p);
    return;
  }
  [
    ["Status", status.status],
    ["Package", `${status.package || ""} ${status.package_version || ""}`.trim()],
    ["MCP server", status.mcp_server],
    ["Token", status.token_present ? `${status.token_env_name} present (${status.token_length})` : "not visible"],
    ["Groups", status.groups],
    ["Checked", new Date(status.generated_at).toLocaleString()],
  ].forEach(([label, value]) => {
    const row = document.createElement("div");
    row.className = "kv";
    const key = document.createElement("span");
    key.textContent = label;
    const val = document.createElement("span");
    val.textContent = value || "";
    row.append(key, val);
    target.appendChild(row);
  });
  const note = document.createElement("p");
  note.className = "agent-output";
  note.textContent = status.note || "";
  target.appendChild(note);
}

function renderOvernightData(overnight) {
  const target = document.getElementById("overnightData");
  target.innerHTML = "";
  if (!overnight) return;
  const summary = document.createElement("p");
  summary.className = "artifact-boundary";
  summary.textContent = `${overnight.status}: ${overnight.boundary}`;
  target.appendChild(summary);
  overnight.artifacts
    .filter((artifact) => artifact.exists)
    .forEach((artifact) => {
      const row = document.createElement("article");
      row.className = "artifact-row";
      const path = document.createElement("strong");
      path.textContent = artifact.path;
      const meta = document.createElement("span");
      const rows = artifact.rows === undefined ? artifact.kind : `${artifact.rows} rows`;
      meta.textContent = `${rows}, ${artifact.bytes} bytes, sha256 ${artifact.sha256.slice(0, 12)}`;
      const cols = document.createElement("p");
      cols.textContent = artifact.columns ? artifact.columns.join(", ") : (artifact.json_keys || []).join(", ");
      row.append(path, meta, cols);
      target.appendChild(row);
    });
}

function renderCustody(custody) {
  const target = document.getElementById("custodyDesign");
  target.innerHTML = "";
  if (!custody) return;

  [
    ["Claim ceiling", custody.claim_ceiling],
    ["Conversation policy", custody.conversation_policy],
  ].forEach(([label, value]) => {
    const row = document.createElement("div");
    row.className = "kv";
    const key = document.createElement("span");
    key.textContent = label;
    const val = document.createElement("span");
    val.textContent = value || "";
    row.append(key, val);
    target.appendChild(row);
  });

  const list = document.createElement("ol");
  custody.chain.forEach((step) => {
    const li = document.createElement("li");
    li.textContent = step;
    list.appendChild(li);
  });
  target.appendChild(list);

  const receipts = document.createElement("p");
  receipts.className = "artifact-boundary";
  receipts.textContent = `Receipts: ${custody.receipt_paths.join(", ")}`;
  target.appendChild(receipts);
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
    renderOpenAIAgent(snapshot.integrations.openai_agent);
    renderBrightData(snapshot.integrations.bright_data);
    renderOvernightData(snapshot.overnight);
    renderCustody(snapshot.custody);
    renderProblems(snapshot);
    renderDocs(snapshot.strands.selected_docs);
  })
  .catch((error) => {
    document.getElementById("generatedAt").textContent = error.message;
  });
