"""Multi-mode visualization tool.

Generates a self-contained HTML file and opens it in the browser.
Supports: graph, timeline, sankey, dashboard (auto-picks based on data).
Uses D3.js force simulation with Rive-inspired canvas particle animations.
"""

import json
import os
import tempfile
import webbrowser


# ---------------------------------------------------------------------------
# Public tool
# ---------------------------------------------------------------------------

def generate_visualization(data_json: str) -> str:
    """Generate and open a rich interactive visualization in the browser.

    Picks the best view type automatically, or use the viz_type hint.

    Args:
        data_json: JSON string with:
          {
            "title": "descriptive title",
            "viz_type": "auto|graph|timeline|sankey|dashboard",  // default auto
            "complexity_note": "one-line summary of what makes this complex",
            "nodes": [
              {"id": "str", "label": "str", "type": "bill|member|committee|topic|other",
               "weight": 1}   // weight = importance, optional
            ],
            "edges": [
              {"source": "id", "target": "id", "label": "str", "weight": 1}
            ],
            "events": [   // for timeline view
              {"id": "str", "label": "str", "date": "YYYY-MM-DD",
               "type": "bill|vote|action|hearing|other"}
            ],
            "flows": [    // for sankey view
              {"source": "str", "target": "str", "value": 1, "label": "str"}
            ]
          }

    Returns:
        Confirmation string, or an error message.
    """
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as exc:
        return f"Error: data_json is not valid JSON: {exc}"

    nodes  = data.get("nodes", [])
    edges  = data.get("edges", [])
    events = data.get("events", [])
    flows  = data.get("flows", [])
    title  = data.get("title", "Visualization")
    note   = data.get("complexity_note", "")

    # auto-pick viz type
    hint = data.get("viz_type", "auto")
    if hint == "auto":
        if flows:
            viz_type = "sankey"
        elif events and not nodes:
            viz_type = "timeline"
        elif nodes and (events or flows):
            viz_type = "dashboard"
        else:
            viz_type = "graph"
    else:
        viz_type = hint

    html = _build_html(title, viz_type, nodes, edges, events, flows, note)

    path = os.path.join(tempfile.gettempdir(), "gov_bot_viz.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)

    webbrowser.open(f"file://{path}")
    return (
        f"Visualization opened ({viz_type} mode, {len(nodes)} nodes, "
        f"{len(edges)} edges, {len(events)} events, {len(flows)} flows). "
        f"File: {path}"
    )


# keep old name as alias
def generate_knowledge_graph(graph_json: str) -> str:
    """Alias for generate_visualization (graph mode)."""
    return generate_visualization(graph_json)


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

_TYPE_COLORS = {
    "bill":      "#4A90D9",
    "member":    "#2ECC71",
    "committee": "#E67E22",
    "topic":     "#9B59B6",
    "vote":      "#E74C3C",
    "action":    "#F39C12",
    "hearing":   "#1ABC9C",
    "other":     "#7F8C8D",
}

_LEGEND_ITEMS = [
    ("Bill",      _TYPE_COLORS["bill"]),
    ("Member",    _TYPE_COLORS["member"]),
    ("Committee", _TYPE_COLORS["committee"]),
    ("Topic",     _TYPE_COLORS["topic"]),
    ("Vote",      _TYPE_COLORS["vote"]),
    ("Other",     _TYPE_COLORS["other"]),
]


def _legend_html() -> str:
    rows = "\n".join(
        f'    <div class="li"><div class="dot" style="background:{c}"></div>{lbl}</div>'
        for lbl, c in _LEGEND_ITEMS
    )
    return rows


def _build_html(title, viz_type, nodes, edges, events, flows, note):
    safe_title = title.replace("<", "&lt;").replace(">", "&gt;")
    safe_note  = note.replace("<", "&lt;").replace(">", "&gt;")

    nodes_js  = json.dumps(nodes)
    edges_js  = json.dumps(edges)
    events_js = json.dumps(events)
    flows_js  = json.dumps(flows)

    node_count = len(nodes)
    edge_count = len(edges)
    density = round(edge_count / max(node_count, 1), 2)

    # Complexity score 0-100 based on nodes, edges, density
    complexity = min(100, int(node_count * 3 + edge_count * 2 + density * 10))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{safe_title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3-sankey/0.12.3/d3-sankey.min.js"></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0d0d1a;--surface:rgba(255,255,255,0.04);--border:rgba(255,255,255,0.08);
  --text:#e0e4f0;--dim:#8899aa;--accent:#4A90D9;
}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;height:100vh}}
svg,canvas{{display:block}}

