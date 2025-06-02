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

![AlurMDSProjekII](https://github.com/user-attachments/assets/1a150d5c-2955-44f2-8b00-109677a165fb)

Proyek ini mencakup empat tahapan utama: **Scraping**, **Penggunaan MongoDB**, **Agregasi**, dan **Visualisasi**. Data peringkat universitas dikumpulkan secara otomatis melalui teknik scraping dari situs web dengan hasil berupa format tabular. Setelah itu, data dibersihkan dan ditransformasi ke format BSON agar dapat disimpan di **MongoDB**. Di dalam MongoDB, data dibuat menjadi database dan kemudian digunakan Python dalam proses **agregasi** dan **clustering** untuk menghasilkan informasi yang lebih terstruktur. Hasil akhir kemudian disajikan dalam bentuk **visualisasi** agar pola dan insight dari data dapat dipahami secara mudah dan informatif.


### Scraping
Scraping adalah proses otomatis untuk mengambil data dari sebuah situs web menggunakan program atau skrip tertentu. Dalam konteks proyek ini, scraping digunakan untuk mengambil data peringkat universitas yang tersedia dalam bentuk tabel di halaman web. Dengan scraping, data yang ditampilkan secara visual di situs web bisa diubah menjadi format terstruktur (seperti DataFrame atau file Excel) sehingga dapat digunakan untuk analisis lebih lanjut.

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
Tahap **preprocessing** dalam proyek ini berperan penting dalam menyiapkan data sebelum dimasukkan ke dalam database MongoDB. Proses ini dimulai dengan **menggabungkan beberapa file Excel** yang berisi data peringkat universitas dari berbagai sumber atau periode. Setelah penggabungan, dilakukan proses **pembersihan data** (data cleaning), seperti menghapus duplikasi, memperbaiki format kolom, serta memastikan konsistensi dan kelengkapan informasi. Setelah data rapi dan siap digunakan, langkah selanjutnya adalah **mentransformasikan format data Excel ke format BSON (Binary JSON)**. Format ini digunakan agar data dapat disimpan dan diproses secara efisien di dalam MongoDB, yang merupakan basis data berbasis dokumen. Dengan preprocessing yang baik, data menjadi lebih terstruktur, bersih, dan kompatibel untuk tahap-tahap berikutnya seperti agregasi dan visualisasi.

### MongoDB
Pada tahap **MongoDB**, perannya difokuskan sebagai **media penyimpanan data** hasil preprocessing. Data yang telah dirapikan dan ditransformasikan ke dalam format BSON dimasukkan ke dalam **koleksi** di MongoDB untuk disimpan secara terstruktur. MongoDB tidak digunakan untuk proses analisis atau agregasi langsung, melainkan hanya sebagai **data warehouse** yang menyimpan dokumen-dokumen peringkat universitas.
Setelah data tersimpan, proses **agregasi dilakukan di Python** dengan mengambil data kembali dari MongoDB menggunakan library seperti `pymongo`. Data yang di-*fetch* ke dalam Python dikonversi menjadi DataFrame, lalu dilakukan agregasi, clustering, dan analisis lainnya secara langsung di lingkungan Python. Dengan demikian, MongoDB berfungsi sebagai tempat penyimpanan terpusat, sementara seluruh proses analitik tetap dilakukan di Python.

### Agregasi dan Visualisasi
Secara umum, tahap **agregasi** dalam proyek ini bertujuan untuk merangkum dan menyederhanakan data peringkat universitas yang telah diambil dari MongoDB. Proses ini mencakup pengelompokan data, perhitungan statistik seperti rata-rata atau jumlah, serta penyusunan data berdasarkan kategori tertentu seperti negara, wilayah, atau peringkat. Agregasi dilakukan di Python agar data lebih siap untuk dianalisis dan divisualisasikan. Selanjutnya, tahap **visualisasi** digunakan untuk menyajikan hasil agregasi dalam bentuk grafik yang informatif dan mudah dipahami. Beragam jenis visualisasi digunakan, seperti bar chart, pie chart, scatter plot, dan lain-lain, untuk menggambarkan pola, tren, dan perbandingan antaruniversitas atau antarindikator. Visualisasi ini membantu menyampaikan insight yang diperoleh dari data secara lebih efektif kepada pengguna atau pembaca.

## DASHBOARD VISUALISASI
### Beranda 
Halaman **Beranda** menampilkan gambaran umum proyek visualisasi *University Rankings 2025* hasil kolaborasi Times Higher Education dan IPB University. Di bagian atas terdapat judul dan latar mahasiswa wisuda yang memperkuat kesan akademik. Tersedia ringkasan data berupa jumlah universitas (3311), negara (135), tahun rilis (2025), dan indikator SDGs (17). Empat dropdown interaktif disediakan untuk menjelaskan tren posisi universitas, faktor performa, peran SDGs, dan strategi peningkatan. Di bagian bawah, ditampilkan cuplikan visualisasi berupa peta sebaran universitas terbaik secara global dan analisis performa negara berdasarkan jumlah universitas dan skor rata-rata.
![Untitled design_page-0001](https://github.com/user-attachments/assets/91961cd7-d5bb-4515-ba90-38cb08e52085)





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
