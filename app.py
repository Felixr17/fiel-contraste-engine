"""
The Fiel Contraste Engine
A gamified, business-centric art history route through Madrid & Segovia.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_image_comparison import image_comparison
import base64, os

# ─────────────────────────────────────────────────────────────────────────────
# ASSET RESOLUTION — probes candidate extensions so any uploaded file format works
# ─────────────────────────────────────────────────────────────────────────────
_PHOTO_EXTS = (".jpeg", ".jpg", ".png", ".webp")
_COIN_EXTS  = (".png", ".jpg", ".jpeg", ".webp")

def resolve_asset(base: str, exts: tuple = _PHOTO_EXTS) -> str | None:
    """Return the first existing path formed by appending each candidate extension
    to *base*, or None if none of them exist."""
    for ext in exts:
        path = base + ext
        if os.path.exists(path):
            return path
    return None

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Fiel Contraste Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS – Premium FinTech Aesthetic + 3D Flip Cards (mobile-first)
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
<style>
/* ── Global palette ───────────────────────────────────────── */
:root {
    --teal:      #004d40;
    --teal-mid:  #00695c;
    --teal-lite: #e0f2f1;
    --gold:      #d4af37;
    --gold-dark: #b8942e;
    --offwhite:  #f5f5f0;
    --text-dark: #1a1a2e;
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Georgia', serif;
    background-color: var(--offwhite);
    color: var(--text-dark);
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--teal) 0%, #002b22 100%);
    color: var(--offwhite);
}
[data-testid="stSidebar"] * { color: var(--offwhite) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: var(--gold) !important; }

/* ── Hero banner ──────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, var(--teal) 0%, var(--teal-mid) 60%, #1b5e20 100%);
    border-radius: 12px;
    padding: 2.5rem 2rem 2rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 2px solid var(--gold);
}
.hero-banner h1 {
    color: var(--gold);
    font-size: clamp(1.6rem, 4vw, 2.8rem);
    letter-spacing: 2px;
    margin: 0 0 0.4rem 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.hero-banner p {
    color: var(--offwhite);
    font-size: clamp(0.85rem, 2vw, 1.05rem);
    margin: 0;
    opacity: 0.9;
}

/* ── Section headers ──────────────────────────────────────── */
.stop-header {
    background: var(--teal);
    border-left: 6px solid var(--gold);
    border-radius: 6px 12px 12px 6px;
    padding: 1rem 1.4rem;
    margin: 1.5rem 0 1rem 0;
}
.stop-header h2 { color: var(--gold); margin: 0 0 0.2rem 0; font-size: 1.35rem; }
.stop-header p  { color: var(--offwhite); margin: 0; font-size: 0.9rem; opacity: 0.85; }

/* ── Info card ────────────────────────────────────────────── */
.info-card {
    background: #fff;
    border: 1px solid #ddd;
    border-top: 4px solid var(--teal);
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    line-height: 1.7;
    font-size: 0.95rem;
}

/* ── Insight boxes ────────────────────────────────────────── */
.insight-box {
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.93rem;
    line-height: 1.6;
}
.insight-box.marketing {
    background: linear-gradient(135deg, #fff8e1, #fff3cd);
    border-left: 5px solid var(--gold);
    color: #5d4037;
}
.insight-box.business {
    background: linear-gradient(135deg, #e8f5e9, #dcedc8);
    border-left: 5px solid #388e3c;
    color: #1b5e20;
}
.insight-box.psychology {
    background: linear-gradient(135deg, #f3e5f5, #e8d5f5);
    border-left: 5px solid #7b1fa2;
    color: #4a148c;
}

/* ── Citation ─────────────────────────────────────────────── */
.citation {
    font-size: 0.78rem;
    color: #777;
    font-style: italic;
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    border-top: 1px solid #eee;
}

/* ── Badge ────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), var(--gold-dark));
    color: var(--text-dark);
    border-radius: 50px;
    padding: 0.45rem 1.2rem;
    font-weight: bold;
    font-size: 0.88rem;
    box-shadow: 0 3px 10px rgba(212,175,55,0.45);
    margin-top: 0.5rem;
    letter-spacing: 0.5px;
}
.badge-locked {
    display: inline-block;
    background: #ccc;
    color: #555;
    border-radius: 50px;
    padding: 0.45rem 1.2rem;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}

/* ── 3-D Flip Card ────────────────────────────────────────── */
.flip-scene {
    perspective: 900px;
    width: 220px;
    height: 220px;
    margin: 0 auto;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}
.flip-card {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.65s cubic-bezier(.4,0,.2,1);
    border-radius: 50%;
}
.flip-scene:hover .flip-card,
.flip-scene.flipped .flip-card {
    transform: rotateY(180deg);
}
.flip-card__face {
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.flip-card__face--front { background: var(--gold); }
.flip-card__face--back  { background: var(--teal); transform: rotateY(180deg); }
.flip-card__face img    { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }

/* Touch-tap JS helper */
.flip-scene { user-select: none; }

/* ── Progress bar ─────────────────────────────────────────── */
.progress-bar-outer {
    background: #ddd;
    border-radius: 50px;
    height: 14px;
    width: 100%;
    margin: 0.5rem 0 1.2rem 0;
}
.progress-bar-inner {
    background: linear-gradient(90deg, var(--teal), var(--gold));
    height: 14px;
    border-radius: 50px;
    transition: width 0.6s ease;
}

/* ── Final conclusion ──────────────────────────────────────── */
.conclusion-card {
    background: linear-gradient(135deg, var(--teal) 0%, #002b22 100%);
    border: 2px solid var(--gold);
    border-radius: 14px;
    padding: 2rem 2.2rem;
    color: var(--offwhite);
    margin-top: 1rem;
}
.conclusion-card h2 { color: var(--gold); margin-top: 0; }
.conclusion-card li { margin-bottom: 0.5rem; line-height: 1.7; }

/* ── Map container ─────────────────────────────────────────── */
.map-container {
    border: 2px solid var(--gold);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

/* ── Divider ───────────────────────────────────────────────── */
.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── Responsive tweaks ─────────────────────────────────────── */
@media (max-width: 640px) {
    .flip-scene { width: 170px; height: 170px; }
    .hero-banner { padding: 1.5rem 1rem; }
}
</style>

<script>
// Enable tap-to-flip on mobile
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.flip-scene').forEach(function(scene) {
        scene.addEventListener('click', function() {
            scene.classList.toggle('flipped');
        });
    });
});
// Re-init on Streamlit re-renders
window.addEventListener('load', function() {
    setTimeout(function() {
        document.querySelectorAll('.flip-scene').forEach(function(scene) {
            scene.addEventListener('click', function() {
                scene.classList.toggle('flipped');
            });
        });
    }, 500);
});
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# BILINGUAL CONTENT DICTIONARY
# ─────────────────────────────────────────────────────────────────────────────
CONTENT = {
    "en": {
        "app_title": "The Fiel Contraste Engine",
        "app_subtitle": "A Gamified Business Route Through the History of Money · Madrid & Segovia",
        "sidebar_title": "⚖️ Navigation",
        "lang_label": "Language / Idioma",
        "major_label": "Choose Your Major",
        "major_options": ["— Select —", "Business", "Marketing", "Psychology"],
        "nav_label": "Route Section",
        "nav_options": ["🗺️ Interactive Map", "Stop 1 – Segovia", "Stop 2 – Mint Museum",
                        "Stop 3 – Anthropology Museum", "Stop 4 – The Euro",
                        "Stop 5 – 10,000 Peseta", "Stop 6 – Plaza Mayor",
                        "🏁 Final Conclusion"],
        "progress_label": "Route Progress",
        "checkin_btn": "✅ Check In & Unlock Badge",
        "checkin_done": "Badge already unlocked!",
        "badge_locked": "🔒 Badge Locked — Check in to unlock",
        "coin_front_label": "FRONT: The Currency",
        "coin_back_label": "BACK: The Mechanism",
        "coin_tap": "Tap / hover to flip",
        "past_label": "Past",
        "present_label": "Present",
        "map_title": "🗺️ Route Map — Madrid & Segovia",
        "map_desc": "Six stops connecting monetary history to modern business strategy. Click a marker for details.",
        "stops": [
            {
                "id": 1,
                "slug": "stop1",
                "nav": "Stop 1 – Segovia",
                "location": "Segovia — Real Ingenio de la Moneda",
                "coords": [40.9482, -4.1184],
                "business_lesson": "The Industrialization of Trust",
                "tagline": "When quality control became a machine.",
                "body": """
