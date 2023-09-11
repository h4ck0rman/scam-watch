import os
import openai 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def scamWatch():

    with open(".env", 'r') as APIKey:
        openai.api_key = APIKey.read().strip()

    systemPrompt = {"role": "system", 
                    "content": """
    You are a cyber security specialist who is very skilled with offensive cyber security, and defensive cyber security and have a thorough knowledge of phishing, smishing, spear phishing, and scam emails or texts. 

    When I send you a sample text message or email, I want you to evaluate whether it is a phishing or scam text or email based on the criteria that you have researched. Evaluate twice, and when you are confident send back a response.

    Respond with a JSON object that contains a lot of details.: 
    - Evaluation: conclusion on whether the message is "Scam/Phishing" or "Regular" 
    - Suspiciousness Score: Percentage value of the likelihood of the message being a "Scam/Phishing". 100% means the text message is definitely a scam. 0% means it is definitely a regular text.
    - Attributes: Return all the attributes from the text that affected your decision and explain each attribute.
    - Advice: Provide cautious advice on what actions to take to avoid being scammed."""}



    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            systemPrompt,
            {"role": "user", "content": "Is this text message likely to be a scam message? \"The IRS is trying to reach you regarding a tax refund. Please call us at (phone number) to claim it. Hurry – your IRS tax refund is ready to be accepted! You only have 24 hours, so click below: [link]. Take advantage of this fantastic opportunity for extra cash – act now and receive your IRS tax refund today!\""},
        ]
    )

    return response.choices[0].message.content

if __name__ == '__main__':
   app.run()