### Project Overview
The project is made to take in audio inputs, whether it is base64 encoded audio, or audio files, and convert it to text.
The text can then be used to be recognized against a specific data set. For example if you are in the media
industry, you can determine if it is an artist or a song name.

Specifically for property management information, that information has been fed into a model that takes in a prompt and
responds based on the information provided. This can be useful since the information simply needs to be in a list
and it can be applied to any property like an AI agent.

### How to Run
We are utilizing uvicorn to setup an API that can be triggered through postman. Once the project is cloned locally,
you can run the uvicorn setup by starting the program at the bottom of the `main.py` file.
Once the app is loaded, prompts can be transcribed and generated through the `/prompt/encodedAudio` or `/prompt/file` APIs


:
