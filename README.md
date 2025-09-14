# Academic Research Collaborator

A comprehensive AI-powered research assistant system designed to help scholars with literature reviews, hypothesis validation, and draft polishing using Google's Gemini Flash 2.0.

## 🚀 Features

### 🔬 Research Management
- **Research Question Tracking**: Store and manage your core research questions
- **Citation Management**: Organize and analyze research sources
- **Note Taking**: Keep track of research insights and observations
- **Progress Tracking**: Monitor completion across different research phases

### 📖 Literature Review Agent
- **Comprehensive Literature Analysis**: Generate structured literature reviews from your citations
- **Source Quality Assessment**: Analyze the credibility and relevance of research sources
- **Gap Identification**: Identify research gaps and opportunities
- **Research Recommendations**: Get suggestions for additional sources and methodologies
- **Thematic Analysis**: Extract key themes and patterns from existing literature

### 💡 Hypothesis Validator Agent
- **Multi-Criteria Validation**: Evaluate hypotheses on 7 key criteria (clarity, testability, specificity, etc.)
- **Scoring System**: Get detailed scores (1-10) for each validation criterion
- **Improvement Recommendations**: Receive specific suggestions to strengthen your hypothesis
- **Alternative Generation**: Generate alternative hypotheses for your research question
- **Theoretical Grounding**: Assess theoretical foundation and originality

### ✍️ Draft Polisher Agent
- **Multiple Polish Types**: 
  - Comprehensive editing (structure, clarity, style)
  - Grammar and language mechanics
  - Structural organization
  - Clarity and readability
  - Citation integration
- **Target Audience Adaptation**: Tailor content for different academic audiences
- **Quality Assessment**: Get quality scores and improvement metrics
- **Version Comparison**: Compare different versions of your drafts
- **Academic Style Enhancement**: Ensure proper academic tone and formatting

## 🏗️ System Architecture

```
Academic-Research-Collaborator/
├── backend/                    # FastAPI backend
│   ├── agents/
│   │   ├── base.py            # Base agent class with Gemini integration
│   │   ├── Literature Review Agent.py
│   │   ├── Hypothesis Validator Agent.py
│   │   └── Draft Polisher Agent.py
│   └── main.py                # FastAPI application
├── memory/
│   └── memory_store.json      # Persistent memory storage
├── frontend/
│   └── app.py                 # Streamlit frontend
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Gemini API key
- FastAPI
- Streamlit
- Required Python packages

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Academic-Research-Collaborator
```

### 2. Install Dependencies
```bash
# Backend dependencies
pip install fastapi uvicorn google-generativeai python-multipart

# Frontend dependencies
pip install streamlit requests

# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Configure API Key
Edit `backend/agents/base.py` and replace the API key:
```python
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

### 4. Run the Application

