[app]

# (str) Judul aplikasi Kakak
title = SmartTots World

# (str) Nama package (tanpa spasi)
package.name = smarttots

# (str) Domain package (biasanya dibalik dari nama pembuat/perusahaan)
package.domain = org.smarttots

# (list) Berkas sumber (kode dan aset) yang mau dimasukkan ke APK
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Berkas utama yang dijalankan pertama kali
source.include_dir = .
main.file = main.py

# (list) Pustaka/library Python yang wajib ikut di-install
requirements = python3,kivy

# (str) Orientasi layar aplikasi (portrait = berdiri, landscape = mendatar)
orientation = portrait

# (list) Izin akses Android (permissions) jika nanti butuh internet atau suara
android.permissions = INTERNET

[buildozer]

# (int) Tingkat log/error (0 = info ringan, 2 = debug lengkap)
log_level = 2

# (int) Lewati pembaruan android SDK jika tidak perlu
warn_on_root = 1

