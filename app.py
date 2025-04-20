from flask import Flask, render_template, request, jsonify
import openai
import dotenv
import os

dotenv.load_dotenv()  # Loads variables from .env
app.logger.info('2')

openai_api_key = os.getenv("OPENAI_API_KEY")
app.logger.info('3')
app.logger.info(openai_api_key)

#config = dotenv.dotenv_values('.env')
#openai.api_key = config["OPENAI_API_KEY"]
#openai.api_key = openai_api_key

client = openai.OpenAI(api_key=openai_api_key)

def get_response(msg):
    prompt = f"""
    Take in the input, and respond with itself back, but adding "yopta" in the end. Here is the input: {msg}
    """
    
    response = client.responses.create(
        input = prompt,
        model = 'gpt-4.1'
    )
    print((response.output[0].content[0].text))
    response = response.output[0].content[0].text
    return response


app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'  
)


@app.route("/")
def hello_world():
    app.logger.info('2')
    return render_template("index.html")


@app.route("/execute", methods=["POST"])    
def execute():                    
    input_query = request.form.get("query")       
    app.logger.info(input_query)
    app.logger.info('1')
    llm_response = get_response(input_query)
    return {"output": llm_response}


