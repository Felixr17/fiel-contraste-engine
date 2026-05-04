"""
Run this script once to generate placeholder images in /assets/.
Replace them with your actual photos before deploying.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

STOPS = [
    ("stop1", "Segovia\nReal Ingenio"),
    ("stop2", "Mint Museum\nCivil War Coins"),
    ("stop3", "Anthropology\nMuseum (Manillas)"),
    ("stop4", "The Euro\nFictional Bridges"),
    ("stop5", "10,000 Peseta\n1992"),
    ("stop6", "Plaza Mayor\nCasa de la Panadería"),
]

COLORS_PAST = [
    (60, 80, 60),
    (80, 60, 40),
    (70, 50, 70),
    (40, 60, 80),
    (80, 70, 40),
    (60, 40, 40),
]
COLORS_PRESENT = [
    (0, 77, 64),
    (0, 77, 64),
    (0, 77, 64),
    (0, 77, 64),
    (0, 77, 64),
    (0, 77, 64),
]

COIN_LABELS = [
    "Hydraulic\nPress",
    "Republican\nStamp",
    "Manilla\nCurrency",
    "Euro Arch\nBridge",
    "Juan Carlos I\nPortrait",
    "Fiel Contraste\nSeal",
]
COIN_BACK = [
    "Mechanical\nTrust Engine",
    "Decentralized\nMedia",
    "Hostile Market\nEntry",
    "Political\nNeutrality",
    "Transition\nCEO",
    "Physical\nAPI",
]


def make_placeholder(path, label, bg_color, size=(600, 400)):
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    # border
    draw.rectangle([4, 4, size[0] - 5, size[1] - 5], outline=(212, 175, 55), width=3)
    # watermark text
    text = f"[ PLACEHOLDER ]\n{label}\nReplace with real image"
    draw.multiline_text(
        (size[0] // 2, size[1] // 2),
        text,
        fill=(212, 175, 55),
        anchor="mm",
        align="center",
    )
    img.save(path)
    print(f"  Created: {path}")


def make_coin(path, label, bg_color, size=(300, 300)):
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    r = min(size) // 2 - 10
    cx, cy = size[0] // 2, size[1] // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(212, 175, 55), outline=(180, 140, 20), width=4)
    draw.multiline_text((cx, cy), label, fill=(30, 30, 30), anchor="mm", align="center")
    img.save(path)
    print(f"  Created: {path}")


print("Generating placeholder images...")
for i, (slug, label) in enumerate(STOPS):
    make_placeholder(f"{ASSETS_DIR}/{slug}_past.jpg", f"Past — {label}", COLORS_PAST[i])
    make_placeholder(f"{ASSETS_DIR}/{slug}_present.jpg", f"Present — {label}", COLORS_PRESENT[i])
    make_coin(f"{ASSETS_DIR}/{slug}_coin_front.png", COIN_LABELS[i], (40, 30, 10))
    make_coin(f"{ASSETS_DIR}/{slug}_coin_back.png", COIN_BACK[i], (0, 50, 40))

print("Done. Drop your real photos into /assets/ using the same filenames.")
