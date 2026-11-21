import streamlit as st
import pandas as pd
import io
import html
import urllib.parse

st.set_page_config(
    page_title="AUTOTEAM - Autodebet Team Achievement & Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    :root {
        color-scheme: light dark;
        --bg-panel: light-dark(
            linear-gradient(145deg, rgba(224, 242, 254, 0.95) 0%, rgba(239, 246, 255, 0.96) 100%),
            linear-gradient(145deg, rgba(13, 28, 62, 0.92) 0%, rgba(15, 23, 42, 0.94) 100%)
        );
        --bg-card-soft: light-dark(#eff6ff, #111c33);
        --bg-card-elevated: light-dark(#ffffff, #16233d);
        --bg-input: light-dark(#ffffff, #0f1e3d);
        --bg-input-hover: light-dark(#e0f2fe, #162b56);
        --border-subtle: light-dark(rgba(29, 78, 216, 0.28), rgba(56, 189, 248, 0.28));
        --border-accent: light-dark(#1d4ed8, #38bdf8);
        --text-primary: light-dark(#0f172a, #f8fafc);
        --text-secondary: light-dark(#334155, #cbd5e1);
        --text-muted: light-dark(#475569, #94a3b8);
        --metric-grad: light-dark(
            linear-gradient(155deg, #dbeafe 0%, #bfdbfe 100%),
            linear-gradient(145deg, #0b2454 0%, #0f367a 100%)
        );
        --metric-border: light-dark(#60a5fa, #2563eb);
        --metric-label: light-dark(#1e3a8a, #bfdbfe);
        --metric-value: light-dark(#0f172a, #ffffff);
        --metric-sub: light-dark(#1e40af, #bae6fd);
        --bank-grad: light-dark(
            linear-gradient(160deg, #e0f2fe 0%, #dbeafe 55%, #bfdbfe 100%),
            linear-gradient(160deg, #0c224d 0%, #113270 100%)
        );
        --bank-title: light-dark(#1e3a8a, #93c5fd);
        --bank-rate: light-dark(#0f172a, #ffffff);
        --bank-sub: light-dark(#1e40af, #e0f2fe);
        --bank-badge: light-dark(#92400e, #fde047);
        --table-head-grad: light-dark(
            linear-gradient(90deg, #1d4ed8 0%, #0284c7 100%),
            linear-gradient(90deg, #003399 0%, #0369a1 100%)
        );
        --table-row-bg: light-dark(#ffffff, rgba(15, 35, 82, 0.65));
        --table-row-alt: light-dark(#f1f5f9, rgba(20, 44, 98, 0.72));
        --table-row-hover: light-dark(#dbeafe, rgba(29, 78, 216, 0.48));
        --solution-bg: light-dark(#ecfdf5, #064e3b);
        --solution-border: light-dark(#059669, #10b981);
        --solution-text: light-dark(#064e3b, #ecfdf5);
        --solution-title: light-dark(#047857, #34d399);
        --reject-reason: light-dark(#dc2626, #f87171);
        --ap-warn-bg: light-dark(rgba(254, 242, 242, 0.96), rgba(127, 29, 29, 0.34));
        --ap-warn-border: light-dark(#ef4444, #f87171);
        --ap-warn-text: light-dark(#991b1b, #fecaca);
        --ap-bang-color: light-dark(#dc2626, #fca5a5);
        --shadow-soft: light-dark(0 4px 16px rgba(29, 78, 216, 0.10), 0 6px 20px rgba(2, 6, 23, 0.42));
        --shadow-glow: light-dark(0 6px 20px rgba(29, 78, 216, 0.22), 0 6px 22px rgba(56, 189, 248, 0.28));
    }

    @keyframes warnPulse {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.12) rotate(3deg); }
    }

    footer {display: none !important; visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071330 0%, #0b1f4d 52%, #091738 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.25);
    }
    section[data-testid="stSidebar"] .stRadio > div { gap: 8px; }
    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(15, 35, 82, 0.72);
        border: 1px solid rgba(96, 165, 250, 0.28);
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: transform 0.16s ease, background-color 0.16s ease;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        transform: translateX(4px);
        background: linear-gradient(90deg, rgba(0, 85, 204, 0.85), rgba(14, 116, 144, 0.78));
    }
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: linear-gradient(90deg, #0044b3 0%, #0284c7 100%) !important;
        border: 1px solid #bae6fd !important;
        border-left: 5px solid #facc15 !important;
    }
    section[data-testid="stSidebar"] .stRadio label p {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    @media (min-width: 1200px) {
        .st-key-mobile_quick_nav { display: none !important; }
    }
    @media (max-width: 1199.98px) {
        .st-key-mobile_quick_nav {
            background: var(--bg-panel);
            border: 1.5px solid var(--metric-border);
            border-left: 5px solid var(--border-accent);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 14px;
            box-shadow: var(--shadow-soft);
        }
        .st-key-mobile_quick_nav div[data-testid="stButton"] > button {
            min-height: 44px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 12.5px;
        }
    }

    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-card-soft);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        margin-bottom: 14px;
    }
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 9px;
        padding: 8px 16px;
        font-weight: 700;
        font-size: 13.5px;
        color: var(--text-secondary);
    }
    div[data-testid="stTabs"] [aria-selected="true"] {
        background: linear-gradient(90deg, #0044b3 0%, #0284c7 100%) !important;
        color: #ffffff !important;
    }

    .hero-banner {
        background: linear-gradient(120deg, #002366, #0044b3, #0369a1);
        padding: 20px 24px;
        border-radius: 14px;
        border: 1px solid rgba(125, 211, 252, 0.45);
        box-shadow: 0 8px 24px rgba(0, 35, 102, 0.25);
        margin-bottom: 18px;
    }
    .hero-title { color: #ffffff !important; font-size: 26px; font-weight: 800; margin: 0; }
    .hero-sub { color: #e0f2fe !important; font-size: 14px; margin-top: 5px; margin-bottom: 10px; }
    .tagline-pill {
        display: inline-block;
        background: linear-gradient(90deg, #003399, #0284c7);
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid rgba(186, 230, 253, 0.7);
    }

    .st-key-panel_filter_status,
    .st-key-panel_filter_bni,
    .st-key-panel_filter_reject,
    .st-key-panel_filter_guide,
    .st-key-panel_filter_accone {
        background: var(--bg-panel);
        border: 1px solid var(--border-subtle);
        border-left: 5px solid var(--border-accent);
        border-top: 3px solid var(--border-accent);
        border-radius: 14px;
        padding: 16px 20px 18px 20px;
        margin-bottom: 16px;
        box-shadow: var(--shadow-soft);
    }
    .filter-chip-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(29, 78, 216, 0.14);
        color: var(--bank-title);
        border: 1px solid var(--border-subtle);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 11.5px;
        font-weight: 700;
    }

    div[data-testid="stSelectbox"] label p,
    div[data-testid="stTextInput"] label p {
        color: var(--bank-title) !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: var(--bg-input) !important;
        border: 1.5px solid var(--metric-border) !important;
        border-radius: 10px !important;
        transition: border-color 0.16s ease, box-shadow 0.16s ease !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
    div[data-testid="stTextInput"] div[data-baseweb="input"]:hover {
        background: var(--bg-input-hover) !important;
        border-color: var(--border-accent) !important;
    }

    .section-panel-title {
        color: var(--text-primary);
        font-size: 16px;
        font-weight: 800;
        margin: 0 0 4px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
    }
    .section-panel-sub { color: var(--text-secondary); font-size: 13px; margin: 0 0 12px 0; }

    .metric-card, .bank-card {
        background: var(--metric-grad);
        padding: 16px;
        border-radius: 12px;
        box-shadow: var(--shadow-soft);
        border: 1.5px solid var(--metric-border);
        border-top: 4px solid var(--border-accent);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label, .bank-title { color: var(--metric-label); font-size: 13.5px; font-weight: 700; }
    .metric-value, .bank-rate { color: var(--metric-value); margin: 6px 0; font-weight: 800; font-size: 26px; line-height: 1.15; }
    .metric-sub, .bank-sub { color: var(--metric-sub); font-size: 12px; }
    .bank-badge { color: var(--bank-badge); font-weight: 700; }

    .lb-panel {
        background: var(--bg-panel);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 16px;
        box-shadow: var(--shadow-soft);
        margin-bottom: 12px;
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
    }
    .top-rank-1 { border-left: 4px solid #eab308; }
    .top-rank-2 { border-left: 4px solid #94a3b8; }
    .top-rank-3 { border-left: 4px solid #d97706; }
    .trophy-anim { font-size: 21px; margin-right: 10px; }
    .rank-name { color: var(--text-primary); font-weight: 700; font-size: 14px; }
    .rank-meta { color: var(--text-secondary); font-size: 12px; }
    .rank-score-pill {
        background: linear-gradient(90deg, #003399, #0284c7);
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 12.5px;
    }

    .styled-table-wrap {
        width: 100%;
        overflow-x: auto;
        max-height: 520px;
        overflow-y: auto;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-soft);
        background: var(--bg-card-elevated);
    }
    .lb-table { width: 100%; border-collapse: collapse; font-size: 13.5px; color: var(--text-primary); }
    .lb-table thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: var(--table-head-grad);
        color: #ffffff !important;
        text-align: left;
        font-weight: 700;
        padding: 12px 14px;
        white-space: nowrap;
    }
    .lb-table td { padding: 11px 14px; border-bottom: 1px solid var(--border-subtle); vertical-align: top; }
    .lb-table tbody tr:nth-child(odd) { background-color: var(--table-row-bg); }
    .lb-table tbody tr:nth-child(even) { background-color: var(--table-row-alt); }
    .lb-table tbody tr:hover { background-color: var(--table-row-hover); }

    .pill-badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; white-space: nowrap; }
    .pill-blue { background: rgba(29, 78, 216, 0.14); color: var(--bank-title); border: 1px solid rgba(29, 78, 216, 0.35); }
    .pill-green { background: rgba(16, 185, 129, 0.15); color: var(--solution-title); border: 1px solid rgba(16, 185, 129, 0.38); }
    .pill-amber { background: rgba(217, 119, 6, 0.15); color: var(--bank-badge); border: 1px solid rgba(217, 119, 6, 0.38); }
    .pill-slate { background: rgba(100, 116, 139, 0.15); color: var(--text-secondary); border: 1px solid rgba(100, 116, 139, 0.35); }
    .rej-pill { display: inline-block; background-color: rgba(220, 38, 38, 0.14); color: var(--reject-reason); border: 1px solid rgba(220, 38, 38, 0.35); padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; white-space: nowrap; }

    .reject-group-banner {
        background: var(--bg-panel);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 10px 0 12px 0;
        box-shadow: var(--shadow-soft);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
    }
    .reject-group-pending { border-left: 5px solid #ef4444; }
    .reject-group-done { border-left: 5px solid #10b981; }

    .reject-box, .bni-box, .accone-note-card {
        background: var(--bg-card-elevated);
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        margin-bottom: 12px;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
    }
    .reject-box { border-left: 5px solid #ef4444; }
    .reject-box-done { border-left: 5px solid #10b981; }
    .bni-box { border-left: 5px solid #0284c7; }
    .accone-note-card { border-left: 5px solid var(--border-accent); }
    .reject-box strong, .bni-box strong { color: var(--text-primary); font-size: 17px; }
    .reject-box small, .bni-box small { color: var(--text-secondary); font-size: 13px; }
    .reject-reason { color: var(--reject-reason); font-weight: 700; font-size: 14.5px; margin-top: 8px; display: block; }

    .ap-payment-alert {
        background: var(--ap-warn-bg);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-left: 4px solid var(--ap-warn-border);
        border-radius: 9px;
        padding: 10px 14px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--ap-warn-text);
        font-size: 13.5px;
        font-weight: 700;
    }
    a.ap-bang-link {
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .ap-bang-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(220, 38, 38, 0.16);
        color: var(--ap-bang-color);
        border: 1.5px solid rgba(220, 38, 38, 0.55);
        border-radius: 7px;
        padding: 3px 9px;
        font-weight: 900;
        font-size: 13.5px;
        letter-spacing: 0.5px;
        cursor: pointer;
        transition: transform 0.16s ease, background-color 0.16s ease, box-shadow 0.16s ease;
        animation: warnPulse 2.2s infinite ease-in-out;
    }
    a.ap-bang-link:hover .ap-bang-icon {
        background: #dc2626;
        color: #ffffff;
        transform: scale(1.1);
        box-shadow: 0 3px 10px rgba(220, 38, 38, 0.35);
    }

    .accone-note-head { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
    .accone-note-title { color: var(--text-primary); font-size: 15.5px; font-weight: 800; margin: 0; }
    .accone-note-body { color: var(--text-secondary); font-size: 13.5px; line-height: 1.55; margin: 0; }
    .accone-sublist { margin: 8px 0 0 0; padding-left: 20px; color: var(--text-primary); font-size: 13.5px; line-height: 1.6; }
    .accone-sublist li { margin-bottom: 4px; }

    .solution-box {
        background: var(--solution-bg);
        padding: 13px 15px;
        border-radius: 9px;
        border-left: 4px solid var(--solution-border);
        margin-top: 10px;
        color: var(--solution-text);
        font-size: 13.5px;
        line-height: 1.5;
    }
    .solution-box span { color: var(--solution-title); font-weight: 700; }

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
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1_WjXj0lShrzkXDDfJQQdwCZ_2yizmigA562GdtFxXEw"
SHEET_EDIT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

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

KAMUS_STATUS = {
    "O": "Open", "F": "Bukcet Finance", "D": "Pengajuan ke Bank",
    "A": "Approved", "R": "Rejected", "C": "Cancelled",
    "B": "Batal", "E": "Edit", "P": "Pending",
}
STATUS_TIDAK_AKTIF = {"C", "B"}
STATUS_AKTIF = {"O", "F", "D", "A", "R", "E", "P"}

AP_PAYMENT_WARNING_TEXT = "Mohon dilengkapi berkas yang kurang kemudian serahkan kembali ke AP Payment"

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

ACCONE_REJECT_NOTES = [
    {
        "no": 1,
        "badge": "Langkah Jika Ditolak",
        "title": "1. Jika hasil pendaftaran di ACC ONE “Ditolak”, maka lakukan:",
        "summary": "Ikuti urutan perbaikan data, dokumen, dan pengajuan ulang berikut secara tepat:",
        "steps": [
            "a. Input Ulang Data yang benar di CSO (pastikan 4 data mandatory terisi lengkap dan benar)",
            "b. Upload Ulang Dokumen di FAB",
            "c. Coba kembali Submit di ACC ONE, pastikan No. Telp sudah terdaftar di BNI & Pulsa minimal Rp 10.000 ya!"
        ]
    },
    {
        "no": 2,
        "badge": "Realtime & Status D",
        "title": "2. Proses Approval Autodebet BNI hasilnya REALTIME",
        "summary": "Jika daftar saat itu, maka HASIL akan ada SAAT ITU JUGA. Maka Status Pending Bank (D) bukan berarti menunggu Bank, tapi CUSTOMER WAJIB SUBMIT DI ACC ONE.",
        "steps": []
    },
    {
        "no": 3,
        "badge": "Pulsa, OTP & Walk-in BNI",
        "title": "3. Syarat Pulsa Minimal Rp 10.000 & Kendala OTP SMS",
        "summary": "Pastikan minimal pulsa customer Rp 10.000 agar OTP dapat masuk ke SMS. Jika pulsa mencukupi namun OTP tetap tidak masuk berarti OTP terkirim ke nomor telp yang terdaftar di BNI (berbeda dengan yang diinput di system ACC). Jika customer ingin mengganti no telp yang baru, maka customer dapat langsung datang ke cabang BNI untuk updation data.",
        "steps": []
    },
    {
        "no": 4,
        "badge": "Sinkronisasi No. Telp",
        "title": "4. Kesamaan No. Telp di System ACC & BNI",
        "summary": "Pastikan No Telp customer yang terinput di system ACC sama dengan yang terdaftar di BNI, agar tidak perlu updation data walk-in ke cabang BNI.",
        "steps": []
    }
]

REJECT_GUIDE_ITEMS = [
    {"No": 1, "Alasan Reject": "Phone number is not correct", "Keterangan": "Nomor telepon nasabah tidak sesuai atau berbeda antara data pengajuan/AOL dengan data yang terdaftar di bank / mobile banking (misalnya BRIMO).", "Tindakan Korektif / Solusi Sales": "Input ulang melalui menu AOL Autodebet CSO dan pastikan nomor HP sesuai dengan yang terdaftar di Bank/BRIMO. Jika belum sinkron, arahkan nasabah walk-in ke bank untuk pembaruan nomor HP."},
    {"No": 2, "Alasan Reject": "Phone number not found", "Keterangan": "Nomor telepon nasabah belum terdaftar atau tidak ditemukan pada sistem bank terkait saat proses pendaftaran autodebet.", "Tindakan Korektif / Solusi Sales": "Arahkan nasabah melakukan registrasi atau pembaruan data nomor HP aktif di bank terkait terlebih dahulu, lalu ajukan ulang."},
    {"No": 3, "Alasan Reject": "Scan Kartu ATM Meragukan / No. Kartu ATM Invalid", "Keterangan": "Foto atau scan kartu ATM kurang jelas/buram, atau nasabah sudah melakukan penggantian kartu ATM sehingga nomor kartu lama sudah tidak berlaku.", "Tindakan Korektif / Solusi Sales": "Minta foto/scan kartu ATM terbaru yang jelas dan valid (pastikan tidak terpotong/buram), lalu lakukan pengajuan ulang."},
    {"No": 4, "Alasan Reject": "Tanda Tangan Tidak Menyentuh Materai / Tidak Sesuai", "Keterangan": "Tanda tangan pada form kuasa/SKPR tidak menyentuh materai atau tidak cocok dengan spesimen tanda tangan pada KTP/buku tabungan.", "Tindakan Korektif / Solusi Sales": "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank nasabah dan pastikan tidak menyimpang dari batas ketentuan."},
    {"No": 5, "Alasan Reject": "Invalid format account number", "Keterangan": "Format nomor rekening tidak sesuai ketentuan bank, salah digit, atau terdapat spasi/karakter yang tidak valid.", "Tindakan Korektif / Solusi Sales": "Periksa kembali nomor rekening nasabah sesuai buku tabungan/rekening asli tanpa spasi atau karakter tambahan, lalu input ulang."},
    {"No": 6, "Alasan Reject": "Saldo tidak mencukupi", "Keterangan": "Saldo rekening nasabah tidak mencukupi untuk memenuhi syarat minimum atau proses pendebetan/validasi.", "Tindakan Korektif / Solusi Sales": "Informasikan nasabah untuk memastikan saldo rekening mencukupi dan aktif sebelum proses penagihan/aktivasi berikutnya."},
    {"No": 7, "Alasan Reject": "Rekening tidak aktif / dormant", "Keterangan": "Rekening sumber autodebet dalam status dormant (tidak aktif) atau diblokir/terbatas transaksinya.", "Tindakan Korektif / Solusi Sales": "Arahkan nasabah untuk mengaktifkan kembali rekening (reaktivasi dormant) di cabang bank terkait."},
    {"No": 8, "Alasan Reject": "Data customer tidak sesuai", "Keterangan": "Terdapat ketidaksesuaian identitas nasabah (nama, NIK/KTP, atau data pendukung) antara kontrak/pengajuan dan data rekening bank.", "Tindakan Korektif / Solusi Sales": "Cocokkan kembali identitas nasabah di KTP, kontrak, dan rekening bank, lalu koordinasikan perbaikan data/dokumen pendukung."}
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
    return "\n".join([
        f"Halo Kak {sales}, mohon bantuannya follow up reject autodebet customer berikut:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        f"- Bank: {bank}",
        f"- Aging/Tanggal: {aging_tgl}",
        f"- Alasan Reject: {alasan}",
        f"- Solusi: {solusi}",
    ])

# Pesan WA Polos (Tanpa Emotikon) - Klik Tanda Seru (!!) AP Payment per Item
def build_wa_ap_payment_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    bank = clean_text(row.get("Bank", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)
    alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum")
    solusi = clean_text(row.get("Solusi", ""), "-")
    return "\n".join([
        f"Halo Kak {sales}, mohon bantuannya follow up reject autodebet customer berikut:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        f"- Bank: {bank}",
        f"- Aging/Tanggal: {aging_tgl}",
        f"- Alasan Reject: {alasan}",
        f"- Solusi: {solusi}",
        f"- Catatan AP Payment: {AP_PAYMENT_WARNING_TEXT}",
    ])

# Pesan WA Polos (Tanpa Emotikon) - Reject Rekap per Sales
def build_wa_rekap_message(df_rekap, nama_sales="Sales"):
    if df_rekap.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
    lines = [sapaan, "Berikut daftar customer reject yang perlu segera di follow up:", ""]
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
            f"   Solusi: {solusi}\n"
        )
    return "\n".join(lines).strip()

def build_wa_bni_item_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)
    return "\n".join([
        f"Halo Kak {sales}, mohon arahkan nasabah BNI berikut untuk pengaktifan ACC ONE:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        "- Bank: BNI",
        "- Status: D (Pengajuan ke Bank)",
        f"- Aging/Tanggal: {aging_tgl}",
        "- Arahan: Wajib mengajukan dan mengaktifkan ACC ONE sesuai arahan Sales.",
    ])

def build_wa_bni_rekap_message(df_bni, nama_sales="Sales"):
    if df_bni.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
    lines = [sapaan, "Berikut daftar nasabah BNI status D (Pengajuan ke Bank) yang wajib diarahkan untuk pengaktifan ACC ONE:", ""]
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
            f"   Arahan: Pengaktifan ACC ONE oleh nasabah dengan arahan Sales.\n"
        )
    return "\n".join(lines).strip()

@st.cache_data(ttl=120)
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
if "reject_contacted_keys" not in st.session_state:
    st.session_state.reject_contacted_keys = set()

DAFTAR_MENU = [
    "🎯 Home Dashboard",
    "📊 Status Customer",
    "🏛️ BNI Autodebet Tracking",
    "⚠️ Reject Tracking",
    "📘 Reject Guide",
    "🔧 Settings",
]

if "active_menu" not in st.session_state:
    st.session_state["active_menu"] = DAFTAR_MENU[0]

def select_menu_callback(nama_menu):
    st.session_state["active_menu"] = nama_menu
    st.session_state["sidebar_nav"] = nama_menu

def on_sidebar_change():
    st.session_state["active_menu"] = st.session_state["sidebar_nav"]

if "sidebar_nav" not in st.session_state:
    st.session_state["sidebar_nav"] = st.session_state["active_menu"]
elif st.session_state["sidebar_nav"] != st.session_state["active_menu"]:
    st.session_state["sidebar_nav"] = st.session_state["active_menu"]

def toggle_reject_contacted(item_key, widget_key):
    if st.session_state.get(widget_key):
        st.session_state.reject_contacted_keys.add(item_key)
    else:
        st.session_state.reject_contacted_keys.discard(item_key)

def toggle_bni_contacted(item_key, widget_key):
    if st.session_state.get(widget_key):
        st.session_state.bni_contacted_keys.add(item_key)
    else:
        st.session_state.bni_contacted_keys.discard(item_key)

st.sidebar.markdown(
    '<div style="padding: 6px 2px 2px 2px;">'
    '<h2 style="color: #ffffff; margin: 0; font-weight: 800; letter-spacing: 0.5px;">⚡ AUTOTEAM</h2>'
    '<p style="color: #93c5fd; font-size: 12.5px; margin: 2px 0 8px 0;">Autodebet Team Achievement & Monitoring</p>'
    '<div class="tagline-pill">Monitor. Improve. Activate.</div>'
    '</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='color:#bae6fd; font-weight:700; font-size:13px;'>MENU UTAMA</span>", unsafe_allow_html=True)
st.sidebar.radio("Navigasi", DAFTAR_MENU, key="sidebar_nav", on_change=on_sidebar_change, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.info("ACC Cabang Makassar — Kolaborasi & monitoring performa autodebet tim lapangan.")

def render_page_banner(title, subtitle):
    st.markdown(
        f'<div class="hero-banner">'
        f'<div class="hero-title">{html.escape(title)}</div>'
        f'<div class="hero-sub">{html.escape(subtitle)}</div>'
        f'<div class="tagline-pill">Monitor. Improve. Activate.</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_metric_card(label, value, subtext):
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{html.escape(str(label))}</div>'
        f'<div class="metric-value">{html.escape(str(value))}</div>'
        f'<div class="metric-sub">{html.escape(str(subtext))}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def format_table_cell(col_name, val):
    raw = str(val).strip()
    esc = html.escape(raw if raw != "" else "-")
    col_u = col_name.upper()
    if col_u in ["NO", "RANK", "BANK", "BANK_AUTODEBET", "% APPROVED", "% AUTODEBET"]:
        prefix = "#" if col_u in ["NO", "RANK"] else ""
        return f'<span class="pill-badge pill-blue">{prefix}{esc}</span>'
    if col_u == "KEAKTIFAN":
        cls = "pill-green" if raw.lower() == "aktif" else "pill-slate"
        return f'<span class="pill-badge {cls}">{esc}</span>'
    if col_u in ["STATUS", "STATUS PENDAFTARAN"]:
        up = raw.upper()
        if up in ["A", "APPROVED"]:
            return f'<span class="pill-badge pill-green">{esc}</span>'
        if up in ["R", "REJECTED"]:
            return f'<span class="rej-pill">{esc}</span>'
        if up in ["D", "PENGAJUAN KE BANK", "F", "BUKCET FINANCE", "O", "OPEN", "E", "EDIT", "P", "PENDING"]:
            return f'<span class="pill-badge pill-amber">{esc}</span>'
        if up in ["C", "CANCELLED", "B", "BATAL"]:
            return f'<span class="pill-badge pill-slate">{esc}</span>'
    if col_u == "REJECTED (R)":
        return f'<span class="rej-pill">{esc}</span>'
    if col_u == "APPROVED (A)":
        return f'<span class="pill-badge pill-green">{esc}</span>'
    if col_u in ["CUSTOMER", "NAMA_CUST", "SALES", "NAME_SO", "ALASAN REJECT"]:
        return f"<b>{esc}</b>"
    return esc

def render_styled_html_table(df, col_labels=None, max_rows=250):
    if df.empty:
        return
    df_show = df.head(max_rows)
    cols = list(df_show.columns)
    parts = ['<div class="styled-table-wrap"><table class="lb-table"><thead><tr>']
    for c in cols:
        hdr = col_labels.get(c, c) if col_labels else c
        parts.append(f"<th>{html.escape(str(hdr))}</th>")
    parts.append("</tr></thead><tbody>")
    for _, row in df_show.iterrows():
        parts.append("<tr>" + "".join(f"<td>{format_table_cell(c, row[c])}</td>" for c in cols) + "</tr>")
    parts.append("</tbody></table></div>")
    if len(df) > max_rows:
        parts.append(f"<div style='font-size:12px; color:var(--text-muted); margin-top:6px;'>Menampilkan {max_rows} dari {len(df)} baris data.</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)

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
        rows.append({"Sales": s_label, "Total Data": tot, "Approved (A)": app, "Rejected (R)": rej, "% Autodebet": round(pct, 1)})
    lb_df = pd.DataFrame(rows)
    if lb_df.empty:
        return pd.DataFrame(), pd.DataFrame()
    top5 = lb_df.sort_values(by=["% Autodebet", "Rejected (R)", "Approved (A)", "Total Data"], ascending=[False, True, False, False]).head(5).copy()
    top5.insert(0, "Rank", range(1, len(top5) + 1))
    bottom5 = lb_df.sort_values(by=["Rejected (R)", "% Autodebet", "Total Data"], ascending=[False, True, False]).head(5).copy()
    bottom5.insert(0, "Rank", range(1, len(bottom5) + 1))
    return top5, bottom5

def render_top5_trophy_cards(top5_df):
    trophy_icons = {1: "🏆", 2: "🥈", 3: "🥉", 4: "🏅", 5: "🎖️"}
    rank_classes = {1: "top-rank-1", 2: "top-rank-2", 3: "top-rank-3"}
    html_parts = ['<div class="lb-panel"><div class="lb-panel-title">🏆 Top 5 Sales — Persentase Autodebet Tertinggi & Reject Paling Sedikit</div>']
    for _, r in top5_df.iterrows():
        rk = int(r["Rank"])
        t_icon = trophy_icons.get(rk, "🏆")
        extra_cls = rank_classes.get(rk, "")
        s_name = html.escape(str(r["Sales"]))
        html_parts.append(
            f'<div class="top-rank-card {extra_cls}">'
            f'<div style="display:flex; align-items:center;">'
            f'<span class="trophy-anim">{t_icon}</span>'
            f'<div><div class="rank-name">#{rk} &nbsp;{s_name}</div>'
            f'<div class="rank-meta">Approved: <b>{int(r["Approved (A)"])}</b> / {int(r["Total Data"])} Data &nbsp;|&nbsp; Rejected: <b>{int(r["Rejected (R)"])}</b></div></div>'
            f'</div><div class="rank-score-pill">{float(r["% Autodebet"]):.1f}%</div></div>'
        )
    html_parts.append('</div>')
    return "".join(html_parts)

def render_bottom5_styled_table(bottom5_df):
    html_parts = [
        '<div class="lb-panel"><div class="lb-panel-title">⚠️ Bottom 5 Sales — Rejected (R) Terbanyak</div>',
        '<div class="styled-table-wrap" style="max-height:none;"><table class="lb-table">',
        '<thead><tr><th>Rank</th><th>Nama Sales</th><th>Total</th><th>Approved</th><th>Rejected (R)</th><th>% Autodebet</th></tr></thead><tbody>'
    ]
    for _, r in bottom5_df.iterrows():
        html_parts.append(
            f'<tr><td><b>#{int(r["Rank"])}</b></td><td><b>{html.escape(str(r["Sales"]))}</b></td>'
            f'<td>{int(r["Total Data"])}</td><td>{int(r["Approved (A)"])}</td>'
            f'<td><span class="rej-pill">{int(r["Rejected (R)"])} Reject</span></td><td><b>{float(r["% Autodebet"]):.1f}%</b></td></tr>'
        )
    html_parts.append('</tbody></table></div></div>')
    return "".join(html_parts)

def render_reject_card_item(idx, row, df_view, is_contacted):
    sales_nama = clean_text(row.get("Sales", ""), "-")
    alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum di sheet")
    solusi_teks = clean_text(row.get("Solusi", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)
    cust_teks = clean_text(row.get("Customer", ""))
    bank_teks = clean_text(row.get("Bank", ""))
    id_teks = clean_text(row.get("ID", ""))
    status_teks = clean_text(row.get("Status", "Rejected"))
    code_teks = clean_text(row.get("Status_Code", "R"))
    item_key = f"{id_teks}_{cust_teks}_{idx}"

    wa_item_url = f"https://wa.me/?text={urllib.parse.quote(build_wa_item_message(row))}"
    wa_ap_url = f"https://wa.me/?text={urllib.parse.quote(build_wa_ap_payment_message(row))}"

    df_sales_ini = df_view[df_view["Sales"] == row.get("Sales", "")]
    jml_sales_ini = len(df_sales_ini)
    wa_sales_group_url = f"https://wa.me/?text={urllib.parse.quote(build_wa_rekap_message(df_sales_ini, sales_nama))}"

    box_extra_cls = " reject-box-done" if is_contacted else ""
    warn_html = ""
    if not is_contacted:
        warn_html = (
            f'<div class="ap-payment-alert">'
            f'<a class="ap-bang-link" href="{wa_ap_url}" target="_blank" title="Klik tanda seru untuk kirim pesan WA beserta catatan AP Payment">'
            f'<span class="ap-bang-icon">!!</span>'
            f'</a>'
            f'<span>{html.escape(AP_PAYMENT_WARNING_TEXT)}</span>'
            f'</div>'
        )

    card_html = (
        f'<div class="reject-box{box_extra_cls}">'
        f'<strong>{html.escape(cust_teks)}</strong> ({html.escape(bank_teks)} - No. Kontrak: {html.escape(id_teks)})<br>'
        f'<small>Sales: <b>{html.escape(sales_nama)}</b> &nbsp;|&nbsp; Status: <b>{html.escape(status_teks)} ({html.escape(code_teks)})</b> &nbsp;|&nbsp; Total Reject Sales ini: <b>{jml_sales_ini} Nasabah</b></small><br>'
        f'<small>Cabang/Area: <b>{html.escape(cabang_area)}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{html.escape(aging_tgl)}</b></small><br>'
        f'<span class="reject-reason">Alasan Reject: {html.escape(alasan)}</span>'
        f'{warn_html}'
        f'<div class="solution-box"><span>Solusi Perbaikan:</span><br>{html.escape(solusi_teks)}</div>'
        f'</div>'
    )

    with st.container():
        card_col, chk_col = st.columns([5.2, 1.3])
        with card_col:
            st.markdown(card_html, unsafe_allow_html=True)
        with chk_col:
            w_key = f"chk_rej_{item_key}"
            st.checkbox(
                "Sudah dihubungi",
                value=is_contacted,
                key=w_key,
                on_change=toggle_reject_contacted,
                args=(item_key, w_key)
            )
            if is_contacted:
                st.markdown('<div class="ceklis-badge">✓ Sudah Dihubungi</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="belum-ceklis-badge">Belum Dihubungi</div>', unsafe_allow_html=True)

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

def main():
    with st.container(key="mobile_quick_nav"):
        st.markdown("<span style='font-weight:800; font-size:12.5px; color:var(--bank-title);'>AKSES CEPAT MENU (HP / TABLET)</span>", unsafe_allow_html=True)
        for row_start in range(0, len(DAFTAR_MENU), 3):
            cols = st.columns(3)
            for idx_col, nama_menu in enumerate(DAFTAR_MENU[row_start:row_start + 3]):
                with cols[idx_col]:
                    st.button(
                        nama_menu,
                        key=f"btn_nav_{row_start}_{idx_col}",
                        type="primary" if st.session_state["active_menu"] == nama_menu else "secondary",
                        use_container_width=True,
                        on_click=select_menu_callback,
                        args=(nama_menu,)
                    )

    halaman_aktif = st.session_state["active_menu"]
    total_data = len(df_tracking)
    df_aktif = df_tracking[df_tracking["Keaktifan"] == "Aktif"] if not df_tracking.empty else pd.DataFrame()
    total_aktif = len(df_aktif)
    total_approved = len(df_tracking[df_tracking["Status_Code"] == "A"]) if not df_tracking.empty else 0
    total_rejected = len(df_tracking[df_tracking["Status_Code"] == "R"]) if not df_tracking.empty else 0
    success_rate_cabang = (total_approved / total_data * 100) if total_data > 0 else 0.0

    if halaman_aktif == "🎯 Home Dashboard":
        render_page_banner("⚡ AUTOTEAM — Home Dashboard", "Autodebet Team Achievement & Monitoring — ACC Cabang Makassar")
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
                    f'<div class="bank-card"><div class="bank-title">{html.escape(bank_name)}</div>'
                    f'<div class="bank-rate">{rate_b:.1f}%</div>'
                    f'<div class="bank-sub">Total: <b>{vol_b}</b> Nasabah ({app_b} Approved)</div>'
                    f'<small class="bank-badge">{html.escape(badge_label)}</small></div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.subheader("Sales Leaderboard")
        top5_df, bottom5_df = build_sales_leaderboard(df_tracking)
        lb_col1, lb_col2 = st.columns(2)
        with lb_col1:
            if not top5_df.empty:
                st.markdown(render_top5_trophy_cards(top5_df), unsafe_allow_html=True)
        with lb_col2:
            if not bottom5_df.empty:
                st.markdown(render_bottom5_styled_table(bottom5_df), unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Master Data Nasabah & Status Tracking (Live from Google Sheets)")
        kolom_tampil = [c for c in ["NOKON", "NAMA_CUST", "CABANG", "NAME_SO", "BANK_AUTODEBET", "STATUS PENDAFTARAN", "Status", "Keaktifan", "REASON REJECT"] if c in df_tracking.columns]
        render_styled_html_table(
            df_tracking[kolom_tampil] if kolom_tampil else df_tracking,
            col_labels={"NOKON": "No. Kontrak", "NAMA_CUST": "Nama Customer", "CABANG": "Cabang", "NAME_SO": "Sales", "BANK_AUTODEBET": "Bank", "STATUS PENDAFTARAN": "Kode", "REASON REJECT": "Alasan Reject"},
            max_rows=200
        )

    elif halaman_aktif == "📊 Status Customer":
        render_page_banner("⚡ AUTOTEAM — Status Customer", "Pemantauan menyeluruh progress pengajuan seluruh nasabah dan kontribusi performa setiap Sales.")
        with st.container(key="panel_filter_status"):
            st.markdown(
                "<div class='section-panel-title'><span>🎛️ Filter & Pencarian Data Nasabah</span><span class='filter-chip-badge'>⚡ Live Filter Aktif</span></div>"
                "<div class='section-panel-sub'>Saring data berdasarkan Sales, status pendaftaran, keaktifan, bank, atau nama/NOKON.</div>",
                unsafe_allow_html=True
            )
            c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns([1.8, 1.3, 1.1, 1.1, 1.5])
            with c_f1:
                sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
                opsi_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
                pilih_sales_all = st.selectbox("Filter Sales:", opsi_sales, key="sales_all_select")
            with c_f2:
                opsi_status = ["SEMUA STATUS", "Open (O)", "Bukcet Finance (F)", "Pengajuan ke Bank (D)", "Approved (A)", "Rejected (R)", "Cancelled (C)", "Batal (B)", "Edit (E)", "Pending (P)"]
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
        status_code_map = {"Open (O)": "O", "Bukcet Finance (F)": "F", "Pengajuan ke Bank (D)": "D", "Approved (A)": "A", "Rejected (R)": "R", "Cancelled (C)": "C", "Batal (B)": "B", "Edit (E)": "E", "Pending (P)": "P"}
        if pilih_status in status_code_map:
            df_all_view = df_all_view[df_all_view["Status_Code"] == status_code_map[pilih_status]]
        if cari_cust_all:
            df_all_view = df_all_view[
                df_all_view["Customer"].astype(str).str.contains(cari_cust_all, case=False, na=False) |
                df_all_view["ID"].astype(str).str.contains(cari_cust_all, case=False, na=False)
            ]

        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: render_metric_card("Total Data", len(df_all_view), "Hasil filter aktif")
        with k2: render_metric_card("Approved (A)", len(df_all_view[df_all_view["Status_Code"] == "A"]), "Autodebet disetujui")
        with k3: render_metric_card("Status Aktif", len(df_all_view[df_all_view["Keaktifan"] == "Aktif"]), "Dalam proses / aktif")
        with k4: render_metric_card("Tidak Aktif (C/B)", len(df_all_view[df_all_view["Keaktifan"] == "Tidak Aktif"]), "Cancelled / Batal")
        with k5: render_metric_card("Rejected (R)", len(df_all_view[df_all_view["Status_Code"] == "R"]), "Perlu follow up")

        st.markdown("---")
        st.subheader("Rekap Progress per Sales")
        if not df_all_view.empty:
            rekap_rows = []
            for sales_name, grp in df_all_view.groupby("Sales"):
                s_label = sales_name if sales_name.strip() != "" else "(Tanpa Nama Sales)"
                tot_s = len(grp)
                app_s = len(grp[grp["Status_Code"] == "A"])
                rekap_rows.append({
                    "Sales": s_label,
                    "Total Data": tot_s,
                    "Approved (A)": app_s,
                    "Aktif": len(grp[grp["Keaktifan"] == "Aktif"]),
                    "Tidak Aktif (C/B)": len(grp[grp["Keaktifan"] == "Tidak Aktif"]),
                    "Rejected (R)": len(grp[grp["Status_Code"] == "R"]),
                    "% Approved": f"{(app_s / tot_s * 100) if tot_s > 0 else 0.0:.1f}%"
                })
            render_styled_html_table(pd.DataFrame(rekap_rows).sort_values(by=["Total Data", "Approved (A)"], ascending=False), max_rows=200)

        st.markdown("---")
        st.subheader(f"Detail Progress Seluruh Nasabah ({len(df_all_view)} Data)")
        if not df_all_view.empty:
            df_detail = df_all_view.copy()
            df_detail["Cabang / Area"] = df_detail.apply(extract_cabang_area, axis=1)
            df_detail["Aging / Tanggal"] = df_detail.apply(extract_aging_tanggal, axis=1)
            kol_detail = [c for c in ["ID", "Customer", "Sales", "Bank", "Cabang / Area", "Aging / Tanggal", "Status_Code", "Status", "Keaktifan", "Alasan Reject"] if c in df_detail.columns]
            render_styled_html_table(df_detail[kol_detail], col_labels={"ID": "No. Kontrak", "Status_Code": "Kode"}, max_rows=250)

    elif halaman_aktif == "🏛️ BNI Autodebet Tracking":
        render_page_banner("⚡ AUTOTEAM — BNI Autodebet Tracking", "Pemantauan nasabah BNI berstatus D (Pengajuan ke Bank) & panduan penanganan jika pengajuan ACC ONE ditolak.")
        tab_mon_bni, tab_guide_accone = st.tabs(["📋 Monitoring BNI Status D", "📌 Panduan Reject ACC ONE"])

        with tab_mon_bni:
            df_bni_d = df_tracking[(df_tracking["Bank"] == "BNI") & (df_tracking["Status_Code"] == "D")].copy()
            with st.container(key="panel_filter_bni"):
                st.markdown(
                    "<div class='section-panel-title'><span>🎛️ Filter Nasabah BNI Status D</span><span class='filter-chip-badge'>🏛️ BNI ACC ONE Filter</span></div>"
                    "<div class='section-panel-sub'>Pilih nama Sales atau cari nama nasabah / NOKON untuk memantau arahan ACC ONE.</div>",
                    unsafe_allow_html=True
                )
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
                df_bni_d = df_bni_d[
                    df_bni_d["Customer"].astype(str).str.contains(cari_bni, case=False, na=False) |
                    df_bni_d["ID"].astype(str).str.contains(cari_bni, case=False, na=False)
                ]

            sudah_hubungi = sum(
                1 for idx, r in df_bni_d.iterrows()
                if f"{clean_text(r.get('ID', ''))}_{clean_text(r.get('Customer', ''))}_{idx}" in st.session_state.bni_contacted_keys
            )
            b_k1, b_k2, b_k3 = st.columns(3)
            with b_k1: render_metric_card("Nasabah BNI Status D", len(df_bni_d), "Pengajuan ke Bank")
            with b_k2: render_metric_card("Jumlah Sales Terkait", df_bni_d["Sales"].nunique() if not df_bni_d.empty else 0, "Tim lapangan aktif")
            with b_k3: render_metric_card("Sudah Dihubungi (ACC ONE)", sudah_hubungi, "Tercatat pada sesi ini")

            st.markdown("---")
            if df_bni_d.empty:
                st.info("Tidak ada nasabah BNI berstatus D (Pengajuan ke Bank) untuk filter saat ini.")
            else:
                if pilih_sales_bni != "SEMUA SALES" and len(df_bni_d) > 1:
                    pesan_bni_rekap = build_wa_bni_rekap_message(df_bni_d, pilih_sales_bni)
                    url_bni_rekap = f"https://wa.me/?text={urllib.parse.quote(pesan_bni_rekap)}"
                    st.markdown(
                        f'<div class="rekap-box"><strong style="font-size:16px;">Rekap Sekaligus Arahan ACC ONE untuk {html.escape(pilih_sales_bni)} ({len(df_bni_d)} Nasabah)</strong><br>'
                        f'<small>Menggabungkan seluruh nasabah BNI status D milik {html.escape(pilih_sales_bni)} ke dalam satu pesan WA polos.</small></div>',
                        unsafe_allow_html=True
                    )
                    col_br1, col_br2 = st.columns([1.4, 2.6])
                    with col_br1:
                        st.markdown(f'<a href="{url_bni_rekap}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim Rekap WA ({len(df_bni_d)} Nasabah)</button></a>', unsafe_allow_html=True)
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
                    url_bni_one = f"https://wa.me/?text={urllib.parse.quote(build_wa_bni_item_message(row))}"
                    url_bni_grp = f"https://wa.me/?text={urllib.parse.quote(build_wa_bni_rekap_message(df_sales_bni, sales_nama))}"

                    with st.container():
                        card_c, status_c = st.columns([5.2, 1.3])
                        with card_c:
                            st.markdown(
                                f'<div class="bni-box"><strong>{html.escape(clean_text(row.get("Customer", "")))}</strong> (No. Kontrak: {html.escape(clean_text(row.get("ID", "")))})<br>'
                                f'<small>Sales: <b>{html.escape(sales_nama)}</b> &nbsp;|&nbsp; Bank: <b>BNI</b> &nbsp;|&nbsp; Status: <b>D — Pengajuan ke Bank</b> &nbsp;|&nbsp; Total BNI (D) Sales ini: <b>{jml_sales_bni} Nasabah</b></small><br>'
                                f'<small>Cabang/Area: <b>{html.escape(cabang_area)}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{html.escape(aging_tgl)}</b></small></div>',
                                unsafe_allow_html=True
                            )
                        with status_c:
                            w_b_key = f"chk_bni_{item_key}"
                            st.checkbox("Sudah dihubungi (ACC ONE)", value=is_checked, key=w_b_key, on_change=toggle_bni_contacted, args=(item_key, w_b_key))
                            if is_checked:
                                st.markdown('<div class="ceklis-badge">✓ Sudah Dihubungi</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="belum-ceklis-badge">Belum Dihubungi</div>', unsafe_allow_html=True)

                        if jml_sales_bni > 1:
                            bc1, bc2 = st.columns([1.2, 2.8])
                            with bc1:
                                st.markdown(f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim 1 Nasabah Saja</button></a>', unsafe_allow_html=True)
                            with bc2:
                                st.markdown(f'<a href="{url_bni_grp}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:700; cursor:pointer;">Rekap Semua ({jml_sales_bni} Nasabah {html.escape(sales_nama)})</button></a>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim WA Arahan ACC ONE</button></a>', unsafe_allow_html=True)
                        st.markdown("---")

        with tab_guide_accone:
            with st.container(key="panel_filter_accone"):
                st.markdown(
                    "<div class='section-panel-title'><span>📌 Catatan & Panduan Apabila Pengajuan ACC ONE Ditolak</span><span class='filter-chip-badge'>💡 Notes BNI ACC ONE</span></div>"
                    "<div class='section-panel-sub'>Acuan cepat langkah tindak lanjut apabila pendaftaran di ACC ONE ditolak, status D, atau kendala OTP/nomor HP BNI.</div>",
                    unsafe_allow_html=True
                )
                cari_accone = st.text_input("Cari Kata Kunci Catatan ACC ONE:", placeholder="Contoh: ditolak, cso, fab, pulsa, otp, bni, status d...", key="accone_note_search")

            filtered_notes = ACCONE_REJECT_NOTES
            if cari_accone:
                kw = cari_accone.lower().strip()
                filtered_notes = [n for n in ACCONE_REJECT_NOTES if kw in n["title"].lower() or kw in n["summary"].lower() or any(kw in stp.lower() for stp in n["steps"])]

            for note in filtered_notes:
                steps_html = ""
                if note["steps"]:
                    steps_html = '<ul class="accone-sublist">' + "".join(f"<li>{html.escape(stp)}</li>" for stp in note["steps"]) + "</ul>"
                st.markdown(
                    f'<div class="accone-note-card"><div class="accone-note-head">'
                    f'<div class="accone-note-title">{html.escape(note["title"])}</div>'
                    f'<span class="pill-badge pill-blue">{html.escape(note["badge"])}</span></div>'
                    f'<p class="accone-note-body">{html.escape(note["summary"])}</p>{steps_html}</div>',
                    unsafe_allow_html=True
                )

    elif halaman_aktif == "⚠️ Reject Tracking":
        render_page_banner("⚡ AUTOTEAM — Reject Tracking", "Pusat pemantauan dan pengelolaan penolakan (Rejected / R) penagihan autodebet nasabah.")
        with st.container(key="panel_filter_reject"):
            st.markdown(
                "<div class='section-panel-title'><span>🎛️ Filter & Pencarian Tanggungan Reject</span><span class='filter-chip-badge'>⚠️ Follow Up & AP Payment</span></div>"
                "<div class='section-panel-sub'>Saring daftar nasabah berstatus Rejected (R) per nama Sales atau kata kunci nama/NOKON.</div>",
                unsafe_allow_html=True
            )
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
                daftar_filter_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
                pilih_sales = st.selectbox("Pilih Nama Sales:", daftar_filter_sales, key="rej_sales_select")
            with col_f2:
                search_box = st.text_input("Cari Nama / No. Kontrak:", placeholder="Ketik nama customer atau NOKON...", key="rej_search_input")

        df_view = df_tracking[df_tracking["Status_Code"] == "R"].copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"].str.upper() == pilih_sales.upper()]
        if search_box:
            df_view = df_view[
                df_view["Customer"].astype(str).str.contains(search_box, case=False, na=False) |
                df_view["ID"].astype(str).str.contains(search_box, case=False, na=False)
            ]

        belum_dihubungi_items, sudah_dihubungi_items = [], []
        for idx, row in df_view.iterrows():
            item_key = f"{clean_text(row.get('ID', ''))}_{clean_text(row.get('Customer', ''))}_{idx}"
            if item_key in st.session_state.reject_contacted_keys:
                sudah_dihubungi_items.append((idx, row))
            else:
                belum_dihubungi_items.append((idx, row))

        r_c1, r_c2, r_c3, r_c4 = st.columns(4)
        with r_c1: render_metric_card("Total Reject Ditampilkan", len(df_view), "Status Rejected (R)")
        with r_c2: render_metric_card("Belum Dihubungi", len(belum_dihubungi_items), "Wajib follow up & AP Payment")
        with r_c3: render_metric_card("Sudah Dihubungi", len(sudah_dihubungi_items), "Tercatat sudah difollow up")
        with r_c4: render_metric_card("Bank Dominan Reject", df_view["Bank"].mode().iloc[0] if not df_view.empty else "-", "Berdasarkan filter aktif")

        st.markdown("---")
        st.info("Akses Database Pusat: Untuk mengelola, menambah, atau menghapus data secara langsung, silakan buka Google Sheets utama.")
        st.markdown(f'<a href="{SHEET_EDIT_URL}" target="_blank"><button style="background-color:#10b981; color:white; border:none; padding:10px 20px; border-radius:8px; font-weight:700; cursor:pointer;">Buka Google Sheets Database Utama</button></a>', unsafe_allow_html=True)

        if len(df_view) > 0:
            if pilih_sales != "SEMUA SALES" and len(df_view) > 1:
                pesan_rekap_sales = build_wa_rekap_message(df_view, pilih_sales)
                url_rekap_sales = f"https://wa.me/?text={urllib.parse.quote(pesan_rekap_sales)}"
                st.markdown(
                    f'<div class="rekap-box"><strong style="font-size:16px;">Opsi Rekap Sekaligus untuk {html.escape(pilih_sales)} ({len(df_view)} Nasabah)</strong><br>'
                    f'<small>Menggabungkan seluruh {len(df_view)} nasabah reject milik {html.escape(pilih_sales)} ke dalam 1 pesan WA polos bernomor.</small></div>',
                    unsafe_allow_html=True
                )
                col_r1, col_r2 = st.columns([1.4, 2.6])
                with col_r1:
                    st.markdown(f'<a href="{url_rekap_sales}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer;">Kirim Rekap Sekaligus ({len(df_view)} Nasabah)</button></a>', unsafe_allow_html=True)
                with col_r2:
                    with st.expander("Lihat / Salin Teks Rekap WA Sales"):
                        st.text_area("Teks Rekap WA Sales", value=pesan_rekap_sales, height=220, label_visibility="collapsed")
                st.markdown("---")

            st.markdown(
                f'<div class="reject-group-banner reject-group-pending"><div>'
                f'<strong style="font-size:16px; color:var(--text-primary);">⏳ List Customer Reject — Belum Dihubungi ({len(belum_dihubungi_items)} Data)</strong><br>'
                f'<small style="color:var(--text-secondary);">Klik tanda seru (!!) untuk kirim pesan WA beserta catatan AP Payment sesuai data nasabah.</small></div>'
                f'<span class="rej-pill">{len(belum_dihubungi_items)} Belum Dihubungi</span></div>',
                unsafe_allow_html=True
            )
            if not belum_dihubungi_items:
                st.success("Seluruh customer reject pada filter ini sudah ditandai 'Sudah dihubungi'.")
            else:
                for idx, row in belum_dihubungi_items:
                    render_reject_card_item(idx, row, df_view, is_contacted=False)

            st.markdown(
                f'<div class="reject-group-banner reject-group-done"><div>'
                f'<strong style="font-size:16px; color:var(--text-primary);">✓ List Customer Reject — Sudah Dihubungi ({len(sudah_dihubungi_items)} Data)</strong><br>'
                f'<small style="color:var(--text-secondary);">Customer yang sudah dicentang sudah dihubungi.</small></div>'
                f'<span class="pill-badge pill-green">{len(sudah_dihubungi_items)} Sudah Dihubungi</span></div>',
                unsafe_allow_html=True
            )
            if not sudah_dihubungi_items:
                st.info("Belum ada customer reject yang dicentang 'Sudah dihubungi' untuk filter saat ini.")
            else:
                for idx, row in sudah_dihubungi_items:
                    render_reject_card_item(idx, row, df_view, is_contacted=True)

    elif halaman_aktif == "📘 Reject Guide":
        render_page_banner("⚡ AUTOTEAM — Panduan Penanganan Reject & Solusi Sales", "Acuan standar operasional lengkap untuk penanganan penolakan autodebet dan tindakan korektif Sales.")
        with st.container(key="panel_filter_guide"):
            st.markdown(
                "<div class='section-panel-title'><span>🔎 Pencarian Cepat SOP Reject</span><span class='filter-chip-badge'>📘 Panduan & Solusi</span></div>"
                "<div class='section-panel-sub'>Ketik kata kunci kendala untuk menyaring solusi korektif yang sesuai.</div>",
                unsafe_allow_html=True
            )
            search_guide = st.text_input("Cari Kata Kunci Panduan / Solusi:", placeholder="Contoh: tanda tangan, rekening, telepon, brimo, saldo, dormant...", key="guide_search_input")

        df_g = pd.DataFrame(REJECT_GUIDE_ITEMS)
        if search_guide:
            df_g = df_g[
                df_g["Alasan Reject"].str.contains(search_guide, case=False, na=False) |
                df_g["Keterangan"].str.contains(search_guide, case=False, na=False) |
                df_g["Tindakan Korektif / Solusi Sales"].str.contains(search_guide, case=False, na=False)
            ]
        render_metric_card("Jumlah Panduan Tersedia", len(df_g), "SOP Penanganan Reject & Solusi Sales")
        if not df_g.empty:
            render_styled_html_table(df_g, max_rows=100)

    elif halaman_aktif == "🔧 Settings":
        render_page_banner("⚡ AUTOTEAM — Pengaturan Sistem & Database", "Informasi koneksi Google Sheets utama, akses pengelolaan data, dan backup rekap Excel.")
        s_c1, s_c2 = st.columns(2)
        with s_c1: render_metric_card("Versi Aplikasi", "AUTOTEAM v8.6", "Adaptif Light / Dark Mode")
        with s_c2: render_metric_card("Total Data Tersinkron", total_data, "Live via Google Sheets")

        if st.button("🔄 Refresh Data dari Google Sheets Sekarang"):
            st.cache_data.clear()
            st.rerun()

        if is_live:
            st.success(f"Status: Terhubung Sempurna ke Google Sheets Database Utama — {total_data} Data")
        else:
            st.warning("Status: Menggunakan mode cadangan sementara.")

        st.markdown("---")
        st.markdown(f'<a href="{SHEET_EDIT_URL}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:10px 20px; border-radius:8px; font-weight:700; cursor:pointer;">Buka Google Sheets Utama</button></a>', unsafe_allow_html=True)

        st.markdown("---")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_tracking.to_excel(writer, sheet_name='Tracking_Backup', index=False)
        st.download_button(
            label="Download Rekap Data Tracking (.xlsx)",
            data=output.getvalue(),
            file_name="Backup_AUTOTEAM_Makassar.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == '__main__':
    main()
