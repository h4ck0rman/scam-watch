import openai 
import prompts
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/checkScam', methods=['POST'])
def scamWatch():

    # Set the openAI api key 
    with open(".env", 'r') as APIKey:
        openai.api_key = APIKey.read().strip()

    # import the prompts constants for making openAI API calls
    systemPrompt = prompts.SYSTEM
    messagePrompt = prompts.MESSAGE

    # get the message to be scanned from the request body 
    textMessage = request.get_json()

    scanText = textMessage['text'] 

    messagePrompt['content'] = messagePrompt['content'] + f"\"{scanText}\""
    print(messagePrompt)

    # Get the response from openAI APIs 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            systemPrompt,
            messagePrompt
        ]
    )

    return response.choices[0].message.content, 200

if __name__ == '__main__':
   app.run()