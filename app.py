import streamlit as st
import os
import glob
import markdown
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_chapter_summaries():
    # Get all Vietnamese chapter summary files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chapter_files = glob.glob(os.path.join(script_dir, "summaries", "viet_summary_chapter_*.md"))
    logger.info(f"Found {len(chapter_files)} chapter files")
    
    chapters = {}
    for file_path in chapter_files:
        # Extract chapter number from filename like "viet_summary_chapter_005_gemini.md"
        filename = os.path.basename(file_path)
        try:
            # Extract the number between "chapter_" and "_gemini"
            chapter_part = filename.split('chapter_')[1].split('_gemini')[0]
            logger.info(f"Extracted chapter part: {chapter_part} from {filename}")
            chapter_num = int(chapter_part)
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            chapters[chapter_num] = content
            logger.info(f"Successfully loaded chapter {chapter_num}, content length: {len(content)}")
        except (IndexError, ValueError) as e:
            logger.error(f"Skipping {filename}: {str(e)}")
            continue
    
    logger.info(f"Total chapters loaded: {len(chapters)}")
    logger.info(f"Chapter numbers available: {sorted(chapters.keys())}")
    return chapters

def main():
    st.set_page_config(
        page_title="The Omnivore's Dilemma",
        page_icon="🌽",
        layout="wide"
    )
    
    st.title("The Omnivore's Dilemma 🌽🐄🍄")
    
    # Load all chapters
    chapters = load_chapter_summaries()
    
    if not chapters:
        st.error("No chapters found. Please check the file path and naming convention.")
        return

    # Initialize session state
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = min(chapters.keys())

    # Handle navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_chapter > min(chapters.keys()):
            if st.button("← Previous Chapter"):
                st.session_state.current_chapter -= 1

    with col2:
        if st.session_state.current_chapter < max(chapters.keys()):
            if st.button("Next Chapter →"):
                st.session_state.current_chapter += 1
    
    # Sidebar for chapter selection
    st.sidebar.title("Chapters")
    selected_chapter = st.sidebar.selectbox(
        "Select a chapter",
        sorted(chapters.keys()),
        index=sorted(chapters.keys()).index(st.session_state.current_chapter),
        format_func=lambda x: f"Chapter {x}"
    )
    
    # Update current chapter when selectbox changes
    st.session_state.current_chapter = selected_chapter
    
    # Always display current chapter content
    current_chapter = st.session_state.current_chapter
    if current_chapter in chapters:
        content = chapters[current_chapter]
        # Add a header if not present
        if not content.strip().startswith('#'):
            if current_chapter == 0:
                content = f"# Introduction\n\n{content}"
            else:
                content = f"# Chapter {current_chapter}\n\n{content}"
        
        # Create container for content
        content_container = st.container()
        with content_container:
            st.markdown(content, unsafe_allow_html=True)
            
        logger.info(f"Displaying chapter {current_chapter} (length: {len(content)})")
    else:
        logger.error(f"Content for Chapter {current_chapter} not found")
        st.error(f"Content for Chapter {current_chapter} not found")

if __name__ == "__main__":
    main() 