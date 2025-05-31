import streamlit as st
from pymongo import MongoClient
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import interact
import plotly.express as px
import numpy as np
from math import pi
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import shap
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from minisom import MiniSom
import hdbscan
import matplotlib.patches as mpatches



# ======= CONFIG PAGE =======
st.set_page_config(page_title="THE University Rankings Intelligence", layout="wide")


# ======= CSS STYLING =======
st.markdown("""
<style>
/* Sidebar full width buttons */
[data-testid="stSidebar"] button {
    width: 100% !important;
    margin-bottom: 8px;
    font-size: 16px;
    padding: 12px 10px;
    text-align: left;
    border-radius: 6px;
    background-color: #e0e0e0; /* Light gray */
    color: #333; /* Dark text */
    border: none;
    transition: background-color 0.3s ease;
}
[data-testid="stSidebar"] button:hover {
    background-color: #b0b0b0; /* Darker gray on hover */
    cursor: pointer;
}


/* Sidebar container padding */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 20px;
}


/* Header styling */
header {
    background-color: #004d40;
    color: white;
    padding: 16px 24px;
    font-weight: 700;
    font-size: 26px;
    text-align: center;
    border-radius: 0 0 10px 10px;
    margin-bottom: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


/* Footer styling */
footer {
    background-color: #004d40;
    color: white;
    padding: 10px 24px;
    font-weight: 500;
    font-size: 14px;
    text-align: center;
    border-radius: 10px 10px 0 0;
    margin-top: 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


/* Body text styling */
body, .stApp {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #fdfdfd;
    color: #333;
}


/* Dark mode overrides */
.dark-mode body, .dark-mode .stApp {
    background-color: #121212 !important;
    color: #eee !important;
}
.dark-mode header, .dark-mode footer {
    background-color: #00332c !important;
}


/* Statistik card */
.stat-card {
    background-color: #e0f2f1;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    text-align: center;
    margin-bottom: 15px;
}
.dark-mode .stat-card {
    background-color: #004d40;
    color: #fff;
}


/* Foto slide styling */
.img-slide {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    max-width: 100%;
    margin: auto;
    display: block;
}
</style>
""", unsafe_allow_html=True)


# ======= LOAD DATA FROM MONGO =======
@st.cache_resource
def get_data():
    uri = "mongodb+srv://Ngurah:Ngurah123@worldrankuniversity.pl6s2eb.mongodb.net/"
    client = MongoClient(uri)
    db = client["WorldUniversityRanking"]
    universities = db["Universities"]
    impact = db["ImpactRank"]
    df_universities = pd.DataFrame(list(universities.find()))
    df_impact = pd.DataFrame(list(impact.find()))
    if "_id" in df_universities.columns:
        df_universities.drop(columns="_id", inplace=True)
    if "_id" in df_impact.columns:
        df_impact.drop(columns="_id", inplace=True)
    return df_universities, df_impact


df, df_impact = get_data()
uri = "mongodb+srv://Ngurah:Ngurah123@worldrankuniversity.pl6s2eb.mongodb.net/"
client = MongoClient(uri)
db = client["WorldUniversityRanking"]
universities = db["Universities"]
impact = db["ImpactRank"]


# ======= HEADER =======
st.markdown("<header> THE University Rankings Intelligence</header>", unsafe_allow_html=True)


# ======= SIDEBAR MENU =======
if 'page' not in st.session_state:
    st.session_state.page = "Beranda"


st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Times_Higher_Education_logo.svg/2560px-Times_Higher_Education_logo.svg.png", width=200)  # Ganti URL logo
st.sidebar.title("🏛️ Menu Navigasi")
if st.sidebar.button("Beranda"):
    st.session_state.page = "Beranda"
if st.sidebar.button("Negara"):
    st.session_state.page = "Negara"
if st.sidebar.button("Universitas"):
    st.session_state.page = "Universitas"
if st.sidebar.button("SDGs"):
    st.session_state.page = "SDGs"
if st.sidebar.button("Indonesia"):
    st.session_state.page = "Indonesia"
if st.sidebar.button("MongoDB"):
    st.session_state.page = "MongoDB"
if st.sidebar.button("Tim"):
    st.session_state.page = "Tim"


# ======= PAGE CONTENT =======
page = st.session_state.page

