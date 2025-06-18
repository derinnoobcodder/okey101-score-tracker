import streamlit as st

st.set_page_config(page_title="Okey 101 Skor Takibi", layout="centered")

# Giriş alanları sadece ilk açılışta gösterilsin
if "giris_yapildi" not in st.session_state:
    st.title("🏁 Okey 101'e Hoş Geldiniz")

    st.session_state.t1 = st.text_input("Takım 1 Adı", value="Takım A")
    st.session_state.t2 = st.text_input("Takım 2 Adı", value="Takım B")
    st.session_state.max_rounds = st.number_input("Kaç oyun oynanacak?", min_value=1, max_value=50, value=13)

    if st.button("Oyunu Başlat"):
        st.session_state.giris_yapildi = True
        st.session_state.scores = {st.session_state.t1: 0, st.session_state.t2: 0}
        st.session_state.round = 1
        st.session_state.history = []
        st.rerun()
    st.stop()

# Ana oyun ekranı
t1 = st.session_state.t1
t2 = st.session_state.t2

st.title("🀄 Okey 101 Skor Takibi")
st.subheader(f"🎯 Tur: {st.session_state.round} / {st.session_state.max_rounds}")
st.markdown(f"### 🔴 {t1}: {st.session_state.scores[t1]} puan")
st.markdown(f"### 🔵 {t2}: {st.session_state.scores[t2]} puan")
st.markdown("---")

# Hızlı ceza
st.subheader("⚡ Hızlı Ceza Butonları")
el_puani = st.number_input("💠 Karşı takımın elinde kalan puan", min_value=0, value=0)

cezalar = [
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
for etiket, puan in cezalar:
    with col1:
        if st.button(f"{etiket} ({t1})", key=f"{etiket}_t1"):
            if etiket in ["Direkt bitti", "Çiftten bitti"]:
                st.session_state.scores[t2] += el_puani * 2
            elif etiket == "Okey vurdu":
                st.session_state.scores[t2] += el_puani * 4
            st.session_state.scores[t1] += puan
            st.rerun()

    with col2:
        if st.button(f"{etiket} ({t2})", key=f"{etiket}_t2"):
            if etiket in ["Direkt bitti", "Çiftten bitti"]:
                st.session_state.scores[t1] += el_puani * 2
            elif etiket == "Okey vurdu":
                st.session_state.scores[t1] += el_puani * 4
            st.session_state.scores[t2] += puan
            st.rerun()

st.markdown("---")

# Manuel puan ekle
st.subheader("✏️ Manuel Puan Ekle")
manuel_puan = st.number_input("Ek puan:", value=0)
hedef_takim = st.radio("Kime eklenecek?", options=[t1, t2])
if st.button("Puanı Ekle"):
    st.session_state.scores[hedef_takim] += manuel_puan
    st.rerun()

st.markdown("---")

# Tur bitirme
if st.button("✅ Turu Bitir"):
    st.session_state.history.append((st.session_state.round, st.session_state.scores[t1], st.session_state.scores[t2]))
    st.session_state.round += 1
    st.session_state.scores[t1] = 0
    st.session_state.scores[t2] = 0
    if st.session_state.round > st.session_state.max_rounds:
        toplam1 = sum([x[1] for x in st.session_state.history])
        toplam2 = sum([x[2] for x in st.session_state.history])
        if toplam1 < toplam2:
            kazanan = t1
        elif toplam2 < toplam1:
            kazanan = t2
        else:
            kazanan = None

        st.success("🏁 Oyun Bitti!")
        if kazanan:
            st.balloons()
            st.markdown(f"## 🏆 Kazanan Takım: **{kazanan}**")
        else:
            st.markdown("## 🤝 Beraberlik!")
    st.rerun()

# Skorları sıfırla
if st.button("🧹 Skorları Sıfırla"):
    st.session_state.scores = {t1: 0, t2: 0}
    st.rerun()

# Geçmiş tablo
if st.button("📋 Geçmişi Göster"):
    if st.session_state.history:
        st.subheader("🕓 Oyun Geçmişi")
        st.table([{ "Tur": tur, t1: s1, t2: s2 } for tur, s1, s2 in st.session_state.history])
    else:
        st.info("Henüz tur oynanmadı.")
