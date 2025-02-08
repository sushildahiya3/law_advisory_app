import streamlit as st
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException

# Initialize Vipas SDK model client
client = model.ModelClient()

# Model ID for Llama model
LLAMA_MODEL_ID = "mdl-s5cdasend8dza"  # Replace with the correct model ID for the Llama model

# Initialize session state for input and response history
if "input_history" not in st.session_state:
    st.session_state.input_history = []
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Streamlit App
st.title("Legal Advisor")
st.image("data:image/webp;base64,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",use_column_width=True)

st.write("This app uses the model from Vipas to answer legal questions only.")

# Input text for the model
input_text = st.text_area("Enter your legal question:", placeholder="Ask a question related to legal matters...")

# Run prediction when user clicks 'Submit'
if st.button("Submit"):
    sanitized_input = input_text.strip().strip('"')
    if sanitized_input:
        try:
            # Prompt engineering to restrict context to legal questions
            prompt = (
                "You are a legal expert. Provide a clear and concise answer to the following legal question:\n\n"
                f"Question: {input_text}\n\n"
                "Answer:"
            )
            payload = {
            "inputs": [
                {
                    "name": "prompt",
                    "shape": [1],
                    "datatype": "BYTES",
                    "data": [prompt]
                }
            ]
        }

            # Call the Llama model
            response = client.predict(model_id=LLAMA_MODEL_ID, input_data=payload)

            # Extract response text
            response_text = response.get("choices", [{}])[0].get("text", "No response text available.")

            # Update session state with input and response
            st.session_state.input_history.append(sanitized_input)
            st.session_state.response_history.append(response_text.strip())

            # Display the extracted response text
            st.write("### Legal Advisor's Response")
            # st.markdown(
            #     f"""
            #     <div style="border: 1px solid #9FC5E8; border-radius: 10px; padding: 15px; background-color: #101921">
            #         {response_text.strip()}
            #     </div>
            #     """,
            #     unsafe_allow_html=True
            # )
            st.markdown(
                """
                <script>
                const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                document.body.setAttribute('data-theme', theme);
                </script>

                <style>
                body[data-theme="dark"] {
                    --text-color: white;
                    --background-color: #101921;
                }
                body[data-theme="light"] {
                    --text-color: black;
                    --background-color: #cfe2f3;
                }
                .dynamic-container {
                    border: 1px solid #9FC5E8;
                    border-radius: 10px;
                    padding: 15px;
                    background-color: var(--background-color);
                    color: var(--text-color);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            # Render the styled div
            st.markdown(
                f"""
                <div class="dynamic-container">
                    {response_text.strip()}
                </div>
                """,
                unsafe_allow_html=True
            )

        except UnauthorizedException:
            st.error("Unauthorized access. Please check your VPS_AUTH_TOKEN.")
        except NotFoundException:
            st.error("Model not found. Please check the model ID.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a legal question.")

# Separator
st.write("---")

# Display input and response history
st.write("### Input and Response History")
if st.session_state.input_history:
    for i, (question, answer) in enumerate(zip(st.session_state.input_history, st.session_state.response_history), 1):
        st.write(f"**Question {i}:** {question}")
        st.write(f"**Answer {i}:** {answer}")
        st.write("---")
else:
    st.write("No questions asked yet.")

# st.write("Powered by Vipas.AI")

st.markdown(
    """
    <div style='font-size:20px; font-weight: bold;'>
        Powered by Vipas.AI
    </div>
    """,
    unsafe_allow_html=True
)
