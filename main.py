"""
Perplexity Sonar Chat Interface
"""

import os
import logging
import gradio as gr
from dotenv import load_dotenv
from perplexity import Perplexity

load_dotenv()

API_KEY = os.environ.get("PERPLEXITY_API_KEY")
if not API_KEY:
    raise EnvironmentError("Missing environment variable: PERPLEXITY_API_KEY")

client = Perplexity(api_key=API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def respond(message, history):
    """
    Streams a chat completion from Perplexity Sonar model.
    Emits partial responses incrementally with citations appended.
    """
    messages = history + [{"role": "user", "content": message}]
    response_chunks = []
    citations = []

    try:
        stream = client.chat.completions.create(
            model="sonar",
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            delta = getattr(chunk.choices[0].delta, "content", None)
            if delta:
                response_chunks.append(delta)
                yield "".join(response_chunks)
            
            # Capture citations from the final chunk
            if hasattr(chunk, 'search_results') and chunk.search_results:
                citations = chunk.search_results

        # Append formatted citations to the response
        if citations:
            full_response = "".join(response_chunks)
            formatted_citations = format_citations(citations)
            final_response = f"{full_response}\n\n{formatted_citations}"
            yield final_response

    except Exception as e:
        logging.error(f"Error in streaming response: {e}")
        yield f"[Error retrieving response: {e}]"


def format_citations(citations):
    """
    Formats search results into a readable citations section.
    
    Args:
        citations: List of APIPublicSearchResult objects with title, url, and optional date attributes
    
    Returns:
        Formatted string with citations
    """
    if not citations:
        return ""
    
    citation_lines = ["---", "**Sources:**"]
    
    for idx, citation in enumerate(citations, start=1):
        title = getattr(citation, 'title', 'Untitled')
        url = getattr(citation, 'url', '#')
        date = getattr(citation, 'date', '')
        
        citation_text = f"[{idx}] [{title}]({url})"
        if date:
            citation_text += f" ({date})"
        
        citation_lines.append(citation_text)
    
    return "\n".join(citation_lines)


def main():
    title = "Perplexity Sonar Chat"
    description = (
        "Chat with Perplexity AI’s **Sonar** model in real time using streaming responses. "
        "Type a message and watch the output evolve live."
    )

    iface = gr.ChatInterface(
        fn=respond,
        type="messages",
        title=title,
        description=description,
        theme="origin",
        analytics_enabled=False,
    )

    iface.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
