from google import genai
import asyncio
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration for audio playback
RATE = 24000
CHANNELS = 1
DTYPE = "int16"  # Corresponds to 16-bit PCM


def process_response(response, audio_stream=None):
    server_content = response.server_content
    if server_content:
        model_turn = server_content.model_turn
        if model_turn:
            for part in model_turn.parts:
                if part.text:
                    print(part.text, end="", flush=True)
                if part.inline_data and audio_stream is not None:
                    inline_data = part.inline_data
                    # Convert data to NumPy array for SoundDevice
                    audio_data = np.frombuffer(inline_data.data, dtype=DTYPE)
                    audio_stream.write(audio_data)


async def chat(tools=[]):
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    model_id = "gemini-2.0-flash-exp"
    config = {"tools": tools, "response_modalities": ["AUDIO"]}
    # Initialize SoundDevice Stream
    with sd.OutputStream(
        samplerate=RATE, channels=CHANNELS, dtype=DTYPE
    ) as audio_stream:
        async with client.aio.live.connect(model=model_id, config=config) as session:
            try:
                while True:
                    message = input("> ")
                    print()
                    if message == "exit":
                        break
                    await session.send(message, end_of_turn=True)

                    async for response in session.receive():
                        process_response(response, audio_stream)

                    print()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("Exiting...")


if __name__ == "__main__":
    asyncio.run(chat())
