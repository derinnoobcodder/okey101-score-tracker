# okey101_streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🀄 Okey 101 Skor Takip Uygulaması (Web Sürüm)")

# --- Giriş Aşaması ---
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.team1 = ""
    st.session_state.team2 = ""
    st.session_state.max_rounds = 13
    st.session_state.scores = []
    st.session_state.current_score = {"team1": 0, "team2": 0}

if not st.session_state.started:
    with st.form("Takım Girişi"):
        st.header("🎯 Takım ve Oyun Ayarları")
        t1 = st.text_input("Takım 1 Adı")
        t2 = st.text_input("Takım 2 Adı")
        rounds = st.number_input("Kaç Oyun Oynanacak?", min_value=1, max_value=50, value=13)
        submitted = st.form_submit_button("Oyunu Başlat")

        if submitted and t1 and t2:
            st.session_state.started = True
            st.session_state.team1 = t1
            st.session_state.team2 = t2
            st.session_state.max_rounds = rounds
            st.rerun()

# --- Oyun Ekranı ---
if st.session_state.started:
    t1 = st.session_state.team1
    t2 = st.session_state.team2
    max_rounds = st.session_state.max_rounds
    current = st.session_state.current_score

    st.header(f"🔢 Skorlar: {t1} - {current['team1']} | {t2} - {current['team2']}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{t1} İçin İşlemler")
        with st.form(f"form1"):
            penalty = st.number_input("Ceza/Puan Ekle (Pozitif = Ceza, Negatif = Bitirme)", key="penalty1")
            submitted1 = st.form_submit_button("Ekle")
            if submitted1:
                current['team1'] += penalty
                st.success(f"{t1} puanı güncellendi.")

    with col2:
        st.subheader(f"{t2} İçin İşlemler")
        with st.form(f"form2"):
            penalty = st.number_input("Ceza/Puan Ekle (Pozitif = Ceza, Negatif = Bitirme)", key="penalty2")
            submitted2 = st.form_submit_button("Ekle")
            if submitted2:
                current['team2'] += penalty
                st.success(f"{t2} puanı güncellendi.")

    st.divider()
    st.subheader("⚡ Otomatik Ceza Butonları")
    col1, col2, col3 = st.columns(3)

    def apply_penalty(team, amount, multiplier=0):
        opp_team = 'team2' if team == 'team1' else 'team1'
        extra = 0
        if multiplier:
            extra = st.number_input("Karşı takımın elinde kalan puan:", min_value=0, key=f"extra_{team}_{amount}")
            current[opp_team] += extra * multiplier
        current[team] += amount

    with col1:
        if st.button("Okey Alma (-101)"):
            apply_penalty("team1", -101)
        if st.button("İşleyerek Bitti (-101)"):
            apply_penalty("team1", -101)
        if st.button("7 Çift Açtı (-101)"):
            apply_penalty("team1", -101)

    with col2:
        if st.button("Direkt Bitti (-202, Rakibe 2x)"):
            apply_penalty("team1", -202, 2)
        if st.button("Çiftten Bitti (-202, Rakibe 2x)"):
            apply_penalty("team1", -202, 2)
        if st.button("51 Üzeri Açtı (-101)"):
            apply_penalty("team1", -101)

    with col3:
        if st.button("Okey Vurdu (-404, Rakibe 4x)"):
            apply_penalty("team1", -404, 4)
        if st.button("Açılım Olmadı (+404)"):
            apply_penalty("team1", 404)

    st.divider()
    col4, col5 = st.columns(2)
    if col4.button("Turu Bitir"):
        st.session_state.scores.append((current['team1'], current['team2']))
        st.session_state.current_score = {"team1": 0, "team2": 0}
        if len(st.session_state.scores) >= max_rounds:
            st.success("Oyun tamamlandı! 🎉")
    if col5.button("Skorları Sıfırla"):
        st.session_state.current_score = {"team1": 0, "team2": 0}

    st.divider()
    st.subheader("📊 Oyun Tablosu")
    if st.session_state.scores:
        df = pd.DataFrame(st.session_state.scores, columns=[t1, t2])
        df.index = [f"Tur {i+1}" for i in range(len(df))]
        df.loc["Toplam"] = df.sum(numeric_only=True)
        st.dataframe(df, height=400)

        if len(st.session_state.scores) >= max_rounds:
            toplam1 = df[t1][:-1].sum()
            toplam2 = df[t2][:-1].sum()
            kazanan = t1 if toplam1 < toplam2 else t2
            st.success(f"🏆 Şampiyon: {kazanan}!")
