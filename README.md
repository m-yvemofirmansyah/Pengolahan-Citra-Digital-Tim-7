# PicLab

**PicLab** adalah aplikasi desktop berbasis Python yang dikembangkan sebagai proyek mata kuliah **Pengolahan Citra Digital (PCD)** oleh Kelompok 7.

Aplikasi ini dirancang untuk melakukan berbagai operasi pengolahan citra digital melalui antarmuka grafis (*Graphical User Interface/GUI*). PicLab menyediakan berbagai kategori operasi, mulai dari operasi dasar, peningkatan kualitas citra, penambahan noise, deteksi tepi, hingga segmentasi.

Pengembangan aplikasi dilakukan secara bertahap dengan mengimplementasikan algoritma yang telah dipelajari selama perkuliahan.

## Tampilan Aplikasi

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/6aa1e97c-b465-451b-b7c8-66318bd7481f" />


## Teknologi yang Digunakan

- **Python** — bahasa pemrograman utama.
- **Tkinter** — membangun antarmuka grafis aplikasi.
- **OpenCV** — melakukan pemrosesan dan manipulasi citra digital.
- **NumPy** — melakukan operasi array dan perhitungan numerik.
- **Pillow (PIL)** — membaca, mengolah, dan menampilkan gambar.
- **Matplotlib** — digunakan untuk visualisasi hasil algoritma selama praktikum.

## Fitur Aplikasi

PicLab memiliki beberapa kategori operasi pengolahan citra digital.

### 1. Basic Operations

Kategori ini berisi berbagai operasi dasar untuk memanipulasi citra digital.

**Fitur yang sudah diintegrasikan:**

| Fitur | Deskripsi | Status |
|---|---|---|
| Negative | Membalik nilai intensitas piksel menggunakan rumus 255 - nilai piksel. | Selesai |
| Flipping Horizontal | Membalik citra dari kiri ke kanan. | Selesai |
| Flipping Vertical | Membalik citra dari atas ke bawah. | Selesai |
| Flipping Both | Membalik citra secara horizontal dan vertikal. | Selesai |
| Arithmetic - Add | Menjumlahkan citra dengan nilai skalar atau citra lain. | Selesai |
| Arithmetic - Subtract | Mengurangi citra dengan nilai skalar atau citra lain. | Selesai |
| Arithmetic - Multiply | Mengalikan citra dengan nilai skalar atau citra lain. | Selesai |
| Arithmetic - Divide | Membagi citra dengan nilai skalar atau citra lain. | Selesai |
| Grayscale Conversion | Mengubah citra RGB menjadi citra grayscale. | Selesai |
| Grayscale Gradient | Menghasilkan citra grayscale 8-bit dengan gradasi intensitas 0–255. | Selesai |
| Binary Image | Menghasilkan citra biner 100 × 100 piksel dengan area putih di bagian tengah. | Selesai |

**Fitur yang belum diintegrasikan:**

- Boolean Operations (NOT, AND, OR, XOR).
- Geometric Operations (Translation, Rotation, Zooming, dan Cropping).
- Thresholding.
- Convolution.
- Fourier Transform.
- Colouring (RGB, HSV, CMY, YUV, YIQ, dan Pseudo).

### 2. Enhancement

Kategori untuk operasi peningkatan kualitas citra.

Rencana fitur:
- Brightness.
- Contrast.
- Histogram Equalization.
- Smoothing (Spatial Domain dan Frequency Domain).
- Sharpening (Spatial Domain dan Frequency Domain).
- Geometric Correction.

### 3. Noise

Kategori untuk menerapkan berbagai jenis noise pada citra digital.

Rencana fitur:
- Gaussian Noise.
- Rayleigh Noise.
- Erlang (Gamma) Noise.
- Exponential Noise.
- Uniform Noise.
- Impulse Noise.

### 4. Edge Detection

Kategori untuk mendeteksi tepian atau batas objek pada citra.

Rencana fitur:
- **First Differential Gradient:** Sobel, Prewitt, dan Robert.
- **Second Differential Gradient:** Laplacian, LoG, dan Canny.

### 5. Segmentation

Kategori untuk pengembangan operasi segmentasi citra digital.

### 6. About

Berisi informasi mengenai aplikasi dan tim pengembang, termasuk:
- Informasi Tim Developer.
- GitHub.
- YouTube.

## Struktur Proyek

```text
PicLab/
│
├── operations/
│   └── basic.py
│
├── Laporan/
│   ├── images/
│   └── Laporan Proyek Akhir PCD.md
│
├── main.py
└── main copy.py
```

Keterangan:
- `main.py` merupakan file utama untuk menjalankan aplikasi dan mengatur antarmuka.
- `operations/` berisi implementasi algoritma pengolahan citra digital.
- `Laporan/` berisi dokumentasi dan laporan proyek.
- `main copy.py` merupakan salinan file utama.

## Instalasi dan Penggunaan

### 1. Clone Repository

```bash
git clone <URL-REPOSITORY>
```

### 2. Masuk ke Direktori Proyek

```bash
cd PicLab
```

### 3. Instalasi Dependencies

```bash
pip install numpy opencv-python pillow matplotlib
```

### 4. Jalankan Aplikasi

```bash
python main.py
```

## Pengembangan

PicLab dikembangkan secara bertahap. Fitur-fitur yang tersedia akan terus ditambahkan dan disempurnakan berdasarkan materi praktikum Pengolahan Citra Digital.

## Pengembang

**Kelompok 7 — Proyek Pengolahan Citra Digital**

Repository ini dikembangkan sebagai bagian dari kegiatan pembelajaran dan implementasi materi mata kuliah Pengolahan Citra Digital.
