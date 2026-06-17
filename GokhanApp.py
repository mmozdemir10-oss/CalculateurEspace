import streamlit as st
import streamlit.components.v1 as components
import json
from math import floor

st.set_page_config(
    page_title="Cargo loader",
    page_icon="⏬️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 🎨 THEME PREMIUM GLOBAL
# =========================
st.markdown("""
<style>
:root{
    --bg:#f8fafc;
    --card:#ffffff;
    --border:#e2e8f0;
    --primary:#2563eb;
    --primary-light:#dbeafe;
    --text:#0f172a;
    --muted:#64748b;
}

/* fond général */
.stApp{
    background:var(--bg);
}

/* conteneur principal */
.block-container{
    padding-top:1rem;
    max-width:1600px;
}

/* boutons */
.stButton button{
    border-radius:12px;
    height:48px;
    font-weight:600;
    border:none;
    transition:0.2s;
}

.stButton button:hover{
    transform:translateY(-2px);
}

/* cartes */
.card{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid var(--border);
    box-shadow:0 4px 15px rgba(0,0,0,0.05);
}

/* titres internes */
.small-label{
    font-size:13px;
    color:var(--muted);
    font-weight:600;
}

.big-value{
    font-size:22px;
    font-weight:700;
    color:var(--text);
}
</style>
""", unsafe_allow_html=True)

# =========================
# 📦 SESSION STATE
# =========================
if "pieces" not in st.session_state:
    st.session_state.pieces = []

if "surface_occupee" not in st.session_state:
    st.session_state.surface_occupee = 0

st.markdown("""
<div style="
background:linear-gradient(135deg,#2563eb,#0ea5e9);
padding:28px;
border-radius:20px;
color:white;
margin-bottom:20px;
box-shadow:0 10px 25px rgba(37,99,235,.25);
">
<h1 style="margin:0;font-size:32px;">
⏬️ Cargo loader
</h1>
</div>
""", unsafe_allow_html=True)
    
col_rect, col_blocs, col_stats, col_actions = st.columns([2.2, 2.2, 1.4, 1])
    
with col_rect:
    bg_mm = st.number_input(
        "Length of the truck (mm)",
        min_value=0,
        max_value=30000,
        value=15000,
        step=100
    )

    bh_mm = st.number_input(
        "Width of the truck (mm)",
        min_value=0,
        max_value=30000,
        value=5000,
        step=100
    )

    grand_largeur_mm = bg_mm
    grand_hauteur_mm = bh_mm

    ECHELLE = 950 / grand_largeur_mm if grand_largeur_mm > 0 else 1

grand_largeur_px = grand_largeur_mm * ECHELLE
grand_hauteur_px = grand_hauteur_mm * ECHELLE

st.markdown(f"""
    <div class="card">
        <div class="small-label">🚛 TRUCK</div>
        <div class="big-value">{bg_mm} mm × {bh_mm} mm</div>
    </div>
    """, unsafe_allow_html=True)

with col_blocs:
    p_long_mm = st.number_input(
        "Block length (mm)",
        min_value=1,
        max_value=30000,
        value=1200,
        step=50
    )

    p_larg_mm = st.number_input(
        "Block width (mm)",
        min_value=1,
        max_value=30000,
        value=800,
        step=50
    )

label_metrique = f"{p_long_mm} × {p_larg_mm} mm"

st.markdown(f"""
    <div class="card">
        <div class="small-label">📦 SELECTED BLOCK</div>
        <div class="big-value">{label_metrique}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

p_nombre = st.number_input("Number of blocks", min_value=1, max_value=50, value=1)

with col_stats:
    surface_totale = round((grand_largeur_mm * grand_hauteur_mm) / 1_000_000, 2)

    html_stats = f"""
    <div class="card">
        <div class="small-label">🚛 TRUCK SURFACE</div>
        <div class="big-value">{surface_totale} m²</div>
        <hr>
        <div class="small-label">📦 BLOCKS</div>
        <div class="big-value">{len(st.session_state.pieces)}</div>
    </div>
    """.replace("\n", "")

    st.markdown(html_stats, unsafe_allow_html=True)

with col_actions:
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
    btn_ajouter = st.button("➕ Add", use_container_width=True, type="primary")
    btn_reset = st.button("🔄 Reset", use_container_width=True)
    btn_effacer = st.button("🗑️ Empty", use_container_width=True)

# LOGIQUE DES BOUTONS
if btn_ajouter:
    f_longueur_mm = p_long_mm
    f_largeur_mm = p_larg_mm

    couleurs = [
        "#2563eb", "#14b8a6", "#f97316",
        "#8b5cf6", "#ef4444", "#0ea5e9", "#22c55e"
    ]
    couleur = couleurs[len(st.session_state.pieces) % len(couleurs)]

    for i in range(p_nombre):
        st.session_state.pieces.append({
            "id": f"piece_{len(st.session_state.pieces)}",
            "w": f_longueur_mm * ECHELLE,
            "h": f_largeur_mm * ECHELLE,
            "color": couleur,
            "label": label_metrique
        })

if btn_effacer or btn_reset:
    st.session_state.pieces = []

# Préparation propre de la variable JSON pour le JavaScript
pieces_json = json.dumps(st.session_state.pieces)

# CONSTRUCTION DE L'IFRAME HTML
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
    font-family: system-ui, sans-serif;
    background:#f8fafc;
    margin:0;
    padding:12px;
    user-select:none;
}}
.container {{
    display:flex;
    flex-direction:column;
    gap:18px;
}}
#zone-stockage {{
    min-height:140px;
    border:2px dashed #cbd5e1;
    background:white;
    border-radius:18px;
    padding:15px;
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    box-shadow:0 4px 15px rgba(0,0,0,0.05);
}}
#zone-depot {{
    width:min(100%, {grand_largeur_px}px);
    height:{grand_hauteur_px}px;
    background:white;
    border:2px dashed #94a3b8;
    border-radius:20px;
    position:relative;
    overflow:hidden;
    box-shadow:0 10px 25px rgba(0,0,0,0.08);
}}
.piece {{
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-weight:700;
    font-size:11px;
    border-radius:10px;
    cursor:grab;
    box-shadow:0 5px 12px rgba(0,0,0,0.2);
    text-shadow:0 1px 2px rgba(0,0,0,0.5);
    transition:transform .12s;
    touch-action:none;
}}
.piece:active {{
    cursor:grabbing;
    transform:scale(1.05);
}}
</style>
</head>
<body>

<div class="container">
    <h3>📦 Cargo</h3>
    <div id="zone-stockage"></div>
    <h3>🚛 Truck</h3>
    <div id="zone-depot"></div>
</div>

<script>
// Injection propre de la variable générée par Python
const pieces = {pieces_json};

function makeDraggable(el, zoneDepot, zoneStock) {{
    let offsetX = 0;
    let offsetY = 0;
    let dragging = false;

    function start(e) {{
        dragging = true;
        const evt = e.touches ? e.touches[0] : e;
        const rect = el.getBoundingClientRect();
        offsetX = evt.clientX - rect.left;
        offsetY = evt.clientY - rect.top;
        document.body.appendChild(el);
        el.style.position = "absolute";
    }}

    function move(e) {{
        if (!dragging) return;
        const evt = e.touches ? e.touches[0] : e;
        el.style.left = (evt.clientX - offsetX) + "px";
        el.style.top = (evt.clientY - offsetY) + "px";
    }}

    function end() {{
        if (!dragging) return;
        dragging = false;

        const depotRect = zoneDepot.getBoundingClientRect();
        const rect = el.getBoundingClientRect();

        const inDepot =
            rect.left > depotRect.left - 50 &&
            rect.right < depotRect.right + 50 &&
            rect.top > depotRect.top - 50 &&
            rect.bottom < depotRect.bottom + 50;

        if (inDepot) {{
            zoneDepot.appendChild(el);
            let x = rect.left - depotRect.left;
            let y = rect.top - depotRect.top;
            el.style.left = x + "px";
            el.style.top = y + "px";
        }} else {{
            zoneStock.appendChild(el);
            el.style.position = "relative";
            el.style.left = "auto";
            el.style.top = "auto";
        }}
    }}

    el.addEventListener("mousedown", start);
    el.addEventListener("touchstart", start, {{passive: true}});
    window.addEventListener("mousemove", move);
    window.addEventListener("touchmove", move, {{passive: false}});
    window.addEventListener("mouseup", end);
    window.addEventListener("touchend", end);
}}

function init() {{
    const zoneStock = document.getElementById("zone-stockage");
    const zoneDepot = document.getElementById("zone-depot");
    
    if (!zoneStock || !zoneDepot) return;

    pieces.forEach(p => {{
        const el = document.createElement("div");
        el.className = "piece";
        el.id = p.id;
        el.style.width = p.w + "px";
        el.style.height = p.h + "px";
        el.style.background = p.color;
        el.innerText = p.label;

        zoneStock.appendChild(el);
        makeDraggable(el, zoneDepot, zoneStock);
    }});
}}

if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", init);
}} else {{
    init();
}}
</script>

</body>
</html>
"""
            
hauteur = max(650, int(grand_hauteur_px) + 250)

components.html(
    html_code,
    height=hauteur,
    scrolling=True
)