if page == "Beranda":
    with st.container():
      st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');

        .bg-container {
            position: relative;
            width: 100%;
            height: 400px;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 30px;
        }
        .bg-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 0;
        }
        .overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(0, 77, 64, 0.7), rgba(0, 121, 107, 0.7));
            z-index: 1;
        }
        .text-content {
            position: relative;
            z-index: 2;
            color: white;
            padding: 30px;
            height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            font-family: 'Poppins', sans-serif;
        }
        .text-content h1 {
            font-size: 42px;
            font-weight: 700; /* Bold */
            margin: 0;
            line-height: 1;
        }
        .text-content p {
            font-size: 16px;
            margin-top: 10px;
        }
        </style>

        <div class="bg-container">
            <img src="https://cdn1.katadata.co.id/media/images/temp/2023/05/08/Ucapan_Selamat_Wisuda_Bahasa_Inggris-2023_05_08-12_25_48_2924ca6ca188a509eacb58b9f6b38036.jpg" class="bg-image" />
            <div class="overlay"></div>
            <div class="text-content">
                <h1>Universitas</h1>
                <h1>Ranking</h1>
                <h1>2025</h1>
                <p>Times Higher Education | IPB University</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Top 5 University Ranking 2025")

    def render_box_gradient(img_url, caption_text, height):
        st.markdown(f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 10px;
                overflow: hidden;
                height: {height}px;
                background-image: 
                    linear-gradient(to bottom, rgba(0,77,64,0.6), rgba(0,77,64,0.3)),
                    url('{img_url}');
                background-size: cover;
                background-position: center;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                padding: 20px;
            ">
                <p style="color: white; font-size: 20px; font-weight: bold; text-align: center; margin: 0;">
                    {caption_text}
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Layout utama
    col_main, col_side = st.columns([2, 3])

    with col_main:
        render_box_gradient(
            "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/oxford.jpg",
            "#1 Oxford University",
            height=800
        )

    with col_side:
        col_a, col_b = st.columns(2)
        with col_a:
            render_box_gradient("https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/MIT.png", "#2 MIT", 400)
            render_box_gradient("https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/prince.jpg", "#4 Princeton University", 400)

        with col_b:
            render_box_gradient("https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/harvard.jpg", "#3 Harvard University", 400)
            render_box_gradient("https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/cambrigde.jpg", "#5 University of Cambridge", 400)

 
    st.markdown("""
        <style>
        .stat-card {
            background: linear-gradient(to right, #004d40, #00695c);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-card h2 {
            margin: 0;
            font-size: 32px;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
        }
        .stat-card p {
            margin-top: 8px;
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="stat-card"><h2>{df["University"].nunique()}</h2><p>Universitas</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="stat-card"><h2>{df["Country"].nunique()}</h2><p>Negara</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="stat-card"><h2>{df["Year"].max()}</h2><p>Tahun Terbaru</p></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="stat-card"><h2>17</h2><p>SDG Metrics</p></div>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .about-section {
            max-width: 1000px;
            margin: 30px auto;
            background: linear-gradient(rgba(224, 242, 241, 0.9), rgba(178, 223, 219, 0.9)), 
                        url('https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/oxford.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 16px;
            padding: 40px;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 6px 18px rgba(0,0,0,0.1);
            border-left: 5px solid #00796b;
            position: relative;
            color: #333;
        }
        
        .about-section h2 {
            text-align: center;
            color: #004d40;
            font-size: 32px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 16px;
            margin-bottom: 25px;
            font-weight: 600;
            text-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .about-section h2 img {
            height: 80px;
            vertical-align: middle;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }
        
        .about-section p {
            font-size: 14px;
            line-height: 1.8;
            text-align: justify;
            margin-bottom: 20px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 15px;
            border-radius: 8px;
            backdrop-filter: blur(2px);
        }
        
        .highlight-box {
            background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(245, 245, 245, 0.85)), 
                      url('https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/oxford.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 12px;
            padding: 30px;
            margin: 40px auto;
            max-width: 900px;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border-top: 3px solid #00796b;
        }
        
        .highlight-box p {
            font-size: 14px;
            line-height: 1.8;
            text-align: justify;
            margin-bottom: 16px;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 15px;
            border-radius: 8px;
        }
        
        .highlight-box strong {
            color: #00796b;
            font-weight: 600;
        }
        </style>

        <div class="about-section">
            <h2>
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Times_Higher_Education_logo.svg/2560px-Times_Higher_Education_logo.svg.png" alt="THE" />
                THE World University Rankings
            </h2>
            <p>
            THE World University Rankings (Times Higher Education World University Rankings) adalah sistem pemeringkatan universitas dunia yang disusun setiap tahun oleh Times Higher Education (THE), sebuah lembaga yang berbasis di Inggris. Pemeringkatan ini bertujuan untuk menilai performa institusi pendidikan tinggi dari seluruh dunia berdasarkan kriteria yang ketat dan menyeluruh, seperti pengajaran (teaching), penelitian (research), sitasi atau pengaruh riset (citations), pendapatan dari industri (industry income), serta perspektif internasional (international outlook). Setiap indikator memiliki bobot tertentu yang dirancang untuk memberikan gambaran seimbang terhadap kekuatan akademik dan kontribusi global dari suatu universitas.
            </p>
            <p>
            THE World University Rankings menjadi rujukan penting bagi calon mahasiswa, akademisi, pemerintah, dan institusi untuk menilai reputasi dan kinerja universitas secara global. Selain peringkat umum, THE juga merilis peringkat berdasarkan bidang studi dan tujuan pembangunan berkelanjutan (SDGs) melalui THE Impact Rankings. Peringkat ini tidak hanya membantu universitas membandingkan posisinya dengan institusi lain, tetapi juga mendorong peningkatan kualitas pendidikan dan penelitian di tingkat global. Keberadaan THE Rankings juga menjadi salah satu faktor strategis dalam kebijakan internasionalisasi dan branding universitas.
            </p>
        </div>

        <div class="highlight-box">
            <p>
                Proyek ini menyajikan <strong>visualisasi interaktif</strong> dan <strong>analisis komprehensif</strong> terhadap data pemeringkatan universitas dunia dari <strong>Times Higher Education (THE)</strong>, mencakup <strong>World University Rankings</strong> dan <strong>Impact Rankings</strong> yang berfokus pada kontribusi universitas terhadap <strong>Sustainable Development Goals (SDGs)</strong>.
            </p>
            <p>
                Proyek ini dirancang untuk membantu <strong>universitas</strong>, <strong>pemerintah</strong>, <strong>peneliti</strong>, dan <strong>masyarakat luas</strong> dalam memahami data dan insight penting terkait performa global institusi pendidikan tinggi, serta memberikan perspektif baru dalam pengambilan keputusan strategis di bidang pendidikan tinggi.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # CSS Styles
    st.markdown("""
    <style>
        /* Expander styling */
        .expander-content {
            background-color: #f8f9fa;
            padding: 1.2rem;
            border-radius: 0 0 8px 8px;
            border-left: 4px solid #00796b;
        }
        .expander-content p {
            color: #333;
            font-size: 14px;
            line-height: 1.7;
            margin-bottom: 0;
        }
        
        /* Quote styling */
        .quote-container {
            background-color: #e0f2f1;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 2rem auto;
            max-width: 800px;
            text-align: center;
        }
        .quote-text {
            font-size: 1.3rem;
            font-weight: 600;
            color: #004d40;
            line-height: 1.6;
        }
        .quote-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
            color: #00796b;
        }
    </style>
    """, unsafe_allow_html=True)

    # Expanders in columns
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🔥 **Pola dan Tren Posisi Universitas**", expanded=False):
            st.markdown("""
            <div class="expander-content">
                <p>
                Pola dan tren posisi universitas dalam pemeringkatan global dan nasional mencerminkan dinamika kompetisi pendidikan tinggi yang semakin kompleks dan tersegmentasi.
                <br><br>
                Secara global, universitas-universitas terkemuka sering menunjukkan konsistensi dalam performa indikator utama seperti penelitian, pengajaran, dan kolaborasi internasional.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("🎯 **Peran Strategis dalam SDGs**", expanded=False):
            st.markdown("""
            <div class="expander-content">
                <p>
                Universitas tidak hanya berperan sebagai pusat akademik dan riset, tetapi juga sebagai agen perubahan sosial yang signifikan dalam mencapai tujuan pembangunan berkelanjutan (SDGs).
                <br><br>
                Dengan fokus pada Impact Rankings, universitas mengintegrasikan SDGs ke dalam strategi institusional mereka.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.expander("💡 **Faktor Penentu Performa**", expanded=False):
            st.markdown("""
            <div class="expander-content">
                <p>
                Berbagai faktor berkontribusi terhadap performa dan peringkat universitas dalam pemeringkatan internasional.
                <br><br>
                Indikator utama meliputi kualitas pengajaran, dampak penelitian, dan kemampuan menarik kolaborasi internasional.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📈 **Strategi Peningkatan Peringkat**", expanded=False):
            st.markdown("""
            <div class="expander-content">
                <p>
                Universitas dapat mengadopsi berbagai strategi untuk meningkatkan peringkat mereka.
                <br><br>
                Pendekatan berbasis data dapat membantu mengidentifikasi area yang membutuhkan perbaikan.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Quote section
    st.markdown("""
    <div class="quote-container">
        <p class="quote-text">
        <span class="quote-icon">🧭</span>
        Tidak hanya menampilkan data, tetapi membangun narasi transformasi pendidikan global.
        </p>
    </div>
    """, unsafe_allow_html=True)

   # Data Preparation
    pipeline = [
        {"$group": {
            "_id": "$Country",
            "count_universities": {"$sum": 1},
            "avg_Overall": {"$avg": "$Overall"},
            "top_university": {"$first": "$Name"}  # Assuming sorted by rank
        }},
        {"$sort": {"count_universities": -1}}
    ]

    data = list(universities.aggregate(pipeline))
    df_country = pd.DataFrame(data)
    df_country.rename(columns={
        "_id": "Country", 
        "count_universities": "Number of Universities",
        "avg_Overall": "Avg Overall",  # Ganti nama kolom disini
        "top_university": "Top University"
    }, inplace=True)

    # Create tabs for different views
    tab1, tab2 = st.tabs(["Peta Global", "Analisis Negara"])

    with tab1:
        # Enhanced Choropleth Map
        fig = px.choropleth(
            df_country,
            locations="Country",
            locationmode="country names",
            color="Number of Universities",
            color_continuous_scale="teal",
            hover_name="Country",
            hover_data={
                "Number of Universities": True,
                "Avg Overall": ":.1f",  # Update label disini
                "Top University": True,
                "Country": False
            },
            title="<b>Distribusi Global Universitas Terbaik</b><br><sub>Jumlah Universitas per Negara</sub>",
            labels={"Number of Universities": "Jumlah Universitas"},
            projection="natural earth"
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                landcolor='lightgray',
                lakecolor='#e0f2f1'
            ),
            margin={"r":0,"t":80,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title="Jumlah",
                thickness=20,
                len=0.75
            ),
            title_font=dict(size=20, color='#004d40'),
            font=dict(family="Poppins", color='#333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Country Analysis
        st.subheader("Analisis Performa Negara")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p style="font-size:16px; font-weight:normal; margin-bottom:10px;">Negara dengan Universitas Terbanyak</p>', unsafe_allow_html=True)
            top_countries = df_country.sort_values(by="Number of Universities", ascending=False).head(10)
            fig1 = px.bar(
                top_countries,
                x="Number of Universities",
                y="Country",
                orientation='h',
                color="Number of Universities",
                color_continuous_scale="teal",
                labels={"Number of Universities": "Jumlah Universitas"}
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("**Kuantitas vs Kualitas (Rata-rata Overall)**")
            fig2 = px.scatter(
                df_country.nlargest(20, "Number of Universities"),
                x="Number of Universities",
                y="Avg Overall",  # Ganti referensi kolom disini
                size="Number of Universities",
                color="Avg Overall",
                color_continuous_scale="teal_r",
                hover_name="Country",
                labels={
                    "Number of Universities": "Jumlah Universitas",
                    "Avg Overall": "Rata-rata Overall"  # Update label disini
                }
            )
            fig2.update_traces(
                marker=dict(line=dict(width=1, color='gray')),
                selector=dict(mode='markers')
            )
            st.plotly_chart(fig2, use_container_width=True)

elif page == "Negara":
    st.header("🌍 Analisis Berdasarkan Negara")


    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Jumlah Universitas",
        "Rata-rata Skor",
        "Distribusi Skor",
        "Top Metrics",
        "International vs Industry",
        "Peta Global"
        ,"Cluster"
    ])


    years = sorted([int(y) for y in df['Year'].unique()])


    def convert_year(year):
        return int(year)

    with tab1:
        st.subheader("🌍 Jumlah Universitas per Negara")

        # Pilih Tahun
        selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="top10_year")
        selected_year = convert_year(selected_year)

        # Pipeline: Ambil Top 10 Negara
        pipeline = [
            {"$match": {"Year": selected_year}},
            {"$group": {"_id": "$Country", "count_universities": {"$sum": 1}}},
            {"$sort": {"count_universities": -1}},
            {"$limit": 10}
        ]
        results = list(universities.aggregate(pipeline))
        df_top10 = pd.DataFrame(results).rename(columns={"_id": "Country"}) if results else pd.DataFrame(columns=["Country", "count_universities"])

        if df_top10.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            # === Barplot ===
            colors = sns.color_palette("Blues", n_colors=10)[::-1]
            palette_dict = dict(zip(df_top10['Country'], colors))
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=df_top10, y='Country', x='count_universities', hue='Country',
                        palette=palette_dict, dodge=False, legend=False, edgecolor='.3', ax=ax)
            for i, v in enumerate(df_top10['count_universities']):
                ax.text(v + 0.5, i, str(v), color='black')
            ax.set_title(f"Top 10 Negara dengan Jumlah Universitas Terbanyak - Tahun {selected_year}", fontsize=16)
            ax.set_xlabel("Jumlah Universitas")
            ax.set_ylabel("Negara")
            st.pyplot(fig)

            # === Top 3 Negara ===
            top3 = df_top10.head(3)
            st.markdown("### 🏆 Top 3 Negara dengan Universitas Terbanyak")

            cols = st.columns(3)
            clicked_country = None

            main_box_colors = [
                "background: linear-gradient(135deg, #a8e063, #56ab2f);",
                "background: linear-gradient(135deg, #7ec850, #3a6f1f);",
                "background: linear-gradient(135deg, #5a8c3b, #2f4d17);"
            ]
            name_box_text_colors = ["#2f4d17", "#274012", "#1f340f"]

            for i, (idx, row) in enumerate(top3.iterrows()):
                country = row['Country']

                with cols[i]:
                    # Kotak utama
                    st.markdown(
                        f"""
                        <div style="
                            {main_box_colors[i]}
                            border-radius: 20px;
                            padding: 20px;
                            text-align: center;
                            font-weight: bold;
                            font-size: 28px;
                            color: white;
                            user-select:none;
                            margin-bottom: 10px;
                        ">
                            #{i+1}
                            <div style="
                                margin-top: 15px;
                                background: linear-gradient(135deg, #c7f0a5, #88bf4a);
                                border-radius: 12px;
                                padding: 12px 20px;
                                font-size: 20px;
                                font-weight: 600;
                                color: {name_box_text_colors[i]};
                                cursor: pointer;
                                user-select:none;
                            " id="country-box-{i}">
                                {country}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button(f"Lihat Universitas {country}", key=f"show_table_{country}_{selected_year}"):
                        clicked_country = country

            # === Tabel Universitas: tampil setelah tombol ditekan ===
            if clicked_country:
                pipeline_univ = [
                    {"$match": {"Year": selected_year, "Country": clicked_country}},
                    {"$project": {"_id": 0, "University": 1, "Rank": 1, "Overall": 1}},
                    {"$sort": {"Rank": 1}}
                ]
                univ_results = list(universities.aggregate(pipeline_univ))

                if univ_results:
                    df_univ = pd.DataFrame(univ_results)
                    df_univ_display = df_univ.rename(columns={
                        "University": "Universitas",
                        "Overall": "Overall",
                        "Rank": "Rank"
                    })[["Rank", "Universitas", "Overall"]]

                    st.markdown(f"### 📚 Daftar Universitas di {clicked_country} Tahun {selected_year}")
                    st.dataframe(df_univ_display, use_container_width=True)
                else:
                    st.info(f"Tidak ada data universitas untuk {clicked_country} tahun {selected_year}")
    with tab2:
       # ---- HEADER SECTION ----
      st.subheader("📊 Rata-rata Overall Score per Negara")
      st.markdown("""<div style="height: 4px; background: linear-gradient(90deg, #4b6cb7, #182848); margin-bottom: 20px;"></div>""", 
                  unsafe_allow_html=True)

      # ---- YEAR SELECTION ----
      selected_year = st.selectbox(
          "Pilih Tahun", 
          years, 
          index=len(years)-1, 
          key="avg_overall_year"
      )
      selected_year = convert_year(selected_year)

      # ---- DATA PROCESSING ----
      pipeline = [
          {"$match": {"Year": selected_year, "Overall": {"$ne": None}}},
          {"$group": {
              "_id": "$Country", 
              "count_universities": {"$sum": 1}, 
              "avg_overall": {"$avg": "$Overall"}
          }},
          {"$sort": {"count_universities": -1}},
          {"$limit": 10}
      ]
      results = list(universities.aggregate(pipeline))
      df_avg = pd.DataFrame(results).rename(columns={"_id": "Country"}) if results else pd.DataFrame()

      # ---- VISUALIZATION ----
      if df_avg.empty:
          st.warning(f"⚠️ Tidak ada data Overall Score yang tersedia untuk tahun {selected_year}")
      else:
          df_avg = df_avg.sort_values(by="avg_overall", ascending=False)
          
          # Create gradient color palette
          n_countries = len(df_avg)
          colors = sns.color_palette("Blues_r", n_colors=n_countries)
          
          # Plot configuration
          fig, ax = plt.subplots(figsize=(12, 6))
          sns.barplot(
              data=df_avg, 
              y='Country', 
              x='avg_overall', 
              palette=colors,
              edgecolor='.2', 
              linewidth=0.5,
              ax=ax
          )
          
          # Value annotations
          for i, value in enumerate(df_avg["avg_overall"]):
              ax.text(
                  value + 0.02, 
                  i, 
                  f'{value:.2f}', 
                  color='black', 
                  va='center',
                  fontsize=10,
                  fontweight='bold'
              )
          
          # Styling
          ax.set_title(
              f"Rata-rata Overall Score 10 Negara Teratas ({selected_year})",
              fontsize=18,
              pad=20,
              fontweight='bold'
          )
          ax.set_xlabel("Skor Rata-rata", labelpad=10)
          ax.set_ylabel("")
          ax.set_xlim(0, df_avg["avg_overall"].max() + 0.5)
          ax.grid(axis='x', linestyle=':', alpha=0.6)
          sns.despine(left=True, bottom=True)
          
          # Display plot
          st.pyplot(fig)
          
          # ---- DATA TABLE ----
          with st.expander("🔍 Lihat Data Lengkap", expanded=False):
              # Format the display dataframe
              df_display = df_avg.copy()
              df_display = df_display.rename(columns={
                  "Country": "Negara",
                  "avg_overall": "Rata-rata Score",
                  "count_universities": "Jumlah Universitas"
              })
              df_display["Rata-rata Score"] = df_display["Rata-rata Score"].apply(lambda x: f"{x:.2f}")
              df_display["Peringkat"] = range(1, len(df_display)+1)
              
              # Reorder columns
              df_display = df_display[["Peringkat", "Negara", "Rata-rata Score", "Jumlah Universitas"]]
              
              # Display with conditional formatting
              st.dataframe(
                  df_display.style.background_gradient(
                      subset=["Rata-rata Score"],
                      cmap="Blues"
                  ),
                  use_container_width=True
              )

    with tab3:
        # ---- HEADER SECTION ----
        st.subheader("📦 Distribusi Skor Overall Universitas")
        st.markdown("""<div style="height: 4px; background: linear-gradient(90deg, #6a11cb, #2575fc); margin-bottom: 20px;"></div>""", 
                    unsafe_allow_html=True)

        # ---- YEAR SELECTION ----
        selected_year = st.selectbox(
            "Pilih Tahun", 
            years, 
            index=len(years)-1, 
            key="boxplot_year",
            help="Pilih tahun untuk melihat distribusi skor universitas"
        )
        selected_year = convert_year(selected_year)

        with st.spinner('Memproses data...'):
            # First get all countries with their data
            pipeline_all = [
                {"$match": {"Year": selected_year, "Overall": {"$ne": None}}},
                {"$group": {
                    "_id": "$Country",
                    "scores": {"$push": "$Overall"},
                    "count": {"$sum": 1}
                }}
            ]
            all_countries = list(universities.aggregate(pipeline_all))
            
            # Calculate median for each country in Python
            country_stats = []
            for country in all_countries:
                scores = sorted(country['scores'])
                n = len(scores)
                if n % 2 == 1:
                    median = scores[n//2]
                else:
                    median = (scores[n//2 - 1] + scores[n//2]) / 2
                
                country_stats.append({
                    "country": country['_id'],
                    "median": median,
                    "count": country['count'],
                    "mean": sum(scores)/len(scores)
                })
            
            # Sort by median and get top 15
            top_countries = sorted(country_stats, key=lambda x: x['median'], reverse=True)[:15]
            top_country_names = [c['country'] for c in top_countries]
            
            if not top_country_names:
                st.warning(f"⚠️ Tidak ada data untuk tahun {selected_year}")
                st.stop()
            
            # Get full data for visualization
            pipeline_data = [
                {"$match": {
                    "Year": selected_year, 
                    "Country": {"$in": top_country_names}, 
                    "Overall": {"$ne": None}
                }},
                {"$project": {"Country": 1, "Overall": 1, "_id": 0}}
            ]
            results = list(universities.aggregate(pipeline_data))
            df_data = pd.DataFrame(results) if results else pd.DataFrame()

        # ---- VISUALIZATION ----
        if df_data.empty:
            st.warning(f"⚠️ Tidak ada data Overall untuk negara-negara teratas di tahun {selected_year}")
        else:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📊 Visualisasi Boxplot", "📈 Statistik Detail"])
            
            with tab1:
                # Enhanced boxplot with proper styling
                plt.figure(figsize=(14, 8))
                
                # Create color palette
                colors = sns.color_palette("viridis", n_colors=len(top_country_names))
                
                # Plot boxplot with explicit styling parameters
                ax = sns.boxplot(
                    data=df_data, 
                    x='Overall', 
                    y='Country', 
                    order=top_country_names,
                    palette=colors,
                    width=0.7,
                    linewidth=1.5,
                    fliersize=3,
                    notch=False,  # Disabled notch to avoid potential issues
                    showmeans=True,  # Show mean markers
                    meanprops={"marker":"*", "markerfacecolor":"red", "markeredgecolor":"red", "markersize":"10"}
                )
                
                # Add swarmplot for data point distribution
                sns.swarmplot(
                    data=df_data,
                    x='Overall',
                    y='Country',
                    order=top_country_names,
                    color=".25",
                    size=3,
                    alpha=0.5
                )
                
                # Styling
                plt.title(
                    f"Distribusi Skor Overall Universitas - Top 15 Negara ({selected_year})",
                    fontsize=16,
                    pad=20,
                    fontweight='bold'
                )
                plt.xlabel('Skor Overall', labelpad=10)
                plt.ylabel('')
                plt.grid(axis='x', linestyle=':', alpha=0.6)
                sns.despine(left=True, bottom=True)
                
                st.pyplot(plt)
                
                # Interpretation note
                st.markdown("""
                <div style="
                    background-color: #f0f2f6;
                    border-radius: 8px;
                    padding: 12px;
                    margin-top: 15px;
                    font-size: 14px;
                ">
                    <b>Keterangan:</b> Kotak menunjukkan kuartil 25-75%, garis tengah menunjukkan median. 
                    Bintang (<span style="color:red">★</span>) menunjukkan nilai rata-rata.
                    Titik-titik menunjukkan distribusi data aktual.
                </div>
                """, unsafe_allow_html=True)
                
            with tab2:
                # Detailed statistics table
                st.markdown(f"### 📋 Statistik Deskriptif - {selected_year}")
                
                # Calculate statistics
                stats_df = df_data.groupby('Country')['Overall'].agg(
                    ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]
                ).rename(columns={
                    '<lambda_0>': 'Q1',
                    '<lambda_1>': 'Q3',
                    'count': 'Jumlah Univ',
                    'mean': 'Rata-rata',
                    'median': 'Median',
                    'min': 'Minimum',
                    'max': 'Maksimum',
                    'std': 'Std Dev'
                })
                
                # Format numbers
                stats_df = stats_df.style.format({
                    'Rata-rata': '{:.2f}',
                    'Median': '{:.2f}',
                    'Std Dev': '{:.2f}',
                    'Q1': '{:.2f}',
                    'Q3': '{:.2f}'
                })
                
                st.dataframe(
                    stats_df.background_gradient(
                        subset=['Rata-rata', 'Median'],
                        cmap='YlGnBu'
                    ),
                    use_container_width=True
                )
                
                # Download button
                csv = stats_df.data.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="📥 Download Data Statistik",
                    data=csv,
                    file_name=f"university_stats_{selected_year}.csv",
                    mime="text/csv"
                )

    with tab4:
        st.subheader("🏆 Top Negara Berdasarkan Metrik")

        metrics = ['Overall', 'Research Quality / Citations', 'Teaching', 'Industry Income']
        selected_metric = st.selectbox("Pilih Metrik", metrics, key="metric_select")
        selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="metric_year")
        selected_year = convert_year(selected_year)

        # Query: ambil top 10 negara berdasarkan rata-rata metrik
        pipeline = [
            {"$match": {"Year": selected_year, selected_metric: {"$ne": None}}},
            {"$group": {"_id": "$Country", "avg_metric": {"$avg": f"${selected_metric}"}}},
            {"$sort": {"avg_metric": -1}},
            {"$limit": 10}
        ]
        results = list(universities.aggregate(pipeline))
        df_top10 = pd.DataFrame(results).rename(columns={"_id": "Country", "avg_metric": selected_metric}) if results else pd.DataFrame(columns=['Country', selected_metric])

        if df_top10.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year} dan metrik {selected_metric}")
        else:
            # === Barplot ===
            plt.figure(figsize=(12,6))
            norm = plt.Normalize(df_top10[selected_metric].min(), df_top10[selected_metric].max())
            colors = plt.cm.Blues(norm(df_top10[selected_metric]))
            sns.barplot(data=df_top10, y='Country', x=selected_metric, palette=colors, edgecolor='.3')
            for i, v in enumerate(df_top10[selected_metric]):
                plt.text(v + 0.02 * v, i, f"{v:.2f}", color='black')
            plt.title(f"Top 10 Negara berdasarkan {selected_metric} Tahun {selected_year}")
            plt.xlabel(selected_metric)
            plt.ylabel("Negara")
            st.pyplot(plt)

            # === Top 3 Negara Teratas ===
            top3 = df_top10.head(3)
            st.markdown("### 🥇 Top 3 Negara Terbaik")

            cols = st.columns(3)
            clicked_country = None

            main_box_colors = [
                "background: linear-gradient(135deg, #a8e063, #56ab2f);",
                "background: linear-gradient(135deg, #7ec850, #3a6f1f);",
                "background: linear-gradient(135deg, #5a8c3b, #2f4d17);"
            ]
            name_box_text_colors = ["#2f4d17", "#274012", "#1f340f"]

            for i, (idx, row) in enumerate(top3.iterrows()):
                country = row['Country']
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="
                            {main_box_colors[i]}
                            border-radius: 20px;
                            padding: 20px;
                            text-align: center;
                            font-weight: bold;
                            font-size: 28px;
                            color: white;
                            user-select:none;
                            margin-bottom: 10px;
                        ">
                            #{i+1}
                            <div style="
                                margin-top: 15px;
                                background: linear-gradient(135deg, #c7f0a5, #88bf4a);
                                border-radius: 12px;
                                padding: 12px 20px;
                                font-size: 20px;
                                font-weight: 600;
                                color: {name_box_text_colors[i]};
                                cursor: pointer;
                                user-select:none;
                            " id="country-box-{i}">
                                {country}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button(f"Lihat Universitas {country}", key=f"show_metric_table_{country}_{selected_year}"):
                        clicked_country = country

            # === Tabel Universitas muncul setelah tombol diklik ===
            if clicked_country:
                pipeline_univ = [
                    {"$match": {"Year": selected_year, "Country": clicked_country}},
                    {"$project": {"_id": 0, "University": 1, "Rank": 1, "Overall": 1}},
                    {"$sort": {"Rank": 1}}
                ]
                univ_results = list(universities.aggregate(pipeline_univ))
                if univ_results:
                    df_univ = pd.DataFrame(univ_results)
                    df_univ_display = df_univ.rename(columns={
                        "University": "Universitas",
                        "Rank": "Rank",
                        "Overall": "Overall"
                    })[["Rank", "Universitas", "Overall"]]
                    st.markdown(f"### 📋 Daftar Universitas di {clicked_country} Tahun {selected_year}")
                    st.dataframe(df_univ_display, use_container_width=True)
                else:
                    st.info(f"Tidak ada data universitas untuk {clicked_country} tahun {selected_year}")



    with tab5:
        st.subheader("🌐 Hubungan International Outlook dan Industry Income")


        selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="scatter_year")
        selected_year = convert_year(selected_year)


        pipeline = [
            {"$match": {"Year": selected_year, "International Outlook": {"$ne": None}, "Industry Income": {"$ne": None}}},
            {"$group": {"_id": "$Country", "avg_international_outlook": {"$avg": "$International Outlook"}, "avg_industry_income": {"$avg": "$Industry Income"}}},
            {"$project": {"Country": "$_id", "International Outlook": "$avg_international_outlook", "Industry Income": "$avg_industry_income", "_id": 0}}
        ]
        results = list(universities.aggregate(pipeline))
        df = pd.DataFrame(results)


        if df.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            plt.figure(figsize=(10,6))
            sns.scatterplot(data=df, x='International Outlook', y='Industry Income', hue='Country', legend=False)
            plt.title(f"Hubungan Rata-rata International Outlook dan Industry Income - Tahun {selected_year}")
            plt.grid(True)
            st.pyplot(plt)


            median_intl = df['International Outlook'].median()
            median_industry = df['Industry Income'].median()


            df['Interpretasi'] = df.apply(lambda row:
                'High Intl Outlook & High Industry Income' if row['International Outlook'] >= median_intl and row['Industry Income'] >= median_industry else
                'High Intl Outlook & Low Industry Income' if row['International Outlook'] >= median_intl else
                'Low Intl Outlook & High Industry Income' if row['Industry Income'] >= median_industry else
                'Low Intl Outlook & Low Industry Income', axis=1)


            summary = df['Interpretasi'].value_counts()
            st.dataframe(summary)
            


    with tab6:
        st.subheader("🗺️ Peta Global Rata-rata Skor Universitas")


        selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="map_year")
        selected_year = convert_year(selected_year)


        pipeline = [
            {"$match": {"Year": selected_year}},
            {"$group": {"_id": "$Country", "avg_overall": {"$avg": "$Overall"}}},
            {"$sort": {"avg_overall": -1}}
        ]
        data = list(universities.aggregate(pipeline))
        df_country = pd.DataFrame(data).rename(columns={"_id": "Country", "avg_overall": "Overall"}) if data else pd.DataFrame(columns=["Country", "Overall"])


        if df_country.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            fig = px.choropleth(df_country, locations="Country", locationmode="country names", color="Overall", color_continuous_scale=px.colors.sequential.Blues, title=f"Rata-rata Skor Overall Universitas per Negara - Tahun {selected_year}", labels={"Overall": "Skor Overall"})
            fig.update_layout(geo=dict(showframe=False, showcoastlines=True), coloraxis_colorbar=dict(title="Skor Overall"))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Pilih Negara untuk Melihat Daftar Universitas")
        selected_country = st.selectbox("Pilih Negara", df_country["Country"].sort_values(), key="map_country")

        if selected_country:
            pipeline_univ = [
                {"$match": {"Year": selected_year, "Country": selected_country}},
                {"$project": {"_id": 0, "University": 1, "Rank": 1, "Overall": 1}},
                {"$sort": {"Rank": 1}}
            ]
            univ_results = list(universities.aggregate(pipeline_univ))
            if univ_results:
                df_univ = pd.DataFrame(univ_results).rename(columns={
                    "University": "Universitas",
                    "Rank": "Rank",
                    "Overall": "Overall"
                })[["Rank", "Universitas", "Overall"]]
                st.markdown(f"### 📋 Daftar Universitas di {selected_country} Tahun {selected_year}")
                st.dataframe(df_univ, use_container_width=True)
            else:
                st.info(f"Tidak ada data universitas untuk {selected_country} tahun {selected_year}")

    with tab7:
        st.header("Clustering SDGs per Tahun")

        # Fungsi pengambilan data tetap sama seperti yang Anda punya
        def get_agg_sdgs_by_year_mongo(year):
            exclude_fields = ['Country', 'Year', 'University', 'id']

            sample_doc = impact.find_one({"Year": year})
            if not sample_doc:
                return pd.DataFrame()

            numeric_fields = [k for k,v in sample_doc.items() if k not in exclude_fields and isinstance(v, (int, float))]

            group_stage = {
                "_id": "$Country",
                "Num_Universities": {"$sum": 1},
            }
            for field in numeric_fields:
                group_stage[f"Avg_{field}"] = {"$avg": f"${field}"}

            pipeline = [
                {"$match": {"Year": year}},
                {"$group": group_stage}
            ]

            results = list(impact.aggregate(pipeline))
            df = pd.DataFrame(results)
            if not df.empty:
                df.rename(columns={"_id": "Country"}, inplace=True)
            else:
                df = pd.DataFrame()
            return df

        def clustering_sdgs_per_year_mongo(year=2024, k_min=2, k_max=10):
            df_agg = get_agg_sdgs_by_year_mongo(year)
            if df_agg.empty:
                st.warning(f"Tidak ada data untuk tahun {year}")
                return

            X = df_agg[[col for col in df_agg.columns if col.startswith('Avg_')]].fillna(0).values

            # === KMeans ===
            silhouettes = []
            K_range = range(k_min, k_max+1)

            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=42)
                labels = kmeans.fit_predict(X)
                if k > 1:
                    sil = silhouette_score(X, labels)
                    silhouettes.append(sil)
                else:
                    silhouettes.append(np.nan)
            best_k_kmeans = K_range[np.nanargmax(silhouettes)]
            kmeans_best = KMeans(n_clusters=best_k_kmeans, random_state=42)
            labels_kmeans = kmeans_best.fit_predict(X)
            sil_kmeans = max(silhouettes)

            # === SOM + KMeans ===
            som_grid_size = 5
            som = MiniSom(som_grid_size, som_grid_size, X.shape[1], sigma=1.0, learning_rate=0.5, random_seed=42)
            som.train_random(X, 100)

            codebook_vectors = som.get_weights().reshape(som_grid_size*som_grid_size, X.shape[1])

            silhouettes_som = []
            labels_list_som = []

            for k in K_range:
                kmeans_som = KMeans(n_clusters=k, random_state=42)
                labels_som_codebook = kmeans_som.fit_predict(codebook_vectors)
                bmu_indices = np.array([som.winner(x)[0]*som_grid_size + som.winner(x)[1] for x in X])
                data_labels = labels_som_codebook[bmu_indices]

                if k > 1:
                    sil = silhouette_score(X, data_labels)
                    silhouettes_som.append(sil)
                else:
                    silhouettes_som.append(np.nan)
                labels_list_som.append(data_labels)

            best_k_som = K_range[np.nanargmax(silhouettes_som)]
            labels_som = labels_list_som[np.nanargmax(silhouettes_som)]
            sil_som = max(silhouettes_som)

            # === HDBSCAN ===
            clusterer = hdbscan.HDBSCAN(min_cluster_size=5)
            labels_hdbscan = clusterer.fit_predict(X)
            unique_clusters = len(set(labels_hdbscan)) - (1 if -1 in labels_hdbscan else 0)
            if unique_clusters > 1:
                sil_hdbscan = silhouette_score(X[labels_hdbscan != -1], labels_hdbscan[labels_hdbscan != -1])
            else:
                sil_hdbscan = -1

            silhouette_scores = {
                'KMeans': sil_kmeans,
                'SOM+KMeans': sil_som,
                'HDBSCAN': sil_hdbscan
            }

            st.subheader("Silhouette Scores per Metode")
            st.table(pd.DataFrame.from_dict(silhouette_scores, orient='index', columns=['Silhouette Score']))

            best_method = max(silhouette_scores, key=silhouette_scores.get)
            st.write(f"**Metode clustering terbaik:** {best_method}")

            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X)

            def plot_clusters(X_2d, labels, title):
                fig, ax = plt.subplots(figsize=(10,8))
                cmap = plt.cm.get_cmap('tab10', np.max(labels) + 1 if np.max(labels) >= 0 else 1)
                scatter = ax.scatter(X_2d[:,0], X_2d[:,1], c=labels, cmap=cmap, s=100, alpha=0.8, marker='o')
                ax.set_xlabel('PCA 1')
                ax.set_ylabel('PCA 2')
                ax.set_title(title)

                unique_labels = np.unique(labels)
                patches = []
                for ul in unique_labels:
                    if ul == -1:
                        label_name = 'Noise'
                        color = 'grey'
                    else:
                        label_name = f'Cluster {ul}'
                        color = cmap(ul)
                    patches.append(mpatches.Patch(color=color, label=label_name))
                ax.legend(handles=patches, title='Cluster', loc='best')

                for i, txt in enumerate(df_agg['Country']):
                    ax.annotate(txt, (X_2d[i,0], X_2d[i,1]), fontsize=8, alpha=0.75)
                st.pyplot(fig)

            plot_clusters(X_pca, labels_kmeans, f'KMeans Clustering (K={best_k_kmeans}) - Tahun {year}')
            plot_clusters(X_pca, labels_som, f'SOM+KMeans Clustering (K={best_k_som}) - Tahun {year}')
            plot_clusters(X_pca, labels_hdbscan, f'HDBSCAN Clustering - Tahun {year}')

        years = sorted(impact.distinct('Year'))
        selected_year = st.selectbox("Pilih Tahun untuk Clustering", years, index=years.index(2024) if 2024 in years else 0)
        if st.button("Jalankan Clustering"):
            clustering_sdgs_per_year_mongo(selected_year)

