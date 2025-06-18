import streamlit as st

st.set_page_config(page_title="Okey 101 Skor Takibi", layout="centered")

# Takım adlarını ve oyun sayısını alma
if "t1" not in st.session_state:
    st.session_state.t1 = st.text_input("Takım 1 Adı", value="Takım A")
else:
    st.text_input("Takım 1 Adı", value=st.session_state.t1, key="t1_display", disabled=True)

if "t2" not in st.session_state:
    st.session_state.t2 = st.text_input("Takım 2 Adı", value="Takım B")
else:
    st.text_input("Takım 2 Adı", value=st.session_state.t2, key="t2_display", disabled=True)

if "max_rounds" not in st.session_state:
    st.session_state.max_rounds = st.number_input("Kaç oyun oynanacak?", min_value=1, max_value=50, value=13)
else:
    st.number_input("Kaç oyun oynanacak?", min_value=1, max_value=50, value=st.session_state.max_rounds, disabled=True)

# Takım isimleri
t1 = st.session_state.t1
t2 = st.session_state.t2

# Skorları session_state'te tut
if "scores" not in st.session_state:
    st.session_state.scores = {t1: 0, t2: 0}
if "round" not in st.session_state:
    st.session_state.round = 1
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🀄 Okey 101 Skor Takibi")
st.markdown("---")

# Skorlar
t1_score = st.session_state.scores.get(t1, 0)
t2_score = st.session_state.scores.get(t2, 0)

st.subheader("📊 Skorlar")
st.write(f"**{t1}:** {t1_score} puan")
st.write(f"**{t2}:** {t2_score} puan")

st.markdown("---")

# Ceza butonları
st.subheader("⚡ Hızlı Ceza Butonları")

el_puani = st.number_input("💠 Karşı takımın elinde kalan puan:", min_value=0, value=0, step=1)

ceza_butonlari = [
    ("Okey alma", -101),
    ("İşleyerek bitti", -101),
    ("7 çift açtı", -101),
    ("51 üzeri açtı", -101),
    ("Direkt bitti", -202),
    ("Çiftten bitti", -202),
    ("Okey vurdu", -404),
    ("Açılım olmadı", 404)
]

col1, col2 = st.columns(2)

for etiket, puan in ceza_butonlari:
    with col1:
        if st.button(f"{etiket} ({t1})", key=f"{etiket}_{t1}"):
            if etiket in ["Direkt bitti", "Çiftten bitti"]:
                st.session_state.scores[t2] = st.session_state.scores.get(t2, 0) + el_puani * 2
            elif etiket == "Okey vurdu":
                st.session_state.scores[t2] = st.session_state.scores.get(t2, 0) + el_puani * 4
            st.session_state.scores[t1] = st.session_state.scores.get(t1, 0) + puan
            st.rerun()

    with col2:
        if st.button(f"{etiket} ({t2})", key=f"{etiket}_{t2}"):
            if etiket in ["Direkt bitti", "Çiftten bitti"]:
                st.session_state.scores[t1] = st.session_state.scores.get(t1, 0) + el_puani * 2
            elif etiket == "Okey vurdu":
                st.session_state.scores[t1] = st.session_state.scores.get(t1, 0) + el_puani * 4
            st.session_state.scores[t2] = st.session_state.scores.get(t2, 0) + puan
            st.rerun()

st.markdown("---")

# Manuel ekleme
st.subheader("✏️ Manuel Puan Ekle")
manuel_puan = st.number_input("Eklemek istediğiniz puanı girin:", value=0)
man_takim = st.radio("Hangi takıma eklemek istiyorsunuz?", options=[t1, t2])
if st.button("Puanı Ekle"):
    st.session_state.scores[man_takim] = st.session_state.scores.get(man_takim, 0) + manuel_puan
    st.rerun()

st.markdown("---")

# Tur bitirme
if st.button("✅ Turu Bitir"):
    st.session_state.history.append((st.session_state.round, t1_score, t2_score))
    st.session_state.round += 1
    st.session_state.scores = {t1: 0, t2: 0}
    st.rerun()

# Skorları sıfırla
if st.button("🧹 Skorları Sıfırla"):
    st.session_state.scores = {t1: 0, t2: 0}
    st.rerun()

# Geçmişi göster
st.markdown("---")
if st.button("📋 Geçmişi Göster"):
    st.subheader("🕓 Oyun Geçmişi")
    if st.session_state.history:
        st.table(
            [{"Tur": tur, t1: s1, t2: s2} for tur, s1, s2 in st.session_state.history]
        )
    else:
        st.info("Henüz oynanmış tur yok.")
