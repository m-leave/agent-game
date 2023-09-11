import json
import os
from langchain import OpenAI, PromptTemplate
from memory import update_memory

# load the person's memory
with open('basic_memory.json') as f:
    basic_memory = json.load(f)

# load the short memory
with open('short_memory.json') as f:
    short_memory = json.load(f)

# load the summary-memory
with open('summary_memory.json') as f:
    summary_memory = json.load(f)

# load the recent events
with open('recent_events.json') as f:
    recent_events = json.load(f)

logs = [
    'LogBlueprintUserMessages: [BP_TestAILogPlayer_C_0] Info from [BP_TestAILogPlayer_C_0] : Tag Als.Gait.Running Added! Time: 1.624091',
    'LogBlueprintUserMessages: [BP_TestAILogPlayer_C_0] Info from  [BP_TestAILogPlayer_C_0] :  Tag Als.Gait.Sprinting Removed! Time: 36.894782',
    'LogBlueprintUserMessages: [BP_TestAILogPlayer_C_0] Info from  [BP_TestAILogPlayer_C_0] :  Tag Als.Gait.Running Added! Time: 36.894782',
    'LogBlueprintUserMessages: [BP_TestAILogPlayer_C_0] Info from  [BP_TestAILogPlayer_C_0] :  Tag Als.Gait.Running Removed! Time: 39.553555',
    'LogBlueprintUserMessages: [BP_TestAILogPlayer_C_0] Info from  [BP_TestAILogPlayer_C_0] :  Tag Als.Gait.Walking Added! Time: 39.553555',
    'Component BP_Paddle0.PLStaticMesh TreeBranch with tag Collision.Paddle in actor BP_Paddle0 with tag Entity.Paddle entered 10m! Time: 11.758633',
    'Component BP_Paddle0.PLStaticMesh TreeBranch with tag Collision.Paddle in actor BP_Paddle0 with tag Entity.Paddle entered 2.5m! Time: 11.758633',
    'Component BP_Paddle0.PLStaticMesh TreeBranch with tag Collision.Paddle in actor BP_Paddle0 with tag Entity.Paddle leaved 2.5m! Time: 11.758633'
]

os.environ["OPENAI_API_KEY"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI()


def action_prompt():
    prompt_template = """
    Persona name:{persona_name}
    Age:{age}
    Gender:{gender}
    Job:{job}
    
    Summary of persona's history: 
    {persona_history}
    
    Objects around the persona:
    {objects_around}
    
    Based on the information provided, the most likely action {persona_name} would take next is: 
    """

    persona_name = basic_memory['name']
    age = basic_memory['age']
    gender = basic_memory['gender']
    job = basic_memory['job']
    persona_history = summary_memory["1"]
    objects_around = short_memory["objects"]

    prompt = prompt_template.format(
        persona_name=persona_name,
        age=age,
        gender=gender,
        job=job,
        persona_history=persona_history,
        objects_around=objects_around
    )
    return prompt


def conv_prompt():
    prompt_template = """
    Persona name: <persona_name>
    Age: <age>
    Gender: <gender> 
    Job: <job>
    
    Summary of persona's history:
    <persona_history>  
    
    Current action: 
    <current_action>
    
    Based on the information provided, the most likely conversation <persona_name> would say is:
    """

    persona_name = basic_memory['name']
    age = basic_memory['age']
    gender = basic_memory['gender']
    job = basic_memory['job']
    persona_history = summary_memory["1"]
    current_action = short_memory["currently"]

    prompt = prompt_template.format(
        persona_name=persona_name,
        age=age,
        gender=gender,
        job=job,
        persona_history=persona_history,
        current_action=current_action
    )
    return prompt


def predict_action():
    update_memory(memory=short_memory, logs=logs)
    prompt = action_prompt()

    possible_action = llm.generate(
        prompts=[f"{prompt}"],
        model="text-davinci-003",
        api_type="open_ai"
    )

    print(possible_action.generations[0][0].text)
    return possible_action.generations[0][0].text


def predict_response():
    prompt = conv_prompt()

    possible_conv = llm.generate(
        prompts=[f"{prompt}"],
        model="text-davinci-003",
        api_type="open_ai"
    )

    print(possible_conv.generations[0][0].text)
    return possible_conv.generations[0][0].text


def reflection():
    """
    reflect and update the summary_memory.json
    :return: new memory
    """
    prompt_template = """
        Persona name:{persona_name}
        Age:{age}
        Gender:{gender}
        Job:{job}

        Summary of persona's history: 
        {persona_history}

        events happened recently:
        {events_recently}

        Based on the information provided, summary three most important conclusions for {persona_name} and return the result with json : 
        """

    persona_name = basic_memory['name']
    age = basic_memory['age']
    gender = basic_memory['gender']
    job = basic_memory['job']
    persona_history = summary_memory
    # for event in recent_events:
    #     events_recently = events_recently + event
    events_recently = recent_events

    prompt = prompt_template.format(
        persona_name=persona_name,
        age=age,
        gender=gender,
        job=job,
        persona_history=persona_history,
        events_recently=events_recently
    )

    result = llm.generate(
        prompts=[f"{prompt}"],
        model="text-davinci-003",
        api_type="open_ai"
    )
    print(result.generations[0][0].text)
    return result.generations[0][0].text


if __name__ == '__main__':
    predict_action()
    predict_response()
    reflection()
