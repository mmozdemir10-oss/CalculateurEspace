import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide", page_title="Simulateur Metrique")

st.title("🧩 Simulateur de rangement avec alignement")
st.write("Ajustez le conteneur, ajoutez vos blocs, puis glissez-les dedans.")

if "pieces" not in st.session_state:
    st.session_state.pieces = []

ECHELLE = 1.5

st.sidebar.header("1. Le Rectangle Principal")
bg_m = st.sidebar.number_input("Longueur du rectangle (m)", min_value=0, max_value=10, value=4, step=1)
bg_cm = st.sidebar.number_input("Longueur du rectangle (cm)", min_value=0, max_value=99, value=0, step=5)

bh_m = st.sidebar.number_input("Largeur du rectangle (m)", min_value=0, max_value=10, value=2, step=1)
bh_cm = st.sidebar.number_input("Largeur du rectangle (cm)", min_value=0, max_value=99, value=50, step=5)

grand_largeur_cm = (bg_m * 100) + bg_cm
grand_hauteur_cm = (bh_m * 100) + bh_cm

grand_largeur_px = grand_largeur_cm * ECHELLE
grand_hauteur_px = grand_hauteur_cm * ECHELLE

st.sidebar.markdown("---")
st.sidebar.header("Options d'alignement")
pas_grille_cm = st.sidebar.selectbox(
    "Aimanter les blocs tous les :",
    options=[0, 1, 2, 5, 10, 20],
    index=3,
    format_func=lambda x: "Pas d'aimantage (libre)" if x == 0 else f"{x} cm"
)
pas_grille_px = pas_grille_cm * ECHELLE

st.sidebar.markdown("---")
st.sidebar.header("2. Ajouter des blocs")

p_long_m = st.sidebar.number_input("Longueur du bloc (m)", min_value=0, max_value=10, value=1, step=1)
p_long_cm = st.sidebar.number_input("Longueur du bloc (cm)", min_value=0, max_value=99, value=20, step=5)

p_larg_m = st.sidebar.number_input("Largeur du bloc (m)", min_value=0, max_value=10, value=0, step=1)
p_larg_cm = st.sidebar.number_input("Largeur du bloc (cm)", min_value=0, max_value=99, value=80, step=5)

p_nombre = st.sidebar.number_input("Nombre de blocs", min_value=1, max_value=20, value=1)

if st.sidebar.button("Ajouter les blocs"):
    f_longueur_cm = (p_long_m * 100) + p_long_cm
    f_largeur_cm = (p_larg_m * 100) + p_larg_cm
    
    txt_long = f"{p_long_m}m" if p_long_m > 0 else ""
    txt_long += f"{p_long_cm}cm" if p_long_cm > 0 or p_long_m == 0 else ""
    
    txt_larg = f"{p_larg_m}m" if p_larg_m > 0 else ""
    txt_larg += f"{p_larg_cm}cm" if p_larg_cm > 0 or p_larg_m == 0 else ""
    
    label_metrique = f"{txt_long} x {txt_larg}"
    
    couleurs = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#33FFF3", "#9333FF", "#FF33A8"]
    couleur = couleurs[len(st.session_state.pieces) % len(couleurs)]
    
    for i in range(p_nombre):
        st.session_state.pieces.append({
            "id": f"piece_{len(st.session_state.pieces)}",
            "w": f_longueur_cm * ECHELLE,
            "h": f_largeur_cm * ECHELLE,
            "color": couleur,
            "label": label_metrique
        })
    st.rerun()

st.sidebar.markdown("---")
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("Reset"): st.rerun()
with col_btn2:
    if st.button("Effacer tout"):
        st.session_state.pieces = []
        st.rerun()

