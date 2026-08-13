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

function renderOpenAIRedTeam(status) {
  const target = document.getElementById("openaiRedTeam");
  target.innerHTML = "";
  if (!status) {
    const p = document.createElement("p");
    p.textContent = "Not run yet. Use npm run redteam:openai, then npm run pull:data.";
    target.appendChild(p);
    return;
  }

  [
    ["Status", status.status],
    ["Provider", status.provider],
    ["Model", status.model_id],
    ["Reviewers", String(status.reviewer_count || 0)],
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

  const blockerList = document.createElement("ul");
  blockerList.className = "redteam-blockers";
  const blockers = status.blockers || [];
  if (blockers.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No blockers reported.";
    blockerList.appendChild(li);
  } else {
    blockers.forEach((blocker) => {
      const li = document.createElement("li");
      li.textContent = blocker;
      blockerList.appendChild(li);
    });
  }
  target.appendChild(blockerList);

  const reviewers = document.createElement("div");
  reviewers.className = "redteam-reviewers";
  (status.reviewers || []).forEach((reviewer) => {
    const card = document.createElement("article");
    card.className = "redteam-reviewer";
    const title = document.createElement("h3");
    title.textContent = `${reviewer.label}: ${reviewer.verdict}`;
    const next = document.createElement("p");
    next.textContent = reviewer.recommended_next_step || "No next step provided.";
    card.append(title, next);
    (reviewer.findings || []).slice(0, 3).forEach((finding) => {
      const item = document.createElement("p");
      item.className = "redteam-finding";
      item.textContent = `${finding.severity}: ${finding.finding} Fix: ${finding.fix}`;
      card.appendChild(item);
    });
    reviewers.appendChild(card);
  });
  target.appendChild(reviewers);
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

function renderEvidenceGraph(graph) {
  const target = document.getElementById("evidenceGraph");
  target.innerHTML = "";
  if (!graph || graph.status !== "included") {
    const p = document.createElement("p");
    p.textContent = "Evidence graph not available in the current snapshot.";
    target.appendChild(p);
    return;
  }

  const summary = document.createElement("p");
  summary.className = "artifact-boundary";
  const figureHash = graph.figure_receipt ? graph.figure_receipt.figure_sha256.slice(0, 12) : "not built";
  summary.textContent = `${graph.node_count} nodes, ${graph.edge_count} edges from ${graph.path}; figure sha256 ${figureHash}`;
  target.appendChild(summary);

  if (graph.figure) {
    const figure = document.createElement("img");
    figure.className = "kg-figure";
    figure.src = graph.figure;
    figure.alt = "FCG perturbation evidence star chart";
    target.appendChild(figure);
    return;
  }

  const width = 980;
  const height = 420;
  const centerX = width / 2;
  const centerY = height / 2;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Knowledge graph showing candidate, adjacent drugs, mechanisms, and evidence status");
  svg.classList.add("kg-svg");

  const candidate = graph.nodes.find((node) => node.kind === "candidate") || graph.nodes[0];
  const otherNodes = graph.nodes.filter((node) => node.id !== candidate.id);
  const positions = new Map();
  positions.set(candidate.id, { x: centerX, y: centerY });
  otherNodes.forEach((node, index) => {
    const angle = (-Math.PI / 2) + (index / Math.max(otherNodes.length, 1)) * Math.PI * 2;
    const radius = node.kind === "drug" ? 155 : 195;
    positions.set(node.id, {
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
    });
  });

  graph.edges.forEach((edge) => {
    const source = positions.get(edge.source);
    const targetPos = positions.get(edge.target);
    if (!source || !targetPos) return;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", source.x);
    line.setAttribute("y1", source.y);
    line.setAttribute("x2", targetPos.x);
    line.setAttribute("y2", targetPos.y);
    line.classList.add(edge.predicate === "MECHANISM_SIMILAR" ? "kg-edge-strong" : "kg-edge");
    svg.appendChild(line);
  });

  graph.nodes.forEach((node) => {
    const pos = positions.get(node.id);
    if (!pos) return;
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.classList.add("kg-node");

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pos.x);
    circle.setAttribute("cy", pos.y);
    circle.setAttribute("r", node.kind === "candidate" ? 42 : 24);
    circle.classList.add(`kg-${node.kind}`);

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", pos.x);
    label.setAttribute("y", pos.y + (node.kind === "candidate" ? 58 : 40));
    label.textContent = node.label;

    group.append(circle, label);
    svg.appendChild(group);
  });

  const legend = document.createElement("div");
  legend.className = "kg-legend";
  [
    ["candidate", "Top candidate"],
    ["drug", "Adjacent comparator"],
    ["evidence", "Mechanism/evidence node"],
  ].forEach(([kind, label]) => {
    const item = document.createElement("span");
    item.innerHTML = `<b class="legend-dot kg-${kind}"></b>${label}`;
    legend.appendChild(item);
  });

  target.append(svg, legend);
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
    renderOpenAIRedTeam(snapshot.integrations.openai_redteam);
    renderBrightData(snapshot.integrations.bright_data);
    renderEvidenceGraph(snapshot.evidence_graph);
    renderOvernightData(snapshot.overnight);
    renderCustody(snapshot.custody);
    renderProblems(snapshot);
    renderDocs(snapshot.strands.selected_docs);
  })
  .catch((error) => {
    document.getElementById("generatedAt").textContent = error.message;
  });
