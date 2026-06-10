import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide", page_title="Simulateur de Rangement Pro")

st.title("🧩 Simulateur de rangement sur mesure")
st.write("Configurez vos dimensions dans les zones colorées ci-dessous, générez vos blocs, puis glissez-les dans le rectangle.")

# --- INITIALISATION DE L'ÉTAT ---
if "pieces" not in st.session_state:
    st.session_state.pieces = []

# --- ZONE SUPÉRIEURE : CONFIGURATION VISUELLE ET ORGANISÉE ---
col_rect, col_blocs, col_boutons = st.columns([2.3, 2.3, 1])

# 🟦 SECTION 1 : RECTANGLE PRINCIPAL (Cadre Bleu)
with col_rect:
    bg_m = st.number_input("Longueur du rectangle (m)", min_value=0, max_value=30, value=15, step=1, key="bg_m")
    bg_cm = st.number_input("Longueur du rectangle (cm)", min_value=0, max_value=99, value=0, step=5, key="bg_cm")
    bh_m = st.number_input("Largeur du rectangle (m)", min_value=0, max_value=30, value=5, step=1, key="bh_m")
    bh_cm = st.number_input("Largeur du rectangle (cm)", min_value=0, max_value=99, value=0, step=5, key="bh_cm")

    grand_largeur_cm = (bg_m * 100) + bg_cm
    grand_hauteur_cm = (bh_m * 100) + bh_cm

    # --- CALCUL DYNAMIQUE DE L'ÉCHELLE POUR PRENDRE TOUTE LA PLACE ---
    # Le rectangle fera environ 950px de large à l'écran qu'il fasse 5m ou 15m
    if grand_largeur_cm > 0:
        ECHELLE = 950 / grand_largeur_cm
    else:
        ECHELLE = 1.0

    grand_largeur_px = grand_largeur_cm * ECHELLE
    grand_hauteur_px = grand_hauteur_cm * ECHELLE

    st.markdown(
        f"""
        <div style="background-color: #e0f2fe; padding: 12px; border-radius: 8px; border-left: 6px solid #0284c7; margin-top: 10px;">
            <span style="color: #0369a1; font-weight: bold; font-size: 15px;">🟦 RECTANGLE : {bg_m}m {bg_cm:02d}cm × {bh_m}m {bh_cm:02d}cm</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

# 🟧 SECTION 2 : DIMENSIONS DES BLOCS (Cadre Orange)
with col_blocs:
    p_long_m = st.number_input("Longueur bloc (m)", min_value=0, max_value=30, value=1, step=1)
    p_long_cm = st.number_input("Longueur bloc (cm)", min_value=0, max_value=99, value=20, step=5)
    p_larg_m = st.number_input("Largeur bloc (m)", min_value=0, max_value=30, value=0, step=1)
    p_larg_cm = st.number_input("Largeur bloc (cm)", min_value=0, max_value=99, value=80, step=5)
    
    txt_long = f"{p_long_m}m" if p_long_m > 0 else ""
    txt_long += f"{p_long_cm}cm" if p_long_cm > 0 or p_long_m == 0 else ""
    
    txt_larg = f"{p_larg_m}m" if p_larg_m > 0 else ""
    txt_larg += f"{p_larg_cm}cm" if p_larg_cm > 0 or p_larg_m == 0 else ""
    
    label_metrique = f"{txt_long} x {txt_larg}"

    st.markdown(
        f"""
        <div style="background-color: #ffedd5; padding: 12px; border-radius: 8px; border-left: 6px solid #ea580c; margin-top: 10px;">
            <span style="color: #c2410c; font-weight: bold; font-size: 15px;">🟧 BLOC SÉLECTIONNÉ : {label_metrique}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    sub_col_opt1, sub_col_opt2 = st.columns(2)
    with sub_col_opt1:
        p_nombre = st.number_input("Nombre de blocs", min_value=1, max_value=50, value=1)
    with sub_col_opt2:
        pas_grille_cm = st.selectbox("Aimantage", options=[0, 1, 5, 10, 20, 50], index=2, format_func=lambda x: "Libre" if x == 0 else f"{x} cm")
        pas_grille_px = pas_grille_cm * ECHELLE

# ⚡ SECTION 3 : LES BOUTONS
with col_boutons:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True) 
    btn_ajouter = st.button("➕ Ajouter les blocs", use_container_width=True, type="primary")
    btn_reset = st.button("🔄 Reset positions", use_container_width=True)
    btn_effacer = st.button("🗑️ Tout effacer", use_container_width=True)


# --- LOGIQUE DE GESTION DES BOUTONS ---
if btn_ajouter:
    f_longueur_cm = (p_long_m * 100) + p_long_cm
    f_largeur_cm = (p_larg_m * 100) + p_larg_cm
    
    couleurs = ["#FF5733", "#22c55e", "#3b82f6", "#eab308", "#a855f7", "#ec4899", "#14b8a6"]
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

if btn_effacer:
    st.session_state.pieces = []
    st.rerun()


# --- INTERFACE DE GLISSER-DÉPOSER AUTOMATIQUE ---
pieces_json = json.dumps(st.session_state.pieces)
reset_trigger = "true" if btn_reset else "false"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; user-select: none; background-color: #f9f9f9; margin: 0; padding: 10px; }}
    .container {{ display: flex; flex-direction: column; gap: 20px; }}
    
    #zone-stockage {{
        min-height: 120px; border: 2px solid #cbd5e1; background-color: #fff; border-radius: 8px;
        padding: 15px; display: flex; flex-wrap: wrap; gap: 10px; align-content: flex-start;
    }}
    
    #zone-depot {{
        width: {grand_largeur_px}px;
        height: {grand_hauteur_px}px;
        background-color: #e2e8f0;
        border: 3px dashed #475569;
        border-radius: 6px;
        position: relative;
        background-image: {f'linear-gradient(to right, #cbd5e1 1px, transparent 1px), linear-gradient(to bottom, #cbd5e1 1px, transparent 1px)' if pas_grille_px > 0 else 'none'};
        background-size: {pas_grille_px}px {pas_grille_px}px;
        margin-top: 5px;
    }}
    
    .piece {{
        display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;
        font-size: 11px; border-radius: 3px; cursor: move; box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7); text-align: center; overflow: hidden; box-sizing: border-box;
    }}
</style>
</head>
<body>

<div class="container">
    <div>
        <h4 style="margin: 0 0 8px 0; color: #475569;">📦 Poche / Réserve de vos blocs :</h4>
        <div id="zone-stockage"></div>
    </div>
    
    <div>
        <h4 style="margin: 0 0 8px 0; color: #475569;">📐 Rectangle Principal ({bg_m}m {bg_cm}cm × {bh_m}m {bh_cm}cm) :</h4>
        <div id="zone-depot"></div>
    </div>
</div>

<script>
    const piecesData = {pieces_json};
    const pasGrille = {pas_grille_px};
    const forceReset = {reset_trigger};
    
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
        
        // Si forceReset est vrai, l'élément est remis à sa position initiale dans le stock
        el.style.position = 'relative';
        el.style.left = 'auto';
        el.style.top = 'auto';
        
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

                if (rectPiece.left >= rectDepot.left - 40 && rectPiece.right <= rectDepot.right + 40 &&
                    rectPiece.top >= rectDepot.top - 40 && rectPiece.bottom <= rectDepot.bottom + 40) {{
                    
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

# Hauteur dynamique basée sur la taille réelle calculée du rectangle principal
hauteur_composant = max(600, int(grand_hauteur_px) + 280)
components.html(html_code, height=hauteur_composant, scrolling=True)