In 1583, Philip II commissioned the Real Ingenio de la Moneda in Segovia—Europe's first hydraulic coin-minting facility. Until that point, coins were hammered by hand (*macuquinas*), an artisanal process that produced inconsistent edges and weights, making counterfeiting trivially easy. The Ingenio replaced human hands with water-powered rolling mills, screw presses, and precision cutters. Every coin now had identical diameter, perfectly round edges, and a mill-edge (*cordoncillo*) that revealed any clipping at a glance.

**Context.** The mint sat on the Eresma river, whose current drove the machinery. The architectural complex—still standing today—was designed by Juan de Herrera, architect of El Escorial, signalling the Crown's intent to brand the project with imperial gravitas.

**Style & Social Impact.** The shift from *macuquina* to *maquinada* coinage is a direct analogue to the Industrial Revolution: standardisation reduced variance, increased throughput, and transferred quality assurance from the individual craftsman to the system. Citizens could verify a coin's legitimacy without expert knowledge—trust was *built into the object*.

**Business Parallel.** This is ISO certification before ISO existed. The Ingenio's hydraulic system is a supply-chain innovation: it removed the artisan as a quality-control bottleneck, scaled production, and created a defensible moat around the Crown's monetary monopoly.
                """,
                "citation": "Real Casa de la Moneda de Segovia. (2022). *Historia del Real Ingenio*. Patrimonio Nacional. https://www.patrimonionacional.es",
                "coin_front": "Philip II\nReal de a Ocho\n1588",
                "coin_back": "Hydraulic\nPress\nEresma River",
                "badge": "🏭 Industrial Trust Pioneer",
                "marketing_insight": "**Brand Strategy:** The Ingenio's mill-edge is the world's first tamper-evident packaging. Philip II understood that trust is a visual language—before a consumer could read, they could *feel* a clipped edge. Modern brands do the same with holograms, QR seals, and proprietary packaging geometry.",
                "business_insight": "**Scaling Logic:** The transition from hammer to hydraulic press mirrors SaaS-era thinking: replace artisan variance with algorithmic consistency. The ROI was not just coins-per-hour but *trust-per-coin*—a metric that compounded over decades as Spanish silver dominated global trade.",
                "psychology_insight": "**Cognitive Trust Cue:** Standardised round edges exploit the brain's preference for geometric regularity (Gestalt's Law of Prägnanz). A perfectly milled coin signals competence and safety before a single word is read—an early example of *System 1* trust design.",
            },
            {
                "id": 2,
                "slug": "stop2",
                "nav": "Stop 2 – Mint Museum",
                "location": "FNMT Mint Museum — Calle Doctor Esquerdo, Madrid",
                "coords": [40.4228, -3.6688],
                "business_lesson": "The PR Crisis & Subversion",
                "tagline": "When citizens turned coins into decentralized billboards.",
                "body": """
During the Spanish Civil War (1936–39), the Republican government issued emergency coinage in cardboard and aluminium as silver was diverted to fund the war effort. Simultaneously, citizens began *reselling* or counter-stamping existing coins with propaganda messages, merchants' names, and Republican or Nationalist slogans. The coin—an object of institutional authority—became a decentralised communication channel.

**Context.** The FNMT (Fábrica Nacional de Moneda y Timbre) in Madrid maintained operations under Republican control. Their wartime output is preserved at the Mint Museum on Calle Doctor Esquerdo, documenting how monetary systems fracture under political stress. Emergency local currencies (*vales*) proliferated in Republican zones when central supply failed.

**Style & Social Impact.** Counter-stamped coins are a form of *culture jamming* ante-litteram. They demonstrate that any medium of mass distribution—money, packaging, the public street—can be subverted into a communications platform by a motivated minority. The practice was dangerous: Nationalist forces treated Republican-stamped coins as evidence of sedition.

**Business Parallel.** Think of the counter-stamp as a 1930s guerrilla marketing stunt. The message rode on a pre-existing, trusted distribution network (legal tender) at near-zero marginal cost. The carrier—the coin—conferred legitimacy to the message because citizens *had* to handle it.
                """,
                "citation": "Fábrica Nacional de Moneda y Timbre – Real Casa de la Moneda (FNMT). (2023). *Colección Numismática: Guerra Civil*. FNMT. https://www.fnmt.es/museo",
                "coin_front": "Republican\nEmergency\nCoin 1937",
                "coin_back": "Counter-Stamp\nCitizen Media\nBillboard",
                "badge": "📢 Guerrilla Media Strategist",
                "marketing_insight": "**Brand Strategy:** Counter-stamping is the 1930s equivalent of brand hijacking on social media. The lesson for marketers: when a trusted platform (coins, Twitter, packaging) is accessible, even zero-budget actors can out-shout institutional voices. Protect your branded surfaces—and identify which distribution channels your competitors could commandeer.",
                "business_insight": "**Scaling Logic:** The Republican emergency currency system is a case study in supply-chain resilience under stress. When central supply (silver) failed, the system devolved to local improvisation. The business lesson: single-source dependencies create catastrophic brittleness. The counter-stamp phenomenon also shows user-generated content as a revenue-free distribution mechanism.",
                "psychology_insight": "**Reactance & Subversion:** Psychological reactance theory (Brehm, 1966) predicts that suppressing a message increases its perceived value. Counter-stamped coins were illegal—which made them *more* persuasive to recipients who saw them as authentic dissent rather than official propaganda.",
            },
            {
                "id": 3,
                "slug": "stop3",
                "nav": "Stop 3 – Anthropology Museum",
                "location": "Museo Nacional de Antropología — Calle Alfonso XII, Madrid",
                "coords": [40.4081, -3.6891],
                "business_lesson": "Hostile Market Entry",
                "tagline": "How the Spanish Crown deleted the competition.",
                "body": """
The Museo Nacional de Antropología's African collection includes *manillas*—copper or brass horseshoe-shaped rings that functioned as currency across West and Central African trade networks for centuries. When Portuguese and later Spanish traders arrived in the 15th–17th centuries, they initially *adopted* manillas as a transaction medium to facilitate the slave trade. Then, systematically, they flooded local markets with cheaply-produced European manillas, devaluing the existing currency, before imposing their own monetary standards.

**Context.** Manillas were not primitive barter objects—they were a sophisticated, portable, and weight-standardised currency system with regional exchange rates. The Museum's collection reveals their aesthetic richness: cast forms, engraved patterns, and regional variations that encoded provenance and quality.

**Style & Social Impact.** The deliberate flooding of manilla supply is a textbook case of what economists call *currency warfare* and what strategists call *platform capture*. By manufacturing cheaper manillas, European traders eroded confidence in the existing system, creating a vacuum that their own monetary regime could fill. The social cost was the erasure of an entire economic infrastructure and its replacement with one that systematically underpriced African labour.

