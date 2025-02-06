import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import time
import os

# ========== 1️⃣ Configuration and Setup ==========
def initialize_gemini():
    # Replace with your actual Gemini API key
    api_key = "AIzaSyA2Zvx2IIPYsfyVla89W3eftlWXUKoT0j4"
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")

def initialize_app():
    st.set_page_config(
        page_title="AI Screenplay Co-Writer Pro",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
        }
        .success-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #D4EDDA;
            color: #155724;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #E7F3FE;
            border-left: 5px solid #2196F3;
            padding: 1rem;
            margin: 1rem 0;
        }
        .feature-header {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

# ========== 2️⃣ Session State Management ==========
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    if 'model' not in st.session_state:
        st.session_state.model = initialize_gemini()

# ========== 3️⃣ AI Generation Functions ==========
def generate_with_error_handling(prompt, generation_type):
    try:
        with st.spinner(f'Generating {generation_type}... 🤔'):
            response = st.session_state.model.generate_content(prompt)
            content = response.text.strip()
            
            # Save to history
            st.session_state.history.append({
                'type': generation_type,
                'content': content,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return content
    except Exception as e:
        st.error(f"Error generating {generation_type}: {str(e)}")
        return None

def generate_screenplay_outline(genre, theme, protagonist, tone, length):
    prompt = f"""
    As an expert screenwriter, create a detailed {length} screenplay outline.
    Genre: {genre}
    Theme: {theme}
    Protagonist: {protagonist}
    Tone: {tone}
    
    Provide a structured outline with:
    1. Act 1 (Setup - 25%)
      - Inciting incident
      - First plot point
    2. Act 2 (Confrontation - 50%)
      - Rising action
      - Midpoint
      - Falling action
    3. Act 3 (Resolution - 25%)
      - Climax
      - Resolution
    
    Include character arcs, emotional journey, and key story beats.
    """
    return generate_with_error_handling(prompt, "Screenplay Outline")

def generate_dialogue(character1, character2, setting, emotion, context):
    prompt = f"""
    Generate natural, cinematic dialogue between two characters.
    Character 1: {character1}
    Character 2: {character2}
    Setting: {setting}
    Emotional Context: {emotion}
    Scene Context: {context}
    
    Format in proper screenplay style:
    - Character names in CAPS
    - Brief action descriptions
    - Natural, revealing dialogue
    - Subtext and character voice
    """
    return generate_with_error_handling(prompt, "Character Dialogue")

def generate_character_profile(name, age, occupation, background, goals):
    prompt = f"""
    Create a detailed character profile for a screenplay.
    Name: {name}
    Age: {age}
    Occupation: {occupation}
    Background: {background}
    Goals/Motivations: {goals}
    
    Include:
    1. Physical description
    2. Psychological profile
    3. Personal history
    4. Relationships
    5. Internal conflicts
    6. Character arc potential
    """
    return generate_with_error_handling(prompt, "Character Profile")

def generate_scene_description(location, time, mood, purpose):
    prompt = f"""
    Write a vivid, cinematic scene description.
    Location: {location}
    Time: {time}
    Mood/Atmosphere: {mood}
    Scene Purpose: {purpose}
    
    Include:
    - Sensory details
    - Visual composition
    - Movement and dynamics
    - Atmospheric elements
    - Story-relevant details
    """
    return generate_with_error_handling(prompt, "Scene Description")

def generate_plot_solutions(problem, context, goals):
    prompt = f"""
    Provide creative solutions for a screenplay's plot challenge.
    Current Problem: {problem}
    Story Context: {context}
    Desired Outcomes: {goals}
    
    Offer three distinct solutions:
    1. Conservative approach
    2. Bold/unexpected direction
    3. Character-focused resolution
    
    For each solution, explain:
    - How it moves the story forward
    - Impact on characters
    - Potential consequences
    """
    return generate_with_error_handling(prompt, "Plot Solutions")

# ========== 4️⃣ UI Components ==========
def render_sidebar():
    with st.sidebar:
        st.header("🎭 Project Navigation")
        
        # Project Management
        st.subheader("Project Settings")
        project_name = st.text_input("Project Name", key="project_name")
        if st.button("Create/Switch Project"):
            st.session_state.current_project = project_name
            st.success(f"Working on project: {project_name}")
        
        st.divider()
        
        # Feature Selection
        st.subheader("Writing Tools")
        return st.radio(
            "Select Tool:",
            ["Story Outline", "Dialogue Generator", "Character Creator",
             "Scene Builder", "Plot Solutions", "Project History"],
            key="selected_feature"
        )

def render_outline_generator():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("📜 Story Outline Generator")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox("Genre", [
            "Drama", "Comedy", "Action", "Sci-Fi", "Horror", "Romance",
            "Thriller", "Fantasy", "Mystery", "Other"
        ])
        theme = st.text_input("Theme", placeholder="e.g., Redemption, Love, Justice")
        protagonist = st.text_area("Protagonist Description", 
                                 placeholder="Describe your main character...")
    
    with col2:
        tone = st.select_slider("Tone", 
                              options=["Dark", "Serious", "Neutral", "Light", "Humorous"])
        length = st.select_slider("Outline Detail",
                                options=["Concise", "Moderate", "Detailed"])
    
    if st.button("Generate Outline", key="generate_outline"):
        outline = generate_screenplay_outline(genre, theme, protagonist, tone, length)
        if outline:
            st.markdown("### 📝 Generated Outline")
            st.markdown(outline)
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save to Project"):
                    if st.session_state.current_project:
                        st.session_state.generated_content[f'outline_{datetime.now().strftime("%Y%m%d_%H%M%S")}'] = outline
                        st.success("Outline saved to current project!")
                    else:
                        st.warning("Please create a project first!")
            
            with col2:
                st.download_button(
                    "Download Outline",
                    outline,
                    file_name=f"screenplay_outline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )

def render_dialogue_generator():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("💬 Dialogue Generator")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        char1 = st.text_input("Character 1 Name & Description")
        char2 = st.text_input("Character 2 Name & Description")
        setting = st.text_input("Scene Setting")
    
    with col2:
        emotion = st.selectbox("Primary Emotion", [
            "Tension", "Love", "Anger", "Fear", "Joy",
            "Sadness", "Suspicion", "Hope", "Other"
        ])
        context = st.text_area("Scene Context/Background")
    
    if st.button("Generate Dialogue"):
        dialogue = generate_dialogue(char1, char2, setting, emotion, context)
        if dialogue:
            st.markdown("### 💭 Generated Dialogue")
            st.text_area("Dialogue Output", dialogue, height=300)
            
            if st.button("Save to Project"):
                if st.session_state.current_project:
                    st.session_state.generated_content[f'dialogue_{datetime.now().strftime("%Y%m%d_%H%M%S")}'] = dialogue
                    st.success("Dialogue saved to current project!")
                else:
                    st.warning("Please create a project first!")

def render_character_creator():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("👤 Character Creator")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Character Name")
        age = st.number_input("Age", min_value=0, max_value=150, value=30)
        occupation = st.text_input("Occupation")
    
    with col2:
        background = st.text_area("Character Background")
        goals = st.text_area("Goals and Motivations")
    
    if st.button("Generate Character Profile"):
        profile = generate_character_profile(name, age, occupation, background, goals)
        if profile:
            st.markdown("### 📋 Character Profile")
            st.markdown(profile)
            
            if st.button("Save Character"):
                if st.session_state.current_project:
                    st.session_state.generated_content[f'character_{name}_{datetime.now().strftime("%Y%m%d")}'] = profile
                    st.success(f"Character '{name}' saved to project!")
                else:
                    st.warning("Please create a project first!")

def render_scene_builder():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("🎬 Scene Builder")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Scene Location")
        time = st.selectbox("Time of Day", [
            "Dawn", "Morning", "Noon", "Afternoon",
            "Dusk", "Evening", "Night", "Midnight"
        ])
    
    with col2:
        mood = st.text_input("Mood/Atmosphere")
        purpose = st.text_area("Scene Purpose/Goals")
    
    if st.button("Generate Scene Description"):
        scene = generate_scene_description(location, time, mood, purpose)
        if scene:
            st.markdown("### 🎥 Scene Description")
            st.markdown(scene)
            
            if st.button("Save Scene"):
                if st.session_state.current_project:
                    st.session_state.generated_content[f'scene_{datetime.now().strftime("%Y%m%d_%H%M%S")}'] = scene
                    st.success("Scene saved to project!")
                else:
                    st.warning("Please create a project first!")

def render_plot_solutions():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("💡 Plot Solutions")
    st.markdown("</div>", unsafe_allow_html=True)
    
    problem = st.text_area("Describe your plot challenge")
    context = st.text_area("Current story context")
    goals = st.text_area("What are you trying to achieve?")
    
    if st.button("Generate Solutions"):
        solutions = generate_plot_solutions(problem, context, goals)
        if solutions:
            st.markdown("### 🎯 Suggested Solutions")
            st.markdown(solutions)
            
            if st.button("Save Solutions"):
                if st.session_state.current_project:
                    st.session_state.generated_content[f'solutions_{datetime.now().strftime("%Y%m%d_%H%M%S")}'] = solutions
                    st.success("Solutions saved to project!")
                else:
                    st.warning("Please create a project first!")

def render_project_history():
    st.markdown("<div class='feature-header'>", unsafe_allow_html=True)
    st.header("📚 Project History")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if not st.session_state.current_project:
        st.warning("Please create or select a project first!")
        return
    
    if not st.session_state.history:
        st.info("No content generated yet. Start creating to see your history!")
        return
    
    for idx, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{item['type']} - {item['timestamp']}"):
            st.markdown(item['content'])
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Copy to Clipboard", key=f"copy_{idx}"):
                    st.write("Content copied!")
            with col2:
                st.download_button(
                    "Download",
                    item['content'],
                    file_name=f"{item['type']}_{item['timestamp']}.txt"
                )

# ========== 5️⃣ Main App ==========
# ========== 5️⃣ Main App ==========
def main():
    # Initialize app configuration
    initialize_app()
    
    # Initialize session state
    initialize_session_state()
    
    # Display app title and description
    st.title("🎬 AI Screenplay Co-Writer Pro")
    st.markdown("""
        <div class='info-box'>
        Welcome to AI Screenplay Co-Writer Pro! This tool helps you develop your screenplay 
        with AI-powered assistance for outlining, dialogue, character development, and more.
        </div>
    """, unsafe_allow_html=True)
    
    # Render sidebar and get selected feature
    selected_feature = render_sidebar()
    
    # Display warning if no project is selected
    if not st.session_state.current_project and selected_feature != "Project History":
        st.warning("⚠️ Please create or select a project in the sidebar to save your work!")
    
    # Render appropriate feature based on selection
    if selected_feature == "Story Outline":
        render_outline_generator()
    elif selected_feature == "Dialogue Generator":
        render_dialogue_generator()
    elif selected_feature == "Character Creator":
        render_character_creator()
    elif selected_feature == "Scene Builder":
        render_scene_builder()
    elif selected_feature == "Plot Solutions":
        render_plot_solutions()
    elif selected_feature == "Project History":
        render_project_history()

    # Add footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
        Made with ❤️ by AI Screenplay Co-Writer Pro | Version 1.0
        </div>
    """, unsafe_allow_html=True)

# ========== 6️⃣ Save/Load Project Functions ==========
def save_project_state():
    """Save current project state to a JSON file"""
    if st.session_state.current_project:
        project_data = {
            'name': st.session_state.current_project,
            'history': st.session_state.history,
            'generated_content': st.session_state.generated_content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            os.makedirs('projects', exist_ok=True)
            with open(f"projects/{st.session_state.current_project}.json", 'w') as f:
                json.dump(project_data, f)
            return True
        except Exception as e:
            st.error(f"Error saving project: {str(e)}")
            return False

def load_project_state(project_name):
    """Load project state from a JSON file"""
    try:
        with open(f"projects/{project_name}.json", 'r') as f:
            project_data = json.load(f)
            st.session_state.current_project = project_data['name']
            st.session_state.history = project_data['history']
            st.session_state.generated_content = project_data['generated_content']
        return True
    except FileNotFoundError:
        st.warning(f"No saved data found for project: {project_name}")
        return False
    except Exception as e:
        st.error(f"Error loading project: {str(e)}")
        return False

# ========== 7️⃣ Run the Application ==========
if __name__ == "__main__":
    main()