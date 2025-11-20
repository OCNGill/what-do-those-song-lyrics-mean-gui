"""
What Do Those Song Lyrics Mean? - Streamlit App v2.0
Now with: Hardware detection, model selection, manual lyrics input, HuggingFace browser
Following 7D Agile: Discover, Define, Design, Develop, Debug, Deploy, Drive.
"""
from __future__ import annotations

import logging
import os
from textwrap import dedent
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from scraper_v2 import get_lyrics_from_input
from hardware import detect_hardware, get_compatible_models, get_recommended_model, HardwareSpecs

# Load environment variables
load_dotenv()

APP_NAME = "What Do Those Song Lyrics Mean? v2.0"
GROQ_MODEL_NAME = "llama-3.1-70b-versatile"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Initialize session state
if "hardware" not in st.session_state:
    st.session_state.hardware = None
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = None


@st.cache_resource(show_spinner=False)
def get_groq_client(api_key: Optional[str]):
    """Initialize Groq client with API key."""
    if not api_key:
        return None
    from groq import Groq
    return Groq(api_key=api_key)


@st.cache_resource(show_spinner=False)
def load_hf_model(model_id: str, use_gpu: bool = False):
    """
    Load a Hugging Face model for inference.
    
    Args:
        model_id: HuggingFace model ID
        use_gpu: Whether to use GPU if available
        
    Returns:
        Pipeline object or None
    """
    try:
        from transformers import pipeline
        import torch
        
        device = -1  # CPU default
        if use_gpu:
            if torch.cuda.is_available():
                device = 0
                logging.info(f"Loading {model_id} on CUDA GPU")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = "mps"
                logging.info(f"Loading {model_id} on Apple Silicon GPU")
        
        if device == -1:
            logging.info(f"Loading {model_id} on CPU")
        
        model = pipeline(
            "text2text-generation",
            model=model_id,
            device=device,
            max_length=512,
        )
        logging.info(f"Model {model_id} loaded successfully")
        return model
    except Exception as e:
        logging.error(f"Failed to load model {model_id}: {e}")
        st.error(f"Failed to load model: {e}")
        return None


def interpret_lyrics_groq(client, lyrics: str) -> str:
    """Send lyrics to Groq cloud LLM for interpretation."""
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
    """Use local Hugging Face model for interpretation."""
    prompt = dedent(
        f"""
        Analyze these song lyrics and explain:
        1. The main theme
        2. Key symbolic meanings
        3. The emotional message
        
        Lyrics:
        {lyrics[:1500]}
        
        Analysis:
        """
    ).strip()
    
    try:
        result = model(prompt, max_length=512, do_sample=False)
        return result[0]["generated_text"]
    except Exception as e:
        logging.error(f"Local inference error: {e}")
        return "Error generating interpretation locally."


def answer_question_groq(client, lyrics: str, question: str) -> str:
    """Answer a question about the lyrics using Groq."""
    system_msg = dedent(
        """
        You are a knowledgeable music analyst. Answer the user's question about the song lyrics provided.
        Use the lyrics as your primary source. Be concise and helpful.
        """
    ).strip()
    
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            temperature=0.5,
            max_tokens=400,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Lyrics:\n{lyrics[:4000]}\n\nQuestion: {question}"},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Groq API error: {e}")
        raise


def answer_question_local(model, lyrics: str, question: str) -> str:
    """Answer a question about the lyrics using local model."""
    prompt = dedent(
        f"""
        Lyrics:
        {lyrics[:1500]}
        
        Question: {question}
        
        Answer:
        """
    ).strip()
    
    try:
        result = model(prompt, max_length=512, do_sample=False)
        return result[0]["generated_text"]
    except Exception as e:
        logging.error(f"Local inference error: {e}")
        return "Error generating answer locally."