elif page == "Universitas":
    st.header("🏫 Analisis Data Universitas")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Top Universitas", 
        "Radar Chart", 
        "Trend Score", 
        "Top by Metric", 
        "Perbandingan", 
        "Universitas Serupa",
        "Top By SDGs",
        "Feature Importance"
    ])
    
    years = sorted([int(y) for y in df['Year'].unique()])
    universities_list = sorted(df['University'].unique())
    metrics_list = [
        "Overall",
        "Teaching",
        "Research Environment",
        "Industry Income",
        "International Outlook",
        "Research Quality / Citations"
    ]
    
    with tab1:
        st.subheader("🏆 Top Universitas Berdasarkan Overall Score")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="top_univ_year")
        with col2:
            top_n = st.slider("Jumlah Universitas", 5, 20, 10, key="top_univ_slider")
        
        pipeline = [
            {"$match": {"Year": selected_year, "Overall": {"$ne": None}}},
            {"$sort": {"Overall": -1}},
            {"$limit": top_n},
            {"$project": {"University": 1, "Overall": 1, "_id": 0}}
        ]
        results = list(universities.aggregate(pipeline))
        df_top = pd.DataFrame(results)
        
        if df_top.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            df_top = df_top.iloc[::-1]  # Reverse for better visualization
            plt.figure(figsize=(12, 6))
            colors = plt.cm.Blues_r(np.linspace(0.2, 1, len(df_top)))
            plt.barh(df_top['University'], df_top['Overall'], color=colors, edgecolor='black')
            
            for i, (univ, score) in enumerate(zip(df_top['University'], df_top['Overall'])):
                plt.text(score + 0.5, i, f"{score:.2f}", va='center')
            
            plt.title(f"Top {top_n} Universitas Tahun {selected_year}")
            plt.xlabel("Overall Score")
            plt.ylabel("Universitas")
            st.pyplot(plt)
            
            st.dataframe(df_top.sort_values("Overall", ascending=False).reset_index(drop=True))
    
    with tab2:
        st.subheader("📊 Radar Chart Metrik Universitas")
                
        col1, col2 = st.columns(2)
        with col1:
            default_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0
            selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_index, key="radar_univ")
        with col2:
            selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="radar_year")
        
        pipeline = [
            {"$match": {"University": selected_univ, "Year": selected_year}},
            {"$project": {
                "_id": 0,
                "Teaching": 1,
                "Research Environment": 1,
                "Industry Income": 1,
                "International Outlook": 1,
                "Research Quality / Citations": 1
            }}
        ]
        data = list(universities.aggregate(pipeline))
        
        if not data:
            st.warning(f"Tidak ada data untuk {selected_univ} tahun {selected_year}")
        else:
            df = pd.DataFrame(data)
            metrics = df.iloc[0].dropna()
            categories = list(metrics.index)
            values = metrics.values.tolist()
            values += values[:1]  # Close the radar
            
            angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
            ax.plot(angles, values, linewidth=2, linestyle='solid', color='#2874A6')
            ax.fill(angles, values, '#5DADE2', alpha=0.4)
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, color='blue', size=11)
            
            for angle, value in zip(angles, values):
                ax.text(angle, value + 0.03 * max(values), f"{value:.2f}",
                        horizontalalignment='center', verticalalignment='center', 
                        color='darkblue', fontsize=10)
            
            plt.title(f"Radar Chart {selected_univ} Tahun {selected_year}", size=14, color='navy', y=1.1)
            st.pyplot(fig)
    
    with tab3:
        st.subheader("📈 Trend Score Universitas")
        default_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0
        selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_index, key="trend_univ")

        pipeline = [
            {"$match": {"University": selected_univ}},
            {"$group": {"_id": "$Year", "avg_overall": {"$avg": "$Overall"}}},
            {"$sort": {"_id": 1}}
        ]
        results = list(universities.aggregate(pipeline))
        df_trend = pd.DataFrame(results).rename(columns={"_id": "Year", "avg_overall": "Overall Score"})
        
        if df_trend.empty:
            st.warning(f"Tidak ada data untuk {selected_univ}")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=df_trend, x="Year", y="Overall Score", marker="o", color="#2874A6", ax=ax)
            
            for x, y in zip(df_trend["Year"], df_trend["Overall Score"]):
                ax.text(x, y, f"{y:.2f}", color="darkblue", fontsize=9, ha="center", va="bottom")
            
            plt.title(f"Trend Skor {selected_univ}")
            plt.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig)
            
            st.write(f"**Rata-rata skor:** {df_trend['Overall Score'].mean():.2f}")
    
    with tab4:
        st.subheader("🏅 Top Universitas Berdasarkan Metrik")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_metric = st.selectbox("Pilih Metrik", metrics_list, key="top_metric")
        with col2:
            selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1, key="top_metric_year")
        with col3:
            top_n = st.slider("Jumlah Universitas", 5, 20, 10, key="top_metric_slider")
        
        pipeline = [
            {"$match": {"Year": selected_year, selected_metric: {"$ne": None}}},
            {"$sort": {selected_metric: -1}},
            {"$limit": top_n},
            {"$project": {"University": 1, selected_metric: 1, "_id": 0}}
        ]
        results = list(universities.aggregate(pipeline))
        df_top = pd.DataFrame(results)
        
        if df_top.empty:
            st.warning(f"Tidak ada data untuk metrik {selected_metric} tahun {selected_year}")
        else:
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(data=df_top, y="University", x=selected_metric, palette="Blues_d")
            
            for i, val in enumerate(df_top[selected_metric]):
                ax.text(val + 0.01 * df_top[selected_metric].max(), i, 
                        f"{val:.2f}", color='black', va='center')
            
            plt.title(f"Top {top_n} Universitas Berdasarkan {selected_metric}")
            st.pyplot(plt)
            
            df_top = df_top.sort_values(selected_metric, ascending=False).reset_index(drop=True)
            df_top.insert(0, "No", df_top.index + 1)
            st.dataframe(df_top)

    
    with tab5:
        st.subheader("🆚 Perbandingan 2 Universitas")

        default1 = universities_list.index("IPB University") if "IPB University" in universities_list else 0
        default2 = universities_list.index("Universitas Gadjah Mada") if "Universitas Gadjah Mada" in universities_list else 1

        col1, col2 = st.columns(2)
        with col1:
            univ1 = st.selectbox("Universitas 1", universities_list, index=default1, key="compare1")
        with col2:
            univ2 = st.selectbox("Universitas 2", universities_list, index=default2, key="compare2")

        pipeline = [
            {"$match": {"University": {"$in": [univ1, univ2]}}},
            {"$project": {"_id": 0}},
            {"$sort": {"Year": 1}}
        ]
        results = list(universities.aggregate(pipeline))
        df = pd.DataFrame(results)

        if df.empty:
            st.warning("❗ Data tidak tersedia untuk salah satu universitas.")
        else:
            if 'Year' not in df.columns or 'University' not in df.columns:
                st.error("❌ Struktur data tidak sesuai.")
            else:
                numeric_cols = df.select_dtypes(include='number').columns.drop('Year', errors='ignore')
                if numeric_cols.empty:
                    st.warning("🔎 Tidak ada metrik numerik yang tersedia untuk dibandingkan.")
                else:
                    df = df.dropna(subset=numeric_cols)

                    n_metrics = len(numeric_cols)
                    n_cols = 3
                    n_rows = (n_metrics + n_cols - 1) // n_cols

                    fig = plt.figure(figsize=(5 * n_cols, 4 * n_rows))
                    for i, metric in enumerate(numeric_cols):
                        plt.subplot(n_rows, n_cols, i + 1)
                        sns.lineplot(data=df[df['University'] == univ1], x='Year', y=metric,
                                    label=univ1, marker='o', color='#2874A6')
                        sns.lineplot(data=df[df['University'] == univ2], x='Year', y=metric,
                                    label=univ2, marker='o', color='#5DADE2')
                        plt.title(metric)
                        plt.grid(True, linestyle="--", alpha=0.5)
                        plt.xlabel("Tahun")
                        plt.ylabel(metric)

                    plt.tight_layout()
                    plt.suptitle(f"Perbandingan: {univ1} vs {univ2}", y=1.02, fontsize=16)
                    st.pyplot(fig)

                    mean_scores = df.groupby("University")[numeric_cols].mean()
                    st.write("**📊 Rata-rata skor masing-masing universitas:**")
                    mean_scores = mean_scores.reset_index()
                    mean_scores.columns = pd.Index([f"{col}_{i}" if mean_scores.columns.duplicated()[i] else col
                                                    for i, col in enumerate(mean_scores.columns)])
                    st.dataframe(mean_scores.style.background_gradient(cmap='Blues'), use_container_width=True)

                    better = mean_scores.set_index('University')[numeric_cols].mean(axis=1).idxmax()
                    st.success(f"🏆 Universitas dengan skor rata-rata tertinggi: **{better}**")

    with tab6:
        st.subheader("🔍 Universitas dengan Karakteristik Serupa")

        default_univ_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0

        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Pilih Tahun", years, index=len(years) - 1, key="similar_year")
        with col2:
            selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_univ_index, key="similar_univ")

        # Query data dari MongoDB
        pipeline = [
            {"$match": {"Year": selected_year}},
            {"$project": {
                "_id": 0,
                "University": 1,
                "Overall": 1,
                "Teaching": 1,
                "Research Environment": 1,
                "Industry Income": 1,
                "International Outlook": 1,
                "Research Quality / Citations": 1
            }}
        ]
        results = list(universities.aggregate(pipeline))
        df_sim = pd.DataFrame(results).set_index("University")

        if selected_univ not in df_sim.index:
            st.warning(f"Tidak ada data untuk {selected_univ} tahun {selected_year}")
        else:
            numeric_cols = df_sim.select_dtypes(include='number').columns
            df_numeric = df_sim[numeric_cols].fillna(0)

            from sklearn.metrics.pairwise import cosine_similarity
            sim_matrix = cosine_similarity(df_numeric)
            sim_df = pd.DataFrame(sim_matrix, index=df_numeric.index, columns=df_numeric.index)

            similar = sim_df[selected_univ].drop(selected_univ).sort_values(ascending=False).head(5)

            st.write(f"5 Universitas paling mirip dengan {selected_univ} tahun {selected_year}:")
            st.dataframe(similar.to_frame("Tingkat Kemiripan"))

            st.write("**Perbandingan Metrik:**")
            compare_df = df_sim.loc[[selected_univ] + similar.index.tolist()]
            st.dataframe(compare_df.style.background_gradient(cmap='Blues'))

    with tab7:
        st.subheader("🌍 Skor SDGs Semua Universitas")

        # Ambil daftar tahun dari koleksi 'impact'
        years_impact = sorted(impact.distinct("Year"))
        selected_year = st.selectbox("Pilih Tahun", years_impact, index=len(years_impact) - 1, key="sdg_year")

        # Query data dari MongoDB untuk tahun yang dipilih
        results = list(impact.find({"Year": selected_year}, {"_id": 0}))
        if not results:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            df = pd.DataFrame(results)

            # Ubah kolom non-string menjadi numerik
            for col in df.columns:
                if col not in ["University", "Country", "Rank SDGS Overall"]:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            df_sorted = df.sort_values("Overall SDGS", ascending=False)

            st.dataframe(df_sorted.style.background_gradient(cmap='Greens'))

    with tab8:
        st.subheader("Analisis Feature Importance dengan Random Forest dan SHAP")

        # Metrics yang kita gabungkan
        metrics_sdg = [
            "Zero Hunger",
            "Impact_life_below_water",
            "Impact_industry_innovation_and_infrastructure",
            "Impact_good_health_and_well_being",
            "Impact_gender_equality",
            "Impact_decent_work_and_economic_growth",
            "Impact_climate_action",
            "Impact_clean_water_and_sanitation",
            "Impact_affordable_and_clean_energy",
            "Sustainable cities and communities",
            "Responsible_consumption_and_production",
            "Reducing_inequalities",
            "Quality_education",
            "Peace_justice_and_strong_institutions",
            "Impact_partnerships_goals",
            "Impact_no-poverty",
            "Impact_life_land"
        ]

        metrics_univ = [
            "Teaching",
            "Industry Income",
            "International Outlook",
            "Research Environment",
            "Student Population",
            "Students per staff",
            "Research Quality / Citations"
        ]

        # Fungsi ambil data gabungan untuk tahun dan negara tertentu
        def fetch_combined_data(year, country):
            pipeline = [
                {"$match": {"Year": year, "Country": country}},
                {"$lookup": {
                    "from": "Universities",
                    "let": {"univ_name": "$University", "yr": "$Year"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [
                            {"$eq": ["$University", "$$univ_name"]},
                            {"$eq": ["$Year", "$$yr"]}
                        ]}}},
                        {"$project": {m: 1 for m in metrics_univ + ["Overall"]}}
                    ],
                    "as": "univ_data"
                }},
                {"$unwind": {
                    "path": "$univ_data",
                    "preserveNullAndEmptyArrays": True
                }},
                {"$project": {
                    "University": 1,
                    **{m: 1 for m in metrics_sdg},
                    **{m: {"$ifNull": [f"$univ_data.{m}", 0]} for m in metrics_univ},
                    "Overall": {"$ifNull": ["$univ_data.Overall", None]}
                }},
                {"$match": {"Overall": {"$ne": None}}}
            ]

            data = list(impact.aggregate(pipeline))
            df = pd.DataFrame(data).set_index("University")
            df.fillna(0, inplace=True)
            return df

        year_example = st.number_input("Pilih Tahun", min_value=2000, max_value=2025, value=2023)
        country_example = st.text_input("Masukkan Negara", value="United States")

        if st.button("Jalankan Analisis"):
            with st.spinner("Mengambil dan memproses data..."):
                df = fetch_combined_data(year_example, country_example)

                if df.empty:
                    st.warning("Data tidak tersedia untuk tahun dan negara yang dipilih.")
                else:
                    st.write(f"Data shape: {df.shape}")

                    X = df[metrics_sdg + metrics_univ]
                    y = df['Overall']

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                    model = RandomForestRegressor(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)

                    y_pred = model.predict(X_test)
                    mse = mean_squared_error(y_test, y_pred)
                    st.write(f"Mean Squared Error: {mse:.4f}")

                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(X_test)

                    mean_abs_shap = np.abs(shap_values).mean(axis=0)
                    feature_names = X_test.columns

                    sorted_idx = np.argsort(mean_abs_shap)[::-1]
                    sorted_features = feature_names[sorted_idx]
                    sorted_values = mean_abs_shap[sorted_idx]

                    fig, ax = plt.subplots(figsize=(12, 8))
                    bars = ax.barh(sorted_features, sorted_values, color="#2874A6")
                    ax.invert_yaxis()
                    ax.set_xlabel("Mean |SHAP value|")
                    ax.set_title("Feature Importance berdasarkan SHAP (mean absolut)")

                    for bar, value in zip(bars, sorted_values):
                        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                                f"{value:.3f}", va='center', fontsize=9)

                    plt.tight_layout()
                    st.pyplot(fig)

