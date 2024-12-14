from google import genai
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


def process_response(response):
    server_content = response.server_content
    if server_content:
        model_turn = server_content.model_turn
        if model_turn:
            for part in model_turn.parts:
                if part.text:
                    print(part.text, end="", flush=True)


async def main():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    async with client.aio.live.connect(model=model_id, config=config) as session:
        try:
            while True:
                message = input("> ")
                print()
                if message == "exit":
                    break
                await session.send(message, end_of_turn=True)

                async for response in session.receive():
                    process_response(response)

                print()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