**Business Parallel.** This is predatory pricing at civilisational scale. In modern terms: Amazon entering a marketplace, undercutting incumbents until they exit, then raising prices. Or a tech platform offering free services to destroy the business model of competitors, then monetising the captured audience.
                """,
                "citation": "Museo Nacional de Antropología. (2021). *Colección África: Monedas y Objetos de Intercambio*. Ministerio de Cultura. https://www.culturaydeporte.gob.es/mna",
                "coin_front": "West African\nManilla\n15th–17th C.",
                "coin_back": "Market\nFlooding\nStrategy",
                "badge": "🌍 Market Entry Architect",
                "marketing_insight": "**Brand Strategy:** The manilla story is a cautionary tale about *platform neutrality*. When a dominant entrant controls both the marketplace and its own competing product, local brands are at existential risk. Today's equivalent: selling on Amazon while Amazon copies your best-seller under 'Amazon Basics.' Know your platform risk.",
                "business_insight": "**Scaling Logic:** Currency flooding is a venture-capital-funded land-grab in historic dress. The Spanish/Portuguese strategy—absorb switching costs, undercut on price, capture the user base, then lock in—is identical to the playbook of Uber, WeWork, and DoorDash. The endgame is always monopoly rent extraction.",
                "psychology_insight": "**Social Proof & Authority Bias:** Manilla devaluation worked partly because colonial traders leveraged *authority bias*—European metal and European commercial relationships were framed as superior. Once enough merchants defected to the new system, social proof cascaded: the old currency lost legitimacy not because it was intrinsically inferior, but because enough people *believed* it was.",
            },
            {
                "id": 4,
                "slug": "stop4",
                "nav": "Stop 4 – The Euro",
                "location": "Puerta del Sol — Madrid (Central Reference Point)",
                "coords": [40.4168, -3.7038],
                "business_lesson": "Neutrality Branding",
                "tagline": "Why the ECB invented architecture that never existed.",
                "body": """
Euro banknotes feature bridges and gateways in seven architectural styles spanning from Classical Antiquity to the 20th century. None of them are real. The European Central Bank and the Eurosystem deliberately chose *fictional* architectural composites so that no member nation could claim the currency for its own cultural identity. The design brief was explicit: the currency must represent Europe without representing any particular European nation.

**Context.** Designer Robert Kalina won the ECB's 1996 design competition with this solution. The bridges on each note (a recurring motif) symbolise connection between European nations—but the specific bridges depicted exist nowhere on the continent. The buildings are plausible European architectural pastiche, carefully scrubbed of national identifiers.

**Style & Social Impact.** This is corporate neutral branding executed at sovereign scale. The ECB's insight was that any *real* monument would immediately politicise the currency—using the Eiffel Tower would make it 'French money,' the Colosseum would make it 'Italian money.' By deploying *intentional vagueness*, the ECB created a visual identity that no stakeholder could reject because no stakeholder was excluded.

**Business Parallel.** This is exactly the strategy used by holding companies that market-test names without cultural baggage (e.g., 'Accenture,' 'Verizon,' 'Agilent')—or by global brands that use abstract logos (Apple's apple, Nike's swoosh) to avoid geographic or cultural specificity that would limit expansion.
                """,
                "citation": "European Central Bank. (2023). *Euro Banknote Design: Bridges and Gateways*. ECB Publication. https://www.ecb.europa.eu/euro/banknotes",
                "coin_front": "€500 Note\nModernist\nBridge\n(Fictional)",
                "coin_back": "Neutrality\nBranding\nECB 1996",
                "badge": "🌐 Neutral Identity Designer",
                "marketing_insight": "**Brand Strategy:** Fictional neutrality is a deliberate positioning tool. When your brand must serve multiple competing stakeholder groups (nations, demographics, political factions), abstract or invented symbols are strategically superior to authentic ones. This is why airline liveries, global fast-food logos, and multinational financial brands avoid flags, local faces, and regional symbolism.",
                "business_insight": "**Scaling Logic:** The ECB's 'fictional bridges' strategy solved a governance problem masquerading as a design problem. In any merger or multi-party joint venture, the visual identity of the combined entity is a political negotiation. The neutral, invented identity was the only solution that all 11 founding Eurozone nations could ratify without ceding cultural ground.",
                "psychology_insight": "**The Mere Exposure Effect:** Fictional Euro architecture has now been seen billions of times. Through Zajonc's (1968) mere exposure effect, these invented images have acquired genuine cultural familiarity—people in Frankfurt, Helsinki, and Lisbon all feel vaguely 'at home' with bridges they have never visited. Manufactured familiarity is real familiarity.",
            },
            {
                "id": 5,
                "slug": "stop5",
                "nav": "Stop 5 – 10,000 Peseta",
                "location": "Banco de España — Calle Alcalá 48, Madrid",
                "coords": [40.4187, -3.6944],
                "business_lesson": "The Transition CEO",
                "tagline": "How a king's portrait stabilised a democratic rebrand.",
                "body": """
The Spanish 10,000 peseta note issued in 1992 features King Juan Carlos I prominently on the obverse. By 1992, Spain had been a democracy for 15 years—yet the monarch's face anchored the highest-denomination note in circulation. This was not nostalgia; it was strategic brand continuity. Juan Carlos I had personally orchestrated the *Transición Democrática* following Franco's death in 1975, rejecting authoritarian continuity and legitimising parliamentary democracy. Putting his face on the currency sent a clear institutional signal: *the new system is guaranteed by the trusted authority figure*.

**Context.** The Banco de España's numismatic archive documents the full arc of peseta design—from Francoist iconography (eagles, helmets, fascist bundling) to constitutional imagery (the Royal Coat of Arms, the Parliament building). The 1992 notes were issued to coincide with the Barcelona Olympics and Expo '92 Seville—a self-conscious national rebranding moment.

**Style & Social Impact.** The 1992 peseta series represents *political brand management* at its most sophisticated: honouring continuity (the king) while signalling rupture (democratic, European, modern). The Olympic and Expo events were the marketing campaign; the banknote was the evergreen brand asset that continued communicating long after the events ended.

**Business Parallel.** This is the classic 'Transition CEO' playbook: a trusted, credible authority figure is positioned as the face of a radical transformation precisely *because* their association with the old order reassures conservatives while their demonstrated support for the new order reassures progressives. Steve Jobs at Apple (1997 return), Satya Nadella at Microsoft—both are variations on this theme.
                """,
                "citation": "Banco de España. (2022). *Colección Numismática: La Peseta y la Transición Democrática*. Banco de España. https://www.bde.es/museo",
                "coin_front": "10,000 Ptas\nJuan Carlos I\n1992",
                "coin_back": "Transition\nCEO\nBrand Strategy",
                "badge": "👑 Transition Strategist",
                "marketing_insight": "**Brand Strategy:** The 1992 peseta is a masterclass in *continuity marketing during disruption*. The brand asset (king's face) borrowed equity from the old regime to fund confidence in the new one. Brand managers call this 'halo transfer'—when a trusted legacy element is strategically paired with a new product or direction to reduce adoption resistance.",
                "business_insight": "**Scaling Logic:** Organisational pivots fail when the internal coalition fractures. Juan Carlos I's face on the 10,000 peseta was a unity signal to two audiences simultaneously: Francoist conservatives (this is still the king's Spain) and European progressives (this king chose democracy). Finding the single symbol that speaks to your entire coalition is the hardest and most valuable leadership task during transformation.",
                "psychology_insight": "**Authority & Legitimacy Transfer:** Cialdini's (2006) principle of authority operates here at scale. The monarch's portrait transfers legitimacy to the paper note—an otherwise worthless rectangle—through pure associative conditioning. The same mechanism underlies celebrity endorsement, scientific testimonials in advertising, and medical authority figures in health communications.",
            },
            {
                "id": 6,
                "slug": "stop6",
                "nav": "Stop 6 – Plaza Mayor",
                "location": "Plaza Mayor — Casa de la Panadería, Madrid",
                "coords": [40.4155, -3.7075],
                "business_lesson": "Market Compliance",
                "tagline": "The Fiel Contraste as the world's first regulatory API.",
                "body": """
