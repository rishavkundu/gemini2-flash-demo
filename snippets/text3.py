from google import genai
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from a .env file
load_dotenv()


async def main():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )
    # Define the AI model and configuration
    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    async with client.aio.live.connect(model=model_id, config=config) as session:

        while True:
            message = input("> ")
            print()

            # Exit the loop if the user types "exit"
            if message == "exit":
                print("Exiting...")
                break

            # Send the user's message to the AI model, marking the end of the turn
            await session.send(message, end_of_turn=True)

            # Receive responses asynchronously and process each response
            async for response in session.receive():
                if not response.server_content.turn_complete:
                    for part in response.server_content.model_turn.parts:
                        print(part.text, end="", flush=True)
            print()


# Run the main function
asyncio.run(main())
