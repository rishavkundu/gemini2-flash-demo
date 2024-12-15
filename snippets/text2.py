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
        await session.send("Hello", end_of_turn=True)

        # Process responses from the AI
        async for response in session.receive():
            if not response.server_content.turn_complete:
                for part in response.server_content.model_turn.parts:
                    print(part.text, end="", flush=True)
        print("TOTO")


# Run the main function
asyncio.run(main())
