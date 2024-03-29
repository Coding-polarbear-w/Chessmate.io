#final attempt 
import os
import streamlit as st
import google.generativeai as genai
import chess.pgn 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

# App title and instructions
st.title("Chessmate.io ♞♟️")
st.markdown(
    """
    Hi! User This is Chessmate.io created by Shreyansh Mishra this website uses Gen Ai from Google
    
    Drag and drop your PGN file here or click to browse: ♜
    """,
    unsafe_allow_html=True,
)

def generate_analysis_prompts(game, opening_analysis_prompt, error_analysis_prompt, similar_games_prompt):
   
    response = model.generate_content(opening_analysis,error_analysis_prompt, similar_games_prompt )
    return response



   
upload_file = st.file_uploader("",type= "pgn")
game_info = upload_file.read()
game = chess.pgn.read_game(game_info)

        # Generate analysis responses using the same prompts
opening_analysis_prompt = f"""Analyze the opening played in this game, considering the context of '{game.headers.get('Event')}', player names/ratings, and tournament level. Identify the opening name, its key characteristics, and the main strategic ideas employed in this specific context. Focus on the opening moves (up to move X, if applicable) to provide a targeted analysis."""

error_analysis_prompt = f"""Identify the most critical tactical errors or missed opportunities made by either player in this game, particularly focusing on the middlegame and endgame phases. Consider the players' strengths and weaknesses to offer insights into their decision-making process. Explain the consequences of these errors or missed opportunities on the game's outcome."""
similar_games_prompt = f"""Find historical games featuring similar opening and strategic themes as this one, prioritizing those with the most analogous opening sequences and strategic plans. Briefly compare and contrast the current game with at least 3 of the most similar games, outlining key similarities and differences in terms of opening variations, middlegame decisions, and endgame techniques."""
opening_analysis = genai.generate_text(opening_analysis_prompt)
error_analysis = genai.generate_text(error_analysis_prompt)
similar_games = genai.generate_text(similar_games_prompt)


        # Display analysis results
st.write(f"**Opening Analysis:** {opening_analysis}")
st.write(f"**Error Analysis:** {error_analysis}")
st.write(f"**Similar Games:** {similar_games}")
