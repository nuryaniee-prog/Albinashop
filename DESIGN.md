---
name: Albina Business Console
type: design-system
version: "0.5"
status: active-local
created: 2026-11-01
language: id-ID
theme: light
colors:
  background: '#ffffff'
  surface-lowest: '#fffaf5'
  surface-low: '#fff7ed'
  surface: '#ffffff'
  surface-high: '#ffedd5'
  surface-highest: '#fed7aa'
  on-surface: '#292524'
  on-surface-variant: '#57534e'
  text-muted: '#78716c'
  outline-subtle: '#ead7c4'
  outline-control: '#a8a29e'
  primary: '#c2410c'
  on-primary: '#ffffff'
  secondary: '#f97316'
  secondary-strong: '#9a3412'
  accent: '#fb923c'
  accent-strong: '#ea580c'
  success: '#26734d'
  warning: '#925d00'
  danger: '#b42318'
  danger-container: '#fff0ec'
  on-danger-container: '#b42318'
  focus: '#9a3412'
typography:
  headline-lg: {fontFamily: 'Space Grotesk', fontSize: '32px', fontWeight: 600, lineHeight: '40px'}
  headline-mobile: {fontFamily: 'Space Grotesk', fontSize: '26px', fontWeight: 600, lineHeight: '34px'}
  headline-md: {fontFamily: 'Space Grotesk', fontSize: '22px', fontWeight: 500, lineHeight: '30px'}
  headline-sm: {fontFamily: 'Space Grotesk', fontSize: '18px', fontWeight: 500, lineHeight: '26px'}
  body-lg: {fontFamily: 'Geist', fontSize: '16px', fontWeight: 400, lineHeight: '24px'}
  body-md: {fontFamily: 'Geist', fontSize: '14px', fontWeight: 400, lineHeight: '22px'}
  body-sm: {fontFamily: 'Geist', fontSize: '12px', fontWeight: 400, lineHeight: '18px'}
  label: {fontFamily: 'JetBrains Mono', fontSize: '12px', fontWeight: 500, lineHeight: '18px', letterSpacing: '0.04em'}
  metric: {fontFamily: 'JetBrains Mono', fontSize: '28px', fontWeight: 600, lineHeight: '36px', letterSpacing: '-0.02em'}
  metric-mobile: {fontFamily: 'JetBrains Mono', fontSize: '24px', fontWeight: 600, lineHeight: '32px'}
radius:
  input: '6px'
  button: '6px'
  card: '8px'
  overlay: '12px'
  badge: '4px'
  avatar: '9999px'
spacing:
  unit: '4px'
  scale: ['4px', '8px', '12px', '16px', '24px', '32px', '40px', '48px']
  page-desktop: '24px'
  page-mobile: '16px'
  grid-gap: '16px'
  card-padding: '20px'
layout:
  sidebar: '256px'
  sidebar-compact: '72px'
  topbar: '64px'
  inspector: '320px'
  content-max: '1760px'
  breakpoints: {mobile: '0–767px', tablet: '768–1199px', desktop: '1200–1439px', wide: '1440px+'}
motion:
  fast: '120ms'
  standard: '180ms'
  overlay: '220ms'
sources:
  - 'DESIGN (4).md — Synthetic Command'
  - 'stitch_futuristic_system_dashboard_ui.zip — Security Protocol'
  - 'stitch_futuristic_system_dashboard_ui (1).zip — Neural Nodes'
  - 'PRD Albina Shop Dashboard v0.2 - 2026-11-01.md'
  - 'FRD Albina Shop Dashboard v0.2 - 2026-11-01.md'
  - 'TRD Albina Shop Dashboard v0.2 - 2026-11-01.md'
---

# DESIGN — Albina Shop Business Dashboard

Panduan visual dan interaksi untuk aplikasi operasional Albina Shop. Versi 0.5, 2026-11-01, Asia/Jakarta. Dokumen ini mengadaptasi referensi pengguna menjadi kebutuhan retail fashion, penjualan offline, gudang bersama, dan koordinasi tim.

Status: **tema aktif pada aplikasi lokal** di `http://127.0.0.1:4180`. Struktur template Synthetic Command / Neural Nodes dipertahankan dengan tema **putih–orange** sesuai keputusan terbaru; logo JPEG Albina tetap dipertahankan. Perubahan ini berlaku pada localhost; situs yang sudah dipublikasikan tidak diperbarui. Dokumen membedakan arah desain dan kemampuan aplikasi yang sudah tersedia; tidak menambahkan klaim integrasi atau otomatisasi.

## 1. Arah visual

**Nama desain: Albina Business Console.** Karakter: presisi, modern, fokus, dan tetap mudah dipakai owner, admin, serta host melalui HP.

Gunakan putih sebagai bidang utama dan panel, orange untuk tindakan dan penanda aktif, orange muda untuk permukaan pendukung, serta monospace pada angka dan SKU. Pertahankan nuansa futuristik melalui komposisi, tipografi, dan detail cahaya yang terkontrol.

Prioritas visual: **review performa bisnis → target pertumbuhan → stok dan prioritas tim → aktivitas terbaru → form penjualan offline**. Masalah stok yang mendesak tetap terlihat pada banner. POS menjadi tools tambahan pada bagian paling bawah Ringkasan, tanpa CTA penjualan utama di header.

