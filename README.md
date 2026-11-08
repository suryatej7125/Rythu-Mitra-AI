# 🌱 Rythu Mitra AI

### Your Farm. Your Language. Your AI Assistant.

Rythu Mitra AI is a Telugu-first agricultural voice assistant designed to help farmers ask farming-related questions in their own language and receive spoken responses.

The project combines Gnani AI's Speech-to-Text and Text-to-Speech technologies with a curated agricultural knowledge base.

## ✨ Features

- 🎙️ **Telugu Voice Input:** Farmers can ask questions using their microphone.
- 📝 **Speech Recognition:** Gnani AI converts spoken Telugu into text.
- 🌾 **Agricultural Knowledge Base:** Provides preliminary guidance for supported crop-related questions.
- 💬 **Text Input:** Farmers can also type their questions.
- 🔊 **Telugu Voice Responses:** Answers are converted into speech using Gnani AI.
- 📚 **Information References:** Displays available information sources.
- 🛡️ **Safe Fallback:** Directs farmers to agricultural experts when reliable information is unavailable.

## 🧠 Supported Crops

The initial knowledge base includes:

1. Cotton
2. Paddy
3. Chilli

More crops and verified agricultural information can be added in future versions.

## ⚙️ Technology Stack

- Python
- Flask
- Gnani AI Speech-to-Text (Prisma)
- Gnani AI Text-to-Speech (Timbre)
- HTML
- CSS
- JavaScript
- JSON

## 🔄 How It Works

**Voice Workflow:**

Farmer speaks in Telugu → Gnani Speech-to-Text → Agricultural Knowledge Base → Gnani Text-to-Speech → Spoken Telugu Answer.

**Text Workflow:**

Farmer types a question → Agricultural Knowledge Base → Gnani Text-to-Speech → Spoken Telugu Answer.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Rythu-Mitra-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your Gnani API key

GNANI_API_KEY=YOUR_GNANI_API_KEY

### 6. Install FFmpeg

FFmpeg must be installed and available in your system PATH for browser audio conversion.

### 7. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🛡️ Responsible AI

Rythu Mitra AI currently uses keyword matching against a small, curated agricultural knowledge base. It is an early prototype, not an autonomous agricultural diagnostic system.

- Responses are preliminary guidance, not confirmed diagnoses.
- It does not prescribe pesticide or fertilizer dosages.
- Farmers should consult agricultural officers or Krishi Vigyan Kendras for field-level diagnosis and treatment recommendations.
- Unsupported questions receive a safe fallback response.

## 🔮 Future Improvements

- Expand the agricultural knowledge base with verified sources.
- Support additional Indian languages.
- Add crop disease image analysis.
- Introduce more conversational agricultural assistance.
- Improve crop-specific recommendations.

## 🙏 Acknowledgements

Built using Gnani AI's Speech-to-Text and Text-to-Speech technologies.

**Project:** Rythu-Mitra-AI  
**Developer:** B. Surya Tej  
**Purpose:** Making agricultural information more accessible to farmers through voice technology.