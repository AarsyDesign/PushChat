---
version: alpha
name: PushChat Refined Utility
description: Modern, distraction-free interface for Instagram automation and direct conversion.
colors:
  primary: "#0F172A"
  secondary: "#475569"
  accent: "#10B981"
  surface: "#FFFFFF"
  surface-muted: "#F8FAFC"
  border: "#E2E8F0"
  border-focus: "#0F172A"
typography:
  h1:
    fontFamily: Geist Sans, Inter, system-ui
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h2:
    fontFamily: Geist Sans, Inter, system-ui
    fontSize: 1.5rem
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Geist Sans, Inter, system-ui
    fontSize: 0.9375rem
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: Geist Sans, Inter, system-ui
    fontSize: 0.8125rem
    fontWeight: 500
    lineHeight: 1.4
rounded:
  sm: 4px
  md: 8px
  lg: 12px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 10px 16px
  button-primary-hover:
    backgroundColor: "#1E293B"
    textColor: "#FFFFFF"
  card-rule:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 20px
  status-active:
    backgroundColor: "#ECFDF5"
    textColor: "{colors.accent}"
    rounded: "{rounded.sm}"
    padding: 4px 8px
---

## Overview

PushChat menerapkan bahasa desain Modern Refined Utility: antarmuka kerja yang tenang, fungsional, dan bebas dari ornamen visual kosong. Dibuat khusus untuk kreator konten dan pemilik bisnis daring yang membutuhkan kecepatan pengaturan tanpa distraksi.

Prinsip utama antarmuka:
- Nol dekorasi nirfungsi (tanpa efek glassmorphism berlebihan atau gradasi warna-warni).
- Mengutamakan tipografi reguler dengan hierarki kontras yang terukur.
- Seluruh elemen interaktif wajib berfungsi penuh dan dapat dioperasikan menggunakan papan ketik.
- Dilarang keras memakai karakter em dash pada seluruh teks antarmuka.

Dial: ENERGY 1 / RHYTHM 2 / MOTION 1

## Colors

- **Primary (#0F172A):** Slate gelap pekat untuk judul utama, teks tubuh, dan tombol tindakan prioritas.
- **Secondary (#475569):** Abu-abu netral untuk teks penjelas sekunder dan label pembantu.
- **Accent (#10B981):** Hijau emerald fungsional yang menandai aturan aktif dan keberhasilan otomasi.
- **Surface (#FFFFFF & #F8FAFC):** Kanvas latar belakang datar yang bersih dan kontras tinggi.
- **Border (#E2E8F0):** Batas hairline 1px halus pemisah konten tanpa bayangan tebal.

## Typography

Menggunakan sans-serif modern (Geist Sans atau Inter) dengan bobot reguler (400) dan semi-bold (600).
- Penekanan teks dilakukan melalui ukuran dan kontras warna, bukan melalui penambahan ketebalan huruf tebal berlebihan.
- Jarak antarbaris diatur longgar (1.5) untuk kenyamanan membaca di layar perangkat bergerak.

## Layout & Spacing

Tata letak berfokus pada alur linear tiga langkah tanpa diagram node yang rumit:
1. Kolom pemilihan konten (Reels atau Feeds aktif).
2. Kolom penentuan kata kunci pemicu dan opsi Follow-Gate.
3. Kolom pratinjau pesan privat langsung (live mobile mockup).

Jarak antarelemen menggunakan sistem modular 8px (8px, 16px, 24px, 32px) untuk menjaga konsistensi perataan.

## Elevation & Depth

- Tidak menggunakan bayangan mengambang yang dramatis.
- Kedalaman antarmuka dicapai melalui batas garis tipis 1px (`#E2E8F0`) dan perbedaan warna latar permukaan (`#FFFFFF` vs `#F8FAFC`).

## Shapes

- Radius sudut dibatasi pada nilai fungsional: 4px untuk badge status, 8px untuk tombol dan input, 12px untuk card container.
- Menghindari bentuk kapsul oval (*pill-shape*) menyeluruh pada seluruh komponen antarmuka.

## Components

- **Header:** Tata letak ringkas dengan tombol aksi berbasis ikon SVG monoline untuk pemilihan akun dan status koneksi API.
- **Rule Card:** Kartu baris horizontal yang menampilkan pemicu, aksi respon, statistik konversi, dan tombol aktif/nonaktif.
- **Live Preview:** Pratinjau visual layar smartphone di sisi kanan formulir yang memperbarui tampilan gelembung pesan privat saat pengguna mengetik.

## Do's and Don'ts

### Do
- Sediakan indikator status jelas (Aktif, Dijeda, Terhubung, Gagal) pada setiap aturan.
- Gunakan ikon SVG monoline dengan goresan seragam (stroke 1.5px).
- Sediakan umpan balik visual instan saat aturan berhasil disimpan atau diuji.
- Pastikan seluruh navigasi dan modal dapat ditutup dengan tombol Escape pada papan ketik.

### Don't
- Dilarang memasang tombol tanpa aksi atau tautan tanpa tujuan yang jelas.
- Dilarang menggunakan emoji sebagai pengganti ikon navigasi inti antarmuka.
- Dilarang menggunakan karakter em dash pada judul, keterangan, maupun pesan konfirmasi.
- Dilarang membuat diagram flowchart labirin yang membingungkan pengguna pemula.