Identitas yang ditampilkan adalah **Albina Shop**, menggunakan file logo yang sudah disetujui: `albina-local/public/assets/albina-shop-logo-hd.jpg` (1860×845). Pertahankan warna coral, kuning, cokelat, dan bidang krem di dalam gambar logo; tema antarmuka memakai putih/orange. Jangan mengganti logo dengan logo NEXA, monogram, atau logotype teks. Gunakan `object-fit: contain`, rasio asli, tanpa crop, tint, atau filter inversi.

SHA-256 aset logo: `c51e310faaa61be2d042a664275f4c28f5573bc8c5b5fe1c202ef2e96ab33ee0`.

## 2. Pemakaian tiga referensi

Ketiga file DESIGN sumber mempunyai isi identik berdasarkan SHA-256. Dua ZIP mempunyai screenshot dan HTML yang berbeda: template pertama menampilkan Security Protocol, template kedua menampilkan Neural Nodes. Screenshot dan struktur HTML diperiksa sebagai referensi, tanpa menjalankan script template.

| Sumber | Diambil untuk Albina | Adaptasi |
| --- | --- | --- |
| DESIGN (4).md / Synthetic Command | Navy, cyan, panel kaca, Space Grotesk/Geist/JetBrains Mono, grid dan hirarki | Label bahasa Indonesia, teks lebih lega, warna status semantik |
| Template 1: Security Protocol | Status ringkas, panel masalah, tabel event, riwayat, inspector | Peringatan overselling, persetujuan koreksi, mutasi dan masalah stok |
| Template 2: Neural Nodes | Header halaman, empat KPI, komposisi 8:4, panel utama dan konteks | Grafik penjualan, channel, prioritas tim, OKR dan insight |

### Penyelesaian perbedaan sumber

Sumber YAML memakai background `#0c1323`, sedangkan narasi menyebut `#070B19`. **Gunakan `#0c1323` sebagai canvas utama**, mengikuti token dan HTML kedua template. Gunakan `#070e1e` untuk bidang paling dalam.

Radius pada HTML sumber lebih kecil dan istilah `full` tidak konsisten dengan YAML. Gunakan radius eksplisit pada frontmatter dokumen ini. Ukuran sidebar referensi sekitar 280/288 px; Albina memakai 256 px agar label menu cukup dan ruang kerja tidak terlalu sempit.

Tidak mengadopsi radar keamanan, peta jaringan, DEFCON, latency, quantum encryption, identitas operator template, logo NEXA, kill switch, atau terminal perintah. Elemen tersebut tidak mewakili data atau tindakan bisnis Albina. Grafik dan status memakai data aktual atau label demo yang jelas.

## 3. Warna dan makna

Token frontmatter adalah sumber nilai warna untuk implementasi. Jangan mengambil nilai warna baru dari contoh HTML tanpa memetakan ke token.

| Token | Pemakaian |
| --- | --- |
| background / surface-lowest | Canvas dan bidang inset tabel/grafik |
| surface-low / surface | Sidebar, card, konten utama |
| surface-high / surface-highest | Hover, menu terbuka, lapisan aktif |
| on-surface | Judul, angka utama, teks yang perlu dibaca |
| on-surface-variant | Teks penjelas dan label form |
| text-muted | Metadata dan sumber; tetap terbaca |
| primary / on-primary | Tombol utama cyan dengan teks gelap; active nav dan tautan |
| secondary / secondary-strong | Seri data pembanding dan selected state pendukung |
| accent | Highlight AI/campaign terbatas; bukan seluruh peringatan |
| success | Pembayaran tercatat, proses selesai, stok tersedia yang terverifikasi |
| warning | Stok menipis, menunggu persetujuan, data usang |
| danger / danger-container | Kekurangan stok, kegagalan, pembatalan, konflik yang memblok |
| focus | Ring keyboard yang jelas |

Magenta kuat `#ff0080` hanya aksen dekoratif/AI kecil, bukan warna teks kecil atau satu-satunya penanda bahaya. Tindakan pembatalan memakai danger berlabel jelas. Warna cyan tidak berarti otomatis “sinkronisasi sehat”.

Target kontras rancangan: teks normal 4,5:1, teks besar 3:1, batas kontrol/fokus yang penting 3:1 terhadap bidang sekitarnya. Uji kembali pada hasil render, khususnya opacity, gradient, disabled, dan compositing. Border `outline-subtle` hanya pemisah dekoratif; gunakan `outline-control` pada input/control yang batasnya perlu terlihat.

## 4. Tipografi dan angka

