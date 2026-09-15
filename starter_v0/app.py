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


init_session_state()


def load_tools() -> list[dict]:
    return to_openai_tools(load_tool_declarations(TOOLS_PATH))


def render_tool_events(tool_events: list[dict]) -> None:
    if not tool_events:
        return

    st.subheader("Tool trace")
    for idx, event in enumerate(tool_events, start=1):
        tool_name = event.get("tool", "unknown_tool")
        with st.expander(f"#{idx} {tool_name}", expanded=True):
            st.markdown("**Input JSON**")
            st.json(event.get("args", {}))
            st.markdown("**Output / Error**")
            st.json(event.get("result", {}))


def render_history() -> None:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("tool_events"):
                render_tool_events(msg["tool_events"])


st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🛠️", layout="wide")

with st.sidebar:
    st.header("Run config")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
    version_value = st.text_input("Version", value=st.session_state.transcript["version"])
    st.session_state.transcript["version"] = version_value

    artifact_ver = build_artifact_version(version_value, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    st.caption(f"Artifact version: {artifact_ver.artifact_version}")
    st.caption(f"Prompt hash: {artifact_ver.prompt_hash[:12]}")
    st.caption(f"Tools hash: {artifact_ver.tools_hash[:12]}")

st.title("IT Helpdesk Agent")
st.caption("Chat UI with tool trace, version metadata, and transcript evidence")

render_history()

prompt = st.chat_input("Nhập yêu cầu hỗ trợ IT...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    provider = make_provider(provider_name)
    model_name = getattr(provider, "default_model", None)
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    history = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        if msg["role"] in {"user", "assistant"}:
            history.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy nghĩ và gọi tool..."):
            result = run_model_tool_loop(
                provider=provider,
                messages=history,
                tools=load_tools(),
                model=model_name,
                max_tool_rounds=4,
            )

        answer = result.get("assistant_text", "")
        tool_events = result.get("tool_events", [])
        st.markdown(answer)
        render_tool_events(tool_events)

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

    st.subheader("Version")
    st.json({
        "version": version_value,
        "provider": provider_name,
        "model": model_name,
        "artifact_version": artifact_ver.artifact_version,
    })

    st.subheader("Transcript")
    st.json(st.session_state.transcript)

    RUNS_DIR.mkdir(exist_ok=True)
    transcript_path = RUNS_DIR / f"{version_value}_{datetime.now().strftime('%Y%m%dT%H%M%S')}.json"
    transcript_path.write_text(str(st.session_state.transcript).replace("'", '"'), encoding="utf-8")

    st.caption(f"Saved transcript: {transcript_path.name}")
