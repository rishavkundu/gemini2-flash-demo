# Gemini 2 Flash Examples

Demo projects for Gemini 2 Flash.

## Setup

1. Create an API key in the [Google AI Studio](https://aistudio.google.com/app/apikey).

2. Rename the `.env_template` file to `.env`, and paste the API key into it.

3. Create a Conda environment:

    ```bash
    conda create --name gemini python=3.11
    ```

4.	Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Examples

- `text.py`: Demonstrates text-only chat functionality.

- `tool.py`: Demonstrates how to use tools.

- `voice.py`: Enables chat with voice responses.

- `vision.py`: Combines text chat with access to screen content.

## How to Run

Run the desired example using the following command:

```
python chat.py
```

Replace `chat.py` with the file name of another example to run it.

To exit the script while chatting, type `exit`.