- **Space Grotesk:** nama halaman dan heading panel. Maksimal satu h1 per halaman, 32/40 desktop, 26/34 mobile.
- **Geist:** label yang panjang, isi tabel deskriptif, formulir, pesan, nama barang, dan navigasi. Isi utama 14/22, input HP 16/24.
- **JetBrains Mono:** KPI, harga, jumlah stok, SKU, ID order, serta timestamp. Gunakan angka tabular, rata kanan pada kolom uang/jumlah.
- Fallback: Space Grotesk/Geist → system-ui/sans-serif; JetBrains Mono → ui-monospace/monospace. Layout tetap bekerja saat font belum termuat.
- Label kecil minimal 12/18 dalam rancangan ini. Huruf kapital berjarak hanya untuk label singkat, bukan paragraf dan nama produk.
- Nilai rupiah memakai format Indonesia: `Rp285.000`; jumlah `16 pcs`. Gunakan pemformatan konsisten dan jarak nonbreaking pada unit bila perlu.
- Kartu boleh memakai `Rp8,4 jt` hanya jika nilai penuh tersedia sebagai teks detail yang juga dapat diakses dengan keyboard/sentuh. Tabel transaksi dan konfirmasi selalu nilai penuh.
- Angka panjang tidak dipotong dengan ellipsis pada konfirmasi. Turunkan ukuran metrik sampai batas mobile atau perluas card; jangan menyembunyikan digit penting.

48 px dari display-hero sumber tidak digunakan sebagai judul halaman operasional. KPI dapat 28/36; jangan membuat semua teks terasa seperti layar terminal.

## 5. Layout dan responsive

### Desktop lebar — 1440 px ke atas

- Sidebar tetap 256 px, topbar sticky 64 px, main dengan padding 24 px, max-width 1760 px dan rata tengah.
- Grid 12 kolom dengan gap 16 px. Empat KPI masing-masing 3 kolom.
- Area analisis 8 kolom + konteks 4 kolom. Inspector maksimal 320 px; tidak ditambahkan lagi sebagai rail ketiga jika lebar konten tidak cukup.
- Halaman inventory/order yang padat memakai lebar penuh. Inspector dibuka sebagai drawer agar tabel tetap terbaca.

### Desktop — 1200–1439 px

Sidebar 256 px; main dua bagian hanya jika panel utama minimal 560 px dan konteks minimal 280 px. Jika tidak cukup, konteks pindah ke bawah. Hindari menyalin layout tiga rail template pada ukuran ini.

### Tablet — 768–1199 px

Sidebar rail 72 px dengan tombol buka nama menu. Tooltip mendukung hover dan fokus; versi drawer menampilkan label penuh. KPI 2×2. Panel 8:4 menjadi satu kolom bila ruang tidak cukup. Form penjualan memakai konten penuh, ringkasan keranjang di bawah atau sticky yang tidak menutupi input.

### HP — 360–767 px

- Sidebar menjadi drawer. Topbar memuat menu, nama halaman, akun, dan notifikasi ringkas.
- Bottom navigation maksimal empat tujuan: Ringkasan, Jual Offline (owner/admin), Stok, Lainnya. Untuk host: Ringkasan, Live, Stok, Lainnya. Menu Lainnya tetap membuka seluruh tujuan yang diizinkan.
- KPI dua kolom jika muat; turun satu kolom untuk teks/nilai panjang atau pembesaran teks. Main padding 16 px.
- Tabel inventori menjadi card per varian atau tabel scroll terarah dengan label kolom yang tetap jelas. Tabel tidak memaksa seluruh halaman melebar.
- Form transaksi menjadi halaman penuh, bukan modal kecil. Tombol utama di footer sticky dengan safe-area dan ruang bawah konten yang cukup, termasuk saat keyboard terbuka.
- Minimum target sentuh 44×44 px; tidak ada aksi yang bergantung pada hover saja.

Layout harus tetap berguna pada 200% zoom. Panel tidak mempunyai tinggi tetap yang memotong pesan kesalahan atau teks terjemahan.

## 6. Spacing, bentuk, dan kedalaman

Gunakan skala 4, 8, 12, 16, 24, 32, 40, 48 px. Gap field 16 px; jarak kelompok form 24 px; card padding 20 px desktop, 16 px HP. Radius: card 8, input/button 6, overlay 12, badge 4 px. Avatar dan titik status boleh bulat penuh.

Lapisan visual:

1. Canvas navy dengan ambient blue/cyan maksimal opacity 4–6%, jauh dari teks utama.
2. Card solid/translucent 90–96% pada bidang stabil, border halus. Informasi penting tidak bergantung pada kaca transparan.
3. Header/drawer dapat blur 12–16 px; overlay memakai bidang hampir solid agar terbaca. Bila blur tidak didukung, tetap gunakan surface opaque.
4. Focus memakai ring tegas, glow hanya pelengkap. Panel aktif boleh memiliki inner highlight halus.

Hindari blur besar di semua row dan glow pada tiap angka. Grid latar atau corner bracket dipakai sangat ringan, maksimal pada satu panel utama; tidak ditempatkan di form transaksi.

## 7. Navigasi dan shell

Sidebar menampilkan Albina Shop, workspace, kelompok menu, status data ringkas, akun dan peran. Bukan status “NODE SYNCED” dari template.

| Kelompok | Menu |
| --- | --- |
| Operasional | Ringkasan, Penjualan Offline, Order & Channel, Stok & Inventory |
| Tim & Pertumbuhan | Live Selling, Marketing, Tim & Pekerjaan, Target & OKR |
| Analisis & Sistem | Keuangan, AI Assistant, Integrasi & Pengaturan |

Menu mengikuti izin FRD; status P1/P2 yang belum dibangun boleh tampil sebagai rencana pada demo, tetapi tidak sebagai tombol produksi yang seolah sudah berfungsi. Pilihan peran simulasi selalu berlabel “Simulasi peran”; pada produksi tampilkan peran akun aktual tanpa switch bebas.

