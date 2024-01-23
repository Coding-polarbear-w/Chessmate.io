from dotenv import load_dotenv 
load_dotenv()
import streamlit as st
import google.generativeai as genai
import chess.pgn
import os

def get_gemini_response(question): 
    response = chat.send_message(question, stream = True)
    return response



# Chessboard image for decoration
CHESSBOARD_IMAGE = "https://www.chess.com/img/www/pieces/48/wP.png"  # Replace with desired image

# Initialize Generative AI model
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro-vision")
except Exception as e:
    st.error(f"Error initializing Generative AI: {e}")
    exit(1)

# App title and instructions
st.title("Chessmate.io ♞♟️")
st.markdown(
    """
    Hi! User This is Chessmate.io created by Shreyansh Mishra this website uses Gen Ai from Google
    
    Drag and drop your PGN file here or click to browse: ♜
    """,
    unsafe_allow_html=True,
)

# File upload and validation
st.markdown(""" Upload here if text file """)
upload_file = st.file_uploader("", type = ".txt")
sub = st.button("Show Analysis")
if upload_file and sub: 
    response = get_gemini_response(upload_file)
    
st.markdown("""Upload here in png format""")
upload_file2 = st.file_uploader("", type = "png")
if upload_file2 and sub: 
    response = get_gemini_response(upload_file2)



uploaded_file = st.file_uploader("", type="pgn")
if not uploaded_file:
    st.info("Please upload a PGN file to analyze.")
else:
    try:
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

        # Generate analysis using Generative AI prompts with improved specificity
        opening_analysis = genai.generate_text(
            f"Analyze the opening played in this game, identifying its name, key characteristics, and strategic ideas within the context of '{game.headers.get('Opening')}'"
        )
        error_analysis = genai.generate_text(
            f"Identify any critical tactical errors or missed opportunities in this game, specifically focusing on middle-game decisions and endgames."
        )
        similar_games = genai.generate_text(
            f"Find historical games featuring similar opening and strategic themes as this one, mentioning {game.headers.get('Event')} if relevant."
        )





        # Display analysis and user interaction elements
        st.markdown(f"**Moves:** {moves_text}")
        st.write(f"**Opening Analysis:** {opening_analysis}")
        st.write(f"**Error Analysis:** {error_analysis}")
        st.write(f"**Similar Games:** {similar_games}")

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