/* ── header ── */
#hdr{{position:fixed;top:0;left:0;right:0;z-index:20;
  background:rgba(13,13,26,.9);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:12px;padding:9px 16px;height:48px}}
#hdr h1{{flex:1;font-size:14px;font-weight:600;letter-spacing:.02em;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.badge{{background:rgba(74,144,217,.18);border:1px solid rgba(74,144,217,.35);
  color:#7ab8f5;border-radius:20px;padding:2px 10px;font-size:11px;white-space:nowrap}}

/* ── tabs ── */
#tabs{{display:flex;gap:4px}}
.tab{{background:none;border:1px solid var(--border);border-radius:6px;
  color:var(--dim);font-size:11px;padding:3px 10px;cursor:pointer;transition:all .15s}}
.tab.active,.tab:hover{{background:var(--accent);border-color:var(--accent);color:#fff}}

/* ── main canvas area ── */
#main{{position:fixed;top:48px;bottom:0;left:0;right:280px}}
#svg-layer{{width:100%;height:100%}}

/* ── side panel ── */
#panel{{position:fixed;top:48px;bottom:0;right:0;width:280px;
  background:rgba(13,13,26,.95);border-left:1px solid var(--border);
  overflow-y:auto;padding:14px}}
.panel-section{{margin-bottom:18px}}
.panel-section h3{{font-size:11px;font-weight:600;letter-spacing:.08em;
  text-transform:uppercase;color:var(--dim);margin-bottom:8px}}

/* complexity meter */
#complexity-wrap{{position:relative}}
#complexity-bar-bg{{height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden}}
#complexity-bar{{height:6px;border-radius:3px;width:0;transition:width 1.2s cubic-bezier(.22,1,.36,1)}}
#complexity-label{{font-size:22px;font-weight:700;margin:4px 0 2px;letter-spacing:-.02em}}
#complexity-desc{{font-size:11px;color:var(--dim)}}

/* stats grid */
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:4px}}
.stat{{background:var(--surface);border:1px solid var(--border);
  border-radius:6px;padding:8px 10px}}
.stat-val{{font-size:18px;font-weight:700;letter-spacing:-.02em}}
.stat-lbl{{font-size:10px;color:var(--dim);margin-top:1px}}

/* legend */
#legend .li{{display:flex;align-items:center;gap:7px;margin:5px 0;font-size:12px}}
#legend .dot{{width:9px;height:9px;border-radius:50%;flex-shrink:0}}

/* node detail */
#detail{{background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:10px;min-height:48px}}
#detail-name{{font-size:13px;font-weight:600;margin-bottom:4px}}
#detail-type{{font-size:10px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--dim);margin-bottom:6px}}
#detail-connections{{font-size:11px;color:var(--dim)}}

/* ── tooltip ── */
#tip{{position:fixed;z-index:30;pointer-events:none;
  background:rgba(13,13,26,.96);border:1px solid rgba(255,255,255,.14);
  border-radius:7px;padding:7px 11px;font-size:12px;display:none;
  box-shadow:0 4px 20px rgba(0,0,0,.5)}}

/* controls */
#ctrl{{position:fixed;bottom:16px;left:16px;z-index:20;display:flex;gap:6px}}
.ctrl-btn{{background:rgba(13,13,26,.85);backdrop-filter:blur(6px);
  border:1px solid var(--border);border-radius:7px;color:var(--dim);
  font-size:15px;width:32px;height:32px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:all .15s}}
