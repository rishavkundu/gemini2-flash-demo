from google import genai
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (e.g., GOOGLE_API_KEY)
load_dotenv()


async def main():
    # Initialize the GenAI client with API key and HTTP options
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    # Define the AI model ID and its configuration
    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    async with client.aio.live.connect(model=model_id, config=config) as session:
        try:
            # Continuously interact with the user until they choose to exit
            while True:
                message = input("> ")
                print()

                # Exit the loop if the user types "exit"
                if message == "exit":
                    break

                # Send the user's message to the AI model, marking the end of the turn
                await session.send(message, end_of_turn=True)

                # Receive responses asynchronously and process each response
                async for response in session.receive():
                    if not response.server_content.turn_complete:
                        for part in response.server_content.model_turn.parts:
                            if part.text is not None:
                                print(part.text, end="", flush=True)
                print()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