elif page == "SDGs":
    st.header("📈 Analisis SDGs Universitas")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Top SDGs", 
        "Distribusi Skor", 
        "Trend SDGs", 
        "Perbandingan", 
        "Kontribusi", 
        "Skor per Tahun",
        "Analisis Negara"
    ])
    
    # Get unique years and universities from impact data
    years_impact = sorted([int(y) for y in df_impact['Year'].unique()])
    universities_list = sorted(df_impact['University'].unique())
    countries_list = sorted(df_impact['Country'].unique())
    
    # SDGs metrics
    sdgs_metrics = [
        "Overall SDGS", "Zero Hunger", "Impact_life_below_water", 
        "Impact_industry_innovation_and_infrastructure", "Impact_good_health_and_well_being",
        "Impact_gender_equality", "Impact_decent_work_and_economic_growth", "Impact_climate_action",
        "Impact_clean_water_and_sanitation", "Impact_affordable_and_clean_energy",
        "Sustainable cities and communities", "Responsible_consumption_and_production",
        "Reducing_inequalities", "Quality_education", "Peace_justice_and_strong_institutions",
        "Impact_partnerships_goals", "Impact_no-poverty", "Impact_life_land"
    ]
    
    with tab1:
        st.subheader("🏆 Top Universitas Berdasarkan Skor SDGs")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Pilih Tahun", years_impact, index=len(years_impact)-1, key="top_sdg_year")
        with col2:
            top_n = st.slider("Jumlah Universitas", 5, 20, 10, key="top_sdg_slider")
        
        pipeline = [
            {"$match": {"Year": selected_year}},
            {"$sort": {"Overall SDGS": -1}},
            {"$limit": top_n},
            {"$project": {"_id": 0, "University": 1, "Overall SDGS": 1}}
        ]
        results = list(impact.aggregate(pipeline))
        df_top = pd.DataFrame(results)
        
        if df_top.empty:
            st.warning(f"Tidak ada data untuk tahun {selected_year}")
        else:
            df_top = df_top.iloc[::-1]  # Reverse for better visualization
            plt.figure(figsize=(12, 6))
            colors = plt.cm.Blues_r(np.linspace(0.2, 1, len(df_top)))
            plt.barh(df_top['University'], df_top['Overall SDGS'], color=colors, edgecolor='black')
            
            for i, (univ, score) in enumerate(zip(df_top['University'], df_top['Overall SDGS'])):
                plt.text(score + 0.5, i, f"{score:.2f}", va='center')
            
            plt.title(f"Top {top_n} Universitas Berdasarkan Skor SDGs Tahun {selected_year}")
            plt.xlabel("Overall SDGS Score")
            plt.ylabel("Universitas")
            st.pyplot(plt)
            
            st.dataframe(df_top.sort_values("Overall SDGS", ascending=False).reset_index(drop=True))

    def parse_range(value):
        try:
            # Ubah koma ke titik untuk desimal
            value = value.replace(',', '.')
            if '-' in value:
                parts = value.split('-')
                nums = [float(p) for p in parts]
                return sum(nums) / len(nums)
            else:
                return float(value)
        except:
            return None

    with tab2:
        st.subheader("📊 Distribusi Skor SDGs")

        selected_metric = st.selectbox("Pilih Metrik SDGs", [m for m in sdgs_metrics if m != "Overall SDGS"], key="dist_sdg_metric")

        pipeline = [
            {"$match": {selected_metric: {"$ne": None}}},
            {"$project": {"_id": 0, selected_metric: 1}}
        ]
        results = list(impact.aggregate(pipeline))
        df = pd.DataFrame(results)

        if df.empty:
            st.warning(f"Tidak ada data untuk metrik {selected_metric}")
        else:
            # Bersihkan dan konversi nilai ke angka tunggal
            df[selected_metric] = df[selected_metric].astype(str).apply(parse_range)

            plt.figure(figsize=(10, 6))
            sns.boxplot(x=df[selected_metric].dropna(), color="#3498db")
            plt.title(f"Distribusi Skor {selected_metric}")
            plt.xlabel("Skor")
            st.pyplot(plt)

            st.write(f"**Statistik Deskriptif {selected_metric}:**")
            st.write(df[selected_metric].describe().to_frame().T)
    with tab3:
        st.subheader("📈 Trend Skor SDGs Universitas")
        
        col1, col2 = st.columns(2)
        with col1:
            default_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0
            selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_index, key="trend_sdg_univ")
        with col2:
            selected_metric = st.selectbox("Pilih Metrik", sdgs_metrics, key="trend_sdg_metric")
        
        pipeline = [
            {"$match": {"University": selected_univ, selected_metric: {"$ne": None}}},
            {"$sort": {"Year": 1}},
            {"$project": {"_id": 0, "Year": 1, selected_metric: 1}}
        ]
        results = list(impact.aggregate(pipeline))
        df_trend = pd.DataFrame(results)
        
        if df_trend.empty:
            st.warning(f"Tidak ada data untuk {selected_univ} dan metrik {selected_metric}")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=df_trend, x="Year", y=selected_metric, marker="o", color="#2980b9", ax=ax)
            
            for x, y in zip(df_trend["Year"], df_trend[selected_metric]):
                ax.text(x, y, f"{y:.2f}", color="darkblue", fontsize=9, ha="center", va="bottom")
            
            plt.title(f"Trend {selected_metric} - {selected_univ}")
            plt.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig)
    
    with tab4:
            st.subheader("🆚 Perbandingan 2 Universitas")
            default_index1 = universities_list.index("IPB University") if "IPB University" in universities_list else 0
            default_index2 = universities_list.index("Universitas Gadjah Mada") if "Universitas Gadjah Mada" in universities_list else 1

            col1, col2 = st.columns(2)
            with col1:
                univ1 = st.selectbox("Universitas 1", universities_list, index=default_index1, key="compare_sdg1")
            with col2:
                univ2 = st.selectbox("Universitas 2", universities_list, index=default_index2, key="compare_sdg2")
                        
            year_range = st.slider(
                "Rentang Tahun", 
                min_value=min(years_impact), 
                max_value=max(years_impact),
                value=(min(years_impact), max(years_impact))
            )  # <- Penutupan tanda kurung disini
            
            pipeline = [
                {"$match": {
                    "University": {"$in": [univ1, univ2]},
                    "Year": {"$gte": year_range[0], "$lte": year_range[1]}
                }},
                {"$project": {"_id": 0, "University": 1, "Year": 1, **{m: 1 for m in sdgs_metrics}}}
            ]
            results = list(impact.aggregate(pipeline))
            df = pd.DataFrame(results)
            
            if df.empty:
                st.warning("Data tidak tersedia untuk salah satu universitas")
            else:
                df_avg = df.groupby("University")[sdgs_metrics].mean().reset_index()
                
                fig, axes = plt.subplots(1, 2, figsize=(18, 10), sharex=True)
                plt.subplots_adjust(left=0.2, right=0.95)
                
                sns.barplot(
                    y=[m for m in sdgs_metrics if m != "Overall SDGS"],
                    x=df_avg[df_avg["University"]==univ1][[m for m in sdgs_metrics if m != "Overall SDGS"]].values.flatten(),
                    ax=axes[0], palette="Blues_r", orient="h"
                )
                axes[0].set_title(univ1, fontsize=16)
                axes[0].set_xlabel("Skor")
                
                sns.barplot(
                    y=[m for m in sdgs_metrics if m != "Overall SDGS"],
                    x=df_avg[df_avg["University"]==univ2][[m for m in sdgs_metrics if m != "Overall SDGS"]].values.flatten(),
                    ax=axes[1], palette="Oranges_r", orient="h"
                )
                axes[1].set_title(univ2, fontsize=16)
                axes[1].set_xlabel("Skor")
                axes[1].yaxis.set_ticklabels([])
                
                plt.suptitle(f"Perbandingan Rata-rata Skor SDGs ({year_range[0]}-{year_range[1]})", fontsize=18, y=1.02)
                st.pyplot(fig)
                
                st.write("**Rata-rata Skor:**")
                st.dataframe(df_avg.set_index("University").T.style.background_gradient(cmap='Blues'))
        
    with tab5:
        st.subheader("📊 Kontribusi SDGs per Universitas")
        default_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0
        selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_index, key="contrib_univ")
        
        # Exclude Overall SDGS
        metrics_no_overall = [m for m in sdgs_metrics if m != "Overall SDGS"]
        
        pipeline = [
            {"$match": {"University": selected_univ}},
            {"$group": {**{m: {"$avg": f"${m}"} for m in metrics_no_overall}, "_id": None}}
        ]
        results = list(impact.aggregate(pipeline))
        
        if not results:
            st.warning(f"Tidak ada data untuk {selected_univ}")
        else:
            scores = [results[0].get(m, 0) or 0 for m in metrics_no_overall]
            
            # Short names for display
            short_names = {
                "Zero Hunger": "Zero Hunger",
                "Impact_life_below_water": "Life Below Water",
                "Impact_industry_innovation_and_infrastructure": "Industry & Innovation",
                "Impact_good_health_and_well_being": "Good Health",
                "Impact_gender_equality": "Gender Equality",
                "Impact_decent_work_and_economic_growth": "Decent Work",
                "Impact_climate_action": "Climate Action",
                "Impact_clean_water_and_sanitation": "Clean Water",
                "Impact_affordable_and_clean_energy": "Clean Energy",
                "Sustainable cities and communities": "Sustainable Cities",
                "Responsible_consumption_and_production": "Responsible Consumption",
                "Reducing_inequalities": "Reducing Inequalities",
                "Quality_education": "Quality Education",
                "Peace_justice_and_strong_institutions": "Peace & Justice",
                "Impact_partnerships_goals": "Partnerships",
                "Impact_no-poverty": "No Poverty",
                "Impact_life_land": "Life on Land"
            }
            labels = [short_names.get(m, m) for m in metrics_no_overall]
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 10))
            wedges, texts, autotexts = ax.pie(
                scores, labels=labels, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette("Blues", len(labels)),
                textprops={'fontsize': 9}
            )
            plt.title(f"Kontribusi SDGs - {selected_univ}", fontsize=16)
            
            # Create legend with full names
            legend_labels = [f"{short}: {full}" for short, full in zip(labels, metrics_no_overall)]
            plt.legend(
                wedges, legend_labels,
                title="Keterangan SDGs",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            st.pyplot(fig)
    
    with tab6:
        st.subheader("📅 Skor SDGs per Tahun")
        default_index = universities_list.index("IPB University") if "IPB University" in universities_list else 0
        selected_univ = st.selectbox("Pilih Universitas", universities_list, index=default_index, key="yearly_univ")
        
        pipeline = [
            {"$match": {"University": selected_univ}},
            {"$project": {"_id": 0, "Year": 1, **{m: 1 for m in sdgs_metrics}}}
        ]
        results = list(impact.aggregate(pipeline))
        df = pd.DataFrame(results)
        
        if df.empty:
            st.warning(f"Tidak ada data untuk {selected_univ}")
        else:
            # Melt dataframe for visualization
            df_long = df.melt(id_vars=["Year"], value_vars=[m for m in sdgs_metrics if m != "Overall SDGS"], 
                             var_name="Metric", value_name="Score")
            
            # Pivot table for display
            pivot = df_long.pivot_table(index="Metric", columns="Year", values="Score", aggfunc="mean").round(2)
            
            st.write(f"**Skor SDGs per Tahun - {selected_univ}**")
            st.dataframe(pivot.style.background_gradient(cmap='Blues'))
            
            # Line plot for trends
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=df_long, x="Year", y="Score", hue="Metric", marker="o", ax=ax)
            plt.title(f"Trend Skor SDGs - {selected_univ}")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig)
    
    with tab7:
        st.subheader("🌍 Analisis SDGs per Negara")
        
        tab_country1, tab_country2 = st.tabs(["Kontribusi SDGs", "Skor per Tahun"])
        
        with tab_country1:
            st.subheader("📊 Kontribusi SDGs per Negara")
            
            selected_country = st.selectbox("Pilih Negara", countries_list, key="contrib_country")
            
            pipeline = [
                {"$match": {"Country": selected_country}},
                {"$group": {**{m: {"$avg": f"${m}"} for m in [m for m in sdgs_metrics if m != "Overall SDGS"]}, "_id": None}}
            ]
            results = list(impact.aggregate(pipeline))
            
            if not results:
                st.warning(f"Tidak ada data untuk {selected_country}")
            else:
                scores = [results[0].get(m, 0) or 0 for m in [m for m in sdgs_metrics if m != "Overall SDGS"]]
                
                # Short names for display
                short_names = {
                    "Zero Hunger": "Zero Hunger",
                    "Impact_life_below_water": "Life Below Water",
                    "Impact_industry_innovation_and_infrastructure": "Industry & Innovation",
                    "Impact_good_health_and_well_being": "Good Health",
                    "Impact_gender_equality": "Gender Equality",
                    "Impact_decent_work_and_economic_growth": "Decent Work",
                    "Impact_climate_action": "Climate Action",
                    "Impact_clean_water_and_sanitation": "Clean Water",
                    "Impact_affordable_and_clean_energy": "Clean Energy",
                    "Sustainable cities and communities": "Sustainable Cities",
                    "Responsible_consumption_and_production": "Responsible Consumption",
                    "Reducing_inequalities": "Reducing Inequalities",
                    "Quality_education": "Quality Education",
                    "Peace_justice_and_strong_institutions": "Peace & Justice",
                    "Impact_partnerships_goals": "Partnerships",
                    "Impact_no-poverty": "No Poverty",
                    "Impact_life_land": "Life on Land"
                }
                labels = [short_names.get(m, m) for m in [m for m in sdgs_metrics if m != "Overall SDGS"]]
                
                # Create pie chart
                fig, ax = plt.subplots(figsize=(10, 10))
                wedges, texts, autotexts = ax.pie(
                    scores, labels=labels, autopct='%1.1f%%', startangle=140,
                    colors=sns.color_palette("Greens", len(labels)),
                    textprops={'fontsize': 9}
                )
                plt.title(f"Kontribusi SDGs - {selected_country}", fontsize=16)
                
                # Create legend with full names
                legend_labels = [f"{short}: {full}" for short, full in zip(labels, [m for m in sdgs_metrics if m != "Overall SDGS"])]
                plt.legend(
                    wedges, legend_labels,
                    title="Keterangan SDGs",
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1)
                )
                
                st.pyplot(fig)
        
        with tab_country2:
            st.subheader("📅 Skor SDGs per Tahun per Negara")
            
            selected_country = st.selectbox("Pilih Negara", countries_list, key="yearly_country")
            
            pipeline = [
                {"$match": {"Country": selected_country}},
                {"$project": {"_id": 0, "Year": 1, **{m: 1 for m in sdgs_metrics}}}
            ]
            results = list(impact.aggregate(pipeline))
            df = pd.DataFrame(results)
            
            if df.empty:
                st.warning(f"Tidak ada data untuk {selected_country}")
            else:
                # Melt dataframe for visualization
                df_long = df.melt(id_vars=["Year"], value_vars=[m for m in sdgs_metrics if m != "Overall SDGS"], 
                                 var_name="Metric", value_name="Score")
                
                # Pivot table for display
                pivot = df_long.pivot_table(index="Metric", columns="Year", values="Score", aggfunc="mean").round(2)
                
                st.write(f"**Rata-rata Skor SDGs per Tahun - {selected_country}**")
                st.dataframe(pivot.style.background_gradient(cmap='Greens'))
                
                # Line plot for trends
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=df_long, x="Year", y="Score", hue="Metric", marker="o", ax=ax)
                plt.title(f"Trend Skor SDGs - {selected_country}")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(True, linestyle="--", alpha=0.5)
                st.pyplot(fig)