#### Start Backend Server
```bash
cd backend
python main.py
# Or using uvicorn directly:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start Frontend Application
```bash
cd frontend
streamlit run app.py
```

### 5. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Research Setup
1. Navigate to the "🔬 Research Setup" tab
2. Enter your research question
3. Add citations and sources (one per line)
4. Include any initial research notes
5. Click "💾 Save Research Setup"

### 2. Literature Review
1. Go to "📖 Literature Review" tab
2. Optionally add more citations or notes
3. Click "🔍 Conduct Literature Review"
4. Review the generated analysis and recommendations
5. Use "Analyze Source Quality" for source assessment

### 3. Hypothesis Validation
1. Visit "💡 Hypothesis Validation" tab
2. Enter your research hypothesis
3. Click "🔬 Validate Hypothesis"
4. Review detailed validation scores and feedback
5. Use "Generate Alternatives" for hypothesis variations

### 4. Draft Polishing
1. Open "✍️ Draft Polishing" tab
2. Paste your academic draft
3. Select polish type and target audience
4. Click "✨ Polish Draft"
5. Review improvements and suggestions
6. Compare versions using the comparison feature

### 5. Research Dashboard
1. Check "📊 Dashboard" tab for overview
2. Monitor research progress
3. View statistics and metrics
4. Export research data when complete

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - API status and information
- `GET /health` - Health check
- `GET /memory` - Retrieve current research memory
- `DELETE /memory` - Clear all stored data
- `GET /research-progress` - Get research completion status

### Agent Endpoints
- `POST /literature-review` - Conduct literature review
- `POST /analyze-sources` - Analyze source quality
- `POST /validate-hypothesis` - Validate research hypothesis
- `POST /generate-alternatives` - Generate alternative hypotheses
- `POST /polish-draft` - Polish academic draft
- `POST /compare-drafts` - Compare draft versions
- `GET /export-research` - Export all research data

## 💾 Memory System

The system uses a persistent JSON-based memory store that maintains:

```json
{
  "research_question": "Your research question",
  "citations": ["List of citations"],
  "notes": ["Research notes"],
  "literature_reviews": [{"review data"}],
  "hypotheses": [{"hypothesis validation data"}],
  "drafts": [{"draft versions and improvements"}],
  "progress": {
    "literature_review_completed": false,
    "hypothesis_validated": false,
    "draft_polished": false
  }
}
```

## 🎨 Frontend Features

### User Interface
- **Responsive Design**: Works on desktop and tablet devices
- **Tab-Based Navigation**: Organized workflow across research phases
- **Progress Tracking**: Visual progress bars and completion indicators
- **Real-Time Updates**: Dynamic content updates based on API responses

### Interactive Elements
- **Copy to Clipboard**: Easy copying of generated content
- **Export Functionality**: Download research data as JSON
- **Memory Management**: View and clear stored research data
- **Quality Metrics**: Visual representation of scores and assessments

## 🔒 Security Considerations

### Development Setup
- API key is hardcoded for development (replace with environment variable for production)
- CORS is enabled for all origins (restrict in production)
- No authentication implemented (add authentication for production use)

### Production Recommendations
```python
# Use environment variables for API keys
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Restrict CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add authentication middleware
# Add rate limiting
# Add input validation and sanitization
```

## 🧪 Testing

### Manual Testing
1. Start both backend and frontend
2. Go through each tab in sequence
3. Test with sample research data
4. Verify memory persistence
5. Check API responses

### Sample Test Data
```
Research Question: "What is the impact of remote learning on student engagement in higher education?"

Sample Citation: "Johnson, A. (2023). Remote Learning and Student Engagement. Educational Technology Review, 15(3), 45-62."

Sample Hypothesis: "Students in remote learning environments will show 20% lower engagement rates compared to traditional in-person classes."

Sample Draft: "This study examines the relationship between remote learning modalities and student engagement levels in higher education institutions..."
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

#### Backend Won't Start
- Check if Python dependencies are installed
- Verify API key is properly set
- Ensure port 8000 is available

#### Frontend Connection Error
- Confirm backend is running on port 8000
- Check API_BASE_URL in frontend/app.py
- Verify no firewall blocking connections

#### Memory Not Persisting
- Check write permissions in memory/ directory
- Verify JSON file isn't corrupted
- Ensure backend has file system access

#### Gemini API Errors
- Verify API key is valid and active
- Check API quota and rate limits
- Ensure internet connectivity

### Error Messages
- `"API Error"` - Backend connection issue
- `"Memory cleared"` - Successful memory reset
- `"Failed to conduct literature review"` - Gemini API or processing error

## 🔮 Future Enhancements

### Planned Features
- **Multi-user Support**: User authentication and individual workspaces
- **Collaboration Tools**: Share and collaborate on research projects
- **Citation Management**: Automatic citation formatting (APA, MLA, Chicago)
- **Research Templates**: Pre-built templates for different research types
- **Data Visualization**: Charts and graphs for research insights
- **Integration APIs**: Connect with academic databases and reference managers

### Technical Improvements
- **Database Integration**: Replace JSON storage with proper database
- **Caching System**: Implement Redis caching for better performance
- **Background Tasks**: Async processing for long-running operations
- **Mobile App**: React Native or Flutter mobile application
- **API Versioning**: Proper API versioning and backward compatibility

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section
- Review API documentation at `/docs` endpoint

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- FastAPI for the robust backend framework
- Streamlit for the intuitive frontend interface
- The academic research community for inspiration

---

**Happy Researching! 📚✨**
