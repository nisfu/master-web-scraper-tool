import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Master Scraper Tool", page_icon="🚀")

st.title("🚀 Master Web Scraper")
st.write("Masukkan URL apa saja, dan robot akan mencoba mengambil data link serta judulnya.")

# --- INPUT URL ---
target_url = st.text_input("Masukkan URL Website (Sertakan https://):", placeholder="https://example.com")

# --- PILIHAN ELEMENT ---
st.sidebar.header("Pengaturan Scraper")
limit_data = st.sidebar.slider("Batas Jumlah Data:", 5, 100, 20)
search_type = st.sidebar.selectbox("Apa yang ingin dicari?", ["Judul & Link (Auto)", "Hanya Judul (H1-H3)", "Semua Link"])

if st.button("Mulai Scraping"):
    if not target_url:
        st.warning("Silakan masukkan URL terlebih dahulu!")
    else:
        with st.spinner('Menghubungi server...'):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
                
                response = requests.get(target_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    data_list = []

                    # LOGIKA MASTER: Mencari elemen secara generik
                    if "Judul" in search_type:
                        # Mencari di semua tag heading
                        for tag in ['h1', 'h2', 'h3']:
                            elements = soup.find_all(tag, limit=limit_data)
                            for el in elements:
                                text = el.get_text().strip()
                                link = el.find('a')['href'] if el.find('a') else "Tidak ada link"
                                if text:
                                    data_list.append({"Tipe": tag.upper(), "Konten": text, "Link": link})

                    elif "Link" in search_type:
                        links = soup.find_all('a', href=True, limit=limit_data)
                        for link in links:
                            data_list.append({"Tipe": "LINK", "Konten": link.text.strip() or "Tanpa Teks", "Link": link['href']})

                    # Tampilkan Hasil
                    if data_list:
                        df = pd.DataFrame(data_list)
                        st.success(f"Ditemukan {len(df)} data!")
                        st.table(df) # Menggunakan table agar lebih rapi untuk demo
                        
                        # Download Button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Hasil", csv, "scraped_data.csv", "text/csv")
                    else:
                        st.error("Gagal mengekstrak data. Website mungkin menggunakan proteksi tinggi (JavaScript Rendered).")
                
                else:
                    st.error(f"Website menolak akses (Status Code: {response.status_code})")

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Gunakan alat ini untuk website berita, blog, atau direktori publik.")