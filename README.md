# Albina Local Workspace

Aplikasi lokal dengan Python 3.12+ standard library, SQLite, HTML/CSS/JavaScript. Tidak perlu npm install. Versi ini dijalankan di localhost; belum deployment cloud untuk tim.

## Jalankan

Di PowerShell dari folder ini: `powershell -ExecutionPolicy Bypass -File .\start.ps1`.

Script hanya menjalankan server Python lokal; opsi ExecutionPolicy berlaku untuk proses ini, tidak mengubah kebijakan Windows yang tersimpan. Alternatif: jalankan `python server.py --port 4180` menggunakan Python yang terpasang.

Buka **http://127.0.0.1:4180**. Server terikat pada loopback; ini belum deployment tim di internet/LAN. Tekan Ctrl+C di terminal server untuk menghentikannya. Bila port sudah dipakai server yang sedang berjalan, gunakan URL yang sama; jangan menjalankan dua instance tanpa kebutuhan.

## Mulai dan login

Halaman pertama adalah pratinjau berlabel data contoh. Tekan **Aktifkan workspace**, buat password owner minimal 10 karakter. Tidak ada password default. Pilih katalog contoh hanya untuk dataset percobaan; untuk data operasional mulai dengan katalog kosong dan masukkan SKU/saldo awal yang telah dicocokkan dengan BigSeller dan fisik.

Setelah masuk, buka **Tim & Pekerjaan → Atur akses login** untuk menetapkan password individual. Pilihan akun tetap: Owner; Admin **Upi**; Host **Feby**, **Tantri**, **Bowo**. Total 5 orang, 3 host. Password disimpan sebagai PBKDF2 hash. Host tidak mendapat akses transaksi, pengaturan, HPP atau keuangan. Owner/admin mempunyai izin yang berbeda untuk koreksi dan refund.

## Fitur yang berjalan

- POS offline lunas dan langsung serah, keranjang multi-SKU, metode tunai/transfer/QRIS manual, kembalian dan bukti cetak.
- Validasi jumlah/harga dan total di server, transaksi database atomik, idempotensi operasi dan pencegahan overselling lokal saat transaksi bersamaan.
- Katalog dan saldo, riwayat mutasi, barang masuk, pengajuan koreksi/retur/refund admin dan persetujuan owner. Refund hanya catatan, bukan transfer uang.
- Tim, checklist tugas, jadwal tiga host dan hasil sesi manual, campaign/biaya manual owner, pengeluaran owner, target bulan pertama 3× dan bulan ketiga 5× baseline yang sama.
- Filter periode/channel, ekspor CSV transaksi dan mutasi untuk rekonsiliasi.
- Insight stok berbasis aturan; belum layanan LLM terhubung.
- Tema putih–orange, dengan logo JPEG HD Albina asli di sidebar/login. Form POS selalu terbuka di kanan Ringkasan pada layar minimal 1100 px; pada layar lebih sempit, form tetap terbuka setelah panel review.
- Albina Assistant berbentuk panel chat mengambang di kanan bawah; jawaban memakai aturan dan data lokal sesuai izin akun. Riwayat chat berada di memori halaman dan hilang ketika halaman dimuat ulang.

## BigSeller — sumber stok utama

Status awal **belum terhubung**. Penjualan di aplikasi ini mengurangi **saldo lokal**, tidak otomatis mengurangi stok BigSeller/marketplace. Jangan memakai pencatatan lokal ini sebagai jaminan ketersediaan lintas channel sebelum master/saldo awal dan jalur pembaruan diverifikasi.

Setiap mutasi membuat antrean rekonsiliasi. Owner menandai diverifikasi manual hanya sesudah mutasi yang sama sudah dicatat dan dicocokkan di BigSeller, disertai referensi bukti. CSV yang dihasilkan adalah laporan mutasi untuk rekonsiliasi, bukan klaim format import resmi BigSeller.

Menu **Integrasi & Pengaturan → Hubungkan BigSeller MCP** menerima APP ID/KEY yang diberikan BigSeller. Nilai hanya dikirim ke endpoint resmi `https://mcp.bigseller.pro/mcp`. Program melakukan initialize dan tools/list, bukan pemanggilan tool untuk mengubah stok. Key baru disimpan jika negosiasi berhasil, dienkripsi Windows DPAPI untuk akun OS saat ini. Tidak tersimpan di JavaScript, source, ekspor atau respons state.

Koneksi akun belum diuji tanpa kredensial milik pengguna. Dukungan tulis stok tidak diasumsikan dari kemampuan query MCP; adapter order/stock write membutuhkan dokumentasi privat dan izin yang diberikan pada akun. Tidak ada token login BigSeller yang dicuri/disalin dari browser, tidak ada endpoint write yang direka.

Referensi resmi diperiksa 2026-11-01: [MCP BigSeller](https://help.bigseller.com/in/detailPage/panduan-penggunaan-bigseller-mcp.9417), [Open API BigSeller](https://help.bigseller.com/in/detailPage/panduan-integrasi-api-bigseller.9419).

## Data dan backup

Database: `data/albina.sqlite3`; konfigurasi key: `data/bigseller-key.dpapi` jika pernah berhasil dihubungkan. Folder data diabaikan Git. Sebelum backup, hentikan server dan salin **seluruh folder data** agar file SQLite/WAL ikut terjaga. Key DPAPI terikat akun Windows; koneksi perlu diotorisasi ulang ketika dipindahkan ke akun lain. Jangan menghapus database untuk berpindah dari contoh ke operasional; gunakan database baru melalui argumen `--db` dan simpan arsip dataset sebelumnya.

Belum ada reset-password mandiri; jangan kehilangan password owner. Jangan membuka server HTTP loopback ini ke internet. Multi-perangkat/tim membutuhkan deployment terkontrol dengan HTTPS, backup/restore, kebijakan sesi dan akses jaringan yang ditinjau terpisah.

## Pengujian

`python -m unittest -v`

Pengujian membuat database terisolasi dalam data-tests, bukan data pengguna. Mencakup stok unit terakhir, rollback seluruh keranjang jika satu item kurang, retry, hak akses, persetujuan, pembayaran lunas, retur/refund dan login. Key BigSeller nyata tidak diperlukan dalam unit test; koneksi live belum dinyatakan berhasil.

## Batas versi lokal

Belum semua FRD P0 produksi lengkap: belum impor order/stock otomatis, pembukuan akuntansi/pajak, pemetaan listing platform, expiry/pemesanan offline, penguncian opname lintas marketplace, cash-session closing, atau SLA operasional. Sesuai keputusan terbaru, POS offline **selalu lunas** dan tidak menawarkan reservasi offline. Database bersama di sini berarti satu database pada server lokal; bukan layanan cloud yang sudah bisa diakses perangkat lain.

Logo HD direstorasi dengan built-in ImageGen dari gambar pengguna lalu di-encode JPEG kualitas 95, 1860×845. Detail bisa berbeda tipis karena restorasi AI. Aplikasi menggunakan `public/assets/albina-shop-logo-hd.jpg`. Lihat `DESIGN.md` untuk acuan desain dan riwayat keputusan tampilan.
