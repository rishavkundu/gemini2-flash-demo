from google import genai
import asyncio
from dotenv import load_dotenv
import os
from google.genai import types
from tool_spec import FUNCTIONS, load_file_content_schema

load_dotenv()


async def main():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    model_id = "gemini-2.0-flash-exp"
    # Add search tool
    code_execution_tool = {"code_execution": {}}
    config = {
        "tools": [code_execution_tool],
        "response_modalities": ["TEXT"],
    }

    async with client.aio.live.connect(model=model_id, config=config) as session:
        try:
            while True:
                message = input("> ")
                print()
                if message == "exit":
                    break
                await session.send(message, end_of_turn=True)
                async for response in session.receive():
                    if response.server_content.model_turn is not None:
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
