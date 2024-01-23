from dotenv import load_dotenv 
load_dotenv()
import streamlit as st
import google.generativeai as genai
import chess.pgn
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")
chat = model.start_chat(history=[])

def get_gemini_response(opening_analysis): 
    response = model.generate_content(opening_analysis, stream = True)
    return response

chat = model.start_chat(history=[])




# Chessboard image for decoration
CHESSBOARD_IMAGE = "https://www.chess.com/img/www/pieces/48/wP.png"  # Replace with desired image

# Initialize Generative AI model


# App title and instructions
st.title("Chessmate.io ♞♟️")
st.markdown(""" Step into the dynamic world of Chessmate, where strategic mastery meets cutting-edge technology.
             Harness the power of Google's generative AI for unparalleled chess analysis. Elevate your game, unravel tactics,
             and embark on a journey of chess excellence. Welcome to a realm where intelligence converges with the art of chess. 
            Checkmate awaits!""")
unsafe_allow_html=True,

opening_analysis = genai.generate_text(
"""Analyze the opening played in this game, identifying its name, key characteristics, and strategic ideas within the context of '{game.headers.get('Opening')}'. 
Also Identify any critical tactical errors or missed opportunities in this game, specifically focusing on middle-game decisions and endgames.
And finally Find historical games featuring similar opening and strategic themes as this one, mentioning {game.headers.get('Event')} if relevant."""
)

# File upload and validation

sub = st.button("Show Analysis")
upload_file = st.file_uploader("", type = ".txt")


st.markdown(""" Upload here if text file!!! """)
if upload_file and sub: 
    response = get_gemini_response(opening_analysis)

    
upload_file2 = st.file_uploader("", type = "png")
st.markdown("""Upload here in png format!!!""")
if upload_file2 and sub: 
    response = get_gemini_response(opening_analysis)



uploaded_file = st.file_uploader("", type="pgn")

st.markdown("""Upload here if in pgn format!!!""")


if not uploaded_file:
    st.info("Please upload a PGN file to analyze.")
else:
     # Read and decode PGN data as text
    pgn_data = uploaded_file.readvalue().decode("utf-8")  # Decode here
    game = chess.pgn.read_game(pgn_data)

        # Extract moves and current board state
    moves_text = "\n".join([str(move) for move in game.mainline_moves()])
    board = game.board()
    fen_string = board.fen()

        # Generate visual chessboard with move highlights
    try:
         # Use Chessboard.js library (adjust import if needed)
        from chessboardjs import Board
        board = Board(fen=fen_string, highlightSquares=True)
        st.write(board)
    except ImportError:
        st.warning("Could not import chessboard library. Falling back to text moves.")
        st.markdown(f"**Moves:** {moves_text}")







 # Display analysis and user interaction elements
st.markdown(f"**Moves:** {moves_text}")

        # Predict Elo and confidence score
try:
    elo_prediction = genai.generate_text(
    f"Based on the moves played and overall game flow, estimate the Elo rating of the players in this game, including confidence scores."
    )
    predicted_elo, confidence_score = elo_prediction.split(",", 1)
    confidence_score = float(confidence_score.strip())
    st.write(f"**Predicted Elo:** {predicted_elo} (Confidence Score: {confidence_score:.2f})")
except ValueError:
    st.warning("Failed to parse Elo prediction output.")

except Exception as e:
    st.error(f"Error analyzing PGN file: {e}")
