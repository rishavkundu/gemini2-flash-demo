from google import genai
import asyncio
from dotenv import load_dotenv
import os
from google.genai import types
from tool_spec import FUNCTIONS, load_file_content_schema

load_dotenv()


async def handle_tool_call(session, tool_call):
    for fc in tool_call.function_calls:
        f = FUNCTIONS.get(fc.name)
        tool_response = types.LiveClientToolResponse(
            function_responses=[
                types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response=f(**fc.args),
                )
            ]
        )
    await session.send(tool_response)


async def main():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )

    model_id = "gemini-2.0-flash-exp"
    config = {"tools": {"function_declarations": [load_file_content_schema]}, "response_modalities": ["TEXT"]}

    async with client.aio.live.connect(model=model_id, config=config) as session:
        try:
            while True:
                message = input("> ")
                print()
                if message == "exit":
                    break
                await session.send(message, end_of_turn=True)
                async for response in session.receive():
                    # Process the function call
                    if response.tool_call is not None:
                        await handle_tool_call(session, response.tool_call)
                    elif not response.server_content.turn_complete:
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