The Casa de la Panadería on Plaza Mayor's north side housed, among other civic functions, the office of the *Fiel Contraste*—a Crown-appointed official whose job was to assay, weigh, and certify weights and measures used in Madrid's markets. The title means literally 'Faithful Contrast/Comparison.' The Fiel Contraste was the physical enforcement point of market standards: he could seize fraudulent weights, fine merchants, and certify compliant traders with a lead seal that permitted them to operate.

**Context.** Plaza Mayor was constructed between 1617 and 1619 under Philip III and served as Madrid's primary market space for two centuries. The Casa de la Panadería—the bakery house—was the regulatory centre for bread weights and prices, a commodity so politically sensitive that the Crown maintained direct oversight. The frescoed façade visible today was completed in 1992 (same year as the peseta note) as part of a civic restoration programme.

**Style & Social Impact.** The Fiel Contraste represents the physical instantiation of regulatory infrastructure. Before digital platforms, before ISO, before the FDA—there was a man with a scale standing in the marketplace, physically verifying claims. The institution answered a fundamental market failure: information asymmetry between seller and buyer on the most basic commodity attributes (weight, purity, volume).

**Business Parallel.** The Fiel Contraste is the original API gateway. In software, an API (Application Programming Interface) is the standardised contract that governs how two parties exchange data—it defines format, validates inputs, and rejects non-compliant requests. The Fiel Contraste did exactly this in physical space: defined the standard (Crown weights), validated inputs (merchant scales), and rejected non-compliant actors (fined or seized). Every modern compliance, certification, and auditing function is a digital descendant of this office.
                """,
                "citation": "Ayuntamiento de Madrid. (2023). *Plaza Mayor: Historia Institucional y la Casa de la Panadería*. Madrid Destino. https://www.madrid.es/plazamayor",
                "coin_front": "Fiel\nContraste\nLead Seal",
                "coin_back": "Regulatory\nAPI\n1619–Present",
                "badge": "⚖️ Regulatory Architect",
                "marketing_insight": "**Brand Strategy:** The Fiel Contraste seal is a quality mark—the first B2B certification badge in Madrid's market. Modern equivalents: Michelin stars, Fair Trade certification, App Store approval, PCI-DSS compliance badges. Each is a trusted third-party signal that reduces buyer information-gathering costs and enables price premiums for certified vendors.",
                "business_insight": "**Scaling Logic:** The genius of the Fiel Contraste system is that compliance costs were borne by the merchant, not the Crown. This is a platform economics insight: the marketplace (Plaza Mayor / Philip III) set the standards and enforcement mechanism, while participants self-selected into compliance to gain access. Today's equivalents: app store developer agreements, Amazon seller performance standards, financial exchange membership rules.",
                "psychology_insight": "**Trust as Infrastructure:** Fukuyama (1995) argues that high-trust societies have lower transaction costs and higher economic growth. The Fiel Contraste was a trust-production machine: every interaction it supervised reduced the cognitive load on buyers, allowing market velocity to increase. Low-trust markets require exhausting individual verification; high-trust markets route that cognitive work through institutions—freeing mental bandwidth for value creation.",
            },
        ],
        "final": {
            "title": "🏁 Final Conclusion — The Bottom Line",
            "subtitle": "For the Professor: What Six Currencies Teach About Business Strategy",
            "summary": "This route through Madrid and Segovia traces a single thesis across six centuries of monetary history:",
            "thesis": "**Trust is not a feeling. It is an engineered system with a supply chain, a brand identity, a regulatory infrastructure, and a communications strategy.**",
            "lessons": [
                ("Segovia", "Industrialise your quality control or your competitors will. Variance is a vulnerability."),
                ("Civil War Coins", "Every mass-distribution channel is a potential media platform. Protect your surfaces; exploit others'."),
                ("Manillas", "Market entry without ethical guardrails is predatory pricing with civilisational consequences. Know your playbook's shadow."),
                ("The Euro", "When your audience is divided, neutral invented symbols outperform authentic specific ones. Vagueness is a feature, not a bug."),
                ("10,000 Peseta", "During transformation, borrow equity from trusted legacy assets to fund confidence in the new direction. The Transition CEO is a repeatable pattern."),
                ("Plaza Mayor", "Every marketplace needs a Fiel Contraste. Build the API before you need the regulator to force you to."),
            ],
            "closing": "The Fiel Contraste Engine is not a history lesson. It is a business school in six stops, built into the streets of a city that has been managing the branding of trust for five hundred years.",
        },
    },
    "es": {
        "app_title": "El Motor Fiel Contraste",
        "app_subtitle": "Una Ruta de Negocios Gamificada por la Historia del Dinero · Madrid y Segovia",
        "sidebar_title": "⚖️ Navegación",
        "lang_label": "Language / Idioma",
        "major_label": "Elige Tu Carrera",
        "major_options": ["— Seleccionar —", "Empresariales", "Marketing", "Psicología"],
        "nav_label": "Sección de la Ruta",
        "nav_options": ["🗺️ Mapa Interactivo", "Parada 1 – Segovia", "Parada 2 – Casa de la Moneda",
                        "Parada 3 – Museo de Antropología", "Parada 4 – El Euro",
                        "Parada 5 – 10.000 Pesetas", "Parada 6 – Plaza Mayor",
                        "🏁 Conclusión Final"],
        "progress_label": "Progreso de la Ruta",
        "checkin_btn": "✅ Registrarme y Desbloquear Insignia",
        "checkin_done": "¡Insignia ya desbloqueada!",
        "badge_locked": "🔒 Insignia Bloqueada — Regístrate para desbloquear",
        "coin_front_label": "CARA: La Moneda",
        "coin_back_label": "CRUZ: El Mecanismo",
        "coin_tap": "Toca / pasa el ratón para girar",
        "past_label": "Pasado",
        "present_label": "Presente",
        "map_title": "🗺️ Mapa de la Ruta — Madrid y Segovia",
        "map_desc": "Seis paradas que conectan la historia monetaria con la estrategia empresarial moderna. Haz clic en un marcador para más detalles.",
        "stops": [
            {
                "id": 1,
                "slug": "stop1",
                "nav": "Parada 1 – Segovia",
                "location": "Segovia — Real Ingenio de la Moneda",
                "coords": [40.9482, -4.1184],
                "business_lesson": "La Industrialización de la Confianza",
                "tagline": "Cuando el control de calidad se convirtió en máquina.",
                "body": """
En 1583, Felipe II encargó el Real Ingenio de la Moneda en Segovia—la primera instalación hidráulica de acuñación de monedas de Europa. Hasta ese momento, las monedas se acuñaban a martillo (*macuquinas*), un proceso artesanal que producía bordes y pesos inconsistentes, haciendo la falsificación trivialmente fácil. El Ingenio reemplazó las manos humanas con laminadoras accionadas por agua, prensas de tornillo y cortadoras de precisión.

**Contexto.** La casa de la moneda se asentaba sobre el río Eresma, cuya corriente impulsaba la maquinaria. El complejo arquitectónico—que aún se conserva hoy—fue diseñado por Juan de Herrera, arquitecto de El Escorial, señalando la intención de la Corona de marcar el proyecto con gravitas imperial.

**Estilo e Impacto Social.** El paso de la moneda *macuquina* a la *maquinada* es un análogo directo de la Revolución Industrial: la estandarización redujo la varianza, aumentó la producción y transfirió el control de calidad del artesano individual al sistema.