elif page == "Indonesia":
    st.header("Data Indonesia")
    tab1, tab2, tab3 = st.tabs(["Top 5 Universitas", "Distribusi Rata-Rata SDGs", "Radar Chart Interaktif"])

    with tab1:
        st.subheader("📈 Tren Skor Overall Universitas di Indonesia")

        top_n = st.slider("Pilih Jumlah Top Universitas", 3, 10, 5, key="topn_tab1")

        # Ambil data dari MongoDB (pastikan collection dan field sudah benar)
        pipeline = [
            {"$match": {"Country": "Indonesia"}},
            {"$group": {
                "_id": {"University": "$University", "Year": "$Year"},
                "overall": {"$max": "$Overall"}
            }},
            {"$sort": {"_id.Year": 1}}
        ]
        data = list(universities.aggregate(pipeline))
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("Data tidak tersedia")
        else:
            df["University"] = df["_id"].apply(lambda x: x["University"])
            df["Year"] = df["_id"].apply(lambda x: x["Year"])
            df.drop(columns=["_id"], inplace=True)

            # Ambil top N universitas berdasar nilai overall max
            top_univ = df.groupby("University")["overall"].max().nlargest(top_n).index.tolist()
            df_top = df[df["University"].isin(top_univ)]

            # Plot tren skor Overall
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=df_top, x="Year", y="overall", hue="University", marker="o", palette="tab10", ax=ax)
            for _, row in df_top.iterrows():
                ax.text(row["Year"], row["overall"]+0.3, f"{row['overall']:.1f}", fontsize=8, ha='center', va='bottom')

            ax.set_title(f"Top {top_n} Tren Skor Overall Universitas di Indonesia", fontsize=14)
            ax.set_ylabel("Skor Overall")
            ax.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout(rect=[0, 0.1, 1, 0.95])
            ax.legend(title="Universitas", loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=9)
            st.pyplot(fig)

            # --- Detail metrik SDGs top 3 dengan expander ---
            st.markdown("### 🏅 Detail Metrik SDGs dari Top 3 Universitas Terbaik")

            top3 = df.groupby("University")["overall"].max().nlargest(3).index.tolist()

            sdgs_metrics = [
                "Overall SDGS",
                "Zero Hunger",
                "Impact_life_below_water",
                "Impact_industry_innovation_and_infrastructure",
                "Impact_good_health_and_well_being",
                "Impact_gender_equality",
                "Impact_decent_work_and_economic_growth",
                "Impact_climate_action",
                "Impact_clean_water_and_sanitation",
                "Impact_affordable_and_clean_energy",
                "Sustainable cities and communities",
                "Responsible_consumption_and_production",
                "Reducing_inequalities",
                "Quality_education",
                "Peace_justice_and_strong_institutions",
                "Impact_partnerships_goals",
                "Impact_no-poverty",
                "Impact_life_land"
            ]

            for univ in top3:
                with st.expander(f"{univ}"):
                    pipeline_detail = [
                        {"$match": {"University": univ}},
                        {"$group": {
                            "_id": None,
                            **{m: {"$avg": f"${m}"} for m in sdgs_metrics}
                        }}
                    ]
                    detail_result = list(impact.aggregate(pipeline_detail))

                    if detail_result:
                        df_detail = pd.DataFrame([detail_result[0]])
                        # Convert tipe object ke numeric
                        for col in df_detail.columns:
                            df_detail[col] = pd.to_numeric(df_detail[col], errors='coerce')

                        df_detail = df_detail.T.reset_index()
                        df_detail.columns = ["Metrik SDGs", "Skor Rata-rata"]
                        df_detail = df_detail.dropna().sort_values("Skor Rata-rata", ascending=False).reset_index(drop=True)
                        st.dataframe(df_detail)
                    else:
                        st.write("Data metrik SDGs tidak tersedia.")
                        
            # --- Tabel semua universitas ---
            st.markdown("### 📋 Seluruh Universitas di Indonesia dan Skor Overall Terbaru")
            df_all_latest = df.sort_values("Year", ascending=False).drop_duplicates("University")
            df_all_sorted = df_all_latest.sort_values("overall", ascending=False).reset_index(drop=True)
            df_all_sorted.index += 1
            st.dataframe(df_all_sorted[["University", "Year", "overall"]].rename(columns={"overall": "Skor Overall"}))


    with tab2:
      st.subheader("Distribusi Rata-rata Skor SDGs per Metrik - Indonesia")
      metrics = [
          "Overall SDGS",
          "Zero Hunger",
          "Impact_life_below_water",
          "Impact_industry_innovation_and_infrastructure",
          "Impact_good_health_and_well_being",
          "Impact_gender_equality",
          "Impact_decent_work_and_economic_growth",
          "Impact_climate_action",
          "Impact_clean_water_and_sanitation",
          "Impact_affordable_and_clean_energy",
          "Sustainable cities and communities",
          "Responsible_consumption_and_production",
          "Reducing_inequalities",
          "Quality_education",
          "Peace_justice_and_strong_institutions",
          "Impact_partnerships_goals",
          "Impact_no-poverty",
          "Impact_life_land"
      ]
      
      pipeline = [
          {"$match": {"Country": "Indonesia"}},
          {"$group": {
              "_id": None,
              **{m: {"$avg": f"${m}"} for m in metrics}
          }}
      ]
      agg = list(impact.aggregate(pipeline))
      if not agg:
          st.warning("Data tidak tersedia")
      else:
          agg = agg[0]
          sdg_avg = pd.DataFrame.from_dict(
              {k: v for k, v in agg.items() if k != "_id"},
              orient='index',
              columns=["Average Score"]
          ).sort_values("Average Score", ascending=False)

          plt.figure(figsize=(12,8))
          barplot = sns.barplot(
              x="Average Score",
              y=sdg_avg.index,
              data=sdg_avg,
              palette=sns.color_palette("Blues", len(sdg_avg))
          )

          plt.title("Distribusi Rata-rata Skor SDGs per Metrik - Indonesia", fontsize=16)
          plt.xlabel("Rata-rata Skor")
          plt.ylabel("Metrik SDGs")

          for index, score in enumerate(sdg_avg["Average Score"]):
              barplot.text(score + 0.2, index, f"{score:.2f}", color='black', va="center")

          plt.grid(axis='x', linestyle='--', alpha=0.7)
          plt.tight_layout()
          st.pyplot(plt)
          
      # --- Subtab Top Universities by Metrik dan Tahun ---
      st.markdown("---")
      st.subheader("🏆 Top Universities Berdasarkan Metrik SDGs dan Tahun")

      # Pilih metrik dan tahun
      selected_metric = st.selectbox("Pilih Metrik SDGs", metrics, index=0, key="metric_tab2")
      
      # Ambil daftar tahun dari data impact
      years_data = list(impact.distinct("Year", {"Country": "Indonesia"}))
      years_data.sort()
      selected_year = st.selectbox("Pilih Tahun", years_data, index=len(years_data)-1, key="year_tab2")
      
      # Filter dan agregasi top universitas berdasarkan metrik dan tahun
      pipeline_top = [
          {"$match": {"Country": "Indonesia", "Year": selected_year}},
          {"$group": {
              "_id": "$University",
              "avg_score": {"$avg": f"${selected_metric}"}
          }},
          {"$sort": {"avg_score": -1}},
          {"$limit": 10}  # Limit top 10 untuk tampil
      ]
      top_univ_data = list(impact.aggregate(pipeline_top))
      if not top_univ_data:
          st.warning(f"Tidak ada data untuk tahun {selected_year} dan metrik {selected_metric}")
      else:
          df_top_univ = pd.DataFrame(top_univ_data)
          df_top_univ.rename(columns={"_id": "Universitas", "avg_score": f"Rata-rata {selected_metric}"}, inplace=True)

          # Plot bar top universitas
          plt.figure(figsize=(10,6))
          sns.barplot(
              x=f"Rata-rata {selected_metric}",
              y="Universitas",
              data=df_top_univ,
              palette=sns.color_palette("viridis", len(df_top_univ))
          )
          plt.title(f"Top 10 Universitas berdasarkan {selected_metric} Tahun {selected_year}", fontsize=14)
          plt.xlabel(f"Rata-rata Skor {selected_metric}")
          plt.ylabel("Universitas")
          plt.tight_layout()
          st.pyplot(plt)

          # Tabel top universitas
          st.dataframe(df_top_univ.reset_index(drop=True))

    with tab3:
        st.subheader("Radar Chart SDGs Interaktif")

        # List universitas dan tahun dari DB
        indo_univ = sorted(impact.distinct("University", {"Country": "Indonesia"}))
        years = sorted(impact.distinct("Year", {"Country": "Indonesia"}))
        years_options = ["Rata-rata Semua Tahun"] + years

        # Cari index IPB University di indo_univ (sesuaikan nama tepatnya)
        try:
            default_ipb_idx = indo_univ.index("Institut Pertanian Bogor")
        except ValueError:
            default_ipb_idx = 0  # fallback kalau tidak ditemukan

        university = st.selectbox("Pilih Universitas", indo_univ, index=default_ipb_idx)
        year = st.selectbox("Pilih Tahun", years_options)

        def get_radar_data(university, year):
            if year == "Rata-rata Semua Tahun":
                pipeline = [
                    {"$match": {"Country": "Indonesia", "University": university}},
                    {"$group": {
                        "_id": "$University",
                        **{m: {"$avg": f"${m}"} for m in metrics}
                    }}
                ]
            else:
                pipeline = [
                    {"$match": {"Country": "Indonesia", "University": university, "Year": year}},
                    {"$group": {
                        "_id": "$University",
                        **{m: {"$avg": f"${m}"} for m in metrics}
                    }}
                ]
            result = list(impact.aggregate(pipeline))
            if not result:
                return None
            return [result[0].get(m, 0) or 0 for m in metrics]

        values = get_radar_data(university, year)
        if values is None:
            st.warning(f"Tidak ada data untuk {university} pada tahun {year}")
        else:
            values += values[:1]
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))

            ax.plot(angles, values, color="#2980B9", linewidth=2)
            ax.fill(angles, values, color="#3498DB", alpha=0.25)

            ax.set_thetagrids(np.degrees(angles[:-1]), metrics, fontsize=9)
            ax.set_ylim(0, 100)

            for angle, value in zip(angles, values):
                ax.text(angle, value + 3, f"{value:.1f}", ha='center', va='center', fontsize=8, color='black')

            ax.set_title(f"Radar Chart SDGs - {university} ({year})", size=16, pad=40)
            ax.spines['polar'].set_visible(False)

            st.pyplot(fig)

