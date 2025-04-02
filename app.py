import streamlit as st
import requests
import openai
import json
from datetime import datetime
import time
from streamlit.components.v1 import html as components_html

# App configuration
st.set_page_config(
    page_title="Breathe",
    page_icon="assets/lungicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ultra-minimalist design with improved aesthetics
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400&family=Inter:wght@300;400;500&display=swap');
    
    /* Overall theme */
    .main {
        background-color: #faf9f7;
        color: #333;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 300;
        color: #444;
        letter-spacing: 0.5px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Custom buttons */
    .breathe-button {
        background-color: rgba(255, 255, 255, 0.7);
        border: 1px solid #e0ddd8;
        color: #555;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.6s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin: 0 auto;
        font-family: 'Cormorant Garamond', serif;
        letter-spacing: 1px;
    }
    
    .breathe-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    /* Tabs styling */
    .stTabs {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        border-bottom: none;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        color: #888;
        font-size: 16px;
        font-family: 'Cormorant Garamond', serif;
        letter-spacing: 1px;
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #444 !important;
        border-bottom: 1px solid #c7c1b7 !important;
        font-weight: 300;
    }
    
    /* Breathing animations */
    .breathing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 300px;
        margin: 40px 0;
    }
    
    .breathing-circle {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle, #f0ebe5, #e0ddd8);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #555;
        font-size: 22px;
        font-family: 'Cormorant Garamond', serif;
        letter-spacing: 1px;
        box-shadow: 0 6px 30px rgba(0,0,0,0.05);
        animation: breathe 8s infinite ease-in-out;
        position: relative;
    }
    
    .breathing-text {
        opacity: 0.8;
        transition: opacity 2s ease;
    }
    
    .breathing-instruction {
        margin-top: 30px;
        color: #888;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        letter-spacing: 0.5px;
        text-align: center;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        border: 1px solid #e0ddd8;
        animation: ripple 8s infinite ease-out;
        opacity: 0;
    }
    
    .ripple-1 { animation-delay: 0s; }
    .ripple-2 { animation-delay: 2s; }
    .ripple-3 { animation-delay: 4s; }
    
    @keyframes breathe {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 6px 30px rgba(0,0,0,0.05);
        }
        50% {
            transform: scale(1.3);
            box-shadow: 0 6px 40px rgba(0,0,0,0.1);
        }
    }
    
    @keyframes ripple {
        0% {
            width: 180px;
            height: 180px;
            opacity: 0.5;
        }
        100% {
            width: 400px;
            height: 400px;
            opacity: 0;
        }
    }
    
    /* Response box */
    .meditation-response {
        max-width: 650px;
        margin: 40px auto;
        padding: 40px;
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.04);
        transition: all 0.6s ease;
        opacity: 0.95;
        line-height: 1.8;
    }
    
    .meditation-response:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 40px rgba(0,0,0,0.08);
    }
    
    /* Mood bubbles */
    .mood-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin: 30px 0;
    }
    
    .mood-bubble {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background-color: white;
        border: 1px solid #e0ddd8;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
        color: #666;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    .mood-bubble:hover {
        transform: scale(1.05);
        border-color: #c7c1b7;
    }
    
    .mood-bubble.selected {
        border: 2px solid #a7a29a;
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    
    /* Form controls */
    .form-control {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .form-control h4 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 300;
        color: #666;
        margin-bottom: 15px;
        text-align: center;
        font-size: 18px;
        letter-spacing: 0.5px;
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #faf9f7 0%, #f0ebe5 100%);
    }
    
    /* Decorative elements */
    .decorative-line {
        height: 1px;
        background: linear-gradient(to right, rgba(0,0,0,0), rgba(199, 193, 183, 0.5), rgba(0,0,0,0));
        width: 100%;
        margin: 30px 0;
    }
    
    /* Loading animation */
    .loading-animation {
        width: 100px;
        height: 100px;
        border: 3px solid #f0ebe5;
        border-radius: 50%;
        border-top-color: #c7c1b7;
        animation: spin 1s infinite linear;
        margin: 40px auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    

    
    /* Radio buttons */
    div.stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background-color: #faf9f7;
        border: 1px solid #e0ddd8;
        border-radius: 6px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #faf9f7;
        border: 1px solid #e0ddd8;
        border-radius: 6px;
    }
            



    div.stButton {
        display: flex;
        justify-content: center;
    }


    div.stButton > button {
        background: linear-gradient(135deg, #F1E1D0, #D8D8D6);  /* Soft Beige to Light Off-White */
        color: #4A403A;  /* Calm Deep Brown */
        font-size: 16px;
        font-weight: 600;
        font-family: "Helvetica Neue", sans-serif;
        padding: 12px 20px;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);  /* Light shadow for a soft floating effect */
    }

    /* Hover Effect - Soft Glow & Slight Lift */
    div.stButton > button:hover {
        background: linear-gradient(135deg, #E3D7C8, #D0D0D0);  /* Slightly darker Beige */
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
    }

    /* Active/Pressed Effect - Subtle Compression */
    div.stButton > button:active {
        background: linear-gradient(135deg, #C9BBAA, #D1D1D1);  /* Slightly darker beige */
        transform: scale(0.98);
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }
            
</style>

""", unsafe_allow_html=True)

# API Keys in session state
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {"mistral": "", "openai": ""}

# Initialize session state for application
if "mood" not in st.session_state:
    st.session_state.mood = "calm"
if "duration" not in st.session_state:
    st.session_state.duration = 10
if "style" not in st.session_state:
    st.session_state.style = "breathing"
if "experience" not in st.session_state:
    st.session_state.experience = "beginner"
if "recommendation" not in st.session_state:
    st.session_state.recommendation = None
if "breathing_state" not in st.session_state:
    st.session_state.breathing_state = "inhale"
    st.session_state.breathing_counter = 0
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "breathe"
if "ai_model" not in st.session_state:
    st.session_state.ai_model = "mistral"

with st.sidebar:
    st.markdown("<h3 style='font-weight: 300; text-align: center;'>Settings</h3>", unsafe_allow_html=True)
    # Decorative line
    st.markdown("""
    <div class="decorative-line"></div>
    <p style='font-size: 0.8em; color: #888; text-align: center; font-family: "Cormorant Garamond", serif; letter-spacing: 1px;'>
    </p>
    """, unsafe_allow_html=True)


    # AI Model Selection
    selected_model = st.selectbox(
        "Select an AI Model",
        ["","mistral", "openai"],
        index=0,  # Default to "Select a model..."
        key="sidebar_model"
    )

    # Display API Key Input based on selection
    if selected_model == "mistral":
        st.session_state.api_keys["mistral"] = st.text_input(
            "Hugging Face API Key", 
            value=st.session_state.api_keys.get("mistral", ""), 
            type="password",
            placeholder="Enter Hugging Face API key"
        )

    elif selected_model == "openai":
        st.session_state.api_keys["openai"] = st.text_input(
            "OpenAI API Key", 
            value=st.session_state.api_keys.get("openai", ""), 
            type="password",
            placeholder="Enter OpenAI API key"
        )

    st.markdown("""
        <div class="decorative-line"></div>

        <p style='font-size: 0.8em; color: #666; text-align: center; font-family: "Cormorant Garamond", serif;'>
            <a href="https://koulmesahil.github.io/BreatheCalm/" target="_blank" style="color: #0077b5; text-decoration: none;">
                BreatheCalm
            </a> – The original mindful breathing web app designed to help you relax and focus. This new AI-powered addition enhances the experience by offering personalized breathing exercises and meditation practices tailored to your needs.
        </p>
        <p style='font-size: 0.8em; text-align: center;'>
            <a href="https://www.linkedin.com/in/sahilkoul123/" target="_blank" style="color: #0077b5; text-decoration: none;">LinkedIn</a> |
            <a href="https://koulmesahil.github.io/" target="_blank" style="color: #0077b5; text-decoration: none;">GitHub</a>
        </p>
    """, unsafe_allow_html=True)


def get_mistral_recommendation(prompt):
    if not st.session_state.api_keys.get("mistral"):
        return "Please add your Hugging Face API key in the sidebar settings."
    
    headers = {
        "Authorization": f"Bearer {st.session_state.api_keys['mistral']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers=headers,
            json=payload
        )
        response_data = response.json()
        
        generated_text = ""
        if isinstance(response_data, list) and len(response_data) > 0:
            if 'generated_text' in response_data[0]:
                generated_text = response_data[0]['generated_text']
        elif isinstance(response_data, dict) and 'generated_text' in response_data:
            generated_text = response_data['generated_text']
        else:
            return str(response_data)
        
        # Remove the original prompt from the response
        if prompt in generated_text:
            generated_text = generated_text.replace(prompt, "").strip()
        
        return generated_text
    except Exception as e:
        return f"Error connecting to Mistral API: {str(e)}"
    




def get_openai_recommendation(prompt):
    if not st.session_state.api_keys.get("openai"):
        return "Please add your OpenAI API key in the sidebar settings."

    # Set the OpenAI API key
    openai.api_key = st.session_state.api_keys['openai']
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a meditation guide specializing in creating personalized meditation exercises. Provide clear, practical instructions tailored to the user's specific needs. Keep the response under 250 words."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        # Check if response contains choices
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return "No valid response format from OpenAI API."
    
    except openai.error.OpenAIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error connecting to OpenAI API: {str(e)}"



# Main content area
def main_page():
    # Initialize session state for meditation response if it doesn't exist
    if 'meditation_response' not in st.session_state:
        st.session_state.meditation_response = ""

    # Create the main layout - use top-level columns
    left_col, main_col, right_col = st.columns([1, 3, 1])
    
    with main_col:
        # App title - minimal
        st.markdown("""
        <h1 style='text-align: center; font-weight: 200; margin-top: 50px; font-size: 48px;'>
            breathe
        </h1>
        <p style='text-align: center; color: #888; margin-bottom: 40px; font-family: "Inter", sans-serif; font-weight: 300;'>
            mindful moments for your day
        </p>
        """, unsafe_allow_html=True)
        
        # Tabs for different sections
        tab1, tab2 = st.tabs(["Discover", "Breathe"])



        with tab1:
            # Mood selection with circles - enhanced
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

            # Mood selection title
            st.markdown("""
            <p style='text-align: center; color: #666; font-family: "Cormorant Garamond", serif; font-size: 22px; letter-spacing: 1px;'>
                How are you feeling today?
            </p>
            """, unsafe_allow_html=True)

            # Pre-define moods with associated colors
            mood_data = {
                "calm": "#d5e8eb",
                "anxious": "#ebe6d5",
                "tired": "#e0d5eb",
                "restless": "#ebd5d5",
                "focused": "#d5ebda",
                "scattered": "#e6d5eb",
                "happy": "#ebd5e6",
                "sad": "#d5e0eb",
                "energized": "#ebebd5",
                "stressed": "#ebd5e0"
            }

            # Generate mood bubbles HTML
            mood_html = """
            <script>
            function selectMood(mood) {
                // Update visual selection
                document.querySelectorAll('.mood-bubble').forEach(el => {
                    el.classList.remove('selected');
                });
                event.currentTarget.classList.add('selected');
                
                // Send value to Streamlit
                window.parent.postMessage({
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    api: "component_0",
                    key: "selected_mood",
                    value: mood
                }, '*');
            }
            </script>
            
            <style>
                .mood-bubble {
                    transition: all 0.3s ease;
                }
                .mood-bubble:hover {
                    transform: scale(1.1);
                }
                .mood-bubble.selected {
                    border: 3px solid #555;
                    box-shadow: 0 0 10px rgba(0,0,0,0.2);
                    transform: scale(1.1);
                }
            </style>
            <div class="mood-container" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; max-width: 800px; margin: 0 auto;">
            """
            
            # Create mood bubbles
            for mood, color in mood_data.items():
                selected_class = "selected" if st.session_state.get('mood') == mood else ""
                mood_html += f"""
                <div class="mood-bubble {selected_class}" 
                    style="background-color: {color}; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #555; font-size: 14px; cursor: pointer; margin-bottom: 15px;"
                    onclick="selectMood('{mood}')">
                    {mood}
                </div>
                """
            
            mood_html += '</div>'

            # Create the component
            selected_mood = components_html(mood_html, height=250)

            # User description input
            st.markdown("""
            <p style='text-align: center; color: #666; font-family: "Cormorant Garamond", serif; font-size: 22px; letter-spacing: 1px; margin-top: 30px;'>
                Tell us more about what you need...
            </p>
            """, unsafe_allow_html=True)

            user_description = st.text_area(
                "Describe your current state or what you're looking for in this meditation",
                key="user_desc",
                height=120,
                label_visibility="collapsed",
                placeholder="e.g. I'm feeling overwhelmed with work and need something to help me focus..."
            )



            # Generate meditation button
            if st.button("Generate Meditation", key="generate_button", type="primary"):
                if not user_description:
                    st.warning("Please describe how you're feeling or what you need help with.")
                else:
                    with st.spinner("Creating your personalized meditation..."):
                        # Construct prompt based on mood and description
                        selected_mood_value = selected_mood if selected_mood else "neutral"
                        
                        prompt = f"""
                        You are a compassionate AI meditation guide. A user has shared: "{user_description}"

                        Gently acknowledge their current state in a warm and understanding way (1-2 sentences). Offer a soft invitation to settle into a moment of calm, such as:  
                        *"Let’s take a gentle pause together."*  

                        Then, guide them through a personalized meditation with adaptable elements:

                        **A) BREATH AWARENESS:**  
                        Invite them to connect with their breath in a way that feels right:  
                        - Simply noticing its natural rhythm  
                        - Counting gentle inhales and exhales  
                        - Following a paced breathing pattern  

                        **B) BODY & MIND CONNECTION:**  
                        Help them tune into their body and thoughts with a choice of:  
                        - A light body scan to release tension  
                        - A moment of emotional awareness without judgment  
                        - Grounding in physical sensations (feet on the floor, warmth of breath, etc.)  

                        **C) MINDFUL FOCUS:**  
                        Encourage focus on:  
                        - A peaceful image (a soft light, waves, a safe place)  
                        - A simple affirmation (e.g., "I am here. I am steady.")  
                        - The rhythm of ambient sounds or gentle movement  

                        **Closing:**  
                        - Remind them they can return to this anytime.  
                        - Offer a small action to carry the calm forward (e.g., "Feel your next three breaths with care.")  
                        - Optionally, include an uplifting phrase: "Stillness is always within reach."  

                        **Tone:** Gentle, patient, and accepting—like a supportive friend who shares meditation techniques naturally. Keep the language soothing, with soft pauses for reflection.  

                        **Length:** About 200-300 words, with space for pauses between instructions.
                        """

                        # Get recommendation based on selected model
                        if selected_model == "openai":
                            meditation_response = get_openai_recommendation(prompt)
                        else:  # Mistral
                            meditation_response = get_mistral_recommendation(prompt)
                        
                        # Store the response in session state
                        st.session_state.meditation_response = meditation_response
                        
                        # Show the response
                        st.markdown("""
                        <p style='text-align: center; color: #666; font-family: "Cormorant Garamond", serif; font-size: 22px; letter-spacing: 1px; margin-top: 30px;'>
                            Your Personalized Meditation
                        </p>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div style="background-color: #f8f8f8; padding: 20px; border-radius: 10px; margin-top: 20px;">
                            {meditation_response}
                        </div>
                        """, unsafe_allow_html=True)



        
        with tab2:
            # Enhanced breathing visualization
            st.markdown("""
            <div class="breathing-container">
                <div class="breathing-circle">
                    <div class="ripple ripple-1"></div>
                    <div class="ripple ripple-2"></div>
                    <div class="ripple ripple-3"></div>
                    <span class="breathing-text">breathe</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Decorative line
            st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
            
            # Breathing patterns
            st.markdown("""
                <div class="breathing-instruction">
                    <span id="breath-instruction">inhale through nose · hold · exhale through mouth</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

            # Display meditation response if available
            if st.session_state.meditation_response:
                st.markdown("""
                <p style='text-align: center; color: #666; font-family: "Cormorant Garamond", serif; font-size: 22px; letter-spacing: 1px; margin-top: 30px;'>
                    Your Personalized Meditation
                </p>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background-color: #f8f8f8; padding: 20px; border-radius: 10px; margin-top: 20px;">
                    {st.session_state.meditation_response}
                </div>
                """, unsafe_allow_html=True)
        

                        










            



# Run the main page
main_page()