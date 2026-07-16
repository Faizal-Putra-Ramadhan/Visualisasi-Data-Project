import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Performance & Habits Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR MINIMALIST DESIGN ---
st.markdown("""
    <style>
    /* Remove padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Clean headers */
    h1, h2, h3 {
        color: #2C3E50;
        font-family: 'Inter', sans-serif;
    }
    /* Storytelling text styling */
    .story-text {
        font-size: 1.1rem;
        color: #555;
        border-left: 4px solid #3498DB;
        padding-left: 15px;
        margin-top: 10px;
        margin-bottom: 30px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_path = "global_university_students_performance_habits_10000.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # Fallback to empty dataframe if not found to avoid crashing before data is provided
        st.error(f"File {file_path} tidak ditemukan. Mohon pastikan file berada di direktori yang sama.")
        return pd.DataFrame()
    
    # Ensure column names are stripped of whitespace and lowercase
    df.columns = df.columns.str.strip().str.lower()
    return df

df_raw = load_data()

if df_raw.empty:
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")

def multiselect_filter(col_name, label):
    if col_name in df_raw.columns:
        options = ["All"] + sorted(df_raw[col_name].dropna().unique().tolist())
        selected = st.sidebar.multiselect(label, options, default="All")
        return selected
    return ["All"]

selected_country = multiselect_filter('country', 'Negara (Country)')
selected_major = multiselect_filter('major', 'Jurusan (Major)')
selected_job = multiselect_filter('part_time_job', 'Pekerjaan Paruh Waktu')
selected_age = multiselect_filter('age', 'Usia (Age)')
selected_gender = multiselect_filter('gender', 'Gender (Jenis Kelamin)')

# Apply filters
df = df_raw.copy()
if "All" not in selected_country and len(selected_country) > 0:
    df = df[df['country'].isin(selected_country)]
if "All" not in selected_major and len(selected_major) > 0:
    df = df[df['major'].isin(selected_major)]
if "All" not in selected_job and len(selected_job) > 0:
    df = df[df['part_time_job'].isin(selected_job)]
if "All" not in selected_age and len(selected_age) > 0:
    df = df[df['age'].isin(selected_age)]
if "All" not in selected_gender and len(selected_gender) > 0:
    df = df[df['gender'].isin(selected_gender)]

# --- MAIN DASHBOARD TITLE ---
st.title("Global Student Analytics Dashboard")
st.markdown("Menganalisis pola perilaku, stres, dan dampaknya terhadap performa akademik mahasiswa secara global.")
st.markdown("---")

# --- PLOTLY CONFIG (No Gridlines) ---
def clean_layout(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

# --- TABS ---
tab1, tab2, tab3 = st.tabs([
    "Tab 1: Overview & Demografi", 
    "Tab 2: Faktor Performa Akademik", 
    "Tab 3: Gaya Hidup & Stres"
])

# ==========================================
# TAB 1: OVERVIEW & DEMOGRAFI
# ==========================================
with tab1:
    st.header("Overview Eksekutif & Sebaran Demografi")
    
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Mahasiswa", f"{len(df):,}")
    with col2:
        if 'gpa' in df.columns:
            st.metric("Rata-rata GPA", f"{df['gpa'].mean():.2f}")
    with col3:
        # Check for attendance column, use alternative if missing
        attendance_col = next((col for col in df.columns if 'attendance' in col), None)
        if attendance_col:
            st.metric("Rata-rata Kehadiran", f"{df[attendance_col].mean():.1f}%")
        else:
            st.metric("Total Fitur (Kolom)", f"{len(df.columns)}")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    
    with colA:
        if 'gpa' in df.columns:
            fig_gpa = px.histogram(
                df, x="gpa", 
                nbins=20, 
                title="Sebaran GPA (Cenderung Ke Kanan)",
                color_discrete_sequence=['#3498db'],
                opacity=0.8
            )
            fig_gpa = clean_layout(fig_gpa)
            fig_gpa.update_traces(marker_line_width=1, marker_line_color="white")
            st.plotly_chart(fig_gpa, use_container_width=True)
            st.markdown(
                '<div class="story-text">Sebaran nilai IPK (GPA) mahasiswa tidak terdistribusi normal, melainkan menumpuk di sisi kanan (left-skewed). Hal ini mengindikasikan bahwa secara umum, mahasiswa mendapatkan nilai yang baik, atau standar penilaian yang cenderung longgar.</div>', 
                unsafe_allow_html=True
            )
            
    with colB:
        if 'major' in df.columns:
            major_counts = df['major'].value_counts().reset_index()
            major_counts.columns = ['major', 'count']
            
            fig_major = px.bar(
                major_counts, 
                y='major', x='count', 
                orientation='h',
                title="Distribusi Mahasiswa per Jurusan (Zero Demographic Bias)",
                color='count',
                color_continuous_scale='Blues'
            )
            fig_major = clean_layout(fig_major)
            fig_major.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_major, use_container_width=True)
            st.markdown(
                '<div class="story-text">Distribusi jurusan atau asal negara menunjukkan pola yang sangat merata (flat). Tidak ada satu kelompok demografi yang mendominasi data, memastikan bahwa analisis perilaku selanjutnya minim bias latar belakang.</div>', 
                unsafe_allow_html=True
            )

# ==========================================
# TAB 2: FAKTOR PERFORMA AKADEMIK
# ==========================================
with tab2:
    st.header("Analisis Faktor Penentu Performa (GPA)")
    
    # Grafik 1: Scatter Plot Study Hours vs GPA
    if 'study_hours_per_day' in df.columns and 'gpa' in df.columns:
        fig_scatter = px.scatter(
            df, x='study_hours_per_day', y='gpa',
            opacity=0.4,
            trendline="ols",
            trendline_color_override="red",
            title="Korelasi Jam Belajar Harian vs GPA",
            color_discrete_sequence=['#2ecc71']
        )
        fig_scatter = clean_layout(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown(
            '<div class="story-text">Setiap titik mewakili satu mahasiswa. Garis tren merah menunjukkan arah korelasi: waktu belajar harian memiliki dampak positif yang konsisten terhadap IPK mahasiswa. Pola ini terlihat sangat jelas dari level individu tanpa agregasi.</div>', 
            unsafe_allow_html=True
        )
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafik 2: Binned Bar Chart (Study Hours vs GPA)
        if 'study_hours_per_day' in df.columns and 'gpa' in df.columns:
            df_binned = df.copy()
            df_binned['study_hours_bin'] = np.floor(df_binned['study_hours_per_day']).astype(int)
            binned_gpa = df_binned.groupby('study_hours_bin')['gpa'].mean().reset_index()
            
            fig_binned = px.bar(
                binned_gpa, x='study_hours_bin', y='gpa',
                title="Rata-rata GPA Berdasarkan Jam Belajar (Pola Naik-Tangga)",
                color='gpa',
                color_continuous_scale='Viridis'
            )
            fig_binned = clean_layout(fig_binned)
            fig_binned.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_binned, use_container_width=True)
            st.markdown(
                '<div class="story-text">Ketika dikelompokkan per 1 jam pelajaran, rata-rata IPK membentuk pola anak tangga yang naik konsisten. Semakin banyak jam belajar, semakin tinggi rata-rata skor yang diperoleh.</div>', 
                unsafe_allow_html=True
            )
            
    with col2:
        # Grafik 3: Box Plot GPA by Income/Gender
        group_col = 'family_income_level' if 'family_income_level' in df.columns else 'gender'
        if group_col in df.columns and 'gpa' in df.columns:
            fig_box = px.box(
                df, x=group_col, y='gpa',
                color=group_col,
                title=f"Distribusi GPA Berdasarkan {group_col.replace('_', ' ').title()}",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_box = clean_layout(fig_box)
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
            st.markdown(
                f'<div class="story-text">Garis median (tengah kotak) di berbagai kelompok {group_col.replace("_", " ")} tampak sejajar sempurna. Ini adalah bukti visual kuat bahwa faktor sosioekonomi/demografi tidak mendikte performa akademik pada sampel ini.</div>', 
                unsafe_allow_html=True
            )

# ==========================================
# TAB 3: GAYA HIDUP & STRES
# ==========================================
with tab3:
    st.header("Analisis Triangulasi Gaya Hidup & Stres")
    
    # Grafik 1: Social Media vs Stress (Color: Final Score)
    required_cols = ['social_media_hours', 'mental_stress_level', 'final_exam_score']
    if all(col in df.columns for col in required_cols):
        # We need trendline for scatter
        fig_stress = px.scatter(
            df, x='social_media_hours', y='mental_stress_level',
            color='final_exam_score',
            color_continuous_scale='RdYlGn', # Red to Green
            opacity=0.7,
            trendline='ols',
            trendline_color_override='black',
            title="Penggunaan Media Sosial vs Stres Mental (Warna: Skor Ujian Akhir)"
        )
        fig_stress = clean_layout(fig_stress)
        st.plotly_chart(fig_stress, use_container_width=True)
        st.markdown(
            '<div class="story-text">Triangulasi tiga variabel: Sumbu X adalah jam sosmed, Sumbu Y tingkat stres, dan Warna adalah Nilai Ujian (Hijau=Tinggi, Merah=Rendah). Jika diamati, titik-titik hijau (nilai tinggi) cenderung berada di kuadran kiri bawah (rendah sosmed, rendah stres), namun korelasi linier (garis hitam) menunjukkan pola yang kompleks dan mungkin hanya berhubungan lemah.</div>', 
            unsafe_allow_html=True
        )
        
    # Grafik 2: Part Time Job vs Study Hours
    if 'part_time_job' in df.columns and 'study_hours_per_day' in df.columns:
        fig_job = px.box(
            df, y='part_time_job', x='study_hours_per_day',
            color='part_time_job',
            orientation='h',
            title="Manajemen Waktu: Jam Belajar vs Pekerjaan Paruh Waktu",
            color_discrete_sequence=['#e74c3c', '#3498db']
        )
        fig_job = clean_layout(fig_job)
        fig_job.update_layout(showlegend=False)
        st.plotly_chart(fig_job, use_container_width=True)
        st.markdown(
            '<div class="story-text">Boxplot ini memperlihatkan bagaimana mahasiswa dengan pekerjaan paruh waktu mengatur jadwal mereka. Rentang sebaran jam belajar (lebar kotak) memberikan insight mengenai trade-off (kompromi) waktu yang harus dilakukan dibandingkan mereka yang tidak bekerja.</div>', 
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Dashboard Data Storytelling © 2026</p>", unsafe_allow_html=True)
