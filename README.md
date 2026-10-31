# PushChat

Infrastruktur otomatisasi pesan privat Instagram dan Threads berbasis tindakan pengguna (Comment-to-DM, Story Mention, dan Follow-Gate) dengan integrasi resmi Meta Graph API.

Didesain khusus untuk kreator konten, penjual daring, dan bisnis digital di Indonesia: tanpa biaya per kontak yang menghukum pertumbuhan audiens, dan didukung pembayaran langganan prabayar via QRIS lokal.

---

## Nilai Jual Utama (USP)

1. **Flat Subscription via QRIS (Tanpa Pajak Pertumbuhan)**  
   Biaya langganan bulanan tetap tanpa menghitung jumlah kontak yang tersimpan. Lonjakan interaksi pada konten viral tidak memicu kenaikan tarif mendadak.
2. **Alur Kerja Tiga Langkah (Zero-Spaghetti)**  
   Pengaturan selesai dalam 30 detik: pilih postingan pemicu, tentukan kata kunci, dan tulis respon pesan privat beserta tautan tujuan. Tidak memerlukan diagram logika percabangan yang rumit.
3. **Follow-Gate Terintegrasi**  
   Memeriksa status pengikut sebelum tautan dapat diakses untuk mendorong pertumbuhan pengikut secara organik.
4. **Variasi Balasan Komentar Otomatis**  
   Pengacakan respon di kolom komentar publik untuk menjaga reputasi akun dan mematuhi batas frekuensi interaksi platform.
5. **Sinergi Ekosistem Bersama PushNotif**  
   Pengguna dapat menghubungkan prospek dari pesan privat media sosial langsung ke infrastruktur notifikasi web dan pesan transaksional.

---

## Arsitektur Sistem

Proyek ini dibangun sebagai layanan mandiri terisolasi untuk menjamin stabilitas infrastruktur utama:

* **Backend Engine:** FastAPI (Python 3.12) asinkron berkinerja tinggi.
* **Database & Auth:** Berjalan mandiri dengan opsi verifikasi saldo kredit atau status langganan terhubung via SQLite WAL.
* **Isolasi Proses:** Berjalan pada port mandiri (`8092`) dengan isolasi memori terproteksi.
* **Integrasi Eksternal:** Meta Graph API (Instagram Messaging API & Webhook Handler).

---

## Struktur Repositori

```
pushchat/
├── .gitignore
├── Dockerfile
├── requirements.txt
├── database.py       # Pengelola schema, token, dan aturan otomasi
├── main.py           # Endpoint REST API dan Webhook Meta
├── DESIGN.md         # Spesifikasi token visual dan panduan antarmuka
└── tests/
    └── test_pushchat_core.py
```

---

## Cara Menjalankan Layanan

### Menjalankan di Lingkungan Lokal

```bash
# Aktifkan virtual environment
source .venv/bin/activate

# Jalankan server pengembangan
uvicorn main:app --host 0.0.0.0 --port 8092 --reload
```

### Menjalankan Pengujian Terisolasi

```bash
PYTHONPATH=. pytest tests/
```

---

## Lisensi

Hak Cipta (c) 2026 AarsyDesign. Hak cipta dilindungi undang-undang.