**Paralelismo Empresarial.** Esto es la certificación ISO antes de que existiera ISO. El sistema hidráulico del Ingenio es una innovación en la cadena de suministro: eliminó al artesano como cuello de botella del control de calidad y creó un foso defensible alrededor del monopolio monetario de la Corona.
                """,
                "citation": "Real Casa de la Moneda de Segovia. (2022). *Historia del Real Ingenio*. Patrimonio Nacional. https://www.patrimonionacional.es",
                "coin_front": "Felipe II\nReal de a Ocho\n1588",
                "coin_back": "Prensa\nHidráulica\nRío Eresma",
                "badge": "🏭 Pionero de la Confianza Industrial",
                "marketing_insight": "**Estrategia de Marca:** El cordoncillo del Ingenio es el primer envase a prueba de manipulaciones del mundo. Felipe II entendió que la confianza es un lenguaje visual—antes de que un consumidor pudiera leer, podía *sentir* un borde recortado.",
                "business_insight": "**Lógica de Escala:** La transición del martillo a la prensa hidráulica refleja el pensamiento de la era SaaS: reemplazar la varianza artesanal con consistencia algorítmica. El ROI no eran solo monedas-por-hora sino *confianza-por-moneda*.",
                "psychology_insight": "**Señal de Confianza Cognitiva:** Los bordes redondos estandarizados explotan la preferencia del cerebro por la regularidad geométrica (Ley de Prägnanz de la Gestalt). Una moneda perfectamente acuñada señala competencia y seguridad antes de que se lea una sola palabra.",
            },
            {
                "id": 2,
                "slug": "stop2",
                "nav": "Parada 2 – Casa de la Moneda",
                "location": "Museo FNMT — Calle Doctor Esquerdo, Madrid",
                "coords": [40.4228, -3.6688],
                "business_lesson": "La Crisis de PR y la Subversión",
                "tagline": "Cuando los ciudadanos convirtieron las monedas en vallas publicitarias descentralizadas.",
                "body": """
Durante la Guerra Civil española (1936-39), el gobierno republicano emitió monedas de emergencia en cartón y aluminio mientras la plata se desviaba para financiar la guerra. Simultáneamente, los ciudadanos comenzaron a *resellar* o contramarcar monedas existentes con mensajes de propaganda, nombres de comerciantes y eslóganes republicanos o nacionalistas.

**Contexto.** La FNMT (Fábrica Nacional de Moneda y Timbre) en Madrid mantuvo operaciones bajo control republicano. Su producción de guerra está preservada en el Museo de la Casa de la Moneda en la Calle Doctor Esquerdo, documentando cómo los sistemas monetarios se fracturan bajo estrés político.

**Estilo e Impacto Social.** Las monedas contramarcadas son una forma de *culture jamming* ante-litteram. Demuestran que cualquier medio de distribución masiva puede ser subvertido en una plataforma de comunicación por una minoría motivada.

**Paralelismo Empresarial.** El mensaje viajó sobre una red de distribución preexistente y confiable (moneda de curso legal) a un coste marginal casi nulo. El portador—la moneda—confería legitimidad al mensaje porque los ciudadanos *tenían* que manejarla.
                """,
                "citation": "Fábrica Nacional de Moneda y Timbre – Real Casa de la Moneda (FNMT). (2023). *Colección Numismática: Guerra Civil*. FNMT. https://www.fnmt.es/museo",
                "coin_front": "Moneda de\nEmergencia\nRepublicana 1937",
                "coin_back": "Contramarca\nMedia Ciudadana\nValla Publicitaria",
                "badge": "📢 Estratega de Media Guerrilla",
                "marketing_insight": "**Estrategia de Marca:** El contraseño es el equivalente de los años 30 del secuestro de marca en las redes sociales. La lección para los marketeros: cuando una plataforma de confianza es accesible, incluso los actores sin presupuesto pueden superar a las voces institucionales.",
                "business_insight": "**Lógica de Escala:** El sistema de moneda de emergencia republicano es un estudio de caso sobre resiliencia en la cadena de suministro bajo estrés. El fenómeno del contraseño también muestra el contenido generado por el usuario como mecanismo de distribución sin coste.",
                "psychology_insight": "**Reactancia y Subversión:** La teoría de la reactancia psicológica (Brehm, 1966) predice que suprimir un mensaje aumenta su valor percibido. Las monedas contramarcadas eran ilegales—lo que las hacía *más* persuasivas.",
            },
            {
                "id": 3,
                "slug": "stop3",
                "nav": "Parada 3 – Museo de Antropología",
                "location": "Museo Nacional de Antropología — Calle Alfonso XII, Madrid",
                "coords": [40.4081, -3.6891],
                "business_lesson": "Entrada Hostil al Mercado",
                "tagline": "Cómo la Corona española eliminó a la competencia.",
                "body": """
La colección africana del Museo Nacional de Antropología incluye *manillas*—anillos con forma de herradura de cobre o latón que funcionaron como moneda en las redes comerciales de África Occidental y Central durante siglos. Cuando llegaron los comerciantes portugueses y españoles, inicialmente *adoptaron* las manillas como medio de transacción, luego inundaron sistemáticamente los mercados locales con manillas europeas producidas a bajo coste, devaluando la moneda existente.

**Contexto.** Las manillas no eran objetos de trueque primitivos—eran un sofisticado sistema monetario portátil y estandarizado en peso con tipos de cambio regionales.

**Estilo e Impacto Social.** La inundación deliberada del suministro de manillas es un caso de libro de texto de lo que los economistas llaman *guerra de divisas*. Al fabricar manillas más baratas, los comerciantes europeos erosionaron la confianza en el sistema existente, creando un vacío que su propio régimen monetario podía llenar.

**Paralelismo Empresarial.** Esto es precios predatorios a escala civilizacional. En términos modernos: Amazon entrando en un mercado, reduciendo precios hasta que los incumbentes salen, luego subiendo precios.
                """,
                "citation": "Museo Nacional de Antropología. (2021). *Colección África: Monedas y Objetos de Intercambio*. Ministerio de Cultura. https://www.culturaydeporte.gob.es/mna",
                "coin_front": "Manilla\nÁfrica Occidental\nS. XV–XVII",
                "coin_back": "Estrategia de\nInundación\nde Mercado",
                "badge": "🌍 Arquitecto de Entrada al Mercado",
                "marketing_insight": "**Estrategia de Marca:** La historia de la manilla es una advertencia sobre la *neutralidad de la plataforma*. Cuando un entrante dominante controla tanto el mercado como su propio producto competidor, las marcas locales están en riesgo existencial.",
                "business_insight": "**Lógica de Escala:** La inundación de divisas es una conquista de mercado financiada por capital riesgo en vestimenta histórica. La estrategia española/portuguesa es idéntica al manual de Uber, WeWork y DoorDash.",
                "psychology_insight": "**Prueba Social y Sesgo de Autoridad:** La devaluación de la manilla funcionó en parte porque los comerciantes coloniales aprovecharon el *sesgo de autoridad*—el metal europeo se enmarcó como superior. Una vez que suficientes comerciantes defeccionaron, la prueba social en cascada erosionó la legitimidad del sistema antiguo.",
            },
            {
                "id": 4,
                "slug": "stop4",
                "nav": "Parada 4 – El Euro",
                "location": "Puerta del Sol — Madrid (Punto de Referencia Central)",
                "coords": [40.4168, -3.7038],
                "business_lesson": "Marca de Neutralidad",
                "tagline": "Por qué el BCE inventó arquitectura que nunca existió.",
                "body": """
Los billetes de euro presentan puentes y puertas en siete estilos arquitectónicos que van desde la Antigüedad Clásica hasta el siglo XX. Ninguno de ellos es real. El Banco Central Europeo eligió deliberadamente *composites arquitectónicos ficticios* para que ninguna nación miembro pudiera reclamar la moneda para su propia identidad cultural.

**Contexto.** El diseñador Robert Kalina ganó el concurso de diseño del BCE de 1996 con esta solución. Los puentes en cada billete (un motivo recurrente) simbolizan la conexión entre naciones europeas—pero los puentes específicos representados no existen en ningún lugar del continente.

