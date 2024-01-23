import streamlit as st
import google.generativeai as genai
import chess.pgn
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

# App title and instructions
st.title("Chessmate.io ♞♟️")
st.markdown("""...""")  # Instructions remain the same

def generate_analysis_prompts(game_info):
    # Customize prompts based on game_info (e.g., opening, errors, similar games)
    return opening_analysis_prompt, error_analysis_prompt, similar_games_prompt

# File upload and validation
uploaded_file = st.file_uploader("", type=["txt", "png", "pgn"])

if uploaded_file:
    file_type = uploaded_file.type.lower()
    if file_type == ["pgn","txt","png"]:
        pgn_data = uploaded_file.read().decode("utf-8")
        game = chess.pgn.read_game(pgn_data)

        # Extract moves and current board state
        moves_text = "\n".join([str(move) for move in game.mainline_moves()])
        board = game.board()
        fen_string = board.fen()

        # Generate analysis prompts based on game data
        opening_analysis_prompt, error_analysis_prompt, similar_games_prompt = generate_analysis_prompts(game)

        try:
            # Generate analysis responses
            opening_analysis = genai.generate_text(opening_analysis_prompt)
            error_analysis = genai.generate_text(error_analysis_prompt)
            similar_games = genai.generate_text(similar_games_prompt)

            # Predict Elo and confidence score
            elo_prediction = genai.generate_text(
                f"Based on the moves played and overall game flow, estimate the Elo rating of the players in this game, including confidence scores."
            )
            predicted_elo, confidence_score = elo_prediction.split(",", 1)
            confidence_score = float(confidence_score.strip())

            # Display analysis and user interaction elements
            st.markdown(f"**Moves:** {moves_text}")
            st.write(f"**Opening Analysis:** {opening_analysis}")
            st.write(f"**Error Analysis:** {error_analysis}")
            st.write(f"**Similar Games:** {similar_games}")
            st.write(f"**Predicted Elo:** {predicted_elo} (Confidence Score: {confidence_score:.2f})")

        except Exception as e:
            st.error(f"Error analyzing PGN file: {e}")

    else:
        st.warning("Unsupported file type. Please upload a PGN file.")

else:
    st.info("Please upload a file to analyze.")
