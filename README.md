# Global Student Analytics Dashboard

Dashboard interaktif yang dibangun menggunakan **Streamlit** dan **Plotly** untuk menganalisis performa akademik, kebiasaan, dan pola gaya hidup mahasiswa berdasarkan dataset *Global University Students Performance & Habits*. 

Aplikasi ini berfokus pada pendekatan **Data Storytelling**, mendepankan *data-ink ratio* yang tinggi dan meminimalkan bias visual untuk menggali *signal* dari *noise*.

## Fitur Utama

- **Filter Interaktif**: Lakukan filter data berdasarkan *Country*, *Major*, dan *Part-time Job* dari Sidebar.
- **Tab 1: Overview & Demografi**: Melihat distribusi umum dari demografi sampel. Menyoroti absennya bias demografis.
- **Tab 2: Faktor Performa Akademik**: Menganalisis korelasi langsung (secara individu dan kelompok) antara jam belajar dengan IPK (GPA), serta membuktikan tidak adanya bias sosial-ekonomi yang memengaruhi nilai.
- **Tab 3: Gaya Hidup & Stres**: Triangulasi data antara waktu bermedia sosial, level stres, dan skor akhir.

## Prasyarat

Pastikan Anda telah menginstal **Python 3.8+**.

## Instalasi

1. Buka Terminal / Command Prompt / PowerShell.
2. Navigasikan ke direktori project ini:
   ```bash
   cd "d:\kuliah\Smt 6\Tugas Projek\Visdat Tahap 3"
   ```
3. (Opsional) Buat dan aktifkan *virtual environment*:
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Mac/Linux:
   source venv/bin/activate
   ```
4. Install semua dependensi (library) yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi

1. Pastikan file dataset `global_university_students_performance_habits_10000.csv` berada di dalam folder yang sama dengan `app.py`.
2. Jalankan perintah berikut di Terminal:
   ```bash
   streamlit run app.py
   ```
3. Browser akan otomatis terbuka dan menampilkan dashboard di `http://localhost:8501`.

## Teknologi yang Digunakan
- **[Streamlit](https://streamlit.io/)** - Pembuatan Web Apps / Dashboard
- **[Pandas](https://pandas.pydata.org/)** - Manipulasi dan Analisis Data
- **[Plotly](https://plotly.com/)** - Visualisasi Data Interaktif
- **[Numpy](https://numpy.org/)** - Komputasi Numerik
