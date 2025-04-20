
## For digital ocean (TO BE NAMED app.py)

from flask import Flask, render_template, request, jsonify

import os
import dotenv
dotenv.load_dotenv
print(os.environ)#os.environ["OPENAI_API_KEY"]=openai_api_key

import openai

client = openai.OpenAI()


class LLM_agent():
    """comment me"""

    default_prompt = 'You are psychotherapist, but an unconventional one. Take in user message and respond like you are drunk slavic psychotherapist, excessively using word "yopta".'
    
    def __init__(self, prompt=default_prompt):
        self.prompt = prompt
        self.messages = [{"role": "developer", "content": self.prompt}]

    def __repr__(self):
        return self.prompt
        
    def get_response(self, msg):
        app.logger.info(msg)
        
        self.messages.append({"role": "user", "content": msg})
        app.logger.info(self.messages)
        
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=self.messages
        )

        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        print(self.messages)
        return response

agent = LLM_agent()

print(agent.messages)

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'  
)


@app.route("/")
def main_page():
    app.logger.info('2')
    return render_template("index.html")


@app.route("/execute", methods=["POST"])    
def execute():                    
    input_query = request.form.get("query")       
    app.logger.info(input_query)
    app.logger.info('1')
    print(dir())
    llm_response = agent.get_response(input_query)
    return {"output": llm_response}


@app.route("/update", methods=["POST"])    
def update():
    global agent
    new_prompt = request.form.get("prompt")       
    app.logger.info(new_prompt)
    app.logger.info('4')
    agent = LLM_agent(new_prompt)
    print(agent)
    return {"result": f"updated with {new_prompt}"}

@app.route('/reset', methods=['POST'])
def reset():
    global agent
    agent = LLM_agent()
    return jsonify({"status": "reset"})

@app.route('/get_vars')
def get_vars():
    # Put out cuurent prompt and message history
    
    global agent

    return jsonify({
        "current_prompt": f"CURRENT PROMPT IS : {agent.prompt}",
        "message_history": f"MESSAGE HISTORY : {agent.messages}"
    })
