import openai 
import prompts
from flask import Flask, jsonify, request

app = Flask(__name__)

# Validate the input to have the right values
def validateInput(body:object):
    if not body: 
        return False, 'No Post data provided' 

    if 'text' not in body:
        return False, 'No text message provided in user input'
    
    if body['text'] == "":
        return False, 'No text message provided in user input'
    
    # TODO : Add any proper input sanitsation if necessary 

    return True, body['text']

# Handle all possible exceptions from openAI in a simplistic manner 
def sendAPIRequest(systemPrompt, messagePrompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                systemPrompt,
                messagePrompt
            ]
        )

    except openai.error.Timeout as e:
        # Handle timeout error, e.g. retry or log
        return False, f"OpenAI API request timed out: {e}"

    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        return False, f"OpenAI API returned an API Error: {e}"

    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        return False, f"OpenAI API request failed to connect: {e}"

    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        return False, f"OpenAI API request was invalid: {e}"

    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        return False, f"OpenAI API request was not authorized: {e}"

    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        return False, f"OpenAI API request was not permitted: {e}"

    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        return False, f"OpenAI API request exceeded rate limit: {e}"

    return True, response


# API route that initiates the OpenAI API call
@app.route('/checkScam', methods=['POST'])
def scamWatch():

    # Set the openAI api key 
    with open(".env", 'r') as APIKey:
        openai.api_key = APIKey.read().strip()

    # import the prompts constants for making openAI API calls
    systemPrompt = prompts.SYSTEM
    messagePrompt = prompts.MESSAGE

    # get the message to be scanned from the request body 
    status, scanText = validateInput(request.get_json())
    if not status:
        return scanText, 400

    # add the message to be scanned into the message prompt for chatGPT 
    messagePrompt['content'] = messagePrompt['content'] + f"\"{scanText}\""

    # Get the response from openAI APIs 
    status, response = sendAPIRequest(systemPrompt,messagePrompt)
    if not status:
        return response, 500

    return response.choices[0].message.content, 200

if __name__ == '__main__':
   app.run(debug=True)