.ctrl-btn:hover{{background:rgba(74,144,217,.25);color:#fff;border-color:var(--accent)}}

/* ── graph specific ── */
.node-circle{{cursor:pointer;transition:r .2s}}
.node-circle:hover{{stroke:#fff;stroke-width:2px}}
.edge-line{{stroke:rgba(100,120,180,.4);stroke-width:1.5px;fill:none}}
.edge-label{{font-size:9px;fill:#6677aa;pointer-events:none}}
.node-label{{font-size:10px;fill:#cdd3e8;pointer-events:none;
  text-anchor:middle;dominant-baseline:central}}

/* ── timeline specific ── */
.tl-line{{stroke:rgba(255,255,255,.12);stroke-width:1.5px}}
.tl-node{{cursor:pointer}}
.tl-label{{font-size:11px;fill:var(--text)}}
.tl-date{{font-size:9px;fill:var(--dim)}}

/* ── sankey specific ── */
.sk-node rect{{cursor:pointer;rx:4}}
.sk-link{{fill:none;opacity:.4;transition:opacity .2s}}
.sk-link:hover{{opacity:.75}}

/* particle canvas overlay */
#pcanvas{{position:absolute;inset:0;pointer-events:none}}

/* note */
#note-text{{font-size:11px;color:var(--dim);line-height:1.5;
  background:var(--surface);border:1px solid var(--border);
  border-radius:6px;padding:8px 10px}}
</style>
</head>
<body>

<div id="hdr">
  <h1>{safe_title}</h1>
  <div id="tabs">
    <button class="tab active" onclick="switchTab('graph')">Graph</button>
    <button class="tab" onclick="switchTab('timeline')">Timeline</button>
    <button class="tab" onclick="switchTab('sankey')">Flow</button>
  </div>
  <span class="badge" id="mode-badge">{viz_type}</span>
</div>

<div id="main">
  <svg id="svg-layer"></svg>
  <canvas id="pcanvas"></canvas>
</div>

<div id="panel">
  <div class="panel-section">
    <h3>Complexity</h3>
    <div id="complexity-label">—</div>
    <div id="complexity-bar-bg"><div id="complexity-bar"></div></div>
    <div id="complexity-desc" style="margin-top:4px">{safe_note if safe_note else "Structural complexity of the discussion."}</div>
  </div>

  <div class="panel-section">
    <h3>Stats</h3>
    <div class="stats">
      <div class="stat"><div class="stat-val" id="s-nodes">{node_count}</div><div class="stat-lbl">Entities</div></div>
      <div class="stat"><div class="stat-val" id="s-edges">{edge_count}</div><div class="stat-lbl">Relations</div></div>
      <div class="stat"><div class="stat-val" id="s-density">{density}</div><div class="stat-lbl">Density</div></div>
      <div class="stat"><div class="stat-val" id="s-events">{len(events)}</div><div class="stat-lbl">Events</div></div>
    </div>
  </div>

  <div class="panel-section" id="legend">
    <h3>Legend</h3>
{_legend_html()}
  </div>

  <div class="panel-section">
    <h3>Selected</h3>
    <div id="detail">
      <div id="detail-name" style="color:var(--dim)">Click a node</div>
      <div id="detail-type"></div>
      <div id="detail-connections"></div>
    </div>
  </div>
</div>

<div id="tip"></div>

<div id="ctrl">
  <button class="ctrl-btn" id="btn-fit" title="Fit">⊕</button>
  <button class="ctrl-btn" id="btn-zin" title="Zoom in">+</button>
  <button class="ctrl-btn" id="btn-zout" title="Zoom out">−</button>
  <button class="ctrl-btn" id="btn-play" title="Toggle particles">◉</button>
</div>

<script>
// ─────────────────────────────────────────────
// DATA
// ─────────────────────────────────────────────
const RAW_NODES  = {nodes_js};
const RAW_EDGES  = {edges_js};
const RAW_EVENTS = {events_js};
const RAW_FLOWS  = {flows_js};
const COMPLEXITY = {complexity};

const TYPE_COLOR = {{
  bill:'#4A90D9', member:'#2ECC71', committee:'#E67E22',
  topic:'#9B59B6', vote:'#E74C3C', action:'#F39C12',
  hearing:'#1ABC9C', other:'#7F8C8D'
}};

// ─────────────────────────────────────────────
// COMPLEXITY METER (animated on load)
// ─────────────────────────────────────────────
function initComplexity() {{
  const bar   = document.getElementById('complexity-bar');
  const label = document.getElementById('complexity-label');
  const score = COMPLEXITY;
  const color = score < 30 ? '#2ECC71' : score < 60 ? '#F39C12' : score < 80 ? '#E67E22' : '#E74C3C';
  const word  = score < 30 ? 'Simple' : score < 60 ? 'Moderate' : score < 80 ? 'Complex' : 'Highly Complex';
  bar.style.background = color;
  setTimeout(() => {{
    bar.style.width = score + '%';
    let n = 0;
    const step = score / 40;
    const t = setInterval(() => {{
      n = Math.min(n + step, score);
      label.textContent = Math.round(n);
      if (n >= score) {{ clearInterval(t); label.textContent = word + ' (' + score + ')'; }}
    }}, 20);
  }}, 300);
}}

// ─────────────────────────────────────────────
// PARTICLE CANVAS (Rive-inspired animated overlay)
// ─────────────────────────────────────────────
let particlesOn = true;
const pcanvas = document.getElementById('pcanvas');
const pctx    = pcanvas.getContext('2d');
let particles = [];
let simNodes  = [];   // filled when graph is drawn
let animFrame;

function resizeParticleCanvas() {{
  pcanvas.width  = pcanvas.offsetWidth;
  pcanvas.height = pcanvas.offsetHeight;
}}

class Particle {{
  constructor(edge, nodes) {{
    this.edge = edge;
    this.nodes = nodes;
    this.t = Math.random();
    this.speed = 0.002 + Math.random() * 0.003;
    this.alpha = 0;
    this.size  = 2 + Math.random() * 2;
    this.color = TYPE_COLOR[this.edge.srcType] || '#4A90D9';
  }}
  update() {{
    this.t += this.speed;
    if (this.t > 1) {{ this.t = 0; this.alpha = 0; }}
    // fade in/out at endpoints
    const fade = Math.sin(this.t * Math.PI);
    this.alpha = fade * 0.8;
  }}
  draw(ctx, xform) {{
    const s = this.edge.source, tgt = this.edge.target;
    if (!s || !tgt) return;
    const x = s.x + (tgt.x - s.x) * this.t;
    const y = s.y + (tgt.y - s.y) * this.t;
    const [sx,sy] = applyTransform(x, y, xform);
    ctx.beginPath();
    ctx.arc(sx, sy, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.globalAlpha = this.alpha;
    ctx.fill();
    ctx.globalAlpha = 1;
  }}
}}

let currentTransform = {{ k:1, x:0, y:0 }};
function applyTransform(x, y, t) {{
  return [x * t.k + t.x, y * t.k + t.y];
}}

function spawnParticles(edgeData) {{
  particles = [];
  edgeData.forEach(e => {{
    const count = 3 + Math.floor((e.weight || 1) * 2);
    for (let i = 0; i < count; i++) {{
      const p = new Particle(e, simNodes);
      p.t = Math.random();
      particles.push(p);
    }}
  }});
}}

function animateParticles() {{
  animFrame = requestAnimationFrame(animateParticles);
  if (!particlesOn) {{ pctx.clearRect(0, 0, pcanvas.width, pcanvas.height); return; }}
  pctx.clearRect(0, 0, pcanvas.width, pcanvas.height);
  particles.forEach(p => {{ p.update(); p.draw(pctx, currentTransform); }});
}}

// ─────────────────────────────────────────────
// GRAPH VIEW  (D3 force-directed)
// ─────────────────────────────────────────────
let graphSvg, graphSim;

function drawGraph() {{
  const el = document.getElementById('svg-layer');
  el.innerHTML = '';
  resizeParticleCanvas();

  const W = el.clientWidth, H = el.clientHeight;
  const svg = d3.select('#svg-layer');
  graphSvg = svg;

  // arrow marker
  svg.append('defs').append('marker')
    .attr('id','arrow').attr('viewBox','0 -4 8 8').attr('refX',18).attr('refY',0)
    .attr('markerWidth',6).attr('markerHeight',6).attr('orient','auto')
    .append('path').attr('d','M0,-4L8,0L0,4').attr('fill','rgba(100,120,200,.5)');

  const g = svg.append('g');

  // zoom
  const zoom = d3.zoom().scaleExtent([0.15,4])
    .on('zoom', ev => {{
      g.attr('transform', ev.transform);
      currentTransform = {{ k: ev.transform.k, x: ev.transform.x, y: ev.transform.y }};
    }});
  svg.call(zoom);

  // fit button
  document.getElementById('btn-fit').onclick = () =>
    svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(W/2,H/2).scale(0.8));
  document.getElementById('btn-zin').onclick  = () => svg.transition().duration(300).call(zoom.scaleBy, 1.35);
  document.getElementById('btn-zout').onclick = () => svg.transition().duration(300).call(zoom.scaleBy, 1/1.35);

  // build data
  const nodes = RAW_NODES.map(n => ({{
    ...n,
    r: 14 + (n.weight || 1) * 4,
    color: TYPE_COLOR[n.type] || TYPE_COLOR.other
  }}));
  const idMap = Object.fromEntries(nodes.map(n => [n.id, n]));
  const links = RAW_EDGES.map(e => ({{
    ...e,
    source: idMap[e.source] || e.source,
    target: idMap[e.target] || e.target,
    srcType: (idMap[e.source] || {{}}).type || 'other'
  }}));

  simNodes = nodes;

  // simulation
  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d=>d.id).distance(d => 90 + (d.weight||1)*20))
    .force('charge', d3.forceManyBody().strength(-280))
    .force('center', d3.forceCenter(W/2, H/2))
    .force('collide', d3.forceCollide(d => d.r + 8));
  graphSim = sim;

  // edges
  const edgeG = g.append('g');
  const link = edgeG.selectAll('path').data(links).join('path')
    .attr('class','edge-line')
    .attr('marker-end','url(#arrow)');

  const edgeLabel = edgeG.selectAll('text.edge-label').data(links).join('text')
    .attr('class','edge-label').text(d => d.label || '');

  // nodes
  const nodeG = g.append('g');
  const node = nodeG.selectAll('g').data(nodes).join('g')
    .attr('class','node-g')
    .call(d3.drag()
      .on('start', (ev,d) => {{ if(!ev.active) sim.alphaTarget(.3).restart(); d.fx=d.x; d.fy=d.y; }})
      .on('drag',  (ev,d) => {{ d.fx=ev.x; d.fy=ev.y; }})
      .on('end',   (ev,d) => {{ if(!ev.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }}))
    .on('mouseover', (ev,d) => showTip(ev, d.label + ' [' + d.type + ']'))
    .on('mousemove', moveTip)
    .on('mouseout',  hideTip)
    .on('click', (ev,d) => selectNode(d, links));

  // glow filter
  const defs = svg.select('defs');
  const filter = defs.append('filter').attr('id','glow');
  filter.append('feGaussianBlur').attr('stdDeviation','4').attr('result','coloredBlur');
  const feMerge = filter.append('feMerge');
  feMerge.append('feMergeNode').attr('in','coloredBlur');
  feMerge.append('feMergeNode').attr('in','SourceGraphic');

  node.append('circle')
    .attr('class','node-circle')
    .attr('r', d => d.r)
    .attr('fill', d => d.color)
    .attr('fill-opacity',.85)
    .attr('stroke', d => d.color)
    .attr('stroke-width',1.5)
    .attr('filter','url(#glow)');

  // pulse ring (Rive-inspired breathing animation via CSS)
  node.append('circle')
    .attr('r', d => d.r + 6)
    .attr('fill','none')
    .attr('stroke', d => d.color)
    .attr('stroke-width',1)
    .attr('stroke-opacity',0)
    .attr('class','pulse-ring')
    .each(function(d) {{
      const el = this;
      const delay = Math.random() * 2000;
      function pulse() {{
        d3.select(el)
          .attr('r', d.r + 4).attr('stroke-opacity',.6)
          .transition().duration(1200).ease(d3.easeSinOut)
          .attr('r', d.r + 18).attr('stroke-opacity', 0)
          .on('end', () => setTimeout(pulse, 800 + Math.random()*1200));
      }}
      setTimeout(pulse, delay);
    }});

  node.append('text')
    .attr('class','node-label')
    .attr('dy','0.35em')
    .text(d => d.label.length > 16 ? d.label.slice(0,14)+'…' : d.label);

  // tick
  sim.on('tick', () => {{
    link.attr('d', d => {{
      const dx = d.target.x - d.source.x, dy = d.target.y - d.source.y;
      const dr = Math.sqrt(dx*dx+dy*dy)*1.2;
      return `M${{d.source.x}},${{d.source.y}} A${{dr}},${{dr}} 0 0,1 ${{d.target.x}},${{d.target.y}}`;
    }});
    edgeLabel.attr('x', d => (d.source.x+d.target.x)/2)
             .attr('y', d => (d.source.y+d.target.y)/2);
    node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
  }});

  // spawn particles after sim settles a bit
  setTimeout(() => {{
    spawnParticles(links);
    animateParticles();
  }}, 800);

  document.getElementById('btn-play').onclick = () => {{
    particlesOn = !particlesOn;
    document.getElementById('btn-play').style.color = particlesOn ? '#4A90D9' : '';
  }};
}}

// ─────────────────────────────────────────────
// TIMELINE VIEW
// ─────────────────────────────────────────────
function drawTimeline() {{
  const el = document.getElementById('svg-layer');
  el.innerHTML = '';
  cancelAnimationFrame(animFrame);
  pctx.clearRect(0, 0, pcanvas.width, pcanvas.height);

  if (!RAW_EVENTS.length) {{
    d3.select('#svg-layer').append('text')
      .attr('x','50%').attr('y','50%').attr('text-anchor','middle')
      .attr('fill','#8899aa').attr('font-size',14)
      .text('No timeline events in this data.');
    return;
  }}

  const W = el.clientWidth, H = el.clientHeight;
  const svg = d3.select('#svg-layer');
  const margin = {{left:60,right:60,top:80,bottom:40}};
  const iW = W - margin.left - margin.right;

  const events = [...RAW_EVENTS].sort((a,b) => a.date < b.date ? -1 : 1);
  const dates  = events.map(e => new Date(e.date));
  const xScale = d3.scaleTime()
    .domain([d3.min(dates), d3.max(dates)])
    .range([0, iW]).nice();

  const g = svg.append('g').attr('transform', `translate(${{margin.left}},${{H/2}})`);

  // axis line
  g.append('line').attr('class','tl-line').attr('x1',0).attr('x2',iW);

  // tick marks
  const ticks = xScale.ticks(6);
  g.selectAll('.tl-tick').data(ticks).join('line')
    .attr('x1', d=>xScale(d)).attr('x2', d=>xScale(d))
    .attr('y1',-6).attr('y2',6)
    .attr('stroke','rgba(255,255,255,.2)').attr('stroke-width',1);
  g.selectAll('.tl-tick-lbl').data(ticks).join('text')
    .attr('x', d=>xScale(d)).attr('y', 20)
    .attr('text-anchor','middle').attr('class','tl-date')
    .text(d => d3.timeFormat('%b %Y')(d));

  // events — alternate above/below
  events.forEach((ev, i) => {{
    const x = xScale(new Date(ev.date));
    const above = i % 2 === 0;
    const color = TYPE_COLOR[ev.type] || TYPE_COLOR.other;
    const yOff  = above ? -60 - (i % 3)*20 : 60 + (i % 3)*20;

    // stem
    g.append('line')
      .attr('x1',x).attr('x2',x).attr('y1',0).attr('y2', yOff)
      .attr('stroke', color).attr('stroke-width',1).attr('stroke-opacity',.5)
      .attr('stroke-dasharray','2,3');

    // dot (animated entry)
    const circle = g.append('circle').attr('class','tl-node')
      .attr('cx',x).attr('cy',yOff).attr('r',0)
      .attr('fill',color).attr('fill-opacity',.9)
      .on('mouseover', ev2 => showTip(ev2, ev.label + ' (' + ev.date + ')'))
      .on('mousemove', moveTip).on('mouseout', hideTip);

    circle.transition().delay(i*60).duration(400).ease(d3.easeBackOut).attr('r',7);

    // label
    g.append('text').attr('class','tl-label')
      .attr('x', x).attr('y', yOff + (above ? -12 : 16))
      .attr('text-anchor','middle')
      .attr('font-size',10).attr('fill',color)
      .text(ev.label.length > 20 ? ev.label.slice(0,18)+'…' : ev.label)
      .attr('opacity',0)
      .transition().delay(i*60+200).duration(300).attr('opacity',1);
  }});
}}

// ─────────────────────────────────────────────
// SANKEY (FLOW) VIEW
// ─────────────────────────────────────────────
function drawSankey() {{
  const el = document.getElementById('svg-layer');
  el.innerHTML = '';
  cancelAnimationFrame(animFrame);
  pctx.clearRect(0, 0, pcanvas.width, pcanvas.height);

  if (!RAW_FLOWS.length) {{
    d3.select('#svg-layer').append('text')
      .attr('x','50%').attr('y','50%').attr('text-anchor','middle')
      .attr('fill','#8899aa').attr('font-size',14)
      .text('No flow data in this dataset.');
    return;
  }}

  const W = el.clientWidth, H = el.clientHeight;
  const pad = {{left:140,right:140,top:40,bottom:40}};
  const svg = d3.select('#svg-layer');
  const g   = svg.append('g').attr('transform',`translate(${{pad.left}},${{pad.top}})`);
  const iW  = W - pad.left - pad.right;
  const iH  = H - pad.top  - pad.bottom;

  // build unique node list from flows
  const names = [...new Set(RAW_FLOWS.flatMap(f => [f.source, f.target]))];
  const nodeMap = Object.fromEntries(names.map((n,i) => [n, i]));
  const skNodes = names.map(n => ({{ name:n }}));
  const skLinks = RAW_FLOWS.map(f => ({{
    source: nodeMap[f.source],
    target: nodeMap[f.target],
    value:  f.value || 1,
    label:  f.label || ''
  }}));

  const sankey = d3.sankey()
    .nodeWidth(18).nodePadding(12)
    .extent([[0,0],[iW,iH]]);
  const {{nodes:sNodes, links:sLinks}} = sankey({{nodes:skNodes, links:skLinks}});

  // color links
  const linkColors = d3.schemeTableau10;

  // draw links
  const link = g.append('g').selectAll('.sk-link').data(sLinks).join('path')
    .attr('class','sk-link')
    .attr('d', d3.sankeyLinkHorizontal())
    .attr('stroke', (d,i) => linkColors[i % linkColors.length])
    .attr('stroke-width', d => Math.max(1, d.width))
    .on('mouseover', (ev,d) => showTip(ev, (d.label||d.source.name+'→'+d.target.name)+' ('+d.value+')'))
    .on('mousemove', moveTip).on('mouseout', hideTip);

  // animated dash offset to show flow direction
  link.each(function(d) {{
    const len = this.getTotalLength ? this.getTotalLength() : 200;
    d3.select(this)
      .attr('stroke-dasharray', len/3 + ' ' + len)
      .attr('stroke-dashoffset', len)
      .transition().duration(2000).ease(d3.easeLinear)
      .attr('stroke-dashoffset', -len)
      .on('end', function() {{ d3.select(this).attr('stroke-dasharray',null); }});
  }});

  // draw nodes
  const nodeG = g.append('g').selectAll('.sk-node').data(sNodes).join('g')
    .attr('class','sk-node')
    .attr('transform', d => `translate(${{d.x0}},${{d.y0}})`);

  nodeG.append('rect')
    .attr('height', d => d.y1 - d.y0)
    .attr('width',  d => d.x1 - d.x0)
    .attr('rx',4)
    .attr('fill', (d,i) => linkColors[i % linkColors.length])
    .attr('fill-opacity',.85);

  nodeG.append('text')
    .attr('x', d => d.x0 < iW/2 ? (d.x1-d.x0)+8 : -8)
    .attr('y', d => (d.y1-d.y0)/2)
    .attr('text-anchor', d => d.x0 < iW/2 ? 'start' : 'end')
    .attr('dominant-baseline','middle')
    .attr('fill','#cdd3e8').attr('font-size',11)
    .text(d => d.name);
}}

// ─────────────────────────────────────────────
// NODE SELECTION (detail panel)
// ─────────────────────────────────────────────
function selectNode(d, links) {{
  document.getElementById('detail-name').textContent = d.label;
  document.getElementById('detail-name').style.color = d.color;
  document.getElementById('detail-type').textContent = d.type.toUpperCase();
  const conns = links.filter(l =>
    (l.source.id||l.source) === d.id || (l.target.id||l.target) === d.id);
  document.getElementById('detail-connections').textContent =
    conns.length + ' connection' + (conns.length!==1?'s':'') + ': ' +
    conns.map(l => (l.source.id===d.id ? '→'+l.target.label : l.source.label+'→')).join(', ');
}}

// ─────────────────────────────────────────────
// TOOLTIP
// ─────────────────────────────────────────────
const tip = document.getElementById('tip');
function showTip(ev, text) {{ tip.textContent=text; tip.style.display='block'; }}
function moveTip(ev) {{ tip.style.left=(ev.clientX+14)+'px'; tip.style.top=(ev.clientY+14)+'px'; }}
function hideTip()  {{ tip.style.display='none'; }}

// ─────────────────────────────────────────────
// TAB SWITCHING
// ─────────────────────────────────────────────
let currentTab = 'graph';
function switchTab(name) {{
  currentTab = name;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');
  cancelAnimationFrame(animFrame);
  if (name === 'graph')    drawGraph();
  if (name === 'timeline') drawTimeline();
  if (name === 'sankey')   drawSankey();
}}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────
window.addEventListener('resize', () => {{
  resizeParticleCanvas();
  if (currentTab === 'graph') drawGraph();
  else if (currentTab === 'timeline') drawTimeline();
  else drawSankey();
}});

initComplexity();
drawGraph();
</script>
</body>
</html>"""
