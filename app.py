from flask import Flask
from flask import render_template


app = Flask(__name__,
            template_folder='templates',
            static_folder='static'  
)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/execute", methods=["POST"])    
def execute():                    
    input_query = request.form.get("input_query")       
    app.logger.info('got it')
    return 1             


