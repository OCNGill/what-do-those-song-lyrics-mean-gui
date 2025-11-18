"""
What Do Those Song Lyrics Mean? - Streamlit App
Uses Groq (free LLM) and YouTube scraping to find and interpret song lyrics.
Following 7D Agile: Discover, Define, Design, Develop, Debug, Deploy, Drive.
"""
from __future__ import annotations

import logging
import os
from textwrap import dedent

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from scraper import get_lyrics_from_input

# Load environment variables
load_dotenv()

APP_NAME = "What Do Those Song Lyrics Mean?"
MODEL_NAME = "llama-3.1-70b-versatile"  # Groq's free model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@st.cache_resource(show_spinner=False)
def get_groq_client(api_key: str) -> Groq:
    """Initialize Groq client with API key."""
    return Groq(api_key=api_key)


def interpret_lyrics(client: Groq, lyrics: str) -> str:
    """
    Send lyrics to Groq LLM for interpretation.
    
    Args:
        client: Groq API client
        lyrics: Song lyrics text
        
    Returns:
        AI-generated interpretation
    """
    system_msg = dedent(
        """
        You are a knowledgeable music analyst who explains song lyrics with depth,
        cultural context, and empathy. Provide:
        1. A brief synopsis of the song's theme
        2. Key symbolic or metaphorical meanings
        3. The emotional or social message conveyed
        
        Keep your response clear, insightful, and under 300 words.
        """
    ).strip()
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.5,
            max_tokens=600,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Please interpret these song lyrics:\n\n{lyrics[:4000]}"},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Groq API error: {e}")
        raise


def render_sidebar() -> str:
    """Render sidebar with API key input and instructions."""
    with st.sidebar:
        st.header("🎵 How to Use")
        st.markdown(
            """
            **Step 1:** Get your free Groq API key:
            - Visit [console.groq.com](https://console.groq.com)
            - Sign up (free)
            - Copy your API key
            
            **Step 2:** Enter song info:
            - Paste YouTube/YouTube Music URL, OR
            - Type "Artist - Song Name"
            
            **Step 3:** Click "Get Lyrics & Interpret"
            """
        )
        st.divider()
        
        # Check for API key in environment or session state
        default_key = os.getenv("GROQ_API_KEY", "")
        if "groq_api_key" in st.session_state:
            default_key = st.session_state.groq_api_key
        
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=default_key,
            placeholder="gsk_...",
            help="Free API key from console.groq.com"
        )
        
        # Store in session state
        if api_key:
            st.session_state.groq_api_key = api_key
        
        st.divider()
        st.caption("💡 **Examples:**")
        st.code("Radiohead - Karma Police", language=None)
        st.code("https://youtu.be/dQw4w9WgXcQ", language=None)
        
        st.divider()
        st.image("Gillsystems_logo_with_donation_qrcodes.png", use_container_width=True)
        
        return api_key


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🎧",
        layout="centered",
    )
    
    api_key = render_sidebar()

    st.title(APP_NAME)
    st.markdown(
        "🎵 **Find song lyrics from YouTube and get AI-powered interpretations** — no ads, no paywalls!"
    )

    # User input
    user_input = st.text_input(
        "Enter song name or YouTube URL:",
        placeholder="Artist - Song Name  OR  https://youtube.com/watch?v=...",
        help="Examples: 'The Beatles - Let It Be' or paste a YouTube link"
    )
    
    # Main action button
    if st.button("🔍 Get Lyrics & Interpret", type="primary"):
        if not user_input.strip():
            st.warning("⚠️ Please enter a song name or URL.")
            return
        
        if not api_key:
            st.error("❌ Please enter your Groq API key in the sidebar.")
            st.info("Get a free key at: https://console.groq.com")
            return
        
        # Step 1: Scrape lyrics
        with st.spinner("🔎 Searching for lyrics..."):
            lyrics, status = get_lyrics_from_input(user_input)
        
        st.info(status)
        
        if not lyrics:
            st.error("Could not retrieve lyrics. Try a different search or URL.")
            return
        
        # Display lyrics in expandable section
        with st.expander("📜 View Lyrics", expanded=True):
            st.text_area(
                "Extracted Lyrics:",
                value=lyrics,
                height=300,
                disabled=True
            )
        
        # Step 2: Interpret with Groq
        with st.spinner("🤖 Generating interpretation with Groq AI..."):
            try:
                client = get_groq_client(api_key)
                interpretation = interpret_lyrics(client, lyrics)
                
                st.success("✅ Interpretation Complete!")
                st.markdown("### 🎭 What Do These Lyrics Mean?")
                st.markdown(interpretation)
                
                logging.info(f"Successfully interpreted lyrics for: {user_input}")
                
            except Exception as exc:
                st.error("❌ Error communicating with Groq API.")
                st.caption(f"Details: {exc}")
                logging.exception("Groq API request failed")


if __name__ == "__main__":
    main()
