import os
import streamlit as st
from openai import OpenAI

# ==========================================
# SECURE CONFIGURATION (ANTI-LEAK PROTOCOL)
# ==========================================
# Ambil API Key dari brankas rahasia Streamlit Cloud
try:
    API_KEY = st.secrets.get("BLACKBOX_API_KEY", os.getenv("BLACKBOX_API_KEY"))
except FileNotFoundError:
    # Handle the case where the secrets.toml file doesn't exist
    API_KEY = os.getenv("BLACKBOX_API_KEY")

if not API_KEY:
    st.error("API Key tidak ditemukan! Set BLACKBOX_API_KEY di Streamlit secrets atau environment variables.")
    st.stop()

# Kurir: Library OpenAI. 
# Tujuan: Server Blackbox.
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.blackbox.ai"
)

# ==========================================
# FRONTEND: THE B2B INTERFACE
# ==========================================
st.set_page_config(page_title="Quant-Script AI | By Warlord", page_icon="⚡", layout="centered")

st.title("⚡ Quant-Script Generator (Claude Engine)")
st.markdown("Mesin kompilasi otonom. Ubah logika trading manusia menjadi **Pine Script v5** untuk TradingView.")

user_strategy = st.text_area(
    "Deskripsikan algoritma trading lo:", 
    placeholder="Contoh: Long jika EMA 20 cross over EMA 50 dan volume > rata-rata 20 hari. Take profit 5%, Stop Loss 2%.",
    height=150
)

def generate_pine_script(client, strategy_text):
    """Fungsi terpisah untuk menangani logika inference API."""
    system_prompt = """
    Lo adalah Senior Quantitative Developer.
    Tugas lo mengubah input user menjadi kode Pine Script v5 yang valid, efisien, dan siap pakai.
    Sertakan plot di chart dan fungsi risk management (TP/SL).
    HANYA BERIKAN KODE DALAM CODE BLOCK. Dilarang memberikan basa-basi, intro, atau outro.
    """
    try:
        completion = client.chat.completions.create(
            model="claude-sonnet-4.5-20240514", # Memperbaiki penamaan model Claude yang tidak wajar
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": strategy_text}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


if st.button("Generate Algoritma 🚀"):
    if not user_strategy:
        st.warning("Input kosong. Jangan buang-buang compute, NPC!")
    else:
        with st.spinner("Mengkompilasi logika via Claude Sonnet..."):
            generated_code, error = generate_pine_script(client, user_strategy)
            
            if error:
                st.error(f"System Failure / API Error: {error}")
            else:
                st.success("Kompilasi Sukses. Eksekusi di TradingView lo.")
                st.code(generated_code, language="pine")

st.markdown("---")
st.caption("Architecture by Timothy Ronald Protocol | Powered by Blackbox/Claude")
