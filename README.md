
# AI Prompt Enhancer

A full-stack application that leverages Google's Gemini AI to transform basic prompts into more structured, detailed, and effective versions. Built with FastAPI and Streamlit.

## 🌟 Features

- **Real-time Prompt Enhancement** using Google Gemini AI
- **Interactive Web Interface** built with Streamlit
- **RESTful API Backend** powered by FastAPI
- **Side-by-side Comparison** of original and enhanced prompts
- **Error Handling and Logging**

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI Model**: Google Gemini 2.0
- **Documentation**: Swagger UI (via FastAPI)

## 📋 Prerequisites

- Python 3.8+
- Google Cloud API Key
- Git

## 🚀 Quick Start

1. **Clone the repository**
````bash
git clone <https://github.com/DPROM3TH3AN/AI-prompt-enhancer.git>
cd prompt-enhancer
````

2. **Set up virtual environment**
````bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
# or
.\venv\Scripts\activate  # For Windows
````

3. **Install dependencies**
````bash
pip install -r requirements.txt
````

4. **Configure environment variables**
Create a `.env` file in the root directory:
````plaintext
GOOGLE_API_KEY=your_google_api_key_here
````

5. **Start the backend server**
````bash
python main.py
````

6. **Start the frontend (in a new terminal)**
````bash
cd frontend
streamlit run app.py
````

## 🔄 API Endpoints

- `GET /`: Health check endpoint
- `POST /structure-prompt`: Enhance user prompts

## 📁 Project Structure

```
prompt-enhancer/
├── frontend/
│   ├── app.py              # Streamlit web interface
│   └── requirements.txt    # Frontend dependencies
├── main.py                 # FastAPI backend server
├── .env                    # Environment variables (not tracked)
└── requirements.txt        # Project dependencies
```

## 💻 Usage

1. Access the web interface at `http://localhost:8501`
2. Enter your prompt in the text area
3. Click "Enhance My Prompt"
4. View the original and enhanced versions side by side

## 🔧 Development

### Backend
- FastAPI server runs on `http://0.0.0.0:8000`
- API documentation available at `http://localhost:8000/docs`
- Uses Pydantic models for request/response validation

### Frontend
- Streamlit interface with responsive design
- Real-time API communication
- Comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details

## 🙏 Acknowledgments

- Google Gemini AI for providing the language model
- Streamlit for the frontend framework
- FastAPI for the backend framework
