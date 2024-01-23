#final attempt 
import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

# App title and instructions
st.title("Chessmate.io ♞♟️")
st.markdown("""...""")  # Instructions remain the same

# Text input for analysis
user_input_text = st.text_area("Enter text for analysis:")

if user_input_text:
    try:
        # Generate analysis responses using the same prompts
        opening_analysis = genai.generate_text(
                f"Analyze the opening played in this game, identifying its name, key characteristics, and strategic ideas within the context of '{game.headers.get('Opening')}'"
                )
        error_analysis = genai.generate_text(
                f"Identify any critical tactical errors or missed opportunities in this game, specifically focusing on middle-game decisions and endgames."
                )
        similar_games = genai.generate_text(
                f"Find historical games featuring similar opening and strategic themes as this one, mentioning {game.headers.get('Event')} if relevant."
                )
        opening_analysis = genai.generate_text(opening_analysis, query=user_input_text)
        error_analysis = genai.generate_text(error_analysis, query=user_input_text)
        similar_games = genai.generate_text(similar_games, query=user_input_text)

        # Display analysis results
        st.write(f"**Opening Analysis:** {opening_analysis}")
        st.write(f"**Error Analysis:** {error_analysis}")
        st.write(f"**Similar Games:** {similar_games}")

    except Exception as e:
        st.error(f"Error generating analysis: {e}")

else:
    st.info("Please enter text for analysis.")
