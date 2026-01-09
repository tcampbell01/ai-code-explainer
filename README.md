# AI Code Explainer

An intelligent code explanation tool that uses Claude Haiku to provide detailed, level-appropriate explanations of code snippets. Features include interactive chat, curated learning resources, and explanations tailored to beginner, intermediate, or expert levels.

## Features

- **Multi-Level Explanations**: Tailored explanations for beginner, intermediate, and expert developers
- **Interactive Chat**: Ask follow-up questions about explained code
- **Curated Learning Resources**: Verified documentation links for key programming concepts
- **Multiple Languages**: Support for Python, JavaScript, Java, C++, and more
- **Structured Output**: Organized explanations with summaries, walkthroughs, gotchas, and improvements
- **Cost-Effective**: Uses Claude Haiku (~$2/month for moderate usage)

## Architecture

- **Backend**: FastAPI with Claude Haiku integration
- **Frontend**: Simple HTML/JavaScript interface
- **AI Model**: Anthropic Claude Haiku (cheap, fast, reliable)
- **Documentation**: Curated database of verified learning resources

## Quick Start

### Prerequisites

- Python 3.9+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### 1. Backend Setup

```bash
# Clone and navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=your_actual_key_here

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Start simple HTTP server
python3 -m http.server 3000
```

### 3. Access the Application

Open your browser and go to: `http://localhost:3000/simple.html`

## Usage

1. **Paste your code** into the text area
2. **Select programming language** (Python, JavaScript, Java, C++)
3. **Choose skill level** (Beginner, Intermediate, Expert)
4. **Click "Explain Code"** to get detailed explanation
5. **Use the chat** to ask follow-up questions about the code

### Example

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```

**Beginner explanation** will cover what recursion is and how it works.
**Expert explanation** will discuss time complexity, stack overflow risks, and optimization strategies.

## API Endpoints

### `POST /explain`
Explains code with structured output.

**Request:**
```json
{
  "code": "def hello(): print('world')",
  "language": "python",
  "level": "beginner"
}
```

**Response:**
```json
{
  "summary": "Brief explanation",
  "walkthrough": ["Step 1", "Step 2"],
  "concepts": [{"concept": "Function", "learn_more_url": "https://docs.python.org/3/"}],
  "gotchas": ["Potential issues"],
  "improvements": ["How to enhance"],
  "questions_to_ask": ["Deeper questions"],
  "risks": [{"line": 1, "reason": "Security issue"}]
}
```

### `POST /chat`
Interactive chat about explained code.

**Request:**
```json
{
  "question": "What happens with negative numbers?",
  "code": "def factorial(n): ...",
  "language": "python", 
  "level": "beginner"
}
```

## Configuration

### Environment Variables

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional
MODEL_NAME=claude-3-haiku-20240307
```

### Supported Languages

- Python
- JavaScript
- Java
- C++
- And more (the AI adapts to most programming languages)

### Skill Levels

- **Beginner**: Basic concepts, simple explanations
- **Intermediate**: More technical details, best practices
- **Expert**: Advanced concepts, performance considerations, security implications

## Cost Estimation

Using Claude Haiku:
- **Per explanation**: ~$0.0008-0.002
- **Monthly cost**: Under $2 for 1000 explanations
- **Free tier**: None (pay per use)

Much cheaper than GPT-4 while maintaining good quality for code explanation tasks.

## Project Structure

```
ai-code-explainer/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── llm.py           # Claude integration
│   │   ├── prompts.py       # AI prompts
│   │   ├── schemas.py       # Pydantic models
│   │   └── url_database.py  # Curated learning resources
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── simple.html          # Main interface
│   └── package.json
├── README.md
└── GOOGLE_SEARCH_ENHANCEMENT.md
```

## Future Enhancements

### Planned Features

1. **Google Custom Search API Integration**
   - Dynamic discovery of current documentation links
   - Automatic URL verification
   - Broader coverage of programming concepts
   - See `GOOGLE_SEARCH_ENHANCEMENT.md` for implementation details

2. **Enhanced UI/UX**
   - Syntax highlighting for code input
   - Dark/light theme toggle
   - Export explanations to PDF/Markdown
   - Code snippet sharing via URLs

3. **Advanced Features**
   - File upload for larger code files
   - Multi-file project analysis
   - Code diff explanations
   - Integration with popular IDEs (VS Code extension)

4. **User Management**
   - User accounts and saved explanations
   - Explanation history
   - Favorite concepts and bookmarks
   - Usage analytics and insights

5. **AI Improvements**
   - Support for newer Claude models
   - Custom prompts for specific use cases
   - Multi-language explanations (Spanish, French, etc.)
   - Code generation suggestions

6. **Performance & Scaling**
   - Response caching for common code patterns
   - Rate limiting and usage quotas
   - Database integration for persistence
   - Docker containerization

7. **Educational Features**
   - Interactive coding exercises
   - Progressive difficulty levels
   - Code quality scoring
   - Learning path recommendations

### Technical Debt & Improvements

- Add comprehensive error handling
- Implement proper logging
- Add unit and integration tests
- Set up CI/CD pipeline
- Add API documentation (OpenAPI/Swagger)
- Implement request validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include code samples and error messages

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude Haiku API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Pydantic](https://docs.pydantic.dev/) for data validation