pieces_json = json.dumps(st.session_state.pieces)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; user-select: none; background-color: #f9f9f9; margin: 0; padding: 10px; }}
    .container {{ display: flex; flex-direction: column; gap: 20px; }}
    #zone-depot {{
        width: {grand_largeur_px}px;
        height: {grand_hauteur_px}px;
        background-color: #e0e0e0;
        border: 3px dashed #444;
        border-radius: 4px;
        position: relative;
        background-image: {f'linear-gradient(to right, #ccc 1px, transparent 1px), linear-gradient(to bottom, #ccc 1px, transparent 1px)' if pas_grille_px > 0 else 'none'};
        background-size: {pas_grille_px}px {pas_grille_px}px;
    }}
    #zone-depot::before {{
        content: "Rectangle : {bg_m}m {bg_cm}cm x {bh_m}m {bh_cm}cm";
        position: absolute; top: -25px; left: 5px; color: #444; font-weight: bold; font-size: 14px;
    }}
    #zone-stockage {{
        min-height: 150px; border: 2px solid #ccc; background-color: #fff; border-radius: 8px;
        padding: 15px; display: flex; flex-wrap: wrap; gap: 10px; align-content: flex-start; margin-top: 10px;
    }}
    .piece {{
        display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;
        font-size: 11px; border-radius: 2px; cursor: move; box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7); text-align: center; overflow: hidden; box-sizing: border-box;
    }}
</style>
</head>
<body>

<div class="container">
    <div style="margin-top:25px;"><div id="zone-depot"></div></div>
    <h3>Pieces disponibles (Glissez-les vers le haut) :</h3>
    <div id="zone-stockage"></div>
</div>

<script>
    const piecesData = {pieces_json};
    const pasGrille = {pas_grille_px};
    const zoneStockage = document.getElementById('zone-stockage');
    const zoneDepot = document.getElementById('zone-depot');

    piecesData.forEach(p => {{
        const el = document.createElement('div');
        el.id = p.id;
        el.className = 'piece';
        el.style.width = p.w + 'px';
        el.style.height = p.h + 'px';
        el.style.backgroundColor = p.color;
        el.innerText = p.label;
        el.style.position = 'relative';
        
        el.addEventListener('mousedown', function(e) {{
            e.preventDefault();
            if (el.parentElement !== document.body) {{
                const rect = el.getBoundingClientRect();
                el.style.position = 'absolute';
                el.style.left = rect.left + window.scrollX + 'px';
                el.style.top = rect.top + window.scrollY + 'px';
                document.body.appendChild(el);
            }}

            let shiftX = e.clientX - el.getBoundingClientRect().left;
            let shiftY = e.clientY - el.getBoundingClientRect().top;

            function moveAt(clientX, clientY) {{
                el.style.left = (clientX - shiftX + window.scrollX) + 'px';
                el.style.top = (clientY - shiftY + window.scrollY) + 'px';
            }}

            function onMouseMove(e) {{ moveAt(e.clientX, e.clientY); }}
            document.addEventListener('mousemove', onMouseMove);

            document.onmouseup = function() {{
                document.removeEventListener('mousemove', onMouseMove);
                const rectDepot = zoneDepot.getBoundingClientRect();
                const rectPiece = el.getBoundingClientRect();

                if (rectPiece.left >= rectDepot.left - 30 && rectPiece.right <= rectDepot.right + 30 &&
                    rectPiece.top >= rectDepot.top - 30 && rectPiece.bottom <= rectDepot.bottom + 30) {{
                    
                    zoneDepot.appendChild(el);
                    let localX = rectPiece.left - rectDepot.left;
                    let localY = rectPiece.top - rectDepot.top;
                    
                    if (pasGrille > 0) {{
                        localX = Math.round(localX / pasGrille) * pasGrille;
                        localY = Math.round(localY / pasGrille) * pasGrille;
                    }}
                    
                    if (localX < 0) localX = 0;
                    if (localY < 0) localY = 0;
                    if (localX + p.w > rectDepot.width) localX = Math.floor((rectDepot.width - p.w) / (pasGrille || 1)) * (pasGrille || 1);
                    if (localY + p.h > rectDepot.height) localY = Math.floor((rectDepot.height - p.h) / (pasGrille || 1)) * (pasGrille || 1);

                    el.style.left = localX + 'px';
                    el.style.top = localY + 'px';
                }} else {{
                    el.style.position = 'relative'; el.style.left = 'auto'; el.style.top = 'auto';
                    zoneStockage.appendChild(el);
                }}
                document.onmouseup = null;
            }};
        }});
        zoneStockage.appendChild(el);
    }});
</script>
</body>
</html>
"""

hauteur_composant = max(600, int(grand_hauteur_px) + 300)
components.html(html_code, height=hauteur_composant, scrolling=True)


