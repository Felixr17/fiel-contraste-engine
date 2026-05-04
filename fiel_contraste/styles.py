"""Premium FinTech theme + 3D flip cards (mobile touch-friendly)."""

THEME_CSS = """
<style>
/* --- Premium FinTech palette --- */
:root {
    --teal-deep: #004d40;
    --gold: #d4af37;
    --off-white: #f7f5ef;
    --teal-mid: #00695c;
    --text-on-teal: #f7f5ef;
    --shadow: rgba(0, 77, 64, 0.18);
}

/* Streamlit chrome */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, var(--off-white) 0%, #e8e4dc 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #00352c 0%, var(--teal-deep) 100%) !important;
}
[data-testid="stSidebar"] * {
    color: var(--off-white) !important;
}
.stRadio label, .stSelectbox label {
    font-weight: 600 !important;
}
h1, h2, h3 {
    color: var(--teal-deep) !important;
    letter-spacing: -0.02em;
}
.gold-accent {
    color: var(--gold) !important;
}
.fc-card {
    background: #fff;
    border-radius: 16px;
    border: 1px solid rgba(212, 175, 55, 0.35);
    box-shadow: 0 8px 32px var(--shadow);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.fc-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
}
.fc-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #c9a227);
    color: var(--teal-deep);
    font-weight: 700;
    font-size: 0.75rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* --- 3D flip card (checkbox toggle — works on mobile tap) --- */
.flip-scene {
    perspective: 1200px;
    width: 100%;
    max-width: 420px;
    margin: 0 auto 1rem auto;
}
.flip-card {
    position: relative;
    width: 100%;
    min-height: 220px;
}
.flip-toggle {
    position: absolute;
    width: 1px;
    height: 1px;
    opacity: 0;
    pointer-events: none;
}
.flip-label {
    display: block;
    cursor: pointer;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
}
.flip-card-inner {
    position: relative;
    width: 100%;
    min-height: 220px;
    transition: transform 0.65s cubic-bezier(0.4, 0.2, 0.2, 1);
    transform-style: preserve-3d;
    border-radius: 14px;
    box-shadow: 0 12px 40px var(--shadow);
}
.flip-toggle:focus-visible + .flip-label .flip-card-inner {
    outline: 2px solid var(--gold);
    outline-offset: 4px;
}
.flip-toggle:checked + .flip-label .flip-card-inner {
    transform: rotateY(180deg);
}
.flip-card-front,
.flip-card-back {
    position: absolute;
    width: 100%;
    min-height: 220px;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 14px;
    padding: 1.25rem 1.35rem;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.flip-card-front {
    background: linear-gradient(145deg, var(--teal-deep), var(--teal-mid));
    color: var(--text-on-teal);
    border: 1px solid rgba(212, 175, 55, 0.45);
}
.flip-card-back {
    background: linear-gradient(145deg, #fffef9, var(--off-white));
    color: #1a1a1a;
    transform: rotateY(180deg);
    border: 1px solid rgba(0, 77, 64, 0.2);
}
.flip-hint {
    font-size: 0.72rem;
    opacity: 0.85;
    margin-top: 0.75rem;
    text-align: center;
    color: rgba(247, 245, 239, 0.9);
}
.flip-card-back .flip-hint {
    color: var(--teal-deep);
    opacity: 0.8;
}
@media (max-width: 480px) {
    .flip-card-front, .flip-card-back {
        min-height: 260px;
        padding: 1rem 1.1rem;
    }
}
</style>
"""


def inject_theme():
    import streamlit as st

    st.markdown(THEME_CSS, unsafe_allow_html=True)