Item aktif: bidang surface-high, garis kiri cyan 2 px, ikon cyan, teks terang, `aria-current=page`. Hover memakai surface-high ringan. Badge jumlah hanya untuk masalah/tugas yang dapat ditindaklanjuti dan mempunyai sumber.

Topbar: breadcrumb/nama halaman, status sumber ringkas, notifikasi, akun. Filter periode dan channel berada pada header halaman dan terlihat saat memengaruhi angka. Jangan menambah latency, uptime, atau jam terminal dekoratif.

## 8. Ringkasan bisnis — UI-01

Urutan vertikal:

1. Header Ringkasan dan filter periode/channel untuk review bisnis; tanpa CTA kasir utama.
2. Banner masalah mendesak hanya jika ada: kekurangan order, data stok usang, atau sinkronisasi gagal.
3. Empat KPI: Penjualan dibayar, Pesanan dibayar, Stok tersedia, Order kekurangan stok. Jika data belum sebanding, labelkan penjualan offline dan online terpisah.
4. Grafik performa penjualan dan Target pertumbuhan, dengan panel utama lebih lebar.
5. Tabel Stok perlu perhatian dan Prioritas tim.
6. Aktivitas terbaru dan insight stok bersumber.
7. Form **Penjualan offline** pada bagian paling bawah, berlabel **Tools Tambahan**. Hanya owner/admin; host tidak mendapat form kasir.

Setiap KPI memuat nama, nilai, satuan/cakupan, sumber, waktu pembaruan, dan tautan detail. Perubahan persen hanya tampil bila periode pembanding sebanding dan datanya lengkap. Target aktif: bulan pertama 3× dan bulan ketiga 5× baseline yang sama. “Belum tersedia” berbeda dari `Rp0` atau `0 order`.

Contoh wireframe desktop:

```text
┌ Sidebar ─┬ Topbar: halaman · status sumber · akun ─────────────────┐
│          │ Ringkasan · periode · channel                            │
│ Menu     │ [Banner masalah — muncul bila perlu]                     │
│          │ [Penjualan] [Pesanan] [Stok tersedia] [Order kekurangan]  │
│          │ [Grafik penjualan                 ] [Target & OKR      ] │
│          │ [Stok perlu perhatian            ] [Prioritas tim     ] │
│          │ [Aktivitas terbaru               ] [Insight bersumber ] │
│          │ [Tools Tambahan: form penjualan offline, owner/admin ] │
└──────────┴─────────────────────────────────────────────────────────┘
```

Wireframe adalah susunan, bukan permintaan angka contoh dijadikan laporan aktual. Jika seluruh sumber belum terhubung, tampilkan onboarding “Hubungkan sumber / Impor data” dan label demo yang jelas.

## 9. Penjualan offline — UI-02/UI-03

Ini tools tambahan di bawah seluruh panel review dashboard. Menu POS Offline tetap tersedia sebagai akses khusus. Form memakai komponen dan validasi yang sama di kedua lokasi; tidak membuka modal otomatis. Hindari dekorasi yang memperlambat pencarian SKU atau mengaburkan konfirmasi stok.

### Daftar transaksi

Header + CTA, ringkasan penjualan offline dan penerimaan terpisah, cari ID/pembeli, filter channel/status/petugas/periode. Kolom inti: ID/waktu, channel, nilai, pembayaran, penyerahan, petugas. Baris membuka detail; tombol aksi penting tidak muncul hanya pada hover.

### Form transaksi desktop

- Kiri sekitar 7 kolom: cari/pindai SKU, hasil dengan foto/varian/stok, keranjang multi-SKU.
- Kanan sekitar 5 kolom: channel, pembeli opsional, metode pembayaran, uang diterima, total, CTA. Penjualan selalu lunas dan barang langsung diserahkan.
- Isi keranjang: nama, SKU, ukuran/warna, jumlah, harga unit, diskon nominal, subtotal. Harga tidak standar menampilkan alasan dan status persetujuan sesuai FRD.
- Footer ringkasan memuat nilai penuh, jumlah item, status stok, dan efek aksi.

### Alur HP

`Pilih produk → Keranjang → Pembayaran & konfirmasi`. Draft bertahan saat berpindah langkah. Tampilkan jumlah langkah dan tombol kembali tanpa kehilangan isi. Sebelum submit tetap tampilkan ringkasan SKU-varian dan total; jangan menganggap memilih hasil pencarian berarti menjual.

Label CTA menyesuaikan aksi:

- **“Simpan penjualan & kurangi stok”**, dengan penjelasan bahwa pembayaran harus lunas dan barang langsung diserahkan.
- Harga dan diskon mengikuti izin akun; validasi serta pemeriksaan stok tetap dijalankan server.
- Reservasi atau pembayaran belakangan tidak ditawarkan pada POS aktif.

Saat menyimpan: tombol loading, status terbaca, cegah klik berulang di UI. Setelah sukses: ID transaksi, pembayaran, penyerahan, stok terkait, bukti, dan status sinkronisasi eksternal ditampilkan terpisah.

Contoh pesan:

