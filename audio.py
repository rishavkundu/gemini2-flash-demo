from google import genai
import asyncio
from dotenv import load_dotenv
import os
import sounddevice as sd # Used for audio playback
import numpy as np # Used to process audio data

load_dotenv()


async def main():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    model_id = "gemini-2.0-flash-exp"
    # Change response modality to AUDIO
    config = {"response_modalities": ["AUDIO"]} 
    # Initialize SoundDevice Stream
    with sd.OutputStream(samplerate=24000, channels=1, dtype="int16") as audio_stream:
        async with client.aio.live.connect(model=model_id, config=config) as session:
            try:
                while True:
                    message = input("> ")
                    print()
                    if message == "exit":
                        break
                    await session.send(message, end_of_turn=True)
                    async for response in session.receive():
                        if not response.server_content.turn_complete:
                            for part in response.server_content.model_turn.parts:
                                if part.inline_data is not None:
                                    # Get the audio data from the response part and add it to the steam
                                    inline_data = part.inline_data
                                    audio_data = np.frombuffer(inline_data.data, dtype="int16")
                                    audio_stream.write(audio_data)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
