# MDS-Project-II---Kelompok-1
# 🧠 THE University Rankings Intelligence  
### Visualizing Global Academic Performance & Sustainability Commitments  
> _“Data-informed education for a sustainable future.”_

---

## 📚✨ Deskripsi Proyek

Proyek ini menyajikan **visualisasi interaktif** dan **analisis cerdas** terhadap data pemeringkatan universitas dunia dari *Times Higher Education (THE)*, mencakup **World University Rankings** dan **Impact Rankings** yang fokus pada kontribusi universitas terhadap **Sustainable Development Goals (SDGs)**.

---

💡 Data mencakup:  
**🌍 World University Rankings** & **🌱 Impact Rankings**,  
yang menyoroti kontribusi universitas dalam mencapai **Sustainable Development Goals (SDGs)**.

---

🎯 **Ditujukan bagi:**  

🎓 Universitas  🏛️ Pemerintah  🔬 Peneliti  👥 Masyarakat Umum

---

### 📌 Tujuan Proyek

- 🔍 Memahami tren & pola peringkat universitas di level global dan nasional
- 🌱 Menggali kontribusi institusi terhadap pembangunan berkelanjutan
- 🧠 Mengidentifikasi faktor-faktor utama* yang memengaruhi peringkat akademik
- 🗺️ Memberikan insight strategis untuk kebijakan & perencanaan pendidikan tinggi

---

## 🚀 Fitur Utama

📊 **Visualisasi Data Interaktif**  
Menyajikan data peringkat universitas dengan berbagai fitur unggulan berikut:

---

| 🔍 Fitur                        | ✨ Deskripsi Singkat                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------|
| 🌐 **Distribusi Global**       | Peta dunia interaktif & grafik batang jumlah universitas serta kontribusi terhadap SDGs. |
| 🏫 **Profil Universitas**      | Informasi lengkap indikator: Teaching, Research, Citation, International Outlook, SDGs.  |
| 📈 **Tren Ranking Tahunan**    | Visualisasi performa universitas dari 2018 hingga 2025 dalam bentuk line chart.         |
| ♻️ **Analisis SDGs**           | Menyoroti kontribusi kampus terhadap pencapaian tujuan pembangunan berkelanjutan.       |
| 🇮🇩 **Sorotan Univ Indonesia**       | Fokus pada posisi & capaian universitas Indonesia dalam konteks global.                |

---


---

## 🤖 Analisis Machine Learning

- **Clustering Universitas**  
  Mengelompokkan universitas berdasarkan indikator performa untuk memahami pola kemiripan.

- **SHAP + Random Forest**  
  Analisis feature importance untuk mengidentifikasi faktor paling berpengaruh dalam penentuan ranking.

- **PCA Visualization**  
  Visualisasi posisi universitas dalam ruang berdimensi rendah berdasarkan kesamaan performa.

---

## 🤖 Prosedure Analisis
### Scraping
## 🕸️ Pengumpulan Data – Periode 2016–2025

Proyek ini mengandalkan proses **web scraping otomatis menggunakan Selenium** untuk mengambil data pemeringkatan universitas dari situs resmi *Times Higher Education (THE)* dan sumber terkait lainnya.

---

### 🔧 Teknologi yang Digunakan

- **Selenium**: Mengotomatiskan proses browsing dan pengambilan data.
- **ChromeDriver**: Menjalankan browser Google Chrome secara headless.
- **BeautifulSoup**: Membersihkan dan menstrukturkan elemen HTML.
- **Pandas**: Menyimpan hasil scraping ke dalam bentuk dataframe dan file CSV.

---

### 🗓️ Cakupan Data

Data yang dikumpulkan mencakup rentang waktu **2016 hingga 2025**, dengan elemen utama:
- 🎓 Nama Universitas & Negara
- 📊 Peringkat & Skor Total
- 📚 Skor indikator: *Teaching*, *Research*, *Citation*, *International Outlook*
- ♻️ Skor kontribusi terhadap *Sustainable Development Goals (SDGs)*

---

### Preprocessing
### MongoDB
### Agregasi dan Visualisasi


## 🧠 Strategic Policy Insights

| Insight Area                  | Potential Policy Use                                                                 |
|------------------------------|----------------------------------------------------------------------------------------|
| SDG Focus Gap in Indonesia   | Alihkan sumber daya ke SDGs yang kurang tergarap (Life Below Water, Peace & Justice). |
| Global Education Inequality  | Dorong diskursus dekolonialisasi ranking dan dukung institusi dari Global South.      |
| Feature Importance Analysis  | Panduan universitas dalam strategi peningkatan kinerja (citations, kolaborasi, dll). |
| Simulation of Rank Shifts    | Alat perencanaan skenario untuk kementerian dan pengambil kebijakan pendidikan.       |

---

## 💡 Future Development Ideas

- 🧠 **SDGs Strategy Optimizer**  
  Alat rekomendasi fokus SDGs berdasarkan profil institusi.

- 📄 **Research Publication**  
  Rencana publikasi di jurnal akademik bidang *education data science* atau *SDG policy*.

- 🎓 **Educational Curriculum Module**  
  Modul ajar untuk kurikulum *data science* atau *governance of higher education*.

---

## 🌐 Dashboard Interaktif

🔗 **[Demo Dashboard (Dummy Link)](https://streamlit.io/demo-the-rankings)**  
Dashboard Streamlit interaktif untuk eksplorasi data, analisis performa, dan tren SDGs.

---

## 📁 Struktur Proyek

├── /data # Dataset THE & data tambahan (World Bank, HDI, dll)
├── /notebooks # Notebook eksplorasi & machine learning
├── /scripts # Kode preprocessing dan analisis
├── /reports # Visualisasi, screenshot, dan dokumentasi
├── /app # Streamlit dashboard
├── requirements.txt # Daftar dependensi
└── README.md # Dokumentasi utama


---

## 📎 Dokumentasi & Presentasi

- 📄 **[Report Final (PDF)](https://bit.ly/report-the-rankings-intelligence)**  
- 📽️ **[Presentasi PPT](https://bit.ly/ppt-the-rankings-intelligence)**

---

## 👥 Tim Proyek

**THE University Rankings Intelligence Team:**

- 🧑‍💼 Ngurah Sentana  
- 🧑‍💼 Adib  
- 🧑‍💼 Awantara  
- 🧑‍💼 Uniq  
- 🧑‍💼 Desy  

---

## 📜 Lisensi

Proyek ini berlisensi MIT License – silakan digunakan dan dikembangkan dengan tetap menyebut sumber.

---

> 🌏 _“Ketika data berbicara, kebijakan menjadi lebih tajam. Ketika universitas berfokus pada SDGs, masa depan jadi lebih lestari.”_
