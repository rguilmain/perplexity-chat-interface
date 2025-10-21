# Perplexity Chat Interface

A simple web-based chat interface for Perplexity AI with streaming responses, conversation history, and clickable citations.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Perplexity AI API key

## Installation

1. Clone the repository:

```bash
git clone git@github.com:rguilmain/perplexity-chat-interface.git
cd perplexity-chat-interface
```

2. Create a `.env` file with your Perplexity API key:

```bash
PERPLEXITY_API_KEY=your_api_key_here
```

3. Install dependencies using uv:

```bash
uv sync
```

## Running the Application

Start the chat interface:

```bash
uv run python main.py
```

The application will launch a web interface in your default browser where you can interact with Perplexity AI.

## Features

- Real-time streaming responses from Perplexity AI
- Clean and intuitive chat interface powered by Gradio
- Conversation history maintained during the session
- Citation sources are displayed as clickable links below each response with titles and dates
