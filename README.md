# Lang-Tutor: AI-Powered Italian Language Learning System 🇮🇹

A comprehensive Italian language learning platform that combines spaced repetition with AI-powered conversations to help you learn Italian effectively. The AI tutor converses with you using words you already know while gradually introducing new vocabulary.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Ollama AI     │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   (Local LLM)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Spaced        │    │   PostgreSQL     │    │   Redis Cache   │
│   Repetition    │    │   Database       │    │   (Session)     │
│   Algorithm     │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Features

- **Spaced Repetition System**: Scientifically proven learning algorithm
- **AI Conversation Partner**: Personalized conversations using known vocabulary
- **Progressive Learning**: Gradually introduces new words based on mastery
- **Multi-language Support**: Easy to add new target languages
- **Progress Tracking**: Detailed analytics and learning insights
- **Offline Capability**: Works without internet once models are downloaded

## Quick Start (Unraid)

1. **Install Docker on Unraid** (if not already installed)
2. **Clone this repository** to your Unraid server
3. **Configure environment variables** in `.env`
4. **Run the system**:
   ```bash
   docker-compose up -d
   ```

## Components

### 1. Ollama AI Backend
- Lightweight local LLM server
- Supports multiple models (Mistral, Llama, etc.)
- Optimized for conversation and language learning

### 2. Language Learning API
- FastAPI backend with spaced repetition algorithm
- User management and progress tracking
- Integration with Ollama for AI conversations

### 3. React Frontend
- Modern, responsive web interface
- Interactive learning sessions
- Progress visualization and analytics

### 4. Database Layer
- PostgreSQL for persistent data storage
- Redis for session management and caching

## Configuration

See `.env.example` for all available configuration options.

## Development

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **AI**: Ollama with local LLM models
- **Database**: PostgreSQL 15+, Redis 7+

## License

MIT License - see LICENSE file for details. 