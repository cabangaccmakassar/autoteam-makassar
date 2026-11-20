import streamlit as st
import pandas as pd
import io
import html
import urllib.parse

# Konfigurasi Halaman
st.set_page_config(
    page_title="AUTOTEAM - Autodebet Team Achievement & Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat Profesional, Adaptif Light/Dark Mode, Nuansa Biru ACC & Animasi Halus
st.markdown("""
    <style>
    :root {
        color-scheme: light dark;
        --bg-panel: light-dark(rgba(241, 245, 249, 0.92), rgba(15, 23, 42, 0.85));
        --bg-card-soft: light-dark(#f8fafc, #111c33);
        --bg-card-elevated: light-dark(#ffffff, #16233d);
        --border-subtle: light-dark(rgba(30, 64, 175, 0.18), rgba(125, 211, 252, 0.24));
        --border-accent: light-dark(#2563eb, #38bdf8);
        --text-primary: light-dark(#0f172a, #f8fafc);
        --text-secondary: light-dark(#475569, #cbd5e1);
        --text-muted: light-dark(#64748b, #94a3b8);
        --metric-grad: light-dark(
            linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%),
            linear-gradient(145deg, #0b2454 0%, #0f367a 100%)
        );
        --metric-border: light-dark(#93c5fd, #2563eb);
        --metric-label: light-dark(#1e40af, #bfdbfe);
        --metric-value: light-dark(#0f172a, #ffffff);
        --metric-sub: light-dark(#334155, #bae6fd);
        --bank-grad: light-dark(
            linear-gradient(160deg, #f8fafc 0%, #eff6ff 100%),
            linear-gradient(160deg, #0c224d 0%, #113270 100%)
        );
        --bank-title: light-dark(#1d4ed8, #93c5fd);
        --bank-rate: light-dark(#0f172a, #ffffff);
        --bank-sub: light-dark(#334155, #e0f2fe);
        --bank-badge: light-dark(#b45309, #fde047);
        --table-head-grad: light-dark(
            linear-gradient(90deg, #1d4ed8 0%, #0284c7 100%),
            linear-gradient(90deg, #003399 0%, #0369a1 100%)
        );
        --table-row-bg: light-dark(#ffffff, rgba(15, 35, 82, 0.68));
        --table-row-hover: light-dark(#eff6ff, rgba(29, 78, 216, 0.45));
        --solution-bg: light-dark(#ecfdf5, #064e3b);
        --solution-border: light-dark(#059669, #10b981);
        --solution-text: light-dark(#064e3b, #ecfdf5);
        --solution-title: light-dark(#047857, #34d399);
        --reject-reason: light-dark(#dc2626, #f87171);
        --shadow-soft: light-dark(0 4px 14px rgba(15, 23, 42, 0.06), 0 6px 18px rgba(2, 6, 23, 0.38));
    }

    @keyframes floatTrophy {
        0%, 100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 0 5px rgba(234, 179, 8, 0.4)); }
        50% { transform: translateY(-3px) scale(1.06); filter: drop-shadow(0 0 11px rgba(234, 179, 8, 0.75)); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(37, 99, 235, 0.28); }
        50% { box-shadow: 0 0 18px rgba(56, 189, 248, 0.52); }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    footer {display: none !important; visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}

    /* Sidebar Navigasi Korporat Berwarna & Beranimasi */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071330 0%, #0b1f4d 52%, #091738 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.25);
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }
    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(15, 35, 82, 0.72);
        border: 1px solid rgba(96, 165, 250, 0.28);
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        transform: translateX(5px);
        background: linear-gradient(90deg, rgba(0, 85, 204, 0.85), rgba(14, 116, 144, 0.78));
        border-color: #7dd3fc;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.32);
    }
    section[data-testid="stSidebar"] .stRadio label:nth-child(1) { border-left-color: #38bdf8; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(2) { border-left-color: #34d399; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(3) { border-left-color: #fbbf24; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(4) { border-left-color: #f87171; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(5) { border-left-color: #a78bfa; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(6) { border-left-color: #2dd4bf; }

    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: linear-gradient(90deg, #0044b3 0%, #0284c7 100%) !important;
        border: 1px solid #bae6fd !important;
        border-left: 5px solid #facc15 !important;
        transform: translateX(6px);
        animation: pulseGlow 2.8s infinite ease-in-out;
    }
    section[data-testid="stSidebar"] .stRadio label p {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Menu Cepat HP / Tablet: tampil di layar < 992px, tersembunyi di desktop >= 992px */
    @media (min-width: 992px) {
        .st-key-mobile_quick_nav {
            display: none !important;
        }
    }
    @media (max-width: 991.98px) {
        .st-key-mobile_quick_nav {
            background: var(--bg-panel);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 14px;
            box-shadow: var(--shadow-soft);
        }
        .st-key-mobile_quick_nav div[data-testid="stButton"] > button {
            min-height: 46px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 13px;
            padding: 8px 10px;
            margin-bottom: 4px;
        }
    }

    /* Hero Banner Atas Seragam untuk Semua Halaman */
    .hero-banner {
        background: linear-gradient(120deg, #002366, #0044b3, #0369a1, #002b7f);
        background-size: 250% 250%;
        animation: gradientShift 10s ease infinite, fadeSlideUp 0.45s ease-out;
        padding: 20px 24px;
        border-radius: 14px;
        border: 1px solid rgba(125, 211, 252, 0.45);
        box-shadow: 0 8px 24px rgba(0, 35, 102, 0.28);
        margin-bottom: 18px;
    }
    .hero-title {
        color: #ffffff !important;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.3px;
    }
    .hero-sub {
        color: #e0f2fe !important;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .tagline-pill {
        display: inline-block;
        background: linear-gradient(90deg, #003399, #0284c7, #0055cc);
        background-size: 200% 200%;
        animation: gradientShift 7s ease infinite;
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 2px;
        margin-bottom: 4px;
        border: 1px solid rgba(186, 230, 253, 0.7);
    }

    /* Panel Section & Filter Adaptif */
    .section-panel {
        background: var(--bg-panel);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: var(--shadow-soft);
        animation: fadeSlideUp 0.45s ease-out;
    }
    .section-panel-title {
        color: var(--text-primary);
        font-size: 16px;
        font-weight: 700;
        margin: 0 0 6px 0;
    }
    .section-panel-sub {
        color: var(--text-muted);
        font-size: 13px;
        margin: 0 0 12px 0;
    }

    /* Kartu KPI & Metrik Adaptif */
    .metric-card {
        background: var(--metric-grad);
        padding: 18px 16px;
        border-radius: 12px;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--metric-border);
        text-align: center;
        margin-bottom: 10px;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        animation: fadeSlideUp 0.45s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-accent);
    }
    .metric-label {
        color: var(--metric-label);
        font-size: 13.5px;
        font-weight: 700;
    }
    .metric-value {
        color: var(--metric-value);
        margin: 6px 0;
        font-weight: 800;
        font-size: 28px;
        line-height: 1.15;
    }
    .metric-sub {
        color: var(--metric-sub);
        font-size: 12px;
    }

    /* Kartu Per Bank Adaptif */
    .bank-card {
        background: var(--bank-grad);
        padding: 15px;
        border-radius: 12px;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-subtle);
        text-align: center;
        margin-bottom: 8px;
        transition: transform 0.25s ease, border-color 0.25s ease;
        animation: fadeSlideUp 0.45s ease-out;
    }
    .bank-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-accent);
    }
    .bank-title {
        color: var(--bank-title);
        font-size: 15.5px;
        font-weight: 700;
    }
    .bank-rate {
        margin: 6px 0;
        color: var(--bank-rate);
        font-weight: 800;
        font-size: 24px;
    }
    .bank-sub {
        color: var(--bank-sub);
        font-size: 12px;
    }
    .bank-badge {
        color: var(--bank-badge);
        font-weight: 700;
    }

    /* Sales Leaderboard & Tabel Adaptif */
    .lb-panel {
        background: var(--bg-panel);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 16px;
        box-shadow: var(--shadow-soft);
        animation: fadeSlideUp 0.5s ease-out;
    }
    .lb-panel-title {
        color: var(--text-primary);
        font-size: 15.5px;
        font-weight: 700;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .top-rank-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--bg-card-elevated);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }
    .top-rank-card:hover {
        transform: translateX(4px);
        border-color: var(--border-accent);
    }
    .top-rank-1 {
        border-left: 4px solid #eab308;
    }
    .top-rank-2 {
        border-left: 4px solid #94a3b8;
    }
    .top-rank-3 {
        border-left: 4px solid #d97706;
    }
    .trophy-anim {
        display: inline-block;
        font-size: 21px;
        margin-right: 10px;
        animation: floatTrophy 2.6s infinite ease-in-out;
    }
    .rank-name {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 14px;
    }
    .rank-meta {
        color: var(--text-secondary);
        font-size: 12px;
    }
    .rank-score-pill {
        background: linear-gradient(90deg, #003399, #0284c7);
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 12.5px;
        white-space: nowrap;
    }

    .lb-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        color: var(--text-primary);
        border-radius: 10px;
        overflow: hidden;
    }
    .lb-table thead tr {
        background: var(--table-head-grad);
        color: #ffffff;
        text-align: left;
    }
    .lb-table th, .lb-table td {
        padding: 10px 12px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .lb-table tbody tr {
        background-color: var(--table-row-bg);
        transition: background-color 0.2s ease;
    }
    .lb-table tbody tr:hover {
        background-color: var(--table-row-hover);
    }
    .rej-pill {
        background-color: rgba(220, 38, 38, 0.14);
        color: var(--reject-reason);
        border: 1px solid rgba(220, 38, 38, 0.35);
        padding: 2px 9px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
    }

    /* Tabel dataframe Streamlit lebih seragam */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-soft);
        animation: fadeSlideUp 0.5s ease-out;
    }

    /* Kartu Reject & BNI Adaptif */
    .reject-box {
        background: var(--bg-card-elevated);
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        border-left: 5px solid #ef4444;
        margin-bottom: 12px;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
        transition: transform 0.22s ease, border-color 0.22s ease;
        animation: fadeSlideUp 0.45s ease-out;
    }
    .reject-box:hover {
        transform: translateY(-2px);
    }
    .reject-box strong {
        color: var(--text-primary);
        font-size: 17px;
    }
    .reject-box small {
        color: var(--text-secondary);
        font-size: 13px;
    }
    .reject-reason {
        color: var(--reject-reason);
        font-weight: 700;
        font-size: 14.5px;
        margin-top: 8px;
        display: block;
    }
    .solution-box {
        background: var(--solution-bg);
        padding: 13px 15px;
        border-radius: 9px;
        border-left: 4px solid var(--solution-border);
        margin-top: 12px;
        color: var(--solution-text);
        font-size: 13.5px;
    }
    .solution-box span {
        color: var(--solution-title);
        font-weight: 700;
    }

    .bni-box {
        background: var(--bg-card-elevated);
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        border-left: 5px solid #0284c7;
        margin-bottom: 12px;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
        transition: transform 0.22s ease, border-color 0.22s ease;
        animation: fadeSlideUp 0.45s ease-out;
    }
    .bni-box:hover {
        transform: translateY(-2px);
        border-color: var(--border-accent);
    }
    .bni-box strong {
        color: var(--text-primary);
        font-size: 17px;
    }
    .bni-box small {
        color: var(--text-secondary);
        font-size: 13px;
    }

    .ceklis-badge {
        display: inline-block;
        background-color: rgba(16, 185, 129, 0.15);
        color: var(--solution-title);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12.5px;
        margin-top: 6px;
    }
    .belum-ceklis-badge {
        display: inline-block;
        background: var(--bg-card-soft);
        color: var(--bank-title);
        border: 1px solid var(--border-subtle);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 12.5px;
        margin-top: 6px;
    }
    .rekap-box {
        background: var(--bg-panel);
        padding: 16px 18px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        border-left: 5px solid #16a34a;
        margin-bottom: 14px;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
        animation: fadeSlideUp 0.45s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Konfigurasi Google Sheets Utama (Akun Email Baru)
SHEET_ID = "1_WjXj0lShrzkXDDfJQQdwCZ_2yizmigA562GdtFxXEw"
SHEET_EDIT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

# Daftar Resmi Sales ACC Cabang Makassar
DAFTAR_SALES_MAKASSAR = [
    "RESKYANTO PUNDA", "NURUL AZIZAH", "NUR RAHMADANI", "FITRIYANTI MUIS",
    "ANDI ALGAZALI", "MUH RAFLI MUADZ", "M. B. J MUBARAQ MUCHTAR",
    "SEPTIAN MAPPALONGI", "TAHWIL IRZAN", "AMINUDDIN A.", "ANDI IRVAN NATSIR",
    "MUH ASWAR BASRAH", "MUHAMMAD FADHIL RAMADHAN", "DIRGA PRATAMA NUGRAHA",
    "WILANNY NATAL B", "MUH FADLY YUSRI MS", "NAJAMUDDIN",
    "ST. AISYAH NUR HASANAH", "SYAHRIR NUR", "IRAWATI", "TRY YUDHIANTO HAKIM",
    "NASRUL", "HERLIN TANJUNG", "MUKRAWATI", "ZUBAIR M", "NADIA SABIR",
    "KARMILA", "KHUSNUL KHATIMA ASRI", "GOPUR MAULAN", "ENRICKO GUEVARA KARAMOY",
    "GABRIEL", "MIRNA ARSYITA", "ANDI MUHAMMAD WIRYAWAN", "ROHADI MAKMUR",
    "ANDI AYYUB ARHAM", "RIZAL RIZKY RIDWAN", "MUH. ARYA ALIAS", "RANI",
    "MUH ALFIAN TARUNA", "SITI NADIRAH", "PUTRI", "ALFI SAHAR", "NURHIDAYAH", "ASRUL AMRI"
]

# Kamus Arti Status Resmi
KAMUS_STATUS = {
    "O": "Open",
    "F": "Bukcet Finance",
    "D": "Pengajuan ke Bank",
    "A": "Approved",
    "R": "Rejected",
    "C": "Cancelled",
    "B": "Batal",
    "E": "Edit",
    "P": "Pending",
}

STATUS_TIDAK_AKTIF = {"C", "B"}
STATUS_AKTIF = {"O", "F", "D", "A", "R", "E", "P"}

def map_status_label(code):
    c = str(code).upper().strip()
    if c in KAMUS_STATUS:
        return KAMUS_STATUS[c]
    return "Belum Diproses" if c in ["", "NAN", "NONE"] else c

def map_keaktifan_label(code):
    c = str(code).upper().strip()
    if c in STATUS_TIDAK_AKTIF:
        return "Tidak Aktif"
    if c in STATUS_AKTIF:
        return "Aktif"
    return "Aktif" if c not in ["", "NAN", "NONE"] else "Tidak Aktif"

# Katalog Lengkap Panduan & Solusi Reject
REJECT_GUIDE_ITEMS = [
    {
        "No": 1,
        "Alasan Reject": "Phone number is not correct",
        "Keterangan": "Nomor telepon nasabah tidak sesuai atau berbeda antara data pengajuan/AOL dengan data yang terdaftar di bank / mobile banking (misalnya BRIMO).",
        "Tindakan Korektif / Solusi Sales": "Input ulang melalui menu AOL Autodebet CSO dan pastikan nomor HP sesuai dengan yang terdaftar di Bank/BRIMO. Jika belum sinkron, arahkan nasabah walk-in ke bank untuk pembaruan nomor HP."
    },
    {
        "No": 2,
        "Alasan Reject": "Phone number not found",
        "Keterangan": "Nomor telepon nasabah belum terdaftar atau tidak ditemukan pada sistem bank terkait saat proses pendaftaran autodebet.",
        "Tindakan Korektif / Solusi Sales": "Arahkan nasabah melakukan registrasi atau pembaruan data nomor HP aktif di bank terkait terlebih dahulu, lalu ajukan ulang."
    },
    {
        "No": 3,
        "Alasan Reject": "Scan Kartu ATM Meragukan / No. Kartu ATM Invalid",
        "Keterangan": "Foto atau scan kartu ATM kurang jelas/buram, atau nasabah sudah melakukan penggantian kartu ATM sehingga nomor kartu lama sudah tidak berlaku.",
        "Tindakan Korektif / Solusi Sales": "Minta foto/scan kartu ATM terbaru yang jelas dan valid (pastikan tidak terpotong/buram), lalu lakukan pengajuan ulang."
    },
    {
        "No": 4,
        "Alasan Reject": "Tanda Tangan Tidak Menyentuh Materai / Tidak Sesuai",
        "Keterangan": "Tanda tangan pada form kuasa/SKPR tidak menyentuh materai atau tidak cocok dengan spesimen tanda tangan pada KTP/buku tabungan.",
        "Tindakan Korektif / Solusi Sales": "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank nasabah dan pastikan tidak menyimpang dari batas ketentuan."
    },
    {
        "No": 5,
        "Alasan Reject": "Invalid format account number",
        "Keterangan": "Format nomor rekening tidak sesuai ketentuan bank, salah digit, atau terdapat spasi/karakter yang tidak valid.",
        "Tindakan Korektif / Solusi Sales": "Periksa kembali nomor rekening nasabah sesuai buku tabungan/rekening asli tanpa spasi atau karakter tambahan, lalu input ulang."
    },
    {
        "No": 6,
        "Alasan Reject": "Saldo tidak mencukupi",
        "Keterangan": "Saldo rekening nasabah tidak mencukupi untuk memenuhi syarat minimum atau proses pendebetan/validasi.",
        "Tindakan Korektif / Solusi Sales": "Informasikan nasabah untuk memastikan saldo rekening mencukupi dan aktif sebelum proses penagihan/aktivasi berikutnya."
    },
    {
        "No": 7,
        "Alasan Reject": "Rekening tidak aktif / dormant",
        "Keterangan": "Rekening sumber autodebet dalam status dormant (tidak aktif) atau diblokir/terbatas transaksinya.",
        "Tindakan Korektif / Solusi Sales": "Arahkan nasabah untuk mengaktifkan kembali rekening (reaktivasi dormant) di cabang bank terkait."
    },
    {
        "No": 8,
        "Alasan Reject": "Data customer tidak sesuai",
        "Keterangan": "Terdapat ketidaksesuaian identitas nasabah (nama, NIK/KTP, atau data pendukung) antara kontrak/pengajuan dan data rekening bank.",
        "Tindakan Korektif / Solusi Sales": "Cocokkan kembali identitas nasabah di KTP, kontrak, dan rekening bank, lalu koordinasikan perbaikan data/dokumen pendukung."
    }
]

def get_solusi_reject(reason):
    r = str(reason).lower().strip()
    if "not correct" in r:
        return "Input ulang melalui menu AOL Autodebet CSO, pastikan nomor telepon yang diinput sesuai dengan nomor telepon yang terdaftar di Bank / BRIMO. Arahkan customer walk-in ke Bank untuk updation no Telp."
    elif "not found" in r:
        return "Arahkan Customer untuk melakukan registrasi / pembaruan data nomor HP di bank terkait."
    elif "tanda tangan" in r or "skpr" in r or "materai" in r:
        return "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank, lalu lakukan pengajuan ulang."
    elif "kartu atm" in r or "3.1.3" in r or "7. " in r:
        return "Verifikasi ulang nomor kartu ATM aktif & kirim foto/scan kartu ATM yang jelas serta form SKPR sesuai ketentuan."
    elif "account number" in r or "rekening" in r:
        return "Cek dan input ulang nomor rekening sesuai buku tabungan asli tanpa spasi atau karakter tambahan."
    elif "saldo" in r:
        return "Informasikan customer untuk memastikan saldo rekening mencukupi sesuai ketentuan."
    elif "dormant" in r or "tidak aktif" in r:
        return "Arahkan customer untuk mengaktifkan kembali rekening dormant di bank terkait."
    elif "tidak sesuai" in r or "data customer" in r:
        return "Cocokkan kembali data identitas customer antara KTP, kontrak, dan data bank, lalu perbaiki sesuai dokumen sah."
    elif r in ["", "-", "nan", "none"]:
        return "Lakukan pengecekan detail kendala aktivasi autodebet bersama tim Admin / CSO."
    else:
        return "Koordinasikan perbaikan dokumen/data rekening nasabah sesuai catatan reject di AOL."

# Normalisasi Nama Bank
def normalize_bank(val):
    b = str(val).upper().strip()
    if "RAKYAT INDONESIA" in b or b == "BRI":
        return "BRI"
    elif "MANDIRI" in b:
        return "MANDIRI"
    elif "BCA" in b:
        return "BCA"
    elif "BNI" in b:
        return "BNI"
    elif "PERMATA" in b:
        return "PERMATA"
    elif b in ["", "NAN", "NONE"]:
        return "LAINNYA"
    return b

def clean_text(val, default="-"):
    s = str(val).strip()
    if s == "" or s.lower() in ["nan", "none", "nat", "-"]:
        return default
    return s

def extract_cabang_area(row):
    cabang = clean_text(row.get("CABANG", ""), "")
    area_new = clean_text(row.get("AREA NEW", ""), "")
    area = clean_text(row.get("AREA", ""), "")
    area_gabung = area_new if area_new else area
    if cabang and area_gabung and cabang.lower() != area_gabung.lower():
        return f"{cabang} / {area_gabung}"
    return cabang or area_gabung or "-"

def extract_aging_tanggal(row):
    aging = clean_text(row.get("Aging", ""), "")
    aging_raw = clean_text(row.get("AGING_", ""), "")
    tgl_ref = clean_text(row.get("2026-04-11", ""), "")
    dt_golive = clean_text(row.get("DT_GOLIVE", ""), "")

    bagian = []
    if aging:
        bagian.append(f"Aging {aging} hr")
    elif aging_raw:
        bagian.append(f"Aging {aging_raw}")

    if tgl_ref:
        bagian.append(f"Tgl {tgl_ref}")
    elif dt_golive:
        bagian.append(f"Golive {dt_golive}")

    return " | ".join(bagian) if bagian else "-"

# Pesan WA Polos (Tanpa Emotikon) - Reject Satuan
def build_wa_item_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    bank = clean_text(row.get("Bank", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)
    alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum")
    solusi = clean_text(row.get("Solusi", ""), "-")

    lines = [
        f"Halo Kak {sales}, mohon bantuannya follow up reject autodebet customer berikut:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        f"- Bank: {bank}",
        f"- Aging/Tanggal: {aging_tgl}",
        f"- Alasan Reject: {alasan}",
        f"- Solusi: {solusi}",
    ]
    return "\n".join(lines)

# Pesan WA Polos (Tanpa Emotikon) - Reject Rekap per Sales
def build_wa_rekap_message(df_rekap, nama_sales="Sales"):
    if df_rekap.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
    lines = [
        sapaan,
        "Berikut daftar customer reject yang perlu segera di follow up:",
        ""
    ]
    for idx, (_, row) in enumerate(df_rekap.iterrows(), start=1):
        cust = clean_text(row.get("Customer", ""), "-")
        nokon = clean_text(row.get("ID", ""), "-")
        bank = clean_text(row.get("Bank", ""), "-")
        cabang_area = extract_cabang_area(row)
        aging_tgl = extract_aging_tanggal(row)
        alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum")
        solusi = clean_text(row.get("Solusi", ""), "-")
        sales_item = clean_text(row.get("Sales", ""), "-")

        baris_sales = f"\n   Sales: {sales_item}" if nama_sales == "SEMUA SALES" else ""
        lines.append(
            f"{idx}. *{cust}* ({nokon}){baris_sales}\n"
            f"   Cabang/Area: {cabang_area}\n"
            f"   Bank: {bank}\n"
            f"   Aging/Tanggal: {aging_tgl}\n"
            f"   Alasan: {alasan}\n"
            f"   Solusi: {solusi}"
        )
        lines.append("")
    return "\n".join(lines).strip()

# Pesan WA Polos (Tanpa Emotikon) - BNI Status D (Pengajuan ke Bank -> Arahan ACC ONE)
def build_wa_bni_item_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)

    lines = [
        f"Halo Kak {sales}, mohon arahkan nasabah BNI berikut untuk pengaktifan ACC ONE:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        "- Bank: BNI",
        "- Status: D (Pengajuan ke Bank)",
        f"- Aging/Tanggal: {aging_tgl}",
        "- Arahan: Wajib mengajukan dan mengaktifkan ACC ONE sesuai arahan Sales.",
    ]
    return "\n".join(lines)

def build_wa_bni_rekap_message(df_bni, nama_sales="Sales"):
    if df_bni.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
    lines = [
        sapaan,
        "Berikut daftar nasabah BNI status D (Pengajuan ke Bank) yang wajib diarahkan untuk pengaktifan ACC ONE:",
        ""
    ]
    for idx, (_, row) in enumerate(df_bni.iterrows(), start=1):
        cust = clean_text(row.get("Customer", ""), "-")
        nokon = clean_text(row.get("ID", ""), "-")
        cabang_area = extract_cabang_area(row)
        aging_tgl = extract_aging_tanggal(row)
        sales_item = clean_text(row.get("Sales", ""), "-")

        baris_sales = f"\n   Sales: {sales_item}" if nama_sales == "SEMUA SALES" else ""
        lines.append(
            f"{idx}. *{cust}* ({nokon}){baris_sales}\n"
            f"   Cabang/Area: {cabang_area}\n"
            f"   Bank: BNI | Status: D (Pengajuan ke Bank)\n"
            f"   Aging/Tanggal: {aging_tgl}\n"
            f"   Arahan: Pengaktifan ACC ONE oleh nasabah dengan arahan Sales."
        )
        lines.append("")
    return "\n".join(lines).strip()

# Fungsi Memuat Data dari Google Sheets Publik via CSV
@st.cache_data(ttl=10)
def load_data_sheets():
    urls = [
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Tracking",
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0",
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0",
    ]
    for url in urls:
        try:
            df = pd.read_csv(url, dtype=str).fillna("")
            df.columns = [c.strip() for c in df.columns]
            if df.empty or len(df.columns) <= 1:
                continue

            if "NAMA_CUST" in df.columns:
                df = df[df["NAMA_CUST"].str.strip() != ""].copy()
            elif "Customer" in df.columns:
                df = df[df["Customer"].str.strip() != ""].copy()

            df["ID"] = df["NOKON"] if "NOKON" in df.columns else df.get("ID", "-")
            df["Customer"] = df["NAMA_CUST"] if "NAMA_CUST" in df.columns else df.get("Customer", "-")
            df["Bank_Raw"] = df["BANK_AUTODEBET"] if "BANK_AUTODEBET" in df.columns else df.get("Bank", "")
            df["Bank"] = df["Bank_Raw"].apply(normalize_bank)
            df["Sales"] = df["NAME_SO"].str.strip() if "NAME_SO" in df.columns else df.get("Sales", "-")
            df["Status_Code"] = df["STATUS PENDAFTARAN"].str.upper().str.strip() if "STATUS PENDAFTARAN" in df.columns else ""
            df["Status"] = df["Status_Code"].apply(map_status_label)
            df["Keaktifan"] = df["Status_Code"].apply(map_keaktifan_label)
            df["Alasan Reject"] = df["REASON REJECT"].str.strip() if "REASON REJECT" in df.columns else df.get("Alasan Reject", "")
            df["Solusi"] = df["Alasan Reject"].apply(get_solusi_reject)
            return df, True
        except Exception:
            continue

    fallback = pd.DataFrame([
        {"ID": "REG-001", "Customer": "HENRI", "Bank": "BRI", "Sales": "RESKYANTO PUNDA", "Status_Code": "R", "Status": "Rejected", "Keaktifan": "Aktif", "Alasan Reject": "Phone number is not correct", "Solusi": get_solusi_reject("Phone number is not correct"), "CABANG": "MAKASSAR", "AREA NEW": "Area 5", "Aging": "7"}
    ])
    return fallback, False

df_tracking, is_live = load_data_sheets()

if "bni_contacted_keys" not in st.session_state:
    st.session_state.bni_contacted_keys = set()

DAFTAR_MENU = [
    "🎯 Home Dashboard",
    "📊 Status Customer",
    "🏛️ BNI Autodebet Tracking",
    "⚠️ Reject Tracking",
    "📘 Reject Guide",
    "🔧 Settings",
]

if "sidebar_nav" not in st.session_state:
    st.session_state["sidebar_nav"] = DAFTAR_MENU[0]

# Sidebar Navigasi Korporat Berwarna & Beranimasi
st.sidebar.markdown("""
    <div style="padding: 6px 2px 2px 2px;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 800; letter-spacing: 0.5px;">⚡ AUTOTEAM</h2>
        <p style="color: #93c5fd; font-size: 12.5px; margin: 2px 0 8px 0;">Autodebet Team Achievement & Monitoring</p>
        <div class="tagline-pill">Monitor. Improve. Activate.</div>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='color:#bae6fd; font-weight:700; font-size:13px;'>MENU UTAMA</span>", unsafe_allow_html=True)

menu_pilihan = st.sidebar.radio(
    "Navigasi",
    DAFTAR_MENU,
    key="sidebar_nav",
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("ACC Cabang Makassar — Kolaborasi & monitoring performa autodebet tim lapangan.")

def render_page_banner(title, subtitle):
    st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">{html.escape(title)}</div>
            <div class="hero-sub">{html.escape(subtitle)}</div>
            <div class="tagline-pill">Monitor. Improve. Activate.</div>
        </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, subtext):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-sub">{html.escape(str(subtext))}</div>
        </div>
    """, unsafe_allow_html=True)

def build_sales_leaderboard(df):
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    rows = []
    for sales_name, grp in df.groupby("Sales"):
        s_label = sales_name.strip() if str(sales_name).strip() != "" else "(Tanpa Nama Sales)"
        tot = len(grp)
        app = len(grp[grp["Status_Code"] == "A"])
        rej = len(grp[grp["Status_Code"] == "R"])
        pct = (app / tot * 100.0) if tot > 0 else 0.0
        rows.append({
            "Sales": s_label,
            "Total Data": tot,
            "Approved (A)": app,
            "Rejected (R)": rej,
            "% Autodebet": round(pct, 1),
        })

    lb_df = pd.DataFrame(rows)
    if lb_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    top5 = lb_df.sort_values(
        by=["% Autodebet", "Rejected (R)", "Approved (A)", "Total Data"],
        ascending=[False, True, False, False]
    ).head(5).copy()
    top5.insert(0, "Rank", range(1, len(top5) + 1))

    bottom5 = lb_df.sort_values(
        by=["Rejected (R)", "% Autodebet", "Total Data"],
        ascending=[False, True, False]
    ).head(5).copy()
    bottom5.insert(0, "Rank", range(1, len(bottom5) + 1))

    return top5, bottom5

def render_top5_trophy_cards(top5_df):
    trophy_icons = {1: "🏆", 2: "🥈", 3: "🥉", 4: "🏅", 5: "🎖️"}
    rank_classes = {1: "top-rank-1", 2: "top-rank-2", 3: "top-rank-3"}
    html_parts = [
        '<div class="lb-panel">',
        '<div class="lb-panel-title">🏆 Top 5 Sales — Persentase Autodebet Tertinggi & Reject Paling Sedikit</div>'
    ]
    for _, r in top5_df.iterrows():
        rk = int(r["Rank"])
        t_icon = trophy_icons.get(rk, "🏆")
        extra_cls = rank_classes.get(rk, "")
        s_name = html.escape(str(r["Sales"]))
        tot_d = int(r["Total Data"])
        app_d = int(r["Approved (A)"])
        rej_d = int(r["Rejected (R)"])
        pct_v = float(r["% Autodebet"])
        html_parts.append(
            f'<div class="top-rank-card {extra_cls}">'
            f'  <div style="display:flex; align-items:center;">'
            f'    <span class="trophy-anim">{t_icon}</span>'
            f'    <div>'
            f'      <div class="rank-name">#{rk} &nbsp;{s_name}</div>'
            f'      <div class="rank-meta">Approved: <b>{app_d}</b> / {tot_d} Data &nbsp;|&nbsp; Rejected: <b>{rej_d}</b></div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="rank-score-pill">{pct_v:.1f}%</div>'
            f'</div>'
        )
    html_parts.append('</div>')
    return "".join(html_parts)

def render_bottom5_styled_table(bottom5_df):
    html_parts = [
        '<div class="lb-panel">',
        '<div class="lb-panel-title">⚠️ Bottom 5 Sales — Rejected (R) Terbanyak</div>',
        '<table class="lb-table">',
        '<thead><tr><th>Rank</th><th>Nama Sales</th><th>Total</th><th>Approved</th><th>Rejected (R)</th><th>% Autodebet</th></tr></thead>',
        '<tbody>'
    ]
    for _, r in bottom5_df.iterrows():
        rk = int(r["Rank"])
        s_name = html.escape(str(r["Sales"]))
        tot_d = int(r["Total Data"])
        app_d = int(r["Approved (A)"])
        rej_d = int(r["Rejected (R)"])
        pct_v = float(r["% Autodebet"])
        html_parts.append(
            f'<tr>'
            f'  <td><b>#{rk}</b></td>'
            f'  <td><b>{s_name}</b></td>'
            f'  <td>{tot_d}</td>'
            f'  <td>{app_d}</td>'
            f'  <td><span class="rej-pill">{rej_d} Reject</span></td>'
            f'  <td><b>{pct_v:.1f}%</b></td>'
            f'</tr>'
        )
    html_parts.append('</tbody></table></div>')
    return "".join(html_parts)

def main():
    # Menu Cepat khusus HP / Tablet (otomatis tersembunyi di desktop >= 992px & sinkron dua arah dengan sidebar)
    with st.container(key="mobile_quick_nav"):
        st.markdown("<span class='section-panel-label' style='font-weight:700; font-size:12.5px; color:var(--bank-title);'>AKSES CEPAT MENU (HP / TABLET)</span>", unsafe_allow_html=True)
        for row_start in range(0, len(DAFTAR_MENU), 3):
            cols = st.columns(3)
            for idx_col, nama_menu in enumerate(DAFTAR_MENU[row_start:row_start + 3]):
                with cols[idx_col]:
                    is_active = (st.session_state["sidebar_nav"] == nama_menu)
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(nama_menu, key=f"btn_nav_{row_start}_{idx_col}", type=btn_type, use_container_width=True):
                        st.session_state["sidebar_nav"] = nama_menu
                        st.rerun()

    halaman_aktif = st.session_state["sidebar_nav"]

    total_data = len(df_tracking)
    df_aktif = df_tracking[df_tracking["Keaktifan"] == "Aktif"] if not df_tracking.empty else pd.DataFrame()
    total_aktif = len(df_aktif)
    total_approved = len(df_tracking[df_tracking["Status_Code"] == "A"]) if not df_tracking.empty else 0
    total_rejected = len(df_tracking[df_tracking["Status_Code"] == "R"]) if not df_tracking.empty else 0
    success_rate_cabang = (total_approved / total_data * 100) if total_data > 0 else 0.0

    if halaman_aktif == "🎯 Home Dashboard":
        render_page_banner(
            "⚡ AUTOTEAM — Home Dashboard",
            "Autodebet Team Achievement & Monitoring — ACC Cabang Makassar"
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Total Data Tracking", total_data, f"Aktif: {total_aktif} | Non-Aktif (C/B): {total_data - total_aktif}")
        with col2:
            render_metric_card("Total Rejected (R)", total_rejected, "Status Aktif Perlu Tindak Lanjut")
        with col3:
            render_metric_card("Success Rate (Approved / A)", f"{success_rate_cabang:.1f}%", f"{total_approved} Approved dari {total_data} Data")
        with col4:
            render_metric_card("Server Status", "Online", "AUTOTEAM Active")

        st.markdown("---")
        st.subheader("Statistik Volume & Performa per Bank (Data Cabang Makassar)")

        bank_configs = ["BRI", "MANDIRI", "BCA", "BNI", "PERMATA"]
        bank_cols = st.columns(5)
        for idx, bank_name in enumerate(bank_configs):
            sub_b = df_tracking[df_tracking["Bank"] == bank_name]
            vol_b = len(sub_b)
            app_b = len(sub_b[sub_b["Status_Code"] == "A"])
            rate_b = (app_b / vol_b * 100) if vol_b > 0 else 0.0
            badge_label = "Top Rate" if rate_b >= 70 else ("Dominan" if vol_b >= 100 else ("Proses" if vol_b > 0 else "N/A"))
            with bank_cols[idx]:
                st.markdown(
                    f'<div class="bank-card">'
                    f'<div class="bank-title">{html.escape(bank_name)}</div>'
                    f'<div class="bank-rate">{rate_b:.1f}%</div>'
                    f'<div class="bank-sub">Total: <b>{vol_b}</b> Nasabah ({app_b} Approved)</div>'
                    f'<small class="bank-badge">{html.escape(badge_label)}</small>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.subheader("Sales Leaderboard")
        top5_df, bottom5_df = build_sales_leaderboard(df_tracking)
        lb_col1, lb_col2 = st.columns(2)
        with lb_col1:
            if not top5_df.empty:
                st.markdown(render_top5_trophy_cards(top5_df), unsafe_allow_html=True)
            else:
                st.info("Belum ada data Sales.")
        with lb_col2:
            if not bottom5_df.empty:
                st.markdown(render_bottom5_styled_table(bottom5_df), unsafe_allow_html=True)
            else:
                st.info("Belum ada data Sales.")

        st.markdown("---")
        st.subheader("Master Data Nasabah & Status Tracking (Live from Google Sheets)")
        kolom_tampil = [c for c in ["NOKON", "NAMA_CUST", "CABANG", "NAME_SO", "BANK_AUTODEBET", "STATUS PENDAFTARAN", "Status", "Keaktifan", "REASON REJECT"] if c in df_tracking.columns]
        st.dataframe(df_tracking[kolom_tampil] if kolom_tampil else df_tracking, use_container_width=True, hide_index=True)

    elif halaman_aktif == "📊 Status Customer":
        render_page_banner(
            "⚡ AUTOTEAM — Status Customer",
            "Pemantauan menyeluruh progress pengajuan seluruh nasabah dan kontribusi performa setiap Sales."
        )

        with st.container(key="panel_filter_status"):
            st.markdown("<div class='section-panel-title'>Filter & Pencarian Data Nasabah</div><div class='section-panel-sub'>Saring data berdasarkan Sales, status pendaftaran, keaktifan, bank, atau nama/NOKON.</div>", unsafe_allow_html=True)
            c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns([1.8, 1.3, 1.1, 1.1, 1.5])
            with c_f1:
                sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
                opsi_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
                pilih_sales_all = st.selectbox("Filter Sales:", opsi_sales, key="sales_all_select")
            with c_f2:
                opsi_status = [
                    "SEMUA STATUS",
                    "Open (O)",
                    "Bukcet Finance (F)",
                    "Pengajuan ke Bank (D)",
                    "Approved (A)",
                    "Rejected (R)",
                    "Cancelled (C)",
                    "Batal (B)",
                    "Edit (E)",
                    "Pending (P)",
                ]
                pilih_status = st.selectbox("Filter Status:", opsi_status, key="status_all_select")
            with c_f3:
                pilih_keaktifan = st.selectbox("Keaktifan:", ["SEMUA", "Aktif", "Tidak Aktif"], key="aktif_all_select")
            with c_f4:
                opsi_bank = ["SEMUA BANK", "BRI", "MANDIRI", "BCA", "BNI", "PERMATA", "LAINNYA"]
                pilih_bank = st.selectbox("Filter Bank:", opsi_bank, key="bank_all_select")
            with c_f5:
                cari_cust_all = st.text_input("Cari Customer / NOKON:", placeholder="Ketik nama atau no. kontrak...", key="search_all_input")

        df_all_view = df_tracking.copy()
        if pilih_sales_all != "SEMUA SALES":
            df_all_view = df_all_view[df_all_view["Sales"].str.upper() == pilih_sales_all.upper()]
        if pilih_keaktifan != "SEMUA":
            df_all_view = df_all_view[df_all_view["Keaktifan"] == pilih_keaktifan]
        if pilih_bank != "SEMUA BANK":
            df_all_view = df_all_view[df_all_view["Bank"].str.upper() == pilih_bank.upper()]

        status_code_map = {
            "Open (O)": "O",
            "Bukcet Finance (F)": "F",
            "Pengajuan ke Bank (D)": "D",
            "Approved (A)": "A",
            "Rejected (R)": "R",
            "Cancelled (C)": "C",
            "Batal (B)": "B",
            "Edit (E)": "E",
            "Pending (P)": "P",
        }
        if pilih_status in status_code_map:
            df_all_view = df_all_view[df_all_view["Status_Code"] == status_code_map[pilih_status]]

        if cari_cust_all:
            m_n = df_all_view["Customer"].astype(str).str.contains(cari_cust_all, case=False, na=False)
            m_i = df_all_view["ID"].astype(str).str.contains(cari_cust_all, case=False, na=False)
            df_all_view = df_all_view[m_n | m_i]

        cnt_app = len(df_all_view[df_all_view["Status_Code"] == "A"])
        cnt_aktif = len(df_all_view[df_all_view["Keaktifan"] == "Aktif"])
        cnt_nonaktif = len(df_all_view[df_all_view["Keaktifan"] == "Tidak Aktif"])
        cnt_rej = len(df_all_view[df_all_view["Status_Code"] == "R"])

        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            render_metric_card("Total Data", len(df_all_view), "Hasil filter aktif")
        with k2:
            render_metric_card("Approved (A)", cnt_app, "Autodebet disetujui")
        with k3:
            render_metric_card("Status Aktif", cnt_aktif, "Dalam proses / aktif")
        with k4:
            render_metric_card("Tidak Aktif (C/B)", cnt_nonaktif, "Cancelled / Batal")
        with k5:
            render_metric_card("Rejected (R)", cnt_rej, "Perlu follow up")

        st.markdown("---")
        st.subheader("Rekap Progress per Sales")
        if not df_all_view.empty:
            rekap_rows = []
            for sales_name, grp in df_all_view.groupby("Sales"):
                s_label = sales_name if sales_name.strip() != "" else "(Tanpa Nama Sales)"
                tot_s = len(grp)
                app_s = len(grp[grp["Status_Code"] == "A"])
                akt_s = len(grp[grp["Keaktifan"] == "Aktif"])
                nonakt_s = len(grp[grp["Keaktifan"] == "Tidak Aktif"])
                rej_s = len(grp[grp["Status_Code"] == "R"])
                pct_app = (app_s / tot_s * 100) if tot_s > 0 else 0.0
                rekap_rows.append({
                    "Sales": s_label,
                    "Total Data": tot_s,
                    "Approved (A)": app_s,
                    "Aktif": akt_s,
                    "Tidak Aktif (C/B)": nonakt_s,
                    "Rejected (R)": rej_s,
                    "% Approved": f"{pct_app:.1f}%"
                })
            df_rekap_sales = pd.DataFrame(rekap_rows).sort_values(by=["Total Data", "Approved (A)"], ascending=False)
            st.dataframe(df_rekap_sales, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data rekap Sales untuk filter saat ini.")

        st.markdown("---")
        st.subheader(f"Detail Progress Seluruh Nasabah ({len(df_all_view)} Data)")
        if not df_all_view.empty:
            df_detail = df_all_view.copy()
            df_detail["Cabang / Area"] = df_detail.apply(extract_cabang_area, axis=1)
            df_detail["Aging / Tanggal"] = df_detail.apply(extract_aging_tanggal, axis=1)
            kol_detail = [
                c for c in [
                    "ID", "Customer", "Sales", "Bank", "Cabang / Area",
                    "Aging / Tanggal", "Status_Code", "Status", "Keaktifan", "Alasan Reject"
                ] if c in df_detail.columns
            ]
            st.dataframe(df_detail[kol_detail], use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ada data nasabah yang cocok dengan filter yang dipilih.")

    elif halaman_aktif == "🏛️ BNI Autodebet Tracking":
        render_page_banner(
            "⚡ AUTOTEAM — BNI Autodebet Tracking",
            "Pemantauan nasabah BNI berstatus D (Pengajuan ke Bank) yang diarahkan untuk pengaktifan ACC ONE."
        )

        df_bni_d = df_tracking[
            (df_tracking["Bank"] == "BNI") & (df_tracking["Status_Code"] == "D")
        ].copy()

        with st.container(key="panel_filter_bni"):
            st.markdown("<div class='section-panel-title'>Filter Nasabah BNI Status D</div><div class='section-panel-sub'>Pilih nama Sales atau cari nama nasabah / NOKON untuk memantau arahan ACC ONE.</div>", unsafe_allow_html=True)
            f_b1, f_b2 = st.columns([2, 1.5])
            with f_b1:
                sales_bni_list = sorted([s for s in df_bni_d["Sales"].unique() if s not in ["", "-"]])
                opsi_sales_bni = ["SEMUA SALES"] + list(dict.fromkeys([s for s in DAFTAR_SALES_MAKASSAR if s in sales_bni_list] + sales_bni_list))
                pilih_sales_bni = st.selectbox("Pilih Nama Sales (BNI Status D):", opsi_sales_bni, key="bni_sales_select")
            with f_b2:
                cari_bni = st.text_input("Cari Customer / NOKON:", placeholder="Ketik nama atau no. kontrak...", key="bni_search_input")

        if pilih_sales_bni != "SEMUA SALES":
            df_bni_d = df_bni_d[df_bni_d["Sales"].str.upper() == pilih_sales_bni.upper()]
        if cari_bni:
            m_n = df_bni_d["Customer"].astype(str).str.contains(cari_bni, case=False, na=False)
            m_i = df_bni_d["ID"].astype(str).str.contains(cari_bni, case=False, na=False)
            df_bni_d = df_bni_d[m_n | m_i]

        sudah_hubungi = sum(
            1 for idx, r in df_bni_d.iterrows()
            if f"{clean_text(r.get('ID', ''))}_{clean_text(r.get('Customer', ''))}_{idx}" in st.session_state.bni_contacted_keys
        )
        b_k1, b_k2, b_k3 = st.columns(3)
        with b_k1:
            render_metric_card("Nasabah BNI Status D", len(df_bni_d), "Pengajuan ke Bank")
        with b_k2:
            render_metric_card("Jumlah Sales Terkait", df_bni_d["Sales"].nunique() if not df_bni_d.empty else 0, "Tim lapangan aktif")
        with b_k3:
            render_metric_card("Sudah Dihubungi (ACC ONE)", sudah_hubungi, "Tercatat pada sesi ini")

        st.markdown("---")
        if df_bni_d.empty:
            st.info("Tidak ada nasabah BNI berstatus D (Pengajuan ke Bank) untuk filter saat ini.")
        else:
            if pilih_sales_bni != "SEMUA SALES" and len(df_bni_d) > 1:
                pesan_bni_rekap = build_wa_bni_rekap_message(df_bni_d, pilih_sales_bni)
                url_bni_rekap = f"https://wa.me/?text={urllib.parse.quote(pesan_bni_rekap)}"
                with st.container():
                    st.markdown(f"""
                        <div class="rekap-box">
                            <strong style="font-size:16px;">Rekap Sekaligus Arahan ACC ONE untuk {html.escape(pilih_sales_bni)} ({len(df_bni_d)} Nasabah)</strong><br>
                            <small>Menggabungkan seluruh nasabah BNI status D milik {html.escape(pilih_sales_bni)} ke dalam satu pesan WA polos untuk arahan pengaktifan ACC ONE.</small>
                        </div>
                    """, unsafe_allow_html=True)
                    col_br1, col_br2 = st.columns([1.4, 2.6])
                    with col_br1:
                        st.markdown(
                            f'<a href="{url_bni_rekap}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim Rekap WA ({len(df_bni_d)} Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    with col_br2:
                        with st.expander("Lihat / Salin Teks Pesan Rekap ACC ONE"):
                            st.text_area("Teks Rekap BNI ACC ONE", value=pesan_bni_rekap, height=200, label_visibility="collapsed")
                st.markdown("---")

            for idx, row in df_bni_d.iterrows():
                sales_nama = clean_text(row.get("Sales", ""), "-")
                cabang_area = extract_cabang_area(row)
                aging_tgl = extract_aging_tanggal(row)
                item_key = f"{clean_text(row.get('ID', ''))}_{clean_text(row.get('Customer', ''))}_{idx}"
                is_checked = item_key in st.session_state.bni_contacted_keys

                df_sales_bni = df_bni_d[df_bni_d["Sales"] == row.get("Sales", "")]
                jml_sales_bni = len(df_sales_bni)

                wa_bni_one = build_wa_bni_item_message(row)
                url_bni_one = f"https://wa.me/?text={urllib.parse.quote(wa_bni_one)}"

                wa_bni_grp = build_wa_bni_rekap_message(df_sales_bni, sales_nama)
                url_bni_grp = f"https://wa.me/?text={urllib.parse.quote(wa_bni_grp)}"

                with st.container():
                    card_c, status_c = st.columns([5.2, 1.3])
                    with card_c:
                        st.markdown(f"""
                            <div class="bni-box">
                                <strong>{html.escape(clean_text(row.get('Customer', '')))}</strong> (No. Kontrak: {html.escape(clean_text(row.get('ID', '')))})<br>
                                <small>Sales: <b>{html.escape(sales_nama)}</b> &nbsp;|&nbsp; Bank: <b>BNI</b> &nbsp;|&nbsp; Status: <b>D — Pengajuan ke Bank</b> &nbsp;|&nbsp; Total BNI (D) Sales ini: <b>{jml_sales_bni} Nasabah</b></small><br>
                                <small>Cabang/Area: <b>{html.escape(cabang_area)}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{html.escape(aging_tgl)}</b></small>
                            </div>
                        """, unsafe_allow_html=True)
                    with status_c:
                        checked_val = st.checkbox(
                            "Sudah dihubungi (ACC ONE)",
                            value=is_checked,
                            key=f"chk_bni_{item_key}"
                        )
                        if checked_val:
                            st.session_state.bni_contacted_keys.add(item_key)
                            st.markdown('<div class="ceklis-badge">✓ Sudah Dihubungi</div>', unsafe_allow_html=True)
                        else:
                            st.session_state.bni_contacted_keys.discard(item_key)
                            st.markdown('<div class="belum-ceklis-badge">Belum Dihubungi</div>', unsafe_allow_html=True)

                    if jml_sales_bni > 1:
                        bc1, bc2 = st.columns([1.2, 2.8])
                        with bc1:
                            st.markdown(
                                f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim 1 Nasabah Saja</button></a>',
                                unsafe_allow_html=True
                            )
                        with bc2:
                            st.markdown(
                                f'<a href="{url_bni_grp}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Rekap Semua ({jml_sales_bni} Nasabah {html.escape(sales_nama)})</button></a>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim WA Arahan ACC ONE</button></a>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

    elif halaman_aktif == "⚠️ Reject Tracking":
        render_page_banner(
            "⚡ AUTOTEAM — Reject Tracking",
            "Pusat pemantauan dan pengelolaan penolakan (Rejected / R) penagihan autodebet nasabah."
        )

        with st.container(key="panel_filter_reject"):
            st.markdown("<div class='section-panel-title'>Filter & Pencarian Tanggungan Reject</div><div class='section-panel-sub'>Saring daftar nasabah berstatus Rejected (R) per nama Sales atau kata kunci nama/NOKON.</div>", unsafe_allow_html=True)
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
                daftar_filter_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
                pilih_sales = st.selectbox("Pilih Nama Sales:", daftar_filter_sales)
            with col_f2:
                search_box = st.text_input("Cari Nama / No. Kontrak:", placeholder="Ketik nama customer atau NOKON...")

        df_view = df_tracking[df_tracking["Status_Code"] == "R"].copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"].str.upper() == pilih_sales.upper()]
        if search_box:
            mask_nama = df_view["Customer"].astype(str).str.contains(search_box, case=False, na=False)
            mask_id = df_view["ID"].astype(str).str.contains(search_box, case=False, na=False)
            df_view = df_view[mask_nama | mask_id]

        r_c1, r_c2, r_c3 = st.columns(3)
        with r_c1:
            render_metric_card("Total Reject Ditampilkan", len(df_view), "Status Rejected (R)")
        with r_c2:
            render_metric_card("Sales Terkait", df_view["Sales"].nunique() if not df_view.empty else 0, "Perlu tindak lanjut")
        with r_c3:
            render_metric_card("Bank Dominan Reject", df_view["Bank"].mode().iloc[0] if not df_view.empty else "-", "Berdasarkan filter aktif")

        st.markdown("---")
        st.info("Akses Database Pusat: Untuk mengelola, menambah, atau menghapus data secara langsung, silakan buka Google Sheets utama.")
        st.markdown(f'<a href="{SHEET_EDIT_URL}" target="_blank"><button style="background-color:#10b981; color:white; border:none; padding:10px 20px; border-radius:8px; font-weight:700; cursor:pointer;">Buka Google Sheets Database Utama</button></a>', unsafe_allow_html=True)

        st.markdown(f"### Daftar Tanggungan Rejected ({len(df_view)} Data)")

        if len(df_view) == 0:
            st.warning("Tidak ada data rejected yang ditemukan untuk filter tersebut.")
        else:
            if pilih_sales != "SEMUA SALES" and len(df_view) > 1:
                pesan_rekap_sales = build_wa_rekap_message(df_view, pilih_sales)
                url_rekap_sales = f"https://wa.me/?text={urllib.parse.quote(pesan_rekap_sales)}"
                with st.container():
                    st.markdown(f"""
                        <div class="rekap-box">
                            <strong style="font-size:16px;">Opsi Rekap Sekaligus untuk {html.escape(pilih_sales)} ({len(df_view)} Nasabah)</strong><br>
                            <small>Menggabungkan seluruh {len(df_view)} nasabah reject milik {html.escape(pilih_sales)} ke dalam 1 pesan WA polos bernomor (lengkap Cabang/Area, Aging/Tanggal, Alasan & Solusi).</small>
                        </div>
                    """, unsafe_allow_html=True)
                    col_r1, col_r2 = st.columns([1.4, 2.6])
                    with col_r1:
                        st.markdown(
                            f'<a href="{url_rekap_sales}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim Rekap Sekaligus ({len(df_view)} Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    with col_r2:
                        with st.expander("Lihat / Salin Teks Rekap WA Sales"):
                            st.text_area("Teks Rekap WA Sales", value=pesan_rekap_sales, height=220, label_visibility="collapsed")
                st.markdown("---")

            for _, row in df_view.iterrows():
                sales_nama = clean_text(row.get("Sales", ""), "-")
                alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum di sheet")
                cabang_area = extract_cabang_area(row)
                aging_tgl = extract_aging_tanggal(row)

                wa_item_msg = build_wa_item_message(row)
                wa_item_url = f"https://wa.me/?text={urllib.parse.quote(wa_item_msg)}"

                df_sales_ini = df_view[df_view["Sales"] == row.get("Sales", "")]
                jml_sales_ini = len(df_sales_ini)
                wa_sales_group_msg = build_wa_rekap_message(df_sales_ini, sales_nama)
                wa_sales_group_url = f"https://wa.me/?text={urllib.parse.quote(wa_sales_group_msg)}"

                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{html.escape(clean_text(row.get('Customer', '')))}</strong> ({html.escape(clean_text(row.get('Bank', '')))} - No. Kontrak: {html.escape(clean_text(row.get('ID', '')))})<br>
                            <small>Sales: <b>{html.escape(sales_nama)}</b> &nbsp;|&nbsp; Status: <b>{html.escape(clean_text(row.get('Status', 'Rejected')))} ({html.escape(clean_text(row.get('Status_Code', 'R'))))})</b> &nbsp;|&nbsp; Total Reject Sales ini: <b>{jml_sales_ini} Nasabah</b></small><br>
                            <small>Cabang/Area: <b>{html.escape(cabang_area)}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{html.escape(aging_tgl)}</b></small><br>
                            <span class="reject-reason">Alasan Reject: {html.escape(alasan)}</span>
                            <div class="solution-box">
                                <span>Solusi Perbaikan:</span><br>
                                {html.escape(clean_text(row.get('Solusi', '')))}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    if jml_sales_ini > 1:
                        b_col1, b_col2 = st.columns([1.2, 2.8])
                        with b_col1:
                            st.markdown(
                                f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim 1 Nasabah Saja</button></a>',
                                unsafe_allow_html=True
                            )
                        with b_col2:
                            st.markdown(
                                f'<a href="{wa_sales_group_url}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Rekap Semua ({jml_sales_ini} Nasabah {html.escape(sales_nama)})</button></a>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim WA ke Sales (1 Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

    elif halaman_aktif == "📘 Reject Guide":
        render_page_banner(
            "⚡ AUTOTEAM — Panduan Penanganan Reject & Solusi Sales",
            "Acuan standar operasional lengkap untuk penanganan penolakan autodebet dan tindakan korektif Sales di ACC Cabang Makassar."
        )

        with st.container(key="panel_filter_guide"):
            search_guide = st.text_input("Cari Kata Kunci Panduan / Solusi:", placeholder="Contoh: tanda tangan, rekening, telepon, brimo, saldo, dormant...")

        df_g = pd.DataFrame(REJECT_GUIDE_ITEMS)
        if search_guide:
            mask_g = (
                df_g["Alasan Reject"].str.contains(search_guide, case=False, na=False) |
                df_g["Keterangan"].str.contains(search_guide, case=False, na=False) |
                df_g["Tindakan Korektif / Solusi Sales"].str.contains(search_guide, case=False, na=False)
            )
            df_g = df_g[mask_g]

        render_metric_card("Jumlah Panduan Tersedia", len(df_g), "SOP Penanganan Reject & Solusi Sales")
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    elif halaman_aktif == "🔧 Settings":
        render_page_banner(
            "⚡ AUTOTEAM — Pengaturan Sistem & Database",
            "Informasi koneksi Google Sheets utama, akses pengelolaan data, dan backup rekap Excel."
        )

        s_c1, s_c2 = st.columns(2)
        with s_c1:
            render_metric_card("Versi Aplikasi", "AUTOTEAM v7.9", "Adaptif Light / Dark Mode")
        with s_c2:
            render_metric_card("Total Data Tersinkron", total_data, "Live via Google Sheets")

        st.write("Versi Web: **AUTOTEAM** (Autodebet Team Achievement & Monitoring) v7.9")
        if is_live:
            st.success(f"Status: Terhubung Sempurna ke Google Sheets Database Utama — {total_data} Data")
        else:
            st.warning("Status: Menggunakan mode cadangan sementara. Pastikan akses berbagi Google Sheets diset 'Siapa saja yang memiliki link dapat melihat'.")

        st.markdown("---")
        st.subheader("Akses Langsung Google Sheets")
        st.markdown("Anda dapat langsung mengelola, menambah, atau menghapus data Sales melalui tautan berikut:")
        st.markdown(f'<a href="{SHEET_EDIT_URL}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:10px 20px; border-radius:8px; font-weight:700; cursor:pointer;">Buka Google Sheets Utama</button></a>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Download Backup Data (Excel)")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_tracking.to_excel(writer, sheet_name='Tracking_Backup', index=False)
        excel_data = output.getvalue()

        st.download_button(
            label="Download Rekap Data Tracking (.xlsx)",
            data=excel_data,
            file_name="Backup_AUTOTEAM_Makassar.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == '__main__':
    main()
