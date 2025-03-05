# Module for using GPT API to summarize something

import json # json for front end to obtain information
import openai # Ensure you install this so GPT can communicate
import os
from dotenv import load_dotenv # Here is where we will put our GPT API-key

### PROMPT ENGINEERING ###
prompt = ("You are SummaryGPT. You will recieve a page or text and it is your job to generate a short summary of the contents of the page/text. ONLY RESPOND IN JSON FORMAT. DO NOT ADD ANY UNNECESSARY COMMENTS. Valid responses look like this: { \"response\": \"INSERT YOUR SUMMARY HERE GPT!\"}")


def summarize(user_input):
    '''Function that simply calls GPT with the provided prompt'''

    dotenv_path = "/Users/galilearuiz/Desktop/uci/inf141/Assignment3/gptkey.env"

        # "C:\\Users\\lolly\\OneDrive\\Desktop\\Projects\\CS121\\A3\\cs_121_A3\\gptkey.env"

    load_dotenv(dotenv_path, override=True) # override set to true if API key updated
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Grab the API key from the .env file. WE HAVE TO HIDE THIS! WE CANNOT COMMIT API KEYS OTHERWISE THE KEY WILL BE DELETED

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Generate a short summary after scanning this page/text: {user_input}."
            }
        ]
    )
    response = json.loads(completion.choices[0].message.content)

    return response['response']

if __name__ == "__main__":
    script = summarize("Loops") # This is from my ICS 31 project. You can change the string input to fit ur needs.
    print(script)
