import streamlit as st
import time
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from io import BytesIO

# Optional PDF support
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor, white
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Optional Lottie support
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

st.set_page_config(
    page_title="For Dina ❤️",
    page_icon="💗",
    layout="centered",
)

# -------------------- CONFIG & TIMEZONE --------------------

DINA_NAME = "Dina"
BIRTH_MONTH = 9
BIRTH_DAY = 12
BIRTH_YEAR = 2004

APP_TIMEZONE = ZoneInfo("Africa/Algiers")

# -------------------- STYLE --------------------

st.markdown(
    """

""",
    unsafe_allow_html=True,
)

# -------------------- FUNCTIONS --------------------

def next_birthday(tz):
    now = datetime.now(tz)
    year = now.year
    target = datetime(year, BIRTH_MONTH, BIRTH_DAY, tzinfo=tz)
    if now >= target:
        target = datetime(year + 1, BIRTH_MONTH, BIRTH_DAY, tzinfo=tz)
    return target

def generate_birthday_pdf(name, age, message):
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    half = width / 2

    c.setFillColor(HexColor("#FFF7FB"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColor(white)
    c.roundRect(
        half + 1 * cm, 1.5 * cm, half - 2 * cm, height - 3 * cm, 20, fill=1, stroke=0
    )

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor("#D81B60"))
    c.drawCentredString(half + half / 2, height - 4.5 * cm, "Happy Birthday!")

    c.setFont("Helvetica-Bold", 21)
    c.setFillColor(HexColor("#7B1FA2"))
    c.drawCentredString(half + half / 2, height - 7 * cm, f"Dear {name}")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#00897B"))
    c.drawCentredString(half + half / 2, 4 * cm, f"{age} years ❤️")

    c.setFillColor(white)
    c.roundRect(1 * cm, 1.5 * cm, half - 2 * cm, height - 3 * cm, 20, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 25)
    c.setFillColor(HexColor("#C2185B"))
    c.drawCentredString(half / 2, height - 5 * cm, f"{age} Years Young")

    c.setFont("Helvetica-Oblique", 15)
    c.setFillColor(HexColor("#5D4037"))
    c.drawCentredString(half / 2, height - 7 * cm, "A day made especially for you")

    c.setFont("Helvetica", 11)
    text = c.beginText()
    text.setTextOrigin(half + 1.8 * cm, height - 9 * cm)
    text.setLeading(20)
    text.setFillColor(HexColor("#3E2723"))

    for line in message.split("\n"):
        text.textLine(line)

    c.drawText(text)

    c.setFont("Helvetica-Oblique", 12)
    c.setFillColor(HexColor("#8D6E63"))
    c.drawCentredString(half / 2, 3 * cm, "Made with love ❤️")

    c.setStrokeColor(HexColor("#DDC8D3"))
    c.setDash(4, 4)
    c.line(half, 1 * cm, half, height - 1 * cm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def load_lottie_file(path):
    if not LOTTIE_AVAILABLE or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# -------------------- COUNTDOWN --------------------

target = next_birthday(APP_TIMEZONE)
now = datetime.now(APP_TIMEZONE)
remaining = target - now

days = remaining.days
hours = remaining.seconds // 3600
minutes = (remaining.seconds % 3600) // 60
seconds = remaining.seconds % 60
age_on_birthday = target.year - BIRTH_YEAR

# -------------------- HERO --------------------

st.markdown(
    """
