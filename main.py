import gradio as gr
from dotenv import load_dotenv
from perplexity import Perplexity

load_dotenv()

client = Perplexity()


def respond(message, history):
    messages = history + [{"role": "user", "content": message}]
    stream = client.chat.completions.create(
        model="sonar",
        messages=messages,
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            yield response


def main():
    iface = gr.ChatInterface(
        fn=respond,
        type="messages",
        title="Perplexity Chat Interface",
    )
    iface.launch()


if __name__ == "__main__":
    main()
