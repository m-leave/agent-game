import json
import os
from langchain import OpenAI
from memory import update_memory

# load the person's memory
with open('scrath_memory.json') as f:
    scrath_memory = json.load(f)

# load the short memory
with open('short_memory.json') as f:
    short_memory = json.load(f)

# get actions can be done
actions = [
    "swim",
    "walk",
    "boat",
    "rest",
    "bulid a fire",
    "bulid a shelter"
]

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

os.environ["OPENAI_API_KEY"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI()


def predict_action():
    latest_memory = update_memory(scrath_memory=scrath_memory, logs=logs)
    name = latest_memory["name"]
    age = latest_memory["age"]
    innate = latest_memory["innate"]
    learned = latest_memory["learned"]
    currently = short_memory["currently"]
    objects = short_memory["objects"]

    possible_action = llm.generate(
        prompts=[
            f"{learned}, {name} is {innate}, {name} is {currently} and there are just {objects} nearby, give me the most possible action {name} will do, response with the following options:{actions}"],
        model="text-davinci-003",
        api_type="open_ai"
    )

    print(possible_action.generations[0][0].text)
    return possible_action.generations[0][0].text


def predict_response():
    name = scrath_memory["name"]
    innate = scrath_memory["innate"]
    learned = scrath_memory["learned"]
    currently = short_memory["currently"]

    possible_response = llm.generate(
        prompts=[
            f"{learned}, {name} is {innate}, {name} is {currently} , give me the most possible response {name} will say, the response should longer than 10 words."],
        model="text-davinci-003",
        api_type="open_ai"
    )

    print(possible_response.generations[0][0].text)
    return possible_response.generations[0][0].text


if __name__ == '__main__':
    predict_action()
    predict_response()