elif st.session_state.page == "MongoDB":
    st.subheader("🔍 Eksperimen Aggregation MongoDB")

    st.markdown("**1. Pilih koleksi data:**")
    selected_collection = st.selectbox("Koleksi MongoDB", ["Universities", "ImpactRank"])

    st.markdown("**2. Tempel pipeline MongoDB (format JSON):**")
    default_pipeline = '''[
    {"$match": {"Country": "Indonesia"}},
    {"$group": {
        "_id": "$University",
        "max_overall": {"$max": "$Overall"}
    }},
    {"$sort": {"max_overall": -1}},
    {"$limit": 5}
    ]'''
    pipeline_input = st.text_area("Masukkan pipeline di sini:", value=default_pipeline, height=220)

    if "df_pipeline" not in st.session_state:
        st.session_state.df_pipeline = None
        st.session_state.pipeline_hash = None

    import hashlib
    pipeline_hash = hashlib.md5(pipeline_input.encode()).hexdigest()

    run_pipeline = st.button("Jalankan Pipeline")

    # Jika pipeline sudah dijalankan sebelumnya dan tidak ada perubahan pipeline, gunakan cache/stored data
    if run_pipeline or (st.session_state.df_pipeline is not None and pipeline_hash == st.session_state.pipeline_hash):
        if run_pipeline or (st.session_state.df_pipeline is None):
            try:
                import json
                pipeline = json.loads(pipeline_input)
                collection = universities if selected_collection == "Universities" else impact
                result = list(collection.aggregate(pipeline))
                df_pipeline = pd.DataFrame(result)

                # Pecah _id jika dictionary
                if "_id" in df_pipeline.columns and isinstance(df_pipeline["_id"][0], dict):
                    id_df = pd.json_normalize(df_pipeline["_id"])
                    df_pipeline = pd.concat([id_df, df_pipeline.drop(columns=["_id"])], axis=1)

                st.session_state.df_pipeline = df_pipeline
                st.session_state.pipeline_hash = pipeline_hash

                st.success("✅ Pipeline berhasil dijalankan!")
            except Exception as e:
                st.error(f"❌ Gagal memproses pipeline: {e}")
                st.session_state.df_pipeline = None

        if st.session_state.df_pipeline is not None:
            st.dataframe(st.session_state.df_pipeline)

            st.markdown("**3. Pilih visualisasi:**")
            chart_type = st.selectbox("Jenis Visualisasi", ["Bar Chart", "Line Chart", "Pie Chart"])
            df_pipeline = st.session_state.df_pipeline
            numeric_columns = df_pipeline.select_dtypes(include="number").columns.tolist()
            all_columns = df_pipeline.columns.tolist()

            x_col = st.selectbox("Kolom X", all_columns)
            y_col = st.selectbox("Kolom Y", numeric_columns)

            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            if chart_type == "Bar Chart":
                df_pipeline.plot(kind="bar", x=x_col, y=y_col, ax=ax)
            elif chart_type == "Line Chart":
                df_pipeline.plot(kind="line", x=x_col, y=y_col, ax=ax)
            elif chart_type == "Pie Chart":
                df_pipeline.set_index(x_col)[y_col].plot.pie(autopct='%1.1f%%', ax=ax)

            st.pyplot(fig)
    else:
        st.info("Tekan tombol 'Jalankan Pipeline' untuk menjalankan dan menampilkan hasil.")


