
## For digital ocean (TO BE NAMED app.py)

from flask import Flask, render_template, request, jsonify, send_file
import time
import os
import dotenv
dotenv.load_dotenv
print(os.environ)#os.environ["OPENAI_API_KEY"]=openai_api_key

import openai

client = openai.OpenAI()



class LLM_agent():
    """description - TBD"""

    #default_prompt = 'You are psychotherapist, but an unconventional one. Take in user message and respond like you are drunk slavic psychotherapist, excessively using word "yopta".'
    default_prompt = """
        Your goal is to coach the user on how to change their bad habits into good ones. Interact with the user by asking short questions, giving short feedback, and providing instructions in bulleted steps. Use evidence-based strategies explained specifically in each Step. Switch to explaining whenever the user doesn't have ideas, then switch back to the interaction after explaining. Never ask more than one question in each response. Always give examples that are not in user's field of habit. For example, if they talk about smoking, you give example about workout, let them write their own ideas. Give them an exercise at each Step. Do a conclusion at the end of each step. Do exactly this way, don't act creatively. ALWAYS follow the steps below sequentially, unless explicitly asked otherwise; after each turn, assess if current Phase of a Step or Step as a whole is completed and you can move to the next one - if so move on to the next one, and don't come back to the previous step - unless explicitly asked to do so. Try to not stay at the same step for more than 8 turns. \n
        Step 1: Introduction to Habit Formation: Identify the habit you want to change and the perceived underlying reason. Example: "I smoke when stressed." Your Turn: (Write your habit here). Phase 2: Reframe the Habit: Reframe the habit to externalize it. Example: "Stress is affecting me to smoke " Your Turn: (Reframe your habit here). Phase 3: Have a dialog with user, ask it if they can control themselves. Conclusion: Great start! Reflect on what you've written today. Tomorrow, we'll look at positive instances when you resisted this habit. See you then! \n
        Step 2: Recall Positive Instances Objective: Identify times when you resisted or overcame the habit. Phase 1: Recall Positive Instances: Think of times you resisted the habit. Example: "I felt stressed but took a walk instead of smoking." Your Turn: (Write your instances here) Phase 2: Analyze: What Was Different Reflect on what made these times different. Example: "I chose to walk because I enjoy fresh air." Your Turn: (Analyze what was different here) Conclusion: Well done! Recognizing these moments is crucial. Tomorrow, we'll visualize your success. See you then! \n
        Step 3: Visualization Objective: Use visualization to reinforce new habits. Phase 1: Find a Quiet Space: Choose a quiet place where you won't be disturbed. Your Turn: (Find your space) Phase 2: Visualize Success: Visualize yourself successfully changing the habit. Example: Imagine choosing a healthy behavior over the old habit. Your Turn: (Visualize your success) Conclusion: Excellent! Visualization helps reinforce new habits. Tomorrow, we'll write a new, empowering narrative. See you then! \n
        Step 4: Write a New Narrative Objective: Create an empowering narrative about your new habit. Phase 1: Write a New Narrative: Write a positive statement about your ability to change. Example: "I manage stress through healthy activities." Your Turn: (Write your narrative here) Conclusion: Fantastic! Your new narrative will guide your behavior. Tomorrow, we'll implement "If-Then" plans to solidify your habit change. See you then! \n
        Step 5: Implement "If-Then" Plans Objective: Form specific implementation intentions. Phase 1: Create an If-Then Plan: Link a trigger with new, healthier behavior. Example: "If I feel stressed, then I will take a walk." Your Turn: (Write your If-Then plan here) Phase 2: Iterate on Phase 1 for a few times, but not more than 3.
        Step 6: Conclusion: Great job! You've set a solid foundation for changing your habit. Keep practicing these steps, and remember, every small effort counts towards your overall success. Continue your journey and celebrate your progress! Phase 1: Summarize your discussion with the user - follow the following template: start with "Habit to be built" - summarize what is user's habit to be built, then include "Current state of habit and challenges" - outline what you got on this from the discussion, then include "If-Then Plans" - and include here the plans user made in Step 5. Phase 2: make a concrete action plan for the user to follow - based on the conversation you had for the next week. The next week starts on 2nd of June and ends on 8th of June. Try to make 3-5 actions suggestions with start and end time for each - based on your own judgement; if the habit user wants to build is work-related, aim for standard working hours, if the habit is health-related, aim for non-working hours (assume Saturday and Sunday are non-working days). Make a list of these action suggestions. Finish with suggestion to use '/calendar' command to download iOS calendar file with these actions - ALWAYS include this suggestion to the same message where you put the action plan itself.
    """

    #default_prompt = 'Just spit out an .ics file for the user. Make it on absolutely any future date - and make it funny :)'

    def __init__(self, prompt=default_prompt):
        self.prompt = prompt
        self.messages = [{"role": "developer", "content": self.prompt}]

    def __repr__(self):
        return self.prompt
        
    def get_response(self, msg, temperature=0.7):
        #app.logger.info(msg)
        
        self.messages.append({"role": "user", "content": msg})
        #app.logger.info(self.messages)
        
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=self.messages,
            temperature = temperature
        )

        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        #print(self.messages)
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
    #print(dir())
    llm_response = agent.get_response(input_query)
    return {"output": llm_response}


@app.route("/update", methods=["POST"])    
def update():
    global agent
    new_prompt = request.form.get("prompt")       
    app.logger.info(new_prompt)
    app.logger.info('4')
    agent = LLM_agent(new_prompt)
    #print(agent)
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

@app.route('/get_ics_file')
def get_ics_file():
    global agent
    actions = agent.messages[-1]['content']
    print(10*'\n'+actions+5*'\n')
    
    agent_ics_prompt = 'Please take in the user message and make an ics file out of it. Consider the whole message, and then derive actionable items (may be under **Action plan** section). ALWAYS keep all details as they have been in the action, do not change any dates, action names or places. If there are multiple actions provided, make sure they are all on ONE .ics file. Pack each of them within its own BEGIN:VEVENT ... END:VEVENT and make sure each of them has its unique ID. Respond ONLY with ics code - this should be a parseable file. Make sure year on all dates is 2025. Only choose calendar events, for which dates are explicitly mentioned in the message; never make up dates'
    agent_ics_messages = [{'role': 'developer', 'content': agent_ics_prompt}, {'role': 'user', 'content': actions}]
    
    completion = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=agent_ics_messages,
    temperature = 0
    )

    response = completion.choices[0].message.content

    print(response)

    seconds_since_epoch = int(time.time())
    print(seconds_since_epoch)
    temp_filename = f'tmp/temp_{seconds_since_epoch}.ics'
    if os.path.exists('temp_filename'):
        os.remove(temp_filename)
    with open(temp_filename, 'wt') as f:
        f.write(response)
    
    return send_file(temp_filename, as_attachment=True, mimetype='text/calendar')#, download_name='calendar.ics'
