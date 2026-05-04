# ⚖️ The Fiel Contraste Engine

A **gamified, business-centric art history route** through Madrid & Segovia focused on the _Branding of Trust_ and _Market Neutrality_.

Built with **Streamlit** — mobile-first, bilingual (EN/ES), with an interactive map, 3D flip cards, past-vs-present image sliders, and a badge/gamification system.

---

## Features

| Feature | Implementation |
|---|---|
| Interactive Route Map | `streamlit-folium` + Folium markers & polyline |
| 3D Coin Flip Cards | Custom CSS (`perspective`, `rotateY`, touch-enabled) |
| Past vs. Present Slider | `streamlit-image-comparison` |
| EN / ES Toggle | Full bilingual content dictionary |
| Personalisation Filter | Business / Marketing / Psychology insight boxes |
| Badge Gamification | Per-stop check-in unlocks badges, tracked in session state |
| Final Conclusion Page | Summary table + professor bottom-line narrative |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Generate placeholder images
python3 generate_placeholders.py

# 3. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Replacing Placeholder Images

Drop your real photos into `assets/` using these filenames:

| File | Contents |
|---|---|
| `assets/stop1_past.jpg` | Segovia — historical photo |
| `assets/stop1_present.jpg` | Segovia — modern photo |
| `assets/stop1_coin_front.png` | Coin obverse image |
| `assets/stop1_coin_back.png` | Coin reverse image |
| _(repeat for stop2–stop6)_ | |

---

## The Six Stops

| # | Location | Business Lesson |
|---|---|---|
| 1 | Segovia — Real Ingenio | The Industrialization of Trust |
| 2 | FNMT Mint Museum | The PR Crisis & Subversion |
| 3 | Anthropology Museum | Hostile Market Entry |
| 4 | Puerta del Sol (Euro) | Neutrality Branding |
| 5 | Banco de España | The Transition CEO |
| 6 | Plaza Mayor | Market Compliance |

---

## Project Structure

```
.
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── generate_placeholders.py  # Script to generate placeholder images
├── assets/                   # Images (drop real photos here)
│   ├── stop1_past.jpg
│   ├── stop1_present.jpg
│   ├── stop1_coin_front.png
│   ├── stop1_coin_back.png
│   └── ... (stop2–stop6)
└── README.md
```

---

## Aesthetic

- **Primary:** Deep Teal `#004d40`
- **Accent:** Gold `#d4af37`
- **Background:** Off-White `#f5f5f0`
- Font: Georgia (serif) for a premium editorial feel
