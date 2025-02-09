import streamlit as st
import os
import glob
import markdown

def load_chapter_summaries():
    # Get all Vietnamese chapter summary files
    chapter_files = glob.glob("summaries/viet_summary_chapter_*.md")
    
    chapters = {}
    for file_path in chapter_files:
        # Extract chapter number from filename like "viet_summary_chapter_005_gemini.md"
        filename = os.path.basename(file_path)
        try:
            # Extract the number between "chapter_" and "_gemini"
            chapter_num = int(filename.split('chapter_')[1].split('_gemini')[0])
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            chapters[chapter_num] = content
        except (IndexError, ValueError) as e:
            print(f"Skipping {filename}: {str(e)}")
            continue
    
    return chapters

def main():
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
    
    # Display selected chapter
    if selected_chapter:
        st.markdown(chapters[selected_chapter], unsafe_allow_html=True)

if __name__ == "__main__":
    main() 