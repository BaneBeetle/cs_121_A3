from openai import OpenAI

import os
from dotenv import load_dotenv
import json

# Ensure to load the .env file
#dotenv_path = "/Users/galilearuiz/Desktop/uci/inf141/Assignment3/gptkey.env" #CHANGE UR PATH
dotenv_path = "C:\\Users\\lolly\\OneDrive\\Desktop\\Projects\\CS121\\A3\\cs_121_A3\\gptkey.env"
load_dotenv(dotenv_path, override=True)

# Check if the API key is loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI client
client = OpenAI(api_key=api_key)


def summarize(urls):
    '''Function that simply calls GPT with the provided prompt'''

    prompt = (
        "You are SummaryGPT. You will receive a list of webpages and it is your job to generate a short summary of the contents of each webpage. ONLY RESPOND IN JSON FORMAT. DO NOT ADD ANY UNNECESSARY COMMENTS. Valid responses look like this: { \"url\": \"URL\", \"response\": \"INSERT YOUR SUMMARY HERE GPT!\"}")

    user_content = "\n".join([f"Generate a short summary for the page: {url}" for url in urls])
    try:
        completion = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ])

        # parse the response as JSON
        response_text = completion.choices[0].message.content
        # print(f"Raw response from GPT: {response_text}")  # Debugging raw response

        # try to load the response as JSON
        response = json.loads(response_text)

        # return a list of summaries
        if isinstance(response, list):
            return response
        else:
            print("Error: Response is not a list as expected.")
            return []

    except Exception as e:
        print(f"Error during summarization: {e}")
        return []


if __name__ == "__main__":
    script = summarize("Loops")  # Example usage
    print(script)