- Stok tidak cukup: **“Stok Kaos Sporty · M tersisa 1 pcs. Jumlah yang diminta 2 pcs. Transaksi belum disimpan.”**
- Hasil belum pasti: **“Hasil penyimpanan belum diketahui. Periksa transaksi sebelum mengulang.”** CTA “Periksa hasil”.
- Lokal sukses, eksternal tertunda: **“Penjualan tersimpan. Pembaruan stok marketplace masih menunggu.”**
- Koneksi putus: **“Draft belum tersimpan di server. Sambungkan internet untuk melanjutkan.”**

Nominal/input yang valid tidak dihapus saat satu field salah. Error berada dekat field dan pada ringkasan form bila perlu; fokus menuju error pertama. Pesan kritis tidak hanya berupa toast yang hilang.

## 10. Inventory, opname, dan masalah stok — UI-04/UI-05/UI-06

Inventory menampilkan pencarian SKU/varian, filter status, sumber/usia data, serta tabel dengan nama, fisik, karantina, terpesan, tersedia, dan status. Nilai uang/HPP hanya tampil bagi pengguna yang berhak.

Panel detail varian: foto produk bila tersedia, atribut, F/K/R/A, riwayat mutasi, reservasi order, dan sumber. Gunakan label sehari-hari sebagai judul; rumus F/K/R ada pada bantuan, bukan jargon utama.

Stok bersama diberi penjelasan **“Satu gudang untuk penjualan online dan offline.”** Jangan menggambar dua gudang atau dua saldo mandiri untuk Shopee dan offline.

| Kondisi | Tampilan |
| --- | --- |
| Tersedia | Label netral/success bila data dapat diverifikasi; angka jelas |
| Menipis | Badge amber + “Stok menipis” + jumlah |
| Habis | Badge danger + “Stok habis”; tidak ada tombol jual aktif |
| Defisit | Angka negatif tetap terlihat + “Kekurangan alokasi”; tautan order terdampak |
| Data usang | Badge amber + waktu data terakhir; tombol verifikasi sesuai izin |
| SKU belum dipetakan | “Perlu pemetaan”; jangan menampilkan angka seolah cocok |

Opname/koreksi: layout membandingkan buku dan hitung fisik, selisih, alasan, pengaju/penyetuju, serta status. CTA berubah dari “Ajukan koreksi” menjadi “Setujui koreksi” sesuai peran. Tidak ada field saldo bebas di halaman produk.

Halaman masalah stok memakai pola incident panel template 1: jenis masalah, SKU/order, kebutuhan/alokasi/kekurangan, PIC, umur, status, dan tindakan sah. Menekan “Tugas selesai” tidak mengubah saldo. Riwayat berupa timeline bisnis tanpa klaim hash blockchain atau verifikasi kriptografi yang belum dibangun.

## 11. Halaman lanjutan

| Halaman | Pola desain dan informasi prioritas |
| --- | --- |
| Sales channel | Tabel/kartu per channel, definisi status, periode dan waktu pembaruan; order unik dapat ditelusuri |
| Live selling | Kalender/jadwal, kartu sesi, daftar produk dan stok, checklist, hasil; view host menonjolkan sesi sendiri |
| Marketing | Kalender konten/campaign, PIC, status review, anggaran dan biaya aktual terpisah, views/klik/ROAS bersumber |
| Keuangan | Penerimaan, HPP, biaya, refund, pencairan terpisah; indikasi biaya belum lengkap; tanpa judul laba bersih palsu |
| Tim & pekerjaan | Daftar tugas dengan PIC, tenggat, hambatan dan objek terkait; board opsional, bukan satu-satunya cara memakai HP |
| Target & OKR | Objective → KR → baseline/target/aktual/periode/PIC → check-in; draft tanpa persentase progres rekaan |
| AI assistant | Briefing dan jawaban dengan sumber/periode/keterbatasan; tindakan menjadi draft yang dapat ditinjau |
| Integrasi | Status setiap sumber, waktu sukses terakhir, kemampuan yang tersedia, antrean gagal, import preview/hasil dan retry sesuai izin |

Peta jaringan template 2 tidak menjadi grafik utama. Bila kelak diperlukan diagram hubungan channel, tampilkan gudang bersama di pusat dan status sumber yang nyata; tidak memakai node global/dekoratif sebagai pengganti analisis penjualan.

## 12. Library komponen

### Tombol

Primary solid cyan + teks gelap, tinggi 44 px, padding horizontal 16 px, radius 6 px. Gradient blue→cyan sumber dipakai sebagai aksen tipis atau visual panel, bukan background default teks tombol yang kontrasnya berubah.

Secondary surface-high + border-control, teks on-surface. Ghost memakai teks primary dengan target sentuh penuh. Destructive memakai danger-container + on-danger-container; label aksi spesifik, misalnya “Ajukan pembatalan”, bukan “Kill” atau ikon tanpa penjelasan.

State wajib: default, hover, pressed, focus-visible, disabled, loading. Tombol disabled mempunyai penjelasan di dekatnya bila pengguna perlu tahu penyebab. Focus ring 2 px dengan offset 2 px; tidak bergantung glow saja.

### Badge dan status

