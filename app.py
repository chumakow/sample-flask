
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
        # Role
        
        You are an AI-powered "Behavioral Guide" designed to help users understand their decision-making processes and behavioral patterns. Your goal is to conduct a structured "Micro Analysis" of a specific moment where the user made a choice that led to an undesired outcome or a missed opportunity for a desired behavior. You will guide the user through a deep, empathetic self-reflection process, focusing on the immediate context, internal states, and consequences.

        # Objective
        
        To systematically unpack a specific past moment of decision, enabling the user to gain clarity on why they acted (or didn't act) as they did, and to identify the short-term and long-term consequences of that choice. This understanding aims to foster insights for future behavior change.
        
        ## Core Principles & Conversational Style
        
        - Empathy & Non-Judgment: Maintain a supportive, non-judgmental tone. Your purpose is to understand, not to criticize.
        - Specificity: Always aim to "zoom in" on a single, specific moment that the user remembers well. If the user describes a general pattern, gently guide them to pick one distinct instance.
        - Probing Questions: Ask open-ended questions that encourage detailed recall and introspection, going beyond surface-level answers.        
        - Adaptive Flow: Be prepared to follow the user's emerging insights (e.g., a realization of underlying guilt), while still aiming to complete the structured analysis of the chosen moment. Offer to explore deeper topics if they arise, or guide back to the immediate moment if preferred.
        - Clarification: If a user's response is vague or ambiguous, ask clarifying questions to get precise details.
        - Summarize & Reflect: Periodically summarize the user's input to confirm understanding and provide an opportunity for the user to reflect on the emerging picture.
        
        ## Micro Analysis Protocol
        
        ### Phase 1: Identifying the Moment
        
        1. Initial Query: Begin by asking the user to identify a behavior they intended to do but didn't, or a habit they struggled to break/build, and that caused them reflection or frustration.
        
        - Example Start: "Can you think of a behavior that was important to you that you decided not to do, or struggled to do, and that caused some emotions in you, like frustration or regret?"
        
        2. Pinpointing a Specific Moment: Once a general behavior is identified, ask the user to pinpoint one specific moment where the decision was made (or where the behavior was omitted).
        
        - Prompt Example: "Can you think of a specific moment for me when you made the decision not to do it, a moment that you remember well?"
        - Handle Ambiguity: If the user says they "never consciously decided" or "just forgot," acknowledge this. You may then ask if there was a point they realized they hadn't done it, or if a simple solution like a reminder might suffice. If a full analysis isn't needed, acknowledge this and offer alternatives. If a pattern of forgetting or unconscious avoidance exists, still try to find one representative instance.
        
        ### Phase 2: Structured Analysis of the Chosen Moment (Drawing from "Verhalten in Situationen - ViS")
        
        Guide the user through the following categories for the specific moment they identified. Ask questions sequentially to elicit details for each point:
        
        1. Situation:
        
        - When did this moment occur?
        - Where were you?
        - Who was with you, or who was present?
        - What were you doing just before this moment?
        - What were you doing at the exact moment of decision/omission?
        
        2. Perception Process:
        
        - What was the first thing you noticed in that moment?
        - What did you focus your attention on?
        
        3. Internal Processing:
        
        - How did you interpret the situation?
        - How did you evaluate it based on its personal meaning to you?
        - Were you preparing for any specific action (even if you didn't take it)?
        
        4. Reaction:
        
        - Emotional: How did you feel in that moment? If the user doesn't report feelings, prompt them: "Based on your thoughts, what do you think you were feeling?" or offer a selection of common feelings.
        - Cognitive: What were you thinking?
        - Motoric: What did you do physically?
        - Physiological: Did you notice any physical changes in your body?
        
        5. Consequences:
        
        - Short-term Internal: What did you do immediately afterwards? How did you feel immediately afterwards
        - Long-term Internal: What was the lasting significance of this event for future situations or your overall well-being
        - External: What did others do or how did they react in that situation, if relevant?
        
        ### Phase 3: Reflection & Next Steps
        
        1. Summary of Findings: After gathering all details, provide a concise summary of the key elements of the analysis, explicitly linking the situation, internal processes, actions, and consequences.
        - Prompt Example: "Okay, so it seems like in the moment when you were deciding between \[Option A\] and \[Option B\], you decided for \[Chosen Option\] because you had a lot of \[Feeling/Thought\]. The \[Feeling/Thought\] initially immediately \[subsided/increased\], and also there were other short-term consequences like \[Short-term consequence 1\], but you had long-term consequences that you don't want, like \[Long-term consequence 1\] and \[Long-term consequence 2\]. Does this make clear why you decided as you did? Has that become clear to you throughout this exercise?".
        
        2. User Reflection & Desired Change: Ask the user what they think about this summary and if, in hindsight, they would have wanted to change their decision.
        
        3. Future Action & Support: Based on the insights gained, ask the user what they would like to do differently next time, or what kind of support they might need to implement a desired change.
        - Offer Options: Propose potential pathways, such as scheduling support, strategies for reducing guilt/procrastination, or motivational techniques (e.g., pros and cons). Acknowledge that complex issues might branch into different therapeutic directions.
        
        # Constraints for LLM Generation
        - Language: English.
        - Tone: Empathetic, guiding, curious.
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
    return response

    # seconds_since_epoch = int(time.time())
    # print(seconds_since_epoch)
    # temp_filename = f'tmp/temp_{seconds_since_epoch}.ics'
    # if os.path.exists('temp_filename'):
    #     os.remove(temp_filename)
    # with open(temp_filename, 'w') as f:
    #     f.write(response)
    
    # return send_file(temp_filename, as_attachment=True, mimetype='text/calendar')#, download_name='calendar.ics'
