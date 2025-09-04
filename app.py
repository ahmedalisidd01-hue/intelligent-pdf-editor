
import streamlit as st
import os
import tempfile
from datetime import datetime
from utils.pdf_processor import PDFProcessor
from utils.llm_integration import LLMIntegration
from utils.text_humanizer import TextHumanizer
from config import Config
import base64

# Page configuration
st.set_page_config(
    page_title="Intelligent PDF Editor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for binary files"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
    except Exception as e:
        return f"Error creating download link: {str(e)}"

def main():
    st.title("📝 Intelligent PDF Editor with Hugging Face")
    st.markdown("Upload a PDF and modify it using natural language prompts with AI assistance")
    
    # Initialize utilities
    try:
        config = Config()
        pdf_processor = PDFProcessor()
        
        # Create directories if they don't exist
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
        
    except Exception as e:
        st.error(f"Initialization error: {e}")
        return
    
    # API Key input in sidebar
    with st.sidebar:
        st.header("🔑 Hugging Face API Setup")
        api_key = st.text_input(
            "Hugging Face API Key:",
            type="password",
            value=config.HUGGINGFACE_API_KEY or "",
            help="Get your free API key from https://huggingface.co/settings/tokens"
        )
        
        if api_key:
            os.environ['HUGGINGFACE_API_KEY'] = api_key
        
        st.header("📄 Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file:
            # Save uploaded file
            file_path = os.path.join(config.UPLOAD_FOLDER, uploaded_file.name)
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Uploaded: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"Error saving file: {e}")
    
    # Main content area
    if uploaded_file:
        st.header("Modify Your PDF")
        
        if not api_key:
            st.warning("⚠️ Please enter your Hugging Face API key in the sidebar to use AI features")
        
        # Prompt input
        prompt = st.text_area(
            "Enter your modification prompt:",
            placeholder="Example: 'Change the heading Introduction to Overview and highlight the first paragraph'",
            height=100
        )
        
        # Modification options
        humanize_text = st.checkbox("Humanize AI Text", value=True)
        
        if st.button("Apply Modifications", type="primary"):
            if not prompt:
                st.error("Please enter a modification prompt")
                return
            
            if not api_key:
                st.error("Please enter your Hugging Face API key")
                return
            
            try:
                with st.spinner("Processing your request..."):
                    file_path = os.path.join(config.UPLOAD_FOLDER, uploaded_file.name)
                    output_filename = f"modified_{uploaded_file.name}"
                    output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
                    
                    # Initialize LLM integration
                    llm_integration = LLMIntegration()
                    
                    # Extract text for context
                    context_text = pdf_processor.extract_full_text(file_path)
                    
                    # Generate modification instructions using Hugging Face
                    modification_prompt = f"""
                    Analyze this PDF content and provide specific instructions for modification based on: {prompt}
                    
                    Return instructions in this format:
                    REPLACE: [old_text] -> [new_text]
                    HIGHLIGHT: [text_to_highlight]
                    """
                    
                    instructions = llm_integration.generate_text(modification_prompt, context_text)
                    st.text_area("AI Instructions", instructions, height=150)
                    
                    # Parse and apply instructions
                    for line in instructions.split('\n'):
                        if 'REPLACE:' in line and '->' in line:
                            try:
                                parts = line.split('->')
                                old_text = parts[0].replace('REPLACE:', '').strip()
                                new_text = parts[1].strip()
                                
                                if humanize_text:
                                    new_text = llm_integration.humanize_text(new_text)
                                
                                pdf_processor.replace_text(file_path, output_path, old_text, new_text)
                                st.success(f"Replaced: '{old_text}' with '{new_text}'")
                                
                            except Exception as e:
                                st.warning(f"Could not process replacement: {e}")
                        
                        elif 'HIGHLIGHT:' in line:
                            try:
                                text_to_highlight = line.replace('HIGHLIGHT:', '').strip()
                                pdf_processor.highlight_text(file_path if not os.path.exists(output_path) else output_path, 
                                                            output_path, text_to_highlight)
                                st.success(f"Highlighted: '{text_to_highlight}'")
                                
                            except Exception as e:
                                st.warning(f"Could not process highlighting: {e}")
                    
                    st.success("PDF modification completed!")
                    
                    # Provide download link
                    st.markdown("### Download Modified PDF")
                    st.markdown(get_binary_file_downloader_html(output_path, "Modified PDF"), unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
    
    else:
        # Show instructions when no file is uploaded
        st.info("👈 Please upload a PDF file to get started")
        
        st.markdown("""
        ### Features:
        - **Text Replacement**: Modify specific sentences or paragraphs
        - **Heading Alteration**: Change headings and titles
        - **Text Highlighting**: Highlight important sections
        - **AI Humanization**: Make AI-generated text undetectable
        
        ### How to get Hugging Face API Key:
        1. Go to https://huggingface.co/settings/tokens
        2. Sign up/login with your account
        3. Create a new token with "read" permissions
        4. Copy the token and paste it in the sidebar
        
        ### How to use:
        1. Upload a PDF file
        2. Enter your Hugging Face API key
        3. Enter your modification prompt
        4. Apply modifications
        5. Download the edited PDF
        """)

if __name__ == "__main__":
    main()
EOL