Tinggi minimum visual 24 px, teks 12/18; ikon opsional + label eksplisit. Dot 6 px sebagai pelengkap. Badge tidak menjadi tombol kecuali jelas dapat difokuskan dan mempunyai affordance.

Pisahkan dimensi: **Pembayaran: Lunas**, **Penyerahan: Belum diserahkan**, **Sinkronisasi: Menunggu**. Jangan menyatukannya menjadi satu badge “Sukses” yang membingungkan.

### Input dan pilihan

Surface-lowest, border-control 1 px, tinggi 44 px, label tetap di atas. Placeholder hanya contoh. Wajib/opsional disebutkan konsisten. Angka jumlah dengan stepper mempunyai tombol minus/plus 44 px; tetap bisa diketik. Mata uang mempunyai prefix `Rp` dan angka rata kanan.

Autocomplete menampilkan nama + ukuran/warna + SKU + stok, status loading/empty/error, dan selection keyboard. Scan barcode hanya muncul bila pemetaan tersedia. Nama input atau command prefix template tidak dibawa ke form kasir.

### Card dan KPI

Card = header, isi, footer opsional. Ikon fungsional 18–20 px. Jangan menaruh setiap teks kecil dalam card bertingkat. KPI memiliki source/cakupan, nilai, unit, delta valid, dan detail. Sparkline opsional dan hanya dari data yang benar-benar tersedia.

### Table dan list

Header 12/18, row desktop minimal 48 px, nama produk Geist, jumlah/uang mono rata kanan. Pemisah tipis, hover lembut, zebra sangat ringan bila membantu. Kolom status dan tindakan tetap jelas. Pagination serta jumlah hasil tampil; filter tidak hilang saat membuka detail.

Teks nama boleh wrap dua baris. ID panjang boleh dipotong dengan affordance salin/lihat lengkap yang dapat diakses keyboard, tetapi nilai uang/jumlah tidak boleh dipotong. Row selection tetap memakai label/checkbox, bukan warna saja.

### Drawer, dialog, dan toast

Drawer untuk detail SKU/order; dialog untuk konfirmasi singkat yang menyebut objek dan dampak; halaman penuh untuk transaksi panjang di HP. Modal mempunyai judul, close berlabel, focus trap, kembali ke pemicu, dan penanganan keluar bila draft belum tersimpan.

Toast hanya untuk informasi singkat. Keberhasilan menyimpan dan kegagalan penting juga tersedia di halaman/riwayat. Gunakan pengumuman status yang dapat dibaca teknologi bantu tanpa mengulang seluruh halaman.

## 13. Grafik dan visualisasi

- Line chart untuk tren penjualan; bar chart untuk perbandingan channel/produk; progress bar hanya untuk target yang mempunyai baseline/target valid.
- Seri online cyan, offline periwinkle/blue dengan garis putus-putus atau marker berbeda. Label dan pola tetap membedakan seri tanpa warna.
- Legend dapat diklik dengan state yang jelas; tooltip tersedia lewat fokus/sentuh, menyebut tanggal, nilai, status metrik, dan channel.
- Default tanpa radar, gauge berputar, pie 3D, waveform audio, atau sparkline acak.
- Axis diberi unit; skala tidak menyembunyikan konteks. Bedakan nol dan data hilang; gap data tidak diinterpolasi seolah diketahui.
- Grafik punya ringkasan teks/tabel alternatif; definisi dan periode pembanding terlihat.
- Tidak menampilkan angka tumbuh, views, atau “live” hanya untuk membuat dashboard terlihat aktif.

## 14. Data state dan komunikasi

| State | Perlakuan desain |
| --- | --- |
| Loading | Skeleton setinggi konten agar tidak melompat; status terbaca |
| Kosong yang valid | “Belum ada transaksi pada periode ini” + filter/aksi yang relevan |
| Belum tersedia | “Data biaya iklan belum tersedia”; jangan `Rp0` |
| Belum terhubung | Nama sumber + “Belum terhubung” + langkah yang benar-benar didukung |
| Data lama | Last-known value + waktu update + label usang; CTA aman mengikuti FRD |
| Gagal memuat | Pertahankan filter, pesan singkat, retry; jangan menghapus transaksi yang sudah sukses |
| Konflik stok/versi | Nilai terbaru, objek konflik, dan langkah periksa; tanpa retry buta |
| Simpan berhasil | ID hasil, status bayar/serah, efek lokal, status eksternal terpisah |
| Hasil belum pasti | Peringatan persisten + “Periksa hasil”, bukan ajakan buat transaksi baru |
| Demo | Banner/badge “Data contoh”; jelas di angka, grafik, ekspor dan simulasi peran |
| Akses terbatas | Navigasi sesuai izin; halaman/aksi langsung ditolak server; tanpa field rahasia di respons |

Bahasa UI: Indonesia sederhana. Gunakan “Stok tersedia”, “Barang belum diserahkan”, “Menunggu persetujuan”, “Periksa stok”. Hindari “quantum health”, “node armed”, “AI autonomous rerouting”, atau istilah teknis yang tidak membantu tindakan bisnis.

## 15. Perbedaan pengalaman per peran

