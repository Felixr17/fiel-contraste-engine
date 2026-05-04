"""Reusable UI pieces: map, flip cards, comparison slider, personalization."""

from __future__ import annotations

import html
from pathlib import Path

import folium
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

from fiel_contraste.stops import STOPS


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def images_exist(past: str, present: str) -> bool:
    root = project_root()
    return (root / past).is_file() and (root / present).is_file()


def render_route_map(lang: dict) -> None:
    """Interactive Folium map centered on Madrid with Segovia visible."""
    center_lat = 40.55
    center_lon = -3.85
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles="CartoDB positron")
    for stop in STOPS:
        folium.Marker(
            [stop["lat"], stop["lon"]],
            popup=lang[stop["map_label_key"]],
            tooltip=lang[stop["map_label_key"]],
            icon=folium.Icon(color="darkgreen", icon="info-sign"),
        ).add_to(m)
    # Fit bounds roughly
    sw = [40.35, -4.25]
    ne = [41.05, -3.65]
    m.fit_bounds([sw, ne], padding=(24, 24))
    st_folium(m, width=None, height=380, returned_objects=[])


def render_route_map_plotly(lang: dict) -> None:
    """Scatter map — Plotly mapbox for zoom/pan alongside Folium."""
    lats = [s["lat"] for s in STOPS]
    lons = [s["lon"] for s in STOPS]
    labels = [lang[s["map_label_key"]] for s in STOPS]
    fig = go.Figure(
        go.Scattermap(
            lat=lats,
            lon=lons,
            mode="markers+text",
            text=labels,
            textposition="top center",
            marker=dict(size=14, color="#004d40", symbol="circle"),
        )
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=32, b=0),
        height=400,
        paper_bgcolor="#f7f5ef",
        plot_bgcolor="#f7f5ef",
        title=dict(text=lang["map_title"], font=dict(color="#004d40", size=16)),
    )
    fig.update_mapboxes(center=dict(lat=40.52, lon=-3.9), zoom=7.2)
    st.plotly_chart(fig, use_container_width=True)


def render_flip_card(
    stop_index: int,
    stop_id: str,
    lang: dict,
    keys: dict,
) -> None:
    """3D flip using checkbox + CSS (touch-friendly)."""
    uid = f"flip-{stop_id}"
    front_t = html.escape(lang[keys["front_title"]])
    back_t = html.escape(lang[keys["back_title"]])
    front_b = html.escape(lang[keys["front_body"]])
    back_b = html.escape(lang[keys["back_body"]])
    hint = html.escape(lang["flip_tap"])

    flip_markup = f"""
<div class="flip-scene">
  <input type="checkbox" id="{uid}" class="flip-toggle" aria-label="{hint}">
  <label for="{uid}" class="flip-label">
    <div class="flip-card-inner">
      <div class="flip-card-front">
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:rgba(212,175,55,0.95);margin-bottom:0.35rem;">{front_t}</div>
        <div style="font-size:1rem;line-height:1.45;font-weight:600;">{front_b}</div>
        <div class="flip-hint">{hint}</div>
      </div>
      <div class="flip-card-back">
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#004d40;margin-bottom:0.35rem;">{back_t}</div>
        <div style="font-size:0.92rem;line-height:1.5;">{back_b}</div>
        <div class="flip-hint">{hint}</div>
      </div>
    </div>
  </label>
</div>
"""
    st.markdown(flip_markup, unsafe_allow_html=True)


def render_image_comparison(
    past_path: str,
    present_path: str,
    lang: dict,
) -> None:
    from streamlit_image_comparison import image_comparison

    if images_exist(past_path, present_path):
        root = project_root()
        image_comparison(
            img1=str(root / past_path),
            img2=str(root / present_path),
            label1=lang["compare_past"],
            label2=lang["compare_present"],
            width=700,
            starting_position=50,
            show_labels=True,
            make_responsive=True,
        )
    else:
        st.info(lang["compare_placeholder"])
        st.caption(f"`{past_path}` · `{present_path}`")


def personalization_box(major: str, lang: dict, stop_idx: int) -> None:
    """Marketing → Brand Strategy; Business → Scaling Logic; Psychology → Trust Psychology."""
    idx = stop_idx + 1
    if major == "Marketing":
        key = f"brand_{idx}"
        title = html.escape(lang["personalization_brand"])
    elif major == "Business":
        key = f"scale_{idx}"
        title = html.escape(lang["personalization_scale"])
    else:
        key = f"psych_{idx}"
        title = html.escape(lang["personalization_psych"])
    body = html.escape(lang[key])
    st.markdown(
        f'<div class="fc-card"><strong style="color:#004d40;">{title}</strong><br/><span style="color:#333;line-height:1.55;">{body}</span></div>',
        unsafe_allow_html=True,
    )


def stops_dataframe(lang: dict) -> pd.DataFrame:
    rows = []
    for s in STOPS:
        rows.append(
            {
                "Stop": lang[s["name_key"]],
                "Lat": s["lat"],
                "Lon": s["lon"],
            }
        )
    return pd.DataFrame(rows)
