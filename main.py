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
    Emits partial responses incrementally for smooth Gradio output.
    """
    messages = history + [{"role": "user", "content": message}]
    response_chunks = []

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

    except Exception as e:
        logging.error(f"Error in streaming response: {e}")
        yield f"[Error retrieving response: {e}]"


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