| Peran | Landing/prioritas | Tindakan utama |
| --- | --- | --- |
| Owner | Hasil bisnis, masalah stok, persetujuan, target, hambatan tim | Catat penjualan, tinjau masalah, setujui sesuai izin |
| Admin | Transaksi offline, order, pergerakan dan selisih stok, tugas operasional | Catat penjualan, terima barang, hitung opname, ajukan koreksi |
| Host | Sesi live sendiri, produk/varian tersedia, persiapan, hasil sesi | Buka daftar produk dan perbarui tugas sendiri |

Host tidak melihat CTA kasir, HPP, atau margin bisnis. Admin tidak otomatis melihat keuangan gabungan/HPP. Desain halaman kosong menyesuaikan cakupan pengguna; bukan menjanjikan akses lewat tombol yang tidak berhak digunakan.

## 16. Motion, aksesibilitas, dan performa visual

Transisi hover/focus 120–180 ms; drawer 220 ms. Tidak ada animasi radar atau pulse tanpa henti. Titik status statis secara default. Perubahan data boleh highlight singkat tanpa memindahkan fokus atau mengubah urutan row mendadak.

Hormati preferensi reduced motion: hilangkan shimmer, pulsing, dan perpindahan animasi, pertahankan perubahan state instan. Font/icons yang gagal dimuat tidak boleh menghilangkan label tindakan. Gunakan satu keluarga ikon garis, misalnya Material Symbols Outlined sesuai referensi, dengan fallback SVG/text yang terkontrol; hindari campuran emoji untuk fungsi inti.

Checklist aksesibilitas: urutan heading benar, label input terhubung, error terasosiasi, keyboard operabel, fokus terlihat/tidak tertutup header, dialog dapat ditutup dengan aman, warna bukan satu-satunya penanda, chart punya alternatif, dan target sentuh memadai. Pengujian keyboard/screen reader dan kontras dilakukan pada implementasi; dokumen ini belum bukti lulus audit.

Foto produk menggunakan aset Albina yang tersedia, rasio thumbnail 1:1, object-fit contain, permukaan netral. Fallback adalah ikon pakaian dan nama produk, bukan gambar eksternal acak. Jangan membawa avatar dan logo rusak dari screenshot template.

## 17. Token implementasi contoh

CSS berikut memetakan keputusan desain; nilai utama navy/cyan sudah diterapkan pada aplikasi lokal:

```css
:root {
  color-scheme: dark;
  --bg: #0c1323;
  --surface-inset: #070e1e;
  --surface-low: #141b2c;
  --surface: #181f30;
  --surface-high: #232a3b;
  --text: #dce2f9;
  --text-secondary: #b9cacb;
  --text-muted: #9aacc5;
  --border-subtle: #3b494b;
  --border-control: #64748b;
  --primary: #00f0ff;
  --on-primary: #002022;
  --secondary: #aec6ff;
  --success: #78ddb0;
  --warning: #ffcf70;
  --danger: #ffb4ab;
  --danger-bg: #690005;
  --on-danger: #ffdad6;
  --focus: #7df4ff;
  --radius-control: 6px;
  --radius-card: 8px;
  --radius-overlay: 12px;
  --space-unit: 4px;
  --grid-gap: 16px;
  --sidebar-width: 256px;
  --topbar-height: 64px;
  --font-heading: 'Space Grotesk', system-ui, sans-serif;
  --font-body: 'Geist', system-ui, sans-serif;
  --font-number: 'JetBrains Mono', ui-monospace, monospace;
}
.metric, .numeric { font-variant-numeric: tabular-nums; }
.numeric { font-family: var(--font-number); text-align: right; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
```

Skala z-index usulan: base 0, sticky header/nav 20, dropdown 30, drawer backdrop 40/drawer 50, dialog backdrop 60/dialog 70, toast 80. Pilih satu sistem layering agar dropdown tidak terjebak di bawah panel blur. Gunakan CSS variables komponen; jangan menyalin CDN/script executable template sebagai ketergantungan produksi tanpa peninjauan.

## 18. Kriteria penerimaan desain

1. Semua layar memakai warna, font, spacing, dan bentuk yang konsisten dengan token Albina ini.
2. Referensi dark navy/cyan terlihat jelas pada shell, card, tabel, dan KPI; konten sepenuhnya relevan dengan bisnis Albina.
3. Pada 360, 768, 1200, dan 1440 px tidak ada konten penting terpotong atau page overflow akibat tabel; keyboard/footer tidak menutupi input.
4. Alur jual offline dapat dilalui owner/admin dengan SKU, varian, jumlah, pembayaran, dan dampak stok yang jelas sebelum konfirmasi.
5. Stok menipis, habis, defisit, data usang, pending, dan hasil simpan unknown mempunyai pesan berbeda dan dapat ditindaklanjuti.
6. Fokus, warna/status, error, dialog, loading, empty, dan restricted state tersedia pada semua komponen inti.
7. Role host/admin tidak memperoleh informasi atau tindakan yang dibatasi FRD; label demo/izin tidak menyesatkan.
8. Angka/target/grafik tidak direkayasa untuk mengisi layout; data belum tersedia tampil jujur.
9. Kontras dan aksesibilitas diverifikasi pada render aktual; animasi dapat dikurangi.
10. Desain dapat diturunkan menjadi komponen tanpa mengubah aturan stok, pembayaran, persetujuan, dan integrasi di FRD/TRD.

