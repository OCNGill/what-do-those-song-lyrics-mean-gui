"""Song lyric explainer Streamlit app following 7D Agile guardrails."""
from __future__ import annotations

import logging
import os
from textwrap import dedent

import streamlit as st
from openai import OpenAI

APP_NAME = "Song Lyric Explainer"
MODEL_NAME = "gpt-4o-mini"
PHASES = [
    ("DEFINE", "Capture the user intent"),
    ("DESIGN", "Frame an explainable prompt"),
    ("DEVELOP", "Call the LLM cleanly"),
    ("DEBUG", "Expose rich error messages"),
    ("DOCUMENT", "Log insights for the storyteller"),
    ("DELIVER", "Render friendly UI copy"),
    ("DEPLOY", "Keep config ready for future LLMs"),
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@st.cache_resource(show_spinner=False)
def _build_openai_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def get_client(api_key: str) -> OpenAI | None:
    if not api_key:
        return None
    try:
        return _build_openai_client(api_key)
    except Exception as exc:  # pragma: no cover - defensive
        logging.exception("Unable to initialize OpenAI client")
        st.error("Could not initialize OpenAI client. Check the key and try again.")
        st.caption(f"Details: {exc}")
        return None


def explain_lyrics(client: OpenAI, lyrics: str) -> str:
    system_msg = dedent(
        """
        You are a Grammy-winning musicologist who explains song lyrics with empathy,
        cultural context, and literary analysis. Provide: (1) a concise synopsis,
        (2) two thematic insights, and (3) one question for class discussion.
        Keep it under 200 words and avoid speculation beyond the provided lyrics.
        """
    ).strip()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.4,
        max_tokens=500,
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": f"Please explain the following lyrics:\n\n{lyrics.strip()}",
            },
        ],
    )
    return response.choices[0].message.content.strip()


def render_sidebar() -> str:
    with st.sidebar:
        st.header("How to use")
        st.markdown(
            """
            1. Enter your OpenAI API key below.
            2. Paste any verse or chorus into the main panel.
            3. Click **Explain lyrics** and review the insights.
            """
        )
        st.divider()
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your API key is never stored. It's only used for this session."
        )
        st.divider()
        st.subheader("Need lyrics?")
        st.link_button("🎵 Find Lyrics", "https://www.lyrics.com/", use_container_width=True)
        st.divider()
        st.image("Gillsystems_logo_with_donation_qrcodes.png", use_container_width=True)
        return api_key


def main() -> None:
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🎧",
        layout="centered",
    )
    api_key = render_sidebar()

    st.title(f"{APP_NAME} · 7D Edition")
    st.write(
        "Give your class a lively breakdown of what those lyrics really mean."
    )

    lyrics = st.text_area(
        "Paste lyrics",
        height=240,
        placeholder="Enter a verse, chorus, or full song...",
    )
    
    if st.button("Explain lyrics", type="primary"):
        if not lyrics.strip():
            st.warning("Please add some lyrics before requesting an explanation.")
            return
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
            return
        client = get_client(api_key)
        if client is None:
            st.stop()
        with st.spinner("Composing your explainer..."):
            try:
                explanation = explain_lyrics(client, lyrics)
                st.success("Here is your story-ready explainer.")
                st.markdown(explanation)
                logging.info("Explanation generated successfully")
            except Exception as exc:  # pragma: no cover - defensive
                st.error("We hit a snag while talking to OpenAI.")
                st.caption(f"Details: {exc}")
                logging.exception("OpenAI request failed")


if __name__ == "__main__":
    main()
