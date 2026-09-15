from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import run_model_tool_loop
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
RUNS_DIR = ROOT / "runs"

load_lab_env(ROOT)

st.set_page_config(
    page_title="IT Helpdesk AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Modern Custom CSS with Tidio/Lyro Inspired Theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        --bg-main: #f4f6fa;
        --bg-gradient: linear-gradient(180deg, #eef3fc 0%, #f4f6fa 40%, #e9effd 100%);
        --primary-blue: #0066ff;
        --primary-dark: #0046b8;
        --header-gradient: linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%);
        --user-bubble: linear-gradient(135deg, #0066ff 0%, #004bd6 100%);
        --bot-bubble: #ffffff;
        --card-border: rgba(226, 232, 240, 0.8);
        --text-dark: #1e293b;
        --text-muted: #64748b;
        --shadow-sm: 0 4px 12px rgba(0, 82, 212, 0.05);
        --shadow-md: 0 10px 30px -5px rgba(0, 82, 212, 0.12);
        --shadow-lg: 0 20px 40px -10px rgba(0, 82, 212, 0.22);
    }

    /* Global reset & background fix */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, .stApp {
        font-family: var(--font-family) !important;
        background: #eef3fc !important;
        background-color: #eef3fc !important;
        color: var(--text-dark) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1120px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }

    /* Hero Banner Header - Tidio / Lyro Theme */
    .hero-banner {
        position: relative;
        background: var(--header-gradient);
        border-radius: 28px 28px 0 0;
        padding: 2.2rem 2.5rem 2.8rem 2.5rem;
        color: white;
        box-shadow: var(--shadow-lg);
        overflow: hidden;
    }

    .hero-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 2;
    }

    .hero-title-group {
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }

    .bot-avatar-large {
        width: 62px;
        height: 62px;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .hero-text h1 {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 0.4rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .status-dot {
        width: 9px;
        height: 9px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    /* Organic Wave Graphic Divider */
    .hero-wave {
        background: var(--header-gradient);
        margin-bottom: 1.8rem;
        border-radius: 0 0 28px 28px;
        overflow: hidden;
        box-shadow: 0 12px 25px -5px rgba(0, 82, 212, 0.2);
    }

    .hero-wave svg {
        display: block;
        width: 100%;
        height: 38px;
    }

    /* Sidebar Styling - Electric Blue Background with White Text */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #0052D4 0%, #003fa8 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 25px rgba(0, 82, 212, 0.25) !important;
    }

    /* Force all text in sidebar to be WHITE */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stCaption {
        color: #ffffff !important;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.14) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 16px;
        padding: 1.1rem;
        margin-bottom: 1.2rem;
    }

    .sidebar-card-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff !important;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Sidebar Selectbox & Input Controls */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #003fa8 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] div[role="listbox"] * {
        color: #003fa8 !important;
    }

    [data-testid="stSidebar"] code {
        background-color: rgba(0, 0, 0, 0.25) !important;
        color: #7dd3fc !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }

    /* Modern Chat Message Customization */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 0.75rem 0 !important;
    }

    /* User Message Bubble */
    .user-bubble-wrapper {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }

    .user-bubble {
        background: var(--user-bubble);
        color: #ffffff !important;
        border-radius: 22px 22px 4px 22px;
        padding: 0.95rem 1.3rem;
        max-width: 82%;
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.25);
        font-size: 0.98rem;
        line-height: 1.55;
        font-weight: 500;
    }

    /* Bot Message Bubble */
    .bot-bubble-wrapper {
        display: flex;
        gap: 0.9rem;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .bot-avatar-small {
        width: 42px;
        height: 42px;
        min-width: 42px;
        background: var(--header-gradient);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        box-shadow: 0 4px 12px rgba(0, 82, 212, 0.25);
    }

    .bot-bubble {
        background: #ffffff;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-radius: 4px 22px 22px 22px;
        padding: 1.1rem 1.35rem;
        max-width: 85%;
        box-shadow: var(--shadow-sm);
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .bot-bubble p {
        margin-bottom: 0.5rem;
    }
    .bot-bubble p:last-child {
        margin-bottom: 0;
    }

    /* Quick Suggestion Chips */
    .quick-chips-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
    }

    .stButton > button {
        border-radius: 24px !important;
        border: 1.5px solid rgba(0, 102, 255, 0.3) !important;
        background: #ffffff !important;
        color: #0052D4 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.22s ease-in-out !important;
        box-shadow: 0 2px 6px rgba(0, 82, 212, 0.05) !important;
    }

    .stButton > button:hover {
        background: var(--header-gradient) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(0, 82, 212, 0.25) !important;
    }

    /* Tool Trace Accordion & Card Styling */
    .tool-trace-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0066ff;
        border-radius: 14px;
        padding: 1rem;
        margin-top: 0.8rem;
        box-shadow: var(--shadow-sm);
    }

    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #eff6ff;
        color: #0066ff;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.82rem;
        font-family: monospace;
    }

    .metric-badge {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 0.5rem 0.8rem;
        font-size: 0.82rem;
        color: #475569;
    }

    /* Fix Selectbox Popover Dropdown Dark Background */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[role="listbox"],
    div[role="listbox"] *,
    ul[data-baseweb="menu"],
    ul[data-baseweb="menu"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    div[data-baseweb="popover"] li[role="option"]:hover,
    div[role="listbox"] [aria-selected="true"] {
        background-color: #eff6ff !important;
        color: #0066ff !important;
    }

    /* Fix Streamlit Bottom Container & Chat Input Dark Elements */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    footer {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Input Field Customization */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] *,
    [data-baseweb="base-input"],
    [data-baseweb="base-input"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    [data-testid="stChatInput"] {
        border-radius: 28px !important;
        border: 2px solid #cbd5e1 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
        padding: 0.4rem 0.6rem !important;
        transition: border-color 0.2s ease !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #0066ff !important;
        box-shadow: 0 10px 30px rgba(0, 102, 255, 0.18) !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "transcript" not in st.session_state:
        st.session_state.transcript = {
            "version": "v1",
            "provider": "openrouter",
            "model": "",
            "turns": [],
        }
    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = None


init_session_state()


def load_tools() -> list[dict]:
    return to_openai_tools(load_tool_declarations(TOOLS_PATH))


def render_tool_events(tool_events: list[dict]) -> None:
    if not tool_events:
        return

    st.markdown("#### ⚙️ Nhật ký Thực thi Tool (Tool Trace)")
    for idx, event in enumerate(tool_events, start=1):
        tool_name = event.get("tool", "unknown_tool")
        status = "❌ Thất bại" if "error" in event.get("result", {}) else "✅ Thành công"
        with st.expander(f"🔹 #{idx} Call: `{tool_name}` — {status}", expanded=False):
            st.markdown("**📌 Đầu vào (Input JSON):**")
            st.json(event.get("args", {}))
            st.markdown("**📤 Kết quả / Đầu ra (Output):**")
            st.json(event.get("result", {}))


def render_chat_history() -> None:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.markdown(
                f"""
                <div class="user-bubble-wrapper">
                    <div class="user-bubble">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="bot-bubble-wrapper">
                    <div class="bot-avatar-small">🤖</div>
                    <div class="bot-bubble">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if msg.get("tool_events"):
                render_tool_events(msg["tool_events"])


# Sidebar Layout
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/headset.png", width=64)
    st.title("IT Helpdesk Settings")
    st.caption("Cấu hình Model & Trạng thái Hệ thống")

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card-title">🌐 Provider & LLM</div>', unsafe_allow_html=True)
    provider_name = st.selectbox("Chọn Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
    version_value = st.text_input("Phiên bản App", value=st.session_state.transcript.get("version", "v1"))
    st.session_state.transcript["version"] = version_value
    st.markdown('</div>', unsafe_allow_html=True)

    artifact_ver = build_artifact_version(version_value, SYSTEM_PROMPT_PATH, TOOLS_PATH)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card-title">🛡️ Phiên bản Artifact</div>', unsafe_allow_html=True)
    st.markdown(f"**Artifact Version:** `{artifact_ver.artifact_version}`")
    st.markdown(f"**Prompt Hash:** `{artifact_ver.prompt_hash[:12]}`")
    st.markdown(f"**Tools Hash:** `{artifact_ver.tools_hash[:12]}`")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ Xóa Lịch sử Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.transcript["turns"] = []
        st.rerun()


# Main Hero Header (Tidio/Lyro Inspired)
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-title-group">
                <div class="bot-avatar-large">🤖</div>
                <div class="hero-text">
                    <h1>Chat với IT Helpdesk AI</h1>
                    <div class="hero-status-pill">
                        <span class="status-dot"></span>
                        Trực tuyến • Sẵn sàng hỗ trợ 24/7
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="hero-wave">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0,32L48,42.7C96,53,192,75,288,80C384,85,480,75,576,64C672,53,768,43,864,48C960,53,1056,75,1152,80C1248,85,1344,75,1392,69.3L1440,64L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z" fill="#ffffff" fill-opacity="0.25"></path>
            <path d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,53.3C672,53,768,75,864,80C960,85,1056,75,1152,69.3C1248,64,1344,64,1392,64L1440,64L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z" fill="#f4f6fa"></path>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

# Render Chat History
render_chat_history()

# Quick Action Suggestion Chips
if not st.session_state.messages:
    st.markdown('<div class="quick-chips-title">💡 Gợi ý câu hỏi nhanh:</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔍 Kiểm tra thiết bị MB001"):
            st.session_state.quick_prompt = "Kiểm tra thông tin và trạng thái của thiết bị MB001"
            st.rerun()
    with c2:
        if st.button("🎟️ Tạo Ticket IT Khẩn"):
            st.session_state.quick_prompt = "Hãy tạo một ticket hỗ trợ khẩn cấp về sự cố mạng công ty"
            st.rerun()
    with c3:
        if st.button("📋 Quy định cấp Macbook"):
            st.session_state.quick_prompt = "Quy định và chính sách cấp phát Macbook của công ty thế nào?"
            st.rerun()
    with c4:
        if st.button("🔐 Đổi mật khẩu email"):
            st.session_state.quick_prompt = "Hướng dẫn các bước để khôi phục và đổi mật khẩu email công ty"
            st.rerun()

# Handle Prompt Input
user_input = st.chat_input("Nhập yêu cầu hỗ trợ IT của bạn tại đây...")

# Check if quick prompt was clicked
if st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
else:
    prompt = user_input

if prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render new user message immediately
    st.markdown(
        f"""
        <div class="user-bubble-wrapper">
            <div class="user-bubble">
                {prompt}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    provider = make_provider(provider_name)
    model_name = getattr(provider, "default_model", None)
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    history = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        if msg["role"] in {"user", "assistant"}:
            history.append({"role": msg["role"], "content": msg["content"]})

    with st.spinner("🤖 Agent đang suy nghĩ và thực thi các công cụ IT..."):
        result = run_model_tool_loop(
            provider=provider,
            messages=history,
            tools=load_tools(),
            model=model_name,
            max_tool_rounds=4,
        )

    answer = result.get("assistant_text", "")
    tool_events = result.get("tool_events", [])

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tool_events": tool_events,
    })

    st.session_state.transcript["provider"] = provider_name
    st.session_state.transcript["model"] = model_name or ""
    st.session_state.transcript["turns"].append(
        {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "version": version_value,
            "provider": provider_name,
            "model": model_name,
            "user": prompt,
            "assistant": answer,
            "tool_events": tool_events,
        }
    )

    # Save transcript file
    RUNS_DIR.mkdir(exist_ok=True)
    transcript_path = RUNS_DIR / f"{version_value}_{datetime.now().strftime('%Y%m%dT%H%M%S')}.json"
    transcript_path.write_text(str(st.session_state.transcript).replace("'", '"'), encoding="utf-8")

    st.rerun()

# Summary & Transcript Accordion at bottom
if st.session_state.messages:
    st.markdown("---")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.expander("📊 Chi tiết Phiên bản (Version Metadata)"):
            st.json(
                {
                    "version": version_value,
                    "provider": provider_name,
                    "model": getattr(make_provider(provider_name), "default_model", "unknown"),
                    "artifact_version": artifact_ver.artifact_version,
                }
            )

    with col_b:
        with st.expander("📑 Tóm tắt Bằng chứng (Transcript Summary)"):
            st.json(st.session_state.transcript)