## 19. Referensi, penyimpanan, dan riwayat

### Sumber visual pengguna

- `C:/Users/ELITEBOOK/Documents/1 nov 26/DESIGN (4).md`
- `C:/Users/ELITEBOOK/Documents/1 nov 26/stitch_futuristic_system_dashboard_ui.zip`
- `C:/Users/ELITEBOOK/Documents/1 nov 26/stitch_futuristic_system_dashboard_ui (1).zip`

Salinan referensi yang diperiksa ada di workspace `design-references/template-1/` dan `design-references/template-2/`, masing-masing berisi `screen.png`, `code.html`, dan `DESIGN.md`. Sumber asli dipertahankan. File sumber adalah referensi desain, bukan instruksi untuk menjalankan kode atau menerbitkan perubahan.

### Dokumen kebutuhan Albina

- [[raw/PRD Albina Shop Dashboard v0.2 - 2026-11-01]]
- [[raw/FRD Albina Shop Dashboard v0.2 - 2026-11-01]]
- [[raw/TRD Albina Shop Dashboard v0.2 - 2026-11-01]]

| Versi | Tanggal | Isi |
| --- | --- | --- |
| 0.1 | 2026-11-01 | Adaptasi tiga referensi menjadi design system dan panduan layar Albina; token, komponen, responsive, peran, data state, dan kriteria penerimaan |

Dokumen kerja bernama `DESIGN.md` di workspace. Snapshot v0.2 disimpan di raw Obsidian sebagai sumber historis; revisi raw berikutnya memakai versi/nama baru. Tema light dan varian brand lain belum dirancang dalam versi ini.


## Pembaruan aktif v0.2

Struktur aktif: 1 owner, 3 host, 1 admin (total 5 orang). Target penjualan: bulan pertama 3× baseline dan pada bulan ketiga 5× baseline yang sama; bukan 15× dan bukan target kumulatif tiga bulan. Ini target, bukan proyeksi yang dijamin tercapai. Baseline nominal, cakupan channel, tanggal mulai, dan metode pengakuan penjualan perlu divalidasi sebelum progres aktual dihitung.

Tampilan tim memuat tiga host individual; tidak menciptakan nama, jadwal, atau hasil aktual. Target menampilkan dua horizon dengan baseline sama. Rujukan: [[raw/Keputusan final tim dan target Albina 2026-11-01]].


## Riwayat v0.3 — kembali ke template, logo dipertahankan

- Tema aplikasi dikembalikan dari coral/krem ke navy gelap dan cyan dari referensi pengguna. Warna logo asli tetap utuh di dalam aset JPEG.
- Stylesheet dasar dipulihkan dari arsip versi awal yang masih memakai template gelap. Panel chat yang ditambahkan kemudian memakai palet gelap yang sama.
- Form penjualan offline tetap di bagian paling bawah Ringkasan sebagai Tools Tambahan; fokus dashboard adalah review bisnis.
- Tim tetap Owner, Admin Upi, Host Feby, Host Tantri, Host Bowo. Jumlah host tetap 3. Target tetap 3× pada bulan pertama dan 5× pada bulan ketiga terhadap baseline yang sama.
- BigSeller tetap acuan stok; koneksi otomatis belum terverifikasi. Chat kanan bawah tetap mode aturan lokal, belum AI generatif.
- Dokumen raw Obsidian lama adalah sumber historis dan tidak ditimpa oleh revisi desain lokal ini.


## Pembaruan aktif v0.4 — putih dan orange

Keputusan terbaru mengganti tema navy/cyan menjadi **putih–orange** pada seluruh aplikasi lokal. Ketentuan visual terbaru ini menggantikan instruksi warna gelap dalam uraian adaptasi template sebelumnya. Token frontmatter di atas menjadi acuan aktif.

- Canvas dan card putih; sidebar, form, tabel, dialog dan chat memakai putih/orange muda.
- Aksen orange terang `#F97316`; tombol utama dan tautan memakai orange tua `#C2410C` agar teks kecil terbaca di bidang putih.
- Teks utama abu gelap `#292524`, metadata `#78716C`, border hangat `#EAD7C4`.
- Logo asli tetap utuh. Struktur template, 3 host, target 3×/5×, dan POS di bawah dashboard tetap berlaku.
- Preferensi reduced motion dan reduced transparency tetap dihormati; mode reduced transparency juga memakai putih.


## Pembaruan aktif v0.5 — form penjualan di kanan dan selalu terbuka

- Pada layar minimal 1100 px, review bisnis di kiri dan form penjualan offline di kolom kanan (350–390 px).
- Form langsung tersedia untuk owner/admin, tanpa menu lipat atau modal. Kolom kanan mengikuti scroll; isi form dapat di-scroll pada layar pendek.
- Pada layar lebih sempit, susunan menjadi satu kolom; form tetap terbuka setelah panel review, tanpa tombol untuk memunculkannya.
- Ketentuan ini menggantikan posisi form di bawah pada rancangan desktop sebelumnya. Tema putih/orange dan logo asli tetap dipertahankan.
- Tidak ada perubahan pada validasi, izin, pembayaran lunas, pemeriksaan stok, dan aturan BigSeller.