elif page == "Tim":
    # CSS styling
    st.markdown("""
    <style>
    .team-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-bottom: 40px;
    }
    .team-member {
        display: flex;
        width: 100%;
        max-width: 100%;
        margin-bottom: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: all 0.3s ease;
        position: relative;
    }
    .team-member:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    .photo-container {
        width: 40%;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #f8f9fa;
        position: relative;
        z-index: 1;
        overflow: hidden;
    }
    .photo-container img.background {
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.8;
    }
    .team-photo {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4f8bf9;
        position: relative;
        z-index: 2;
    }
    .info-container {
        flex: 1;
        padding: 25px;
        position: relative;
    }
    .region-label {
        position: absolute;
        top: 15px;
        right: 15px;
        background: rgba(79, 139, 249, 0.9);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        z-index: 3;
    }
    .role-badge {
        background: #4f8bf9;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        display: inline-block;
        margin: 8px 0;
        position: relative;
        z-index: 1;
    }
    .github-btn {
        display: inline-block;
        background: #333;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        margin-top: 15px;
        font-size: 14px;
        transition: all 0.3s;
        position: relative;
        z-index: 2;
    }
    .github-btn:hover {
        background: #555;
        transform: scale(1.05);
    }
    .section-title {
        text-align: center;
        margin-bottom: 40px !important;
        color: #2c3e50;
        font-size: 2.5rem;
    }
    .ranking-opinion {
        font-size: 14px;
        color: #555;
        margin-top: 15px;
        padding: 15px;
        background: rgba(248, 249, 250, 0.8);
        border-radius: 8px;
        text-align: left;
        position: relative;
        z-index: 1;
    }
    .member-name {
        color: #2c3e50;
        margin-bottom: 5px;
        position: relative;
        z-index: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <h1 class="section-title">👨‍💻 Tim Data Kami</h1>
    <p style="text-align: center; font-size: 18px; color: #555; max-width: 800px; margin: 0 auto 40px;">
        Tim spesialis data yang membangun infrastruktur data kelas dunia
    </p>
    """, unsafe_allow_html=True)

    # Watermark image URLs
    watermark_images = {
        "BALI": "https://cdn.divessi.com/cached/Indonesia_Bali_Shutterstock_chanchai-duangdoosan.jpg/1200.jpg",
        "AMBON": "https://assets.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/p3/93/2024/07/19/955-jembatan_merah_putih_di_kota_ambon-1-3023159357.jpg",
        "JAWA BARAT": "https://ik.imagekit.io/tvlk/blog/2023/05/pangandaran_shutterstock_1270074370-1.jpg",
        "MAKASSAR": "https://img.okezone.com/content/2023/02/03/406/2758665/menguak-asal-usul-kenapa-makassar-juga-disebut-ujung-pandang-ubKIQMTSus.jpg"
    }

    # Data tim dengan pendapat tentang ranking universitas dan watermark
    team_data = [
        {
            "name": "Ngurah Sentana",
            "role": "Data Engineer | Data Science | Project Management",
            "photo": "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/Ngurah.jpeg",
            "github": "https://github.com/ngurahsentana24",
            "ranking_opinion": "Ranking universitas mencerminkan upaya institusi dalam menjaga kualitas pendidikan, riset, dan reputasi global. Bagi saya, belajar di kampus berperingkat tinggi memberikan akses ke dosen unggulan, jaringan profesional yang luas, dan lingkungan akademik yang menantang. Meskipun kemampuan praktis tetap penting, reputasi universitas dapat menjadi modal awal yang kuat dalam membangun karier.",
            "watermark": "BALI",
            "region": "Bali"
        },
        {
            "name": "Adib Roilsilmi",
            "role": "Data Engineer | Data Science | Project Management",
            "photo": "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/Adib.jpg",
            "github": "https://github.com/bellakartika",
            "ranking_opinion": "Ranking universitas mencerminkan upaya institusi dalam menjaga kualitas pendidikan dan inovasi. Lulusan dari kampus bereputasi umumnya memiliki dasar teori yang kuat, dan ketika ini dikombinasikan dengan pengalaman praktis seperti magang atau proyek nyata, mereka menjadi aset berharga di industri teknologi.",
            "watermark": "MAKASSAR",
            "region": "Makassar"
        },
        {
            "name": "Awantara",
            "role": "Data Engineer | Data Science | Project Management",
            "photo": "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/Awantara.jpg",
            "github": "https://github.com/Awantara7",
            "ranking_opinion": "Ranking universitas memberikan gambaran kualitas institusi, dan akan semakin bernilai ketika kampus juga membekali mahasiswa dengan pemikiran kritis serta kemampuan memecahkan masalah nyata menggunakan data.",
            "watermark": "BALI",
            "region": "Bali"
        },
        {
            "name": "Unique",
            "role": "Data Engineer | Data Science | Project Management",
            "photo": "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/Uniq.jpg",
            "github": "https://github.com/Uniq",
            "ranking_opinion": "Ranking universitas membantu membangun reputasi awal, dan di era digital saat ini, hal itu semakin kuat ketika dipadukan dengan semangat belajar mandiri dan kemampuan beradaptasi yang tinggi.",
            "watermark": "AMBON",
            "region": "Ambon"
        },
        {
            "name": "Desy Endriani",
            "role": "Data Engineer | Data Science | Project Management",
            "photo": "https://raw.githubusercontent.com/Awantara7/MDS-Project-II---Kelompok-1/main/Gambar/Desy.jpeg",
            "github": "https://github.com/desyendriani",
            "ranking_opinion": "Ranking universitas bisa jadi awal yang baik, namun perjalanan karier yang berkelanjutan dibentuk oleh pengalaman nyata, kemampuan yang terasah, dan semangat kerja yang konsisten.",
            "watermark": "JAWA BARAT",
            "region": "Jawa Barat"
        }
    ]

    # Membuat container untuk tim
    st.markdown('<div class="team-container">', unsafe_allow_html=True)

    # Membuat card untuk setiap anggota tim
    for member in team_data:
        st.markdown(f"""
        <div class="team-member">
            <div class="photo-container">
                <img src="{watermark_images[member['watermark']]}" class="background" alt="Background">
                <img src="{member['photo']}" class="team-photo" alt="{member['name']}">
                <a href="{member['github']}" target="_blank" class="github-btn">Profil GitHub</a>
            </div>
            <div class="info-container">
                <div class="region-label">{member['region']}</div>
                <h3 class="member-name">{member['name']}</h3>
                <div class="role-badge">{member['role']}</div>
                <div class="ranking-opinion">
                    <strong>Pendapat tentang ranking universitas:</strong><br>
                    {member['ranking_opinion']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bagian footer
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <h3 style="color: #2c3e50;">Tertarik Bergabung dengan Tim Kami?</h3>
        <p style="font-size: 16px; color: #555; max-width: 600px; margin: 10px auto 20px;">
            Kami mencari talenta data yang percaya bahwa kompetensi lebih penting daripada sekedar gelar
        </p>
    </div>
    """, unsafe_allow_html=True)

# ======= FOOTER =======
st.markdown("<footer>© 2025 THE University Rankings Intelligence. All rights reserved.</footer>", unsafe_allow_html=True)


