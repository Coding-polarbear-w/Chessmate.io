import streamlit as st
from google.generativeai import GenerativeModel as genai 
import chess.pgn
import os


# Chessboard image for decoration
board_image = "https://raw.githubusercontent.com/google/fonts/master/googlefonts/ptsans/fonts/static/PTSans-Bold.woff2"

# Initialize Generative AI model

genai.configure(api_key=os.getenv("google_api"))
model = genai.generativeai('gemini-pro-vision')

st.title("Chessmate.io ♞♟️")

# Upload PGN file with custom styling
st.markdown(
    """
    Drag and drop your PGN file here or click to browse: ♜
    """,
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader("", type="pgn")

# Analyze game if file uploaded
if uploaded_file:
    pgn_data = uploaded_file.read()
    game = chess.pgn.read_game(pgn_data)

    # Extract moves and display chessboard with highlights
    moves_text = "\n".join([str(move) for move in game.mainline_moves()])
    board = game.board()
    fen_string = board.fen()
    # Use an online chessboard library or API to generate a visual board with move highlights based on fen_string

    

    # Generate analysis using Generative AI prompts
    opening_analysis = genai.generate_text(
        f"Analyze the opening played in this game, identifying its name, key characteristics, and strategic ideas."
    )
    error_analysis = genai.generate_text(
        f"Identify any critical tactical errors or missed opportunities in this game, explaining their consequences."
    )
    similar_games = genai.generate_text(
        f"Find historical games featuring similar opening and strategic themes as this one, providing brief descriptions of each."
    )

    # Display analysis and user interaction elements
    st.markdown(f"**Moves:** {moves_text}")
    st.write(f"**Opening Analysis:** {opening_analysis}")
    st.write(f"**Error Analysis:** {error_analysis}")
    st.write(f"**Similar Games:** {similar_games}")


elo_prediction = genai.generate_text(
    f"Based on the moves played and the overall game flow, what is the estimated Elo rating of the players in this game? Please also provide a confidence score for your prediction."
)

predicted_elo, confidence_score = elo_prediction.split(",", 1)
confidence_score = float(confidence_score.strip())

st.write(f"**Predicted Elo:** {predicted_elo} (Confidence Score: {confidence_score:.2f})")