**Estilo e Impacto Social.** Esto es marca corporativa neutral ejecutada a escala soberana. La visión del BCE fue que cualquier monumento *real* politizaría inmediatamente la moneda. Al desplegar *vaguedad intencional*, el BCE creó una identidad visual que ninguna parte interesada podía rechazar porque ninguna parte interesada quedaba excluida.

**Paralelismo Empresarial.** Esta es exactamente la estrategia utilizada por las empresas que prueban nombres sin bagaje cultural (por ejemplo, 'Accenture,' 'Verizon,' 'Agilent').
                """,
                "citation": "Banco Central Europeo. (2023). *Diseño de Billetes de Euro: Puentes y Puertas*. BCE. https://www.ecb.europa.eu/euro/banknotes",
                "coin_front": "Billete de €500\nPuente Modernista\n(Ficticio)",
                "coin_back": "Marca de\nNeutralidad\nBCE 1996",
                "badge": "🌐 Diseñador de Identidad Neutral",
                "marketing_insight": "**Estrategia de Marca:** La neutralidad ficticia es una herramienta de posicionamiento deliberada. Cuando tu marca debe servir a múltiples grupos de partes interesadas competidoras, los símbolos abstractos o inventados son estratégicamente superiores a los auténticos.",
                "business_insight": "**Lógica de Escala:** La estrategia de 'puentes ficticios' del BCE resolvió un problema de gobernanza disfrazado de problema de diseño. En cualquier fusión, la identidad visual de la entidad combinada es una negociación política.",
                "psychology_insight": "**El Efecto de Mera Exposición:** La arquitectura ficticia del Euro ahora ha sido vista miles de millones de veces. A través del efecto de mera exposición de Zajonc (1968), estas imágenes inventadas han adquirido familiaridad cultural genuina.",
            },
            {
                "id": 5,
                "slug": "stop5",
                "nav": "Parada 5 – 10.000 Pesetas",
                "location": "Banco de España — Calle Alcalá 48, Madrid",
                "coords": [40.4187, -3.6944],
                "business_lesson": "El CEO de la Transición",
                "tagline": "Cómo el rostro de un rey estabilizó una nueva marca democrática.",
                "body": """
El billete de 10.000 pesetas emitido en 1992 presenta al Rey Juan Carlos I prominentemente en el anverso. En 1992, España llevaba 15 años siendo una democracia—sin embargo, el rostro del monarca anclaba el billete de mayor denominación en circulación. Juan Carlos I había orquestado personalmente la *Transición Democrática* tras la muerte de Franco en 1975, rechazando la continuidad autoritaria y legitimando la democracia parlamentaria.

**Contexto.** El archivo numismático del Banco de España documenta el arco completo del diseño de la peseta—desde la iconografía franquista hasta la imagen constitucional. Los billetes de 1992 se emitieron para coincidir con los Juegos Olímpicos de Barcelona y la Expo '92 de Sevilla.

**Estilo e Impacto Social.** La serie de pesetas de 1992 representa la *gestión de marca política* en su forma más sofisticada: honrando la continuidad (el rey) mientras señalaba la ruptura (democrática, europea, moderna).

**Paralelismo Empresarial.** Este es el clásico manual del 'CEO de Transición': una figura de autoridad creíble y de confianza se posiciona como la cara de una transformación radical precisamente *porque* su asociación con el orden antiguo tranquiliza a los conservadores.
                """,
                "citation": "Banco de España. (2022). *Colección Numismática: La Peseta y la Transición Democrática*. Banco de España. https://www.bde.es/museo",
                "coin_front": "10.000 Ptas\nJuan Carlos I\n1992",
                "coin_back": "CEO de\nTransición\nEstrategia de Marca",
                "badge": "👑 Estratega de Transición",
                "marketing_insight": "**Estrategia de Marca:** La peseta de 1992 es una clase magistral de *marketing de continuidad durante la disrupción*. El activo de marca (rostro del rey) tomó prestado equity del antiguo régimen para financiar la confianza en el nuevo.",
                "business_insight": "**Lógica de Escala:** Los pivotes organizacionales fracasan cuando la coalición interna se fractura. El rostro de Juan Carlos I en las 10.000 pesetas fue una señal de unidad para dos audiencias simultáneamente: conservadores franquistas y progresistas europeos.",
                "psychology_insight": "**Transferencia de Autoridad y Legitimidad:** El principio de autoridad de Cialdini (2006) opera aquí a escala. El retrato del monarca transfiere legitimidad al billete de papel—un rectángulo por otra parte sin valor—a través del condicionamiento asociativo puro.",
            },
            {
                "id": 6,
                "slug": "stop6",
                "nav": "Parada 6 – Plaza Mayor",
                "location": "Plaza Mayor — Casa de la Panadería, Madrid",
                "coords": [40.4155, -3.7075],
                "business_lesson": "Cumplimiento del Mercado",
                "tagline": "El Fiel Contraste como la primera API regulatoria del mundo.",
                "body": """
La Casa de la Panadería en el lado norte de la Plaza Mayor albergaba, entre otras funciones cívicas, la oficina del *Fiel Contraste*—un funcionario nombrado por la Corona cuyo trabajo era ensayar, pesar y certificar pesas y medidas utilizadas en los mercados de Madrid. El título significa literalmente 'Comparación Fiel.' El Fiel Contraste era el punto de aplicación física de los estándares del mercado.

**Contexto.** La Plaza Mayor fue construida entre 1617 y 1619 bajo Felipe III y sirvió como principal espacio de mercado de Madrid durante dos siglos. La Casa de la Panadería era el centro regulatorio para los pesos y precios del pan, una mercancía tan políticamente sensible que la Corona mantenía supervisión directa.

**Estilo e Impacto Social.** El Fiel Contraste representa la instanciación física de la infraestructura regulatoria. Antes de las plataformas digitales, antes de ISO, antes de la FDA—había un hombre con una balanza de pie en el mercado, verificando físicamente las afirmaciones.

**Paralelismo Empresarial.** El Fiel Contraste es la pasarela API original. En software, una API es el contrato estandarizado que gobierna cómo dos partes intercambian datos. El Fiel Contraste hacía exactamente esto en el espacio físico.
                """,
                "citation": "Ayuntamiento de Madrid. (2023). *Plaza Mayor: Historia Institucional y la Casa de la Panadería*. Madrid Destino. https://www.madrid.es/plazamayor",
                "coin_front": "Sello de\nPlomo\nFiel Contraste",
                "coin_back": "API\nRegulatoria\n1619–Presente",
                "badge": "⚖️ Arquitecto Regulatorio",
                "marketing_insight": "**Estrategia de Marca:** El sello del Fiel Contraste es una marca de calidad—el primer badge de certificación B2B en el mercado de Madrid. Equivalentes modernos: estrellas Michelin, certificación Fair Trade, aprobación App Store.",
                "business_insight": "**Lógica de Escala:** El genio del sistema del Fiel Contraste es que los costes de cumplimiento los pagaba el comerciante, no la Corona. Esto es una visión de economía de plataforma: el mercado (Plaza Mayor / Felipe III) estableció los estándares y el mecanismo de aplicación, mientras los participantes se autoseleccionaron en el cumplimiento para obtener acceso.",
                "psychology_insight": "**La Confianza como Infraestructura:** Fukuyama (1995) argumenta que las sociedades de alta confianza tienen menores costes de transacción y mayor crecimiento económico. El Fiel Contraste era una máquina de producción de confianza.",
            },
        ],
        "final": {
            "title": "🏁 Conclusión Final — La Conclusión",
            "subtitle": "Para el Profesor: Lo Que Seis Monedas Enseñan Sobre Estrategia Empresarial",
            "summary": "Esta ruta por Madrid y Segovia rastrea una sola tesis a través de seis siglos de historia monetaria:",
            "thesis": "**La confianza no es un sentimiento. Es un sistema diseñado con una cadena de suministro, una identidad de marca, una infraestructura regulatoria y una estrategia de comunicaciones.**",
            "lessons": [
                ("Segovia", "Industrializa tu control de calidad o lo harán tus competidores. La varianza es una vulnerabilidad."),
                ("Monedas Guerra Civil", "Cada canal de distribución masiva es una plataforma de medios potencial. Protege tus superficies; explota las de otros."),
                ("Manillas", "La entrada al mercado sin salvaguardas éticas es precios predatorios con consecuencias civilizacionales."),
                ("El Euro", "Cuando tu audiencia está dividida, los símbolos neutrales inventados superan a los auténticos específicos."),
                ("10.000 Pesetas", "Durante la transformación, toma prestado equity de activos heredados de confianza para financiar la confianza en la nueva dirección."),
                ("Plaza Mayor", "Todo mercado necesita un Fiel Contraste. Construye la API antes de que necesites que el regulador te obligue a hacerlo."),
            ],
            "closing": "El Motor Fiel Contraste no es una lección de historia. Es una escuela de negocios en seis paradas, construida en las calles de una ciudad que ha estado gestionando la marca de la confianza durante quinientos años.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "badges" not in st.session_state:
    st.session_state.badges = {}          # stop_slug -> bool
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "major" not in st.session_state:
    st.session_state.major = None
if "nav" not in st.session_state:
    st.session_state.nav = 0

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def img_b64(path: str) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def flip_card_html(front_img: str, back_img: str, front_label: str, back_label: str,
                   front_text: str, back_text: str, uid: str) -> str:
    """Render a 3-D flip card using base64-encoded images or text fallback."""
    def face_content(img_path, text):
        b64 = img_b64(img_path)
        if b64:
            ext = img_path.rsplit(".", 1)[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f'<img src="data:{mime};base64,{b64}" alt="coin" />'
        # Fallback: text on gradient circle
        lines = text.replace("\n", "<br>")
        return f'<div style="text-align:center;padding:1rem;font-weight:bold;font-size:0.85rem;line-height:1.5">{lines}</div>'

    front_content = face_content(front_img, front_text)
    back_content  = face_content(back_img,  back_text)

    return f"""