def render_sidebar() -> tuple[Optional[str], str, bool]:
    """Render sidebar with mode selection and settings."""
    with st.sidebar:
        st.header("🔧 Settings")
        
        # Hardware detection
        if st.button("🖥️ Detect Hardware", use_container_width=True):
            with st.spinner("Detecting hardware..."):
                st.session_state.hardware = detect_hardware()
        
        if st.session_state.hardware:
            with st.expander("💻 Hardware Info", expanded=False):
                st.code(str(st.session_state.hardware), language=None)
        
        st.divider()
        
        # Mode selection
        mode = st.radio(
            "Interpretation Mode:",
            ["Local Model (CPU/GPU)", "Cloud (Groq API)"],
            help="Local runs on your machine, Cloud uses Groq's free API"
        )
        
        use_cloud = (mode == "Cloud (Groq API)")
        
        if use_cloud:
            st.info("☁️ Using Groq cloud API")
            default_key = os.getenv("GROQ_API_KEY", "")
            if "groq_api_key" in st.session_state:
                default_key = st.session_state.groq_api_key
            
            api_key = st.text_input(
                "Groq API Key",
                type="password",
                value=default_key,
                placeholder="gsk_...",
                help="Free at console.groq.com"
            )
            
            if api_key:
                st.session_state.groq_api_key = api_key
        else:
            api_key = None
            st.info("💻 Using local model")
            
            # Model selection for local mode
            if not st.session_state.hardware:
                st.warning("⚠️ Click 'Detect Hardware' above to see compatible models")
                compatible_models = []
            else:
                compatible_models = get_compatible_models(st.session_state.hardware)
                recommended = get_recommended_model(st.session_state.hardware)
                
                st.success(f"✓ Recommended: {recommended.model_name}")
            
            # Model selector
            if compatible_models:
                model_options = {
                    f"{m.model_name} ({m.size_mb}MB)": m.model_id 
                    for m in compatible_models
                }
                
                selected_display = st.selectbox(
                    "Select Model:",
                    options=list(model_options.keys()),
                    help="Models filtered by your hardware"
                )
                
                selected_model_id = model_options[selected_display]
                st.session_state.selected_model = selected_model_id
                
                # Show model details
                selected_info = next(m for m in compatible_models if m.model_id == selected_model_id)
                with st.expander("📊 Model Details"):
                    st.write(f"**ID:** `{selected_info.model_id}`")
                    st.write(f"**Size:** {selected_info.size_mb}MB")
                    st.write(f"**Min RAM:** {selected_info.min_ram_gb}GB")
                    st.write(f"**GPU Required:** {'Yes' if selected_info.requires_gpu else 'No'}")
                    st.write(f"**Description:** {selected_info.description}")
                
                # GPU toggle if available
                if st.session_state.hardware.has_cuda or st.session_state.hardware.has_mps:
                    use_gpu = st.checkbox("Use GPU acceleration", value=True)
                else:
                    use_gpu = False
            else:
                st.session_state.selected_model = "google/flan-t5-small"
                use_gpu = False
            
            # HuggingFace model browser
            if st.button("🤗 Browse More Models on HuggingFace", use_container_width=True):
                st.markdown("[Open HuggingFace Model Hub](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=downloads)")
                st.info("💡 Look for 'text2text-generation' models. Copy the model ID and enter it below.")
            
            custom_model = st.text_input(
                "Custom Model ID (optional):",
                placeholder="e.g., google/flan-t5-base",
                help="Enter any HuggingFace text2text model ID"
            )
            
            if custom_model:
                st.session_state.selected_model = custom_model
                st.warning(f"⚠️ Using custom model: {custom_model}")
        
        st.divider()
        st.caption("💡 **Examples:**")
        st.code("Radiohead - Karma Police", language=None)
        st.code("https://youtu.be/dQw4w9WgXcQ", language=None)
        
        st.divider()
        
        # External Lyrics Links
        st.caption("🔗 **External Lyrics Sites:**")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("AZLyrics", "https://www.azlyrics.com", use_container_width=True)
        with col2:
            st.link_button("Genius", "https://genius.com", use_container_width=True)
            
        st.divider()
        st.image("Gillsystems_logo_with_donation_qrcodes.png", use_container_width=True)
        
        return api_key, mode, use_gpu if not use_cloud else False


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🎧",
        layout="centered",
    )
    
    # Initialize session state for lyrics and interpretation
    if "current_lyrics" not in st.session_state:
        st.session_state.current_lyrics = None
    if "current_interpretation" not in st.session_state:
        st.session_state.current_interpretation = None
    
    api_key, mode, use_gpu = render_sidebar()

    st.title(APP_NAME)
    st.markdown(
        "🎵 **Find song lyrics from YouTube OR paste them manually** — get AI-powered interpretations!"
    )

    # Input mode tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Search/Scrape", "📝 Manual Input", "💬 Q&A"])
    
    with tab1:
        st.subheader("Search for Lyrics")
        user_input = st.text_input(
            "Enter song name or YouTube URL:",
            placeholder="Artist - Song Name  OR  https://youtube.com/watch?v=...",
            help="Examples: 'The Beatles - Let It Be' or paste a YouTube link",
            key="search_input"
        )
        scrape_button = st.button("🔍 Get Lyrics & Interpret", type="primary", key="scrape_btn")
    
    with tab2:
        st.subheader("Paste Lyrics Manually")
        manual_lyrics = st.text_area(
            "Paste song lyrics here:",
            height=300,
            placeholder="Enter a verse, chorus, or full song...",
            help="Paste any lyrics you want to analyze",
            key="manual_input"
        )
        manual_button = st.button("🎭 Interpret These Lyrics", type="primary", key="manual_btn")
    
    # Process inputs
    process_interpretation = False
    
    if scrape_button and user_input.strip():
        with st.spinner("🔎 Searching for lyrics..."):
            lyrics, status = get_lyrics_from_input(user_input)
        st.info(status)
        
        if lyrics:
            st.session_state.current_lyrics = lyrics
            st.session_state.current_interpretation = None # Reset interpretation
            process_interpretation = True
        else:
            st.error("Could not retrieve lyrics. Try a different search or URL, or use Manual Input tab.")
    
    elif manual_button and manual_lyrics.strip():
        st.session_state.current_lyrics = manual_lyrics.strip()
        st.session_state.current_interpretation = None
        st.success("✓ Using your manually entered lyrics")
        process_interpretation = True
    
    # Display lyrics if available
    if st.session_state.current_lyrics:
        with st.expander("📜 View Lyrics", expanded=True):
            st.text_area(
                "Lyrics:",
                value=st.session_state.current_lyrics,
                height=250,
                disabled=True,
                key="lyrics_display"
            )
            
        # Interpret if requested
        if process_interpretation:
            if mode == "Cloud (Groq API)":
                if not api_key:
                    st.error("❌ Please enter your Groq API key in the sidebar.")
                    st.info("Get a free key at: https://console.groq.com")
                else:
                    with st.spinner("🤖 Generating interpretation with Groq AI..."):
                        try:
                            client = get_groq_client(api_key)
                            interpretation = interpret_lyrics_groq(client, st.session_state.current_lyrics)
                            st.session_state.current_interpretation = interpretation
                            logging.info("Successfully interpreted with Groq")
                        except Exception as exc:
                            st.error("❌ Error communicating with Groq API.")
                            st.caption(f"Details: {exc}")
                            logging.exception("Groq API request failed")
            
            else:  # Local model
                if not st.session_state.selected_model:
                    st.error("❌ Please select a model in the sidebar or detect hardware first.")
                else:
                    model_id = st.session_state.selected_model
                    with st.spinner(f"🤖 Loading model: {model_id} (first run may take time)..."):
                        local_model = load_hf_model(model_id, use_gpu)
                    
                    if local_model:
                        with st.spinner("💻 Generating interpretation..."):
                            try:
                                interpretation = interpret_lyrics_local(local_model, st.session_state.current_lyrics)
                                st.session_state.current_interpretation = interpretation
                                logging.info(f"Successfully interpreted with {model_id}")
                            except Exception as exc:
                                st.error("❌ Error with local model.")
                                st.caption(f"Details: {exc}")
                                logging.exception("Local model failed")

        # Display interpretation if available
        if st.session_state.current_interpretation:
            st.success("✅ Interpretation Complete!")
            st.markdown("### 🎭 What Do These Lyrics Mean?")
            st.markdown(st.session_state.current_interpretation)

    # Q&A Tab Logic
    with tab3:
        st.subheader("Ask a Question about the Lyrics")
        if not st.session_state.current_lyrics:
            st.info("Please search for or enter lyrics in the other tabs first.")
        else:
            question = st.text_input("Ask a question:", placeholder="e.g., What does the second verse mean?")
            if st.button("Ask Question", type="primary"):
                if not question.strip():
                    st.warning("Please enter a question.")
                else:
                    if mode == "Cloud (Groq API)":
                        if not api_key:
                            st.error("❌ Please enter your Groq API key in the sidebar.")
                        else:
                            with st.spinner("🤖 Asking Groq AI..."):
                                try:
                                    client = get_groq_client(api_key)
                                    answer = answer_question_groq(client, st.session_state.current_lyrics, question)
                                    st.markdown("### 🤖 Answer")
                                    st.markdown(answer)
                                except Exception as exc:
                                    st.error("❌ Error communicating with Groq API.")
                                    st.caption(f"Details: {exc}")
                    else:
                        if not st.session_state.selected_model:
                            st.error("❌ Please select a model in the sidebar.")
                        else:
                            model_id = st.session_state.selected_model
                            with st.spinner(f"🤖 Loading model: {model_id}..."):
                                local_model = load_hf_model(model_id, use_gpu)
                            
                            if local_model:
                                with st.spinner("💻 Generating answer..."):
                                    try:
                                        answer = answer_question_local(local_model, st.session_state.current_lyrics, question)
                                        st.markdown("### 🤖 Answer")
                                        st.markdown(answer)
                                    except Exception as exc:
                                        st.error("❌ Error with local model.")
                                        st.caption(f"Details: {exc}")


if __name__ == "__main__":
    main()
