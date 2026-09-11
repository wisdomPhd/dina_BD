import streamlit as st
import time
import json
import os
from datetime import datetime
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

# -------------------- STYLE --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(255,120,180,.20), transparent 28%),
        radial-gradient(circle at 90% 80%, rgba(190,100,255,.16), transparent 30%),
        linear-gradient(145deg,#09020a 0%,#210817 48%,#10030f 100%);
    color: white;
}

/* Fixes the black background behind the Lottie animation iframe */
iframe {
    background-color: transparent !important;
    border: none !important;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
.hero { text-align:center; padding:25px 10px 5px; }
.script {
    font-family:'Great Vibes',cursive;
    font-size:clamp(58px,10vw,100px);
    line-height:1;
    color:#ffb8da;
    text-shadow:0 0 25px rgba(255,95,170,.45);
}
.kicker {
    font-family:'Poppins',sans-serif;
    letter-spacing:5px;
    text-transform:uppercase;
    font-size:12px;
    color:#eab8d1;
}
.card {
    background:rgba(255,255,255,.075);
    border:1px solid rgba(255,190,220,.18);
    border-radius:28px;
    padding:30px;
    margin:22px 0;
    box-shadow:0 18px 70px rgba(0,0,0,.28);
    backdrop-filter:blur(12px);
}
.countdown-title {
    text-align:center;
    font-family:'Poppins',sans-serif;
    color:#f6d7e7;
    font-size:15px;
}
.countdown {
    text-align:center;
    font-family:'Poppins',sans-serif;
    font-size:clamp(25px,6vw,45px);
    font-weight:600;
    color:#ffbadb;
    letter-spacing:3px;
    margin-top:8px;
}
.small {
    text-align:center;
    color:#cda8ba;
    font-family:'Poppins',sans-serif;
    font-size:13px;
}
.love-letter {
    font-family:'Poppins',sans-serif;
    color:#ffeaf4;
    line-height:2;
    font-size:16px;
}
.signature {
    font-family:'Great Vibes',cursive;
    font-size:42px;
    color:#ffb8d9;
    text-align:right;
}
.big-heart {
    text-align:center;
    font-size:44px;
    animation:beat 1.5s infinite;
}
@keyframes beat {
    0%,100% {transform:scale(1)}
    50% {transform:scale(1.16)}
}
.gift {
    text-align:center;
    font-size:90px;
    filter:drop-shadow(0 0 22px rgba(255,100,170,.35));
}
div.stButton > button {
    width:100%;
    border-radius:999px;
    min-height:52px;
    border:1px solid rgba(255,255,255,.18);
    background:linear-gradient(90deg,#ff4f9a,#b96bff);
    color:white;
    font-family:'Poppins',sans-serif;
    font-weight:600;
    font-size:16px;
    box-shadow:0 10px 30px rgba(255,70,160,.25);
}
.footer {
    text-align:center;
    color:#9e7188;
    font-family:'Poppins',sans-serif;
    font-size:12px;
    margin-top:35px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DINA --------------------

DINA_NAME = "Dina"
BIRTH_MONTH = 9
BIRTH_DAY = 12
BIRTH_YEAR = 2004

def next_birthday():
    now = datetime.now()
    year = now.year
    target = datetime(year, BIRTH_MONTH, BIRTH_DAY)
    if now >= target:
        year += 1
    return datetime(year, BIRTH_MONTH, BIRTH_DAY)

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
        half + 1*cm, 1.5*cm, half - 2*cm, height - 3*cm,
        20, fill=1, stroke=0
    )

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor("#D81B60"))
    c.drawCentredString(half + half/2, height - 4.5*cm, "Happy Birthday!")

    c.setFont("Helvetica-Bold", 21)
    c.setFillColor(HexColor("#7B1FA2"))
    c.drawCentredString(half + half/2, height - 7*cm, f"Dear {name}")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#00897B"))
    c.drawCentredString(half + half/2, 4*cm, f"{age} years ❤️")

    c.setFillColor(white)
    c.roundRect(
        1*cm, 1.5*cm, half - 2*cm, height - 3*cm,
        20, fill=1, stroke=0
    )

    c.setFont("Helvetica-Bold", 25)
    c.setFillColor(HexColor("#C2185B"))
    c.drawCentredString(half/2, height - 5*cm, f"{age} Years Young")

    c.setFont("Helvetica-Oblique", 15)
    c.setFillColor(HexColor("#5D4037"))
    c.drawCentredString(
        half/2, height - 7*cm, "A day made especially for you"
    )

    c.setFont("Helvetica", 11)
    text = c.beginText()
    text.setTextOrigin(half + 1.8*cm, height - 9*cm)
    text.setLeading(20)
    text.setFillColor(HexColor("#3E2723"))

    for line in message.split("\n"):
        text.textLine(line)

    c.drawText(text)

    c.setFont("Helvetica-Oblique", 12)
    c.setFillColor(HexColor("#8D6E63"))
    c.drawCentredString(half/2, 3*cm, "Made with love ❤️")

    c.setStrokeColor(HexColor("#DDC8D3"))
    c.setDash(4, 4)
    c.line(half, 1*cm, half, height - 1*cm)

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

target = next_birthday()
now = datetime.now()
remaining = target - now

days = remaining.days
hours = remaining.seconds // 3600
minutes = (remaining.seconds % 3600) // 60
seconds = remaining.seconds % 60
age_on_birthday = target.year - BIRTH_YEAR

# -------------------- HERO --------------------

st.markdown("""
<div class="hero">
    <div class="kicker">A little surprise for</div>
    <div class="script">Dina ❤️</div>
    <div class="small">September 12 • 2004</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="big-heart">♥</div>', unsafe_allow_html=True)

# -------------------- COUNTDOWN --------------------

st.markdown(f"""
<div class="card">
    <div class="countdown-title">Counting down to your special day 🎂</div>
    <div class="countdown">
        {days}d&nbsp;&nbsp;{hours:02d}h&nbsp;&nbsp;{minutes:02d}m&nbsp;&nbsp;{seconds:02d}s
    </div>
    <div class="small">
        September 12, {target.year} • You turn {age_on_birthday} ❤️
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- GIFT / SURPRISE --------------------

if "opened" not in st.session_state:
    st.session_state.opened = False

if not st.session_state.opened:
    st.markdown("""
    <div class="card">
        <div class="gift">🎁</div>
        <div class="countdown-title">
            Please do not open your little gift yet...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- THE PASSWORD LOGIC ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ⚠️ CHANGE YOUR SECRET PASSWORD HERE ⚠️
    SECRET_CODE = "midnight22" 
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input("Enter the secret code to open your gift 💌", type="password", key="password_input")
        
        if st.button("Unlock Surprise"):
            # Using .lower().strip() makes it so capitalization and accidental spaces don't break the code
            if user_input.lower().strip() == SECRET_CODE.lower():
                with st.spinner("Preparing something special for Dina..."):
                    time.sleep(1.5)
                st.session_state.opened = True
                st.balloons()
                st.rerun()
            elif user_input:
                st.error("Oops! That's not the right code. You'll have to wait until midnight! 😉")

else:
    st.balloons()

    st.markdown("""
    <div class="card">
        <div class="script" style="font-size:65px;text-align:center;">
            Happy Birthday
        </div>
        <div class="script" style="font-size:75px;text-align:center;">
            Dina ❤️
        </div>
        <div class="countdown-title">
            September 12 • 22 years young 🎂
        </div>
    </div>
    """, unsafe_allow_html=True)

    music_file = "happy_birthday.mp3"
    if os.path.exists(music_file):
        with open(music_file, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

    cake_animation = load_lottie_file("cake.json")
    if cake_animation is not None:
        st_lottie(cake_animation, height=300, key="birthday_cake")
    else:
        st.markdown('<div class="gift">🎂</div>', unsafe_allow_html=True)

    st.markdown("""<div class="card">
<div class="love-letter">
<b>My dear Dina,</b><br><br>
Today is a very special day because it is the day the world got you. ❤️<br><br>
I hope your 22nd year is filled with happiness, beautiful memories, laughter, and everything your heart wishes for.<br><br>
I want you to know that you are incredibly special to me. Your smile, your presence, and all the little moments we share mean more to me than I can put into a few words on a screen.<br><br>
On your birthday, I simply want to see you happy. Keep being the wonderful person you are, keep dreaming, keep smiling, and never forget how loved you are.<br><br>
Happy 22nd birthday, Dina. 🎂💗<br><br>
I hope this is only the beginning of another beautiful year of memories together.
<div class="signature">With all my love ❤️</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("### 📄 A little card to keep")

    pdf_message = """My dear Dina,

Today is a very special day because it is the day 
the world got you.

I hope your 22nd year is filled with happiness, 
beautiful memories, laughter, and everything your
heart wishes for.

You are incredibly special to me, 
and I hope this birthday becomes one 
of your favorite memories.

Happy 22nd birthday, Dina. ❤️

With all my love."""

    pdf = generate_birthday_pdf(DINA_NAME, 22, pdf_message)

    if pdf is not None:
        st.download_button(
            label="💗 Save Dina's birthday card as PDF",
            data=pdf,
            file_name="Dina_22nd_Birthday_Card.pdf",
            mime="application/pdf",
        )
    else:
        st.info("PDF export needs ReportLab. Run: pip install reportlab")

st.markdown(
    '<div class="footer">Made with ❤️ especially for Dina</div>',
    unsafe_allow_html=True
)