<div style="text-align:center;margin:1rem 0">
  <p style="color:#777;font-size:0.8rem;margin-bottom:0.5rem">
    {front_label} &nbsp;↔&nbsp; {back_label}
  </p>
  <div class="flip-scene" id="flip_{uid}" onclick="this.classList.toggle('flipped')">
    <div class="flip-card">
      <div class="flip-card__face flip-card__face--front">{front_content}</div>
      <div class="flip-card__face flip-card__face--back">{back_content}</div>
    </div>
  </div>
  <p style="color:#999;font-size:0.75rem;margin-top:0.5rem">👆 Tap / hover to flip</p>
</div>
"""


def progress_bar_html(checked: int, total: int) -> str:
    pct = int(checked / total * 100) if total else 0
    return f"""
<div style="margin:0.5rem 0 0.3rem 0">
  <div style="display:flex;justify-content:space-between;font-size:0.82rem;color:#555;margin-bottom:4px">
    <span>{checked} / {total} stops completed</span>
    <span>{pct}%</span>
  </div>
  <div class="progress-bar-outer">
    <div class="progress-bar-inner" style="width:{pct}%"></div>
  </div>
</div>
"""


def insight_html(text: str, major_key: str) -> str:
    return f'<div class="insight-box {major_key.lower()}">{text}</div>'


def render_map(stops_data, lang_key):
    m = folium.Map(
        location=[40.55, -3.72],
        zoom_start=9,
        tiles="CartoDB positron",
    )
    icons = ["1", "2", "3", "4", "5", "6"]
    colors = ["darkgreen", "darkgreen", "darkgreen", "darkgreen", "darkgreen", "darkgreen"]
    for i, stop in enumerate(stops_data):
        folium.Marker(
            location=stop["coords"],
            popup=folium.Popup(
                f"<b>Stop {stop['id']}</b><br>{stop['location']}<br><i>{stop['business_lesson']}</i>",
                max_width=220,
            ),
            tooltip=f"Stop {stop['id']}: {stop['business_lesson']}",
            icon=folium.Icon(color=colors[i], icon=icons[i], prefix="fa"),
        ).add_to(m)
    # Draw route line
    coords = [s["coords"] for s in stops_data]
    folium.PolyLine(coords, color="#d4af37", weight=3, opacity=0.7, dash_array="8").add_to(m)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚖️ The Fiel Contraste Engine")
    st.markdown("---")

    # Language toggle
    lang_choice = st.radio(
        "🌐 Language / Idioma",
        ["English", "Español"],
        index=0 if st.session_state.lang == "en" else 1,
        horizontal=True,
    )
    st.session_state.lang = "en" if lang_choice == "English" else "es"
    T = CONTENT[st.session_state.lang]

    st.markdown("---")

    # Major selector
    major_choice = st.selectbox(T["major_label"], T["major_options"], index=0)
    if major_choice != T["major_options"][0]:
        major_map = {"Business": "business", "Marketing": "marketing", "Psychology": "psychology",
                     "Empresariales": "business", "Marketing": "marketing", "Psicología": "psychology"}
        st.session_state.major = major_map.get(major_choice)
    else:
        st.session_state.major = None

    st.markdown("---")

    # Navigation
    nav_idx = st.radio(T["nav_label"], T["nav_options"], index=st.session_state.nav)
    st.session_state.nav = T["nav_options"].index(nav_idx)

    st.markdown("---")

    # Progress
    badges_earned = sum(1 for v in st.session_state.badges.values() if v)
    st.markdown(f"**{T['progress_label']}**")
    st.markdown(progress_bar_html(badges_earned, 6), unsafe_allow_html=True)

    # Badge list
    if badges_earned > 0:
        st.markdown("**Unlocked Badges:**" if st.session_state.lang == "en" else "**Insignias Desbloqueadas:**")
        for stop in T["stops"]:
            if st.session_state.badges.get(stop["slug"]):
                st.markdown(f'<span class="badge">{stop["badge"]}</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <h1>⚖️ {T["app_title"]}</h1>
  <p>{T["app_subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────
nav_idx = st.session_state.nav

# ── MAP PAGE ────────────────────────────────────────────────────────────────
if nav_idx == 0:
    st.markdown(f"### {T['map_title']}")
    st.markdown(T["map_desc"])

    m = render_map(T["stops"], st.session_state.lang)
    with st.container():
        st_folium(m, width="100%", height=520, returned_objects=[])

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown("#### All Stops" if st.session_state.lang == "en" else "#### Todas las Paradas")
    cols = st.columns(3)
    for i, stop in enumerate(T["stops"]):
        with cols[i % 3]:
            earned = st.session_state.badges.get(stop["slug"], False)
            badge_html = (
                f'<span class="badge">{stop["badge"]}</span>'
                if earned
                else f'<span class="badge-locked">🔒 Locked</span>'
            )
            st.markdown(f"""
<div class="info-card" style="min-height:140px">
  <b>Stop {stop['id']}</b><br>
  <span style="color:#004d40;font-weight:bold">{stop['business_lesson']}</span><br>
  <small style="color:#777">{stop['location']}</small><br><br>
  {badge_html}
</div>
""", unsafe_allow_html=True)

# ── STOP PAGES (1-6) ─────────────────────────────────────────────────────────
elif 1 <= nav_idx <= 6:
    stop = T["stops"][nav_idx - 1]
    slug = stop["slug"]

    # Stop header
    st.markdown(f"""
<div class="stop-header">
  <h2>Stop {stop['id']}: {stop['business_lesson']}</h2>
  <p>📍 {stop['location']} &nbsp;·&nbsp; <i>{stop['tagline']}</i></p>
