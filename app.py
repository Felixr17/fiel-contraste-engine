"""Streamlit entry: The Fiel Contraste Engine."""

from __future__ import annotations

import streamlit as st

from fiel_contraste.components import (
    personalization_box,
    render_flip_card,
    render_image_comparison,
    render_route_map,
    render_route_map_plotly,
)
from fiel_contraste.styles import inject_theme
from fiel_contraste.stops import STOPS
from fiel_contraste.texts import TEXTS

FLIP_KEYS = [
    {
        "front_title": "flip_front_1",
        "back_title": "flip_back_1",
        "front_body": "flip_body_front_1",
        "back_body": "flip_body_back_1",
    },
    {
        "front_title": "flip_front_2",
        "back_title": "flip_back_2",
        "front_body": "flip_body_front_2",
        "back_body": "flip_body_back_2",
    },
    {
        "front_title": "flip_front_3",
        "back_title": "flip_back_3",
        "front_body": "flip_body_front_3",
        "back_body": "flip_body_back_3",
    },
    {
        "front_title": "flip_front_4",
        "back_title": "flip_back_4",
        "front_body": "flip_body_front_4",
        "back_body": "flip_body_back_4",
    },
    {
        "front_title": "flip_front_5",
        "back_title": "flip_back_5",
        "front_body": "flip_body_front_5",
        "back_body": "flip_body_back_5",
    },
    {
        "front_title": "flip_front_6",
        "back_title": "flip_back_6",
        "front_body": "flip_body_front_6",
        "back_body": "flip_body_back_6",
    },
]


def init_session():
    if "badges" not in st.session_state:
        st.session_state.badges = {s["id"]: False for s in STOPS}
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"
    if "major" not in st.session_state:
        st.session_state.major = "Business"
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "route"


def toggle_language_choice(lang_label: str):
    st.session_state.lang_code = "es" if lang_label.startswith("Español") else "en"


def main():
    st.set_page_config(
        page_title="The Fiel Contraste Engine",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()
    init_session()

    lang_code = st.session_state.lang_code
    L = TEXTS[lang_code]

    with st.sidebar:
        st.markdown(f"### {L['app_title']}")
        lang_choice = st.radio(
            L["sidebar_language"],
            ("English", "Español"),
            index=0 if lang_code == "en" else 1,
            horizontal=True,
        )
        if (lang_code == "en" and lang_choice == "Español") or (
            lang_code == "es" and lang_choice == "English"
        ):
            toggle_language_choice(lang_choice)
            st.rerun()

        major_opts = (L["major_business"], L["major_marketing"], L["major_psychology"])
        major_index_map = {"Business": 0, "Marketing": 1, "Psychology": 2}
        major_label = st.selectbox(
            L["sidebar_major"],
            major_opts,
            index=major_index_map.get(st.session_state.major, 0),
        )
        if major_label == L["major_business"]:
            major_key = "Business"
        elif major_label == L["major_marketing"]:
            major_key = "Marketing"
        else:
            major_key = "Psychology"
        st.session_state.major = major_key

        nav_choice = st.radio(
            L["sidebar_nav"],
            options=[
                ("route", L["nav_route"]),
                ("conclusion", L["nav_conclusion"]),
            ],
            format_func=lambda x: x[1],
            index=0 if st.session_state.nav_page == "route" else 1,
        )
        st.session_state.nav_page = nav_choice[0]
        page = st.session_state.nav_page

        collected = sum(1 for v in st.session_state.badges.values() if v)
        st.markdown(
            f'<p style="margin-top:1rem;font-size:0.9rem;">{L["badges_collected"]}: '
            f'<span class="gold-accent"><strong>{collected}/6</strong></span></p>',
            unsafe_allow_html=True,
        )

    if page == "conclusion":
        render_conclusion(L)
        return

    # --- Route page ---
    st.title(L["app_title"])
    st.caption(L["tagline"])

    st.markdown(f'<div class="fc-card"><p style="margin:0;line-height:1.6;color:#333;">{L["map_hint"]}</p></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        render_route_map(L)
    with col_b:
        render_route_map_plotly(L)

    st.divider()

    for idx, stop in enumerate(STOPS):
        sid = stop["id"]
        st.subheader(f"{idx + 1}. {L[stop['name_key']]}")
        st.markdown(f"#### {L['section_lesson']}: *{L[f'lesson_{idx + 1}']}*")

        personalization_box(major_key, L, idx)

        with st.expander(L["section_academic"], expanded=(idx == 0)):
            st.markdown(L[f"academic_{idx + 1}"])

        st.markdown(f"**{L['section_flip']}**")
        render_flip_card(idx, sid, L, FLIP_KEYS[idx])

        st.markdown(f"**{L['section_compare']}**")
        render_image_comparison(stop["images"]["past"], stop["images"]["present"], L)

        checked = st.session_state.badges[sid]
        if st.button(L["check_in"], key=f"btn-{sid}", disabled=checked):
            st.session_state.badges[sid] = True
            st.success(L["badge_unlocked"])
            st.rerun()

        if st.session_state.badges[sid]:
            st.markdown(
                f'<div class="fc-badge-row"><span class="fc-badge">{L["badge_unlocked"]} · Stop {idx + 1}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption(L["badge_locked"])

        st.divider()


def render_conclusion(L: dict):
    st.title(L["conclusion_title"])
    st.markdown(
        f'<div class="fc-card"><p style="margin:0;line-height:1.65;color:#333;">{L["conclusion_intro"]}</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"### {L['conclusion_bullets_header']}")
    for i in range(1, 7):
        st.markdown(f"- {L[f'cb{i}']}")
    st.markdown(
        f'<div class="fc-card" style="border-left:4px solid #d4af37;"><p style="margin:0;line-height:1.65;"><em>{L["professor_note"]}</em></p></div>',
        unsafe_allow_html=True,
    )

    collected = sum(1 for v in st.session_state.badges.values() if v)
    st.metric(L["badges_collected"], f"{collected} / 6")


if __name__ == "__main__":
    main()
