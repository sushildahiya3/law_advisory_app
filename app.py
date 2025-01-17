import streamlit as st
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException

# Initialize Vipas SDK model client
client = model.ModelClient()

# Model ID for Llama model
LLAMA_MODEL_ID = "mdl-hy3grx9aoskqu"  # Replace with the correct model ID for the Llama model

# Initialize session state for input and response history
if "input_history" not in st.session_state:
    st.session_state.input_history = []
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Streamlit App
st.title("Legal Advisor")
st.image("./adviosry.webp",use_container_width=True)

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

            # Call the Llama model
            response = client.predict(model_id=LLAMA_MODEL_ID, input_data=prompt)

            # Extract response text
            response_text = response.get("choices", [{}])[0].get("text", "No response text available.")

            # Update session state with input and response
            st.session_state.input_history.append(sanitized_input)
            st.session_state.response_history.append(response_text.strip())

            # Display the extracted response text
            st.write("### Legal Advisor's Response")
            st.markdown(
                f"""
                <div style="border: 1px solid #9FC5E8; border-radius: 10px; padding: 15px; background-color: #101921">
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

st.write("Powered by Vipas.AI")
