
# Intelligent PDF Editor

A Streamlit-based application that uses LLMs to modify PDF documents based on natural language prompts.

## Features

- **Text Replacement**: Modify specific sentences or paragraphs
- **Heading Alteration**: Change headings and titles
- **Text Highlighting**: Highlight important sections
- **AI Humanization**: Make AI-generated text undetectable by tools like Turnitin

## Setup Instructions

1. **Clone and setup**:
   \`\`\`bash
   git clone <your-repo>
   cd intelligent-pdf-editor
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   \`\`\`

2. **Configure API Keys**:
   - Get an OpenAI API key from https://platform.openai.com/
   - Or get a Gemini API key from https://aistudio.google.com/
   - Update the \`.env\` file with your API keys

3. **Run locally**:
   \`\`\`bash
   streamlit run app.py
   \`\`\`

## Deployment to Streamlit Cloud

1. **Push to GitHub**:
   \`\`\`bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   \`\`\`

2. **Deploy to Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Connect your GitHub account
   - Select your repository
   - Deploy!

3. **Configure Secrets**:
   - In Streamlit Cloud, go to Settings → Secrets
   - Add your API keys:
     \`\`\`
     OPENAI_API_KEY=your_key_here
     GEMINI_API_KEY=your_key_here
     \`\`\`

## Usage

1. Upload a PDF file
2. Enter a natural language prompt (e.g., "Change the heading Introduction to Overview")
3. Select modification options
4. Click "Apply Modifications"
5. Download the edited PDF

## Technical Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyMuPDF (Fitz)
- **LLM Integration**: OpenAI GPT/Gemini
- **Deployment**: Streamlit Cloud

## Note

Make sure to add your actual API keys to the \`.env\` file for local development and to Streamlit Cloud secrets for deployment.
EOL