</div>
""", unsafe_allow_html=True)

    # ── Layout: text left, flip card right ──────────────────────────────────
    col_text, col_card = st.columns([3, 2], gap="large")

    with col_text:
        st.markdown(f'<div class="info-card">{stop["body"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="citation">{stop["citation"]}</p>', unsafe_allow_html=True)

        # Personalisation insight
        if st.session_state.major:
            major_key = st.session_state.major
            insight_key = f"{major_key}_insight"
            if insight_key in stop:
                icon = {"marketing": "📣", "business": "📈", "psychology": "🧠"}.get(major_key, "💡")
                label = {"marketing": "Brand Strategy", "business": "Scaling Logic",
                         "psychology": "Psychology Lens"}.get(major_key, "Insight")
                st.markdown(
                    f'<div class="insight-box {major_key}">'
                    f'<strong>{icon} {label}</strong><br>{stop[insight_key]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    with col_card:
        coin_front_path = resolve_asset(f"assets/{slug}_coin_front", _COIN_EXTS) or ""
        coin_back_path  = resolve_asset(f"assets/{slug}_coin_back",  _COIN_EXTS) or ""
        st.markdown(
            flip_card_html(
                front_img=coin_front_path,
                back_img=coin_back_path,
                front_label=T["coin_front_label"],
                back_label=T["coin_back_label"],
                front_text=stop["coin_front"],
                back_text=stop["coin_back"],
                uid=slug,
            ),
            unsafe_allow_html=True,
        )

        # Badge check-in
        st.markdown("---")
        earned = st.session_state.badges.get(slug, False)
        if earned:
            st.markdown(f'<div class="badge">{stop["badge"]}</div>', unsafe_allow_html=True)
            st.caption(T["checkin_done"])
        else:
            st.markdown(f'<span class="badge-locked">{T["badge_locked"]}</span>', unsafe_allow_html=True)
            if st.button(T["checkin_btn"], key=f"btn_{slug}"):
                st.session_state.badges[slug] = True
                st.rerun()

    # ── Image comparison slider ───────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown(
        f"#### 🔄 Past vs. Present — {stop['business_lesson']}"
        if st.session_state.lang == "en"
        else f"#### 🔄 Pasado vs. Presente — {stop['business_lesson']}"
    )

    past_path    = resolve_asset(f"assets/{slug}_past")
    present_path = resolve_asset(f"assets/{slug}_present")

    if past_path and present_path:
        # Both images available — show interactive slider
        image_comparison(
            img1=past_path,
            img2=present_path,
            label1=T["past_label"],
            label2=T["present_label"],
            width=700,
            show_labels=True,
            make_responsive=True,
        )
    elif present_path:
        # Only the present image is available (e.g. Stop 4 missing past photo)
        st.image(
            present_path,
            caption=T["present_label"],
            use_container_width=True,
        )
        st.caption(
            "📷 Only the present-day image is available for this stop. "
            f"Add `assets/{slug}_past.*` to enable the comparison slider."
            if st.session_state.lang == "en"
            else f"📷 Solo está disponible la imagen actual para esta parada. "
            f"Añade `assets/{slug}_past.*` para activar el comparador."
        )
    elif past_path:
        # Only the past image is available
        st.image(
            past_path,
            caption=T["past_label"],
            use_container_width=True,
        )
        st.caption(
            f"📷 Only the historical image is available. "
            f"Add `assets/{slug}_present.*` to enable the comparison slider."
            if st.session_state.lang == "en"
            else f"📷 Solo está disponible la imagen histórica. "
            f"Añade `assets/{slug}_present.*` para activar el comparador."
        )
    else:
        # Neither image exists yet
        st.info(
            f"📁 Drop your images at `assets/{slug}_past.*` and `assets/{slug}_present.*` "
            "to activate the comparison slider."
            if st.session_state.lang == "en"
            else f"📁 Añade tus imágenes en `assets/{slug}_past.*` y `assets/{slug}_present.*` "
            "para activar el comparador."
        )

    # ── Stop navigation buttons ───────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    prev_col, _, next_col = st.columns([1, 3, 1])
    with prev_col:
        if nav_idx > 1:
            if st.button("← Previous" if st.session_state.lang == "en" else "← Anterior"):
                st.session_state.nav = nav_idx - 1
                st.rerun()
    with next_col:
        if nav_idx < 6:
            if st.button("Next →" if st.session_state.lang == "en" else "Siguiente →"):
                st.session_state.nav = nav_idx + 1
                st.rerun()
        else:
            if st.button("Conclusion 🏁" if st.session_state.lang == "en" else "Conclusión 🏁"):
                st.session_state.nav = 7
                st.rerun()

# ── FINAL CONCLUSION ─────────────────────────────────────────────────────────
elif nav_idx == 7:
    F = T["final"]
    badges_earned = sum(1 for v in st.session_state.badges.values() if v)

    st.markdown(f"### {F['title']}")
    st.markdown(f"*{F['subtitle']}*")

    # Completion trophy
    if badges_earned == 6:
        st.balloons()
        st.success(
            "🏆 Congratulations! You have completed all 6 stops and earned every badge!"
            if st.session_state.lang == "en"
            else "🏆 ¡Felicidades! ¡Has completado las 6 paradas y ganado todas las insignias!"
        )
    else:
        remaining = 6 - badges_earned
        st.info(
            f"You have visited {badges_earned}/6 stops. Return to complete the remaining {remaining}."
            if st.session_state.lang == "en"
            else f"Has visitado {badges_earned}/6 paradas. Vuelve para completar las {remaining} restantes."
        )

    st.markdown(progress_bar_html(badges_earned, 6), unsafe_allow_html=True)

    # Main conclusion card
    st.markdown(f"""
<div class="conclusion-card">
  <h2>{F['title']}</h2>
  <p>{F['summary']}</p>
  <blockquote style="border-left:4px solid #d4af37;padding-left:1rem;margin:1rem 0;font-size:1.05rem">
    {F['thesis']}
  </blockquote>
  <hr style="border-color:rgba(212,175,55,0.3)">
  <h3 style="color:#d4af37">{"The Six Strategic Lessons" if st.session_state.lang == "en" else "Las Seis Lecciones Estratégicas"}</h3>
  <ul>
""" + "".join(
        f'<li><strong style="color:#d4af37">{loc}:</strong> {lesson}</li>'
        for loc, lesson in F["lessons"]
    ) + f"""
  </ul>
  <hr style="border-color:rgba(212,175,55,0.3)">
  <p style="font-style:italic;opacity:0.85">{F['closing']}</p>
</div>
""", unsafe_allow_html=True)

    # Badge gallery
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown(
        "#### 🏅 Your Badge Collection"
        if st.session_state.lang == "en"
        else "#### 🏅 Tu Colección de Insignias"
    )
    badge_cols = st.columns(6)
    for i, stop in enumerate(T["stops"]):
        with badge_cols[i]:
            earned = st.session_state.badges.get(stop["slug"], False)
            if earned:
                st.markdown(f'<div style="text-align:center"><span class="badge">{stop["badge"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center"><span class="badge-locked">🔒</span></div>', unsafe_allow_html=True)

    # Professor summary table
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown(
        "#### 📋 Professor Summary Table"
        if st.session_state.lang == "en"
        else "#### 📋 Tabla Resumen para el Profesor"
    )
    import pandas as pd
    rows = []
    for stop in T["stops"]:
        rows.append({
            "Stop": f"Stop {stop['id']}",
            "Location": stop["location"].split("—")[0].strip(),
            "Business Lesson" if st.session_state.lang == "en" else "Lección Empresarial": stop["business_lesson"],
            "Badge Earned" if st.session_state.lang == "en" else "Insignia": "✅" if st.session_state.badges.get(stop["slug"]) else "🔒",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Reset button
    st.markdown("---")
    if st.button(
        "🔄 Reset Route" if st.session_state.lang == "en" else "🔄 Reiniciar Ruta",
        type="secondary",
    ):
        st.session_state.badges = {}
        st.session_state.nav = 0
        st.rerun()
