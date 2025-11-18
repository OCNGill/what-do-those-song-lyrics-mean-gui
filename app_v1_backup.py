"""
What Do Those Song Lyrics Mean? - Streamlit App
Uses Groq (free cloud LLM) OR local CPU model (no API key needed) 
and YouTube scraping to find and interpret song lyrics.
Following 7D Agile: Discover, Define, Design, Develop, Debug, Deploy, Drive.
"""
from __future__ import annotations

import logging
import os
from textwrap import dedent
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from scraper import get_lyrics_from_input

# Load environment variables
load_dotenv()

APP_NAME = "What Do Those Song Lyrics Mean?"
GROQ_MODEL_NAME = "llama-3.1-70b-versatile"
LOCAL_MODEL_NAME = "google/flan-t5-small"  # ~80MB, CPU-friendly

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@st.cache_resource(show_spinner=False)
def get_groq_client(api_key: Optional[str]):
    """Initialize Groq client with API key."""
    if not api_key:
        return None
    from groq import Groq
    return Groq(api_key=api_key)


@st.cache_resource(show_spinner=False)
def get_local_model():
    """
    Initialize local Hugging Face model for CPU inference.
    Uses google/flan-t5-small (~80MB) for minimal resource usage.
    """
    try:
        from transformers import pipeline
        logging.info(f"Loading local model: {LOCAL_MODEL_NAME}")
        model = pipeline(
            "text2text-generation",
            model=LOCAL_MODEL_NAME,
            device=-1,  # CPU only
            max_length=512,
        )
        logging.info("Local model loaded successfully")
        return model
    except Exception as e:
        logging.error(f"Failed to load local model: {e}")
        return None


def interpret_lyrics_groq(client, lyrics: str) -> str:
    """
    Send lyrics to Groq cloud LLM for interpretation.
    
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
            model=GROQ_MODEL_NAME,
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


def interpret_lyrics_local(model, lyrics: str) -> str:
    """
    Use local Hugging Face model for interpretation (CPU-only, no API key).
    
    Args:
        model: HF pipeline model
        lyrics: Song lyrics text
        
    Returns:
        AI-generated interpretation
    """
    prompt = dedent(
        f"""
        Analyze these song lyrics and explain:
        1. The main theme
        2. Key symbolic meanings
        3. The emotional message
        
        Lyrics:
        {lyrics[:1500]}
        
        Interpretation:
        """
    ).strip()
    
    try:
        result = model(prompt, max_length=300, do_sample=False)
        interpretation = result[0]['generated_text'].strip()
        
        # Clean up the output if it includes the prompt
        if "Interpretation:" in interpretation:
            interpretation = interpretation.split("Interpretation:")[-1].strip()
        
        return interpretation if interpretation else "Unable to generate interpretation."
    except Exception as e:
        logging.error(f"Local model error: {e}")
        return f"Error generating interpretation: {str(e)}"


def render_sidebar() -> tuple[Optional[str], bool]:
    """Render sidebar with API key input and mode selection."""
    with st.sidebar:
        st.header("🎵 How to Use")
        
        # Mode selection
        use_local = st.checkbox(
            "🖥️ Use Local CPU Model (no API key needed)",
            value=not bool(os.getenv("GROQ_API_KEY", "")),
            help="Run interpretation locally on your CPU. First run downloads ~80MB model."
        )
        
        if not use_local:
            st.markdown(
                """
                **Optional: Use Cloud (Groq) for Better Quality**
                - Visit [console.groq.com](https://console.groq.com)
                - Sign up (free tier)
                - Copy your API key below
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
        else:
            api_key = None
            st.info("💻 Running in local mode - no API key needed!")
        
        st.divider()
        st.caption("💡 **Examples:**")
        st.code("Radiohead - Karma Police", language=None)
        st.code("https://youtu.be/dQw4w9WgXcQ", language=None)
        
        st.divider()
        st.image("Gillsystems_logo_with_donation_qrcodes.png", use_container_width=True)
        
        return api_key, use_local


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🎧",
        layout="centered",
    )
    
    api_key, use_local = render_sidebar()

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
        
        # Check mode and requirements
        if not use_local and not api_key:
            st.error("❌ Please enter your Groq API key in the sidebar OR enable local mode.")
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
        
        # Step 2: Interpret with chosen method
        if use_local:
            # Local CPU model
            with st.spinner("🤖 Loading local model (first run may take a moment)..."):
                local_model = get_local_model()
                
            if not local_model:
                st.error("❌ Failed to load local model. Check logs or try Groq mode.")
                return
            
            with st.spinner("💻 Generating interpretation locally..."):
                try:
                    interpretation = interpret_lyrics_local(local_model, lyrics)
                    
                    st.success("✅ Interpretation Complete! (Local CPU)")
                    st.markdown("### 🎭 What Do These Lyrics Mean?")
                    st.markdown(interpretation)
                    
                    logging.info(f"Successfully interpreted lyrics locally for: {user_input}")
                    
                except Exception as exc:
                    st.error("❌ Error with local model.")
                    st.caption(f"Details: {exc}")
                    logging.exception("Local model failed")
        else:
            # Groq cloud API
            with st.spinner("🤖 Generating interpretation with Groq AI..."):
                try:
                    client = get_groq_client(api_key)
                    interpretation = interpret_lyrics_groq(client, lyrics)
                    
                    st.success("✅ Interpretation Complete! (Groq Cloud)")
                    st.markdown("### 🎭 What Do These Lyrics Mean?")
                    st.markdown(interpretation)
                    
                    logging.info(f"Successfully interpreted lyrics for: {user_input}")
                    
                except Exception as exc:
                    st.error("❌ Error communicating with Groq API.")
                    st.caption(f"Details: {exc}")
                    logging.exception("Groq API request failed")
                logging.exception("Groq API request failed")


if __name__ == "__main__":
    main()
