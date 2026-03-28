import streamlit as st
from openai import OpenAI

# ==========================================
# SECURE CONFIGURATION (ANTI-LEAK PROTOCOL)
# ==========================================
# Ambil API Key dari brankas rahasia Streamlit Cloud
try:
    API_KEY = st.secrets["BLACKBOX_API_KEY"]
except:
    # Fallback murni buat tes lokal di VS Code lo SEBELUM di-push.
    # KOSONGKAN string ini sebelum lo ketik 'git commit'!
    API_KEY = "sk-EhP7zKwDDqS0vqN8aBpGhA"

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

if st.button("Generate Algoritma 🚀"):
    if not user_strategy:
        st.warning("Input kosong. Jangan buang-buang compute, NPC!")
    else:
        with st.spinner("Mengkompilasi logika via Claude Sonnet..."):
            
            # System Prompt = Aturan main absolut buat AI
            system_prompt = """
            Lo adalah Senior Quantitative Developer. 
            Tugas lo mengubah input user menjadi kode Pine Script v5 yang valid, efisien, dan siap pakai.
            Sertakan plot di chart dan fungsi risk management (TP/SL).
            HANYA BERIKAN KODE DALAM CODE BLOCK. Dilarang memberikan basa-basi, intro, atau outro.
            """
            
            try:
                # ==========================================
                # THE INFERENCE (Eksekusi Otak Claude via Blackbox)
                # ==========================================
                completion = client.chat.completions.create(
                    model="claude-sonnet-4-5-20250514", # Otak Claude sesuai tes Colab lo
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_strategy}
                    ],
                    temperature=0.1 # Presisi tinggi, nol halusinasi
                )
                
                generated_code = completion.choices[0].message.content
                
                st.success("Kompilasi Sukses. Eksekusi di TradingView lo.")
                st.code(generated_code, language="pine")
                
            except Exception as e:
                st.error(f"System Failure / API Error: {e}")

st.markdown("---")
st.caption("Architecture by Timothy Ronald Protocol | Powered by Blackbox/Claude")