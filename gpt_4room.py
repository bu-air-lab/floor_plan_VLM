import os
from openai import OpenAI 
import json
import base64

# Set your OpenAI API key
api_key_file = open("api_key.txt", "r+")
api_key = api_key_file.read()
api_key_file.close()

client = OpenAI(api_key=api_key)

#Folder to images dataset
image_folder = 'maps/dense_labels'

#Output folder for JSON plans from VLM
output_folder = 'output'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of image files
image_files = sorted([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])


#------------------------------------------------------PROMPT------------------------------------------------------#

prompt_A = """I am a robot that cannot go through walls and must use doors to navigate. This is the floor plan of the building I am in right now (provided as an image). 

You are a navigation agent, and your task is to give me a detailed, efficient navigation plan that strictly follows a sequence of actions to achieve the navigation task: Begin in the """

prompt_B = " and arrive at the "

prompt_C = """. The only doors which exist are represented as yellow rectangles and labeled with  'D(N)' distinct positive integers(1,2,3...N). A plan consists of a sequence of the following actions:
 
ApproachDoor(x): Move in front of door x.
OpenDoor(x): Open door x.
GoThrough(x): Move through open door x to the location on the other side.

Include only the necessary doors that are part of the path being used, and do not mention doors that won't be traversed even if they are in the path. 

Explicit Room and Door Descriptions: Alongside the image, make a clear list of all rooms and doors with their connections - which is to be used for the navigation task. 

Remember that the door symbol can overlap with the boundaries or common spaces. Remember to only use the generated door room connections for making the action plan.  Double-check if each action is necessary and correct for traversal to the end goal. Common spaces (eg Hall) and larger rooms may have multiple instances of the same labels to help you understand their boundaries.

Important: The doors close after every GoThrough(x) action. Carefully inspect the floor plan image to ensure the correct correspondence between doors and rooms. Prioritize providing a correct path over the shortest path. Make sure the path avoids any unnecessary doors or rooms. If any unnecessary doors or rooms are included, silently correct the plan before providing the final sequence. Give the final path in a json format.

Remember to make explicit connections for each door, then make a step by step solution for each navigation step and ONLY use the door-room connections to generate the final navigation plan. 
"""


# Define the plans
plans = {
    '1': [
        ('CELLIER', 'TERRASSE COUVERTE'),
        ('GARAGE', 'WC'),
        ('PORCHE', 'GARAGE'),
        ('TERRASSE COUVERTE', 'CHAMBRE 1'),
        ('BAINS', 'GARAGE')
    ],
    '2': [
        ('PORCHE', 'BAINS'),
        ('DEGT', 'CELLIER'),
        ('CUISINE', 'CH.2'),
        ('WC', 'PORCHE'),
        ('CH.1', 'CUISINE')
    ],
    '3': [
        ('GARAGE', 'BUREAU'),
        ('LINGERIE', 'GARAGE'),
        ('GARAGE', 'CHAMBRE ENFANT 1'),
        ('CHAMBRE PARENTS', 'GARAGE'),
        ('GARAGE', 'WC')
    ],
    '4': [
        ('CELLIER', 'TERRASSE COUVERTE'),
        ('GARAGE', 'WC'),
        ('TERRASSE COUVERTE', 'GARAGE 1'),
        ('BAINS 1', 'CUISINE'),
        ('CELLIER 1', 'TERRASSE COUVERTE 1')
    ],
    '5': [
        ('PORCHE', 'BAINS'),
        ('DEGT', 'CELLIER'),
        ('DEGT 1', 'DEGT'),
        ('CUISINE 1', 'CELLIER'),
        ('WC 1', 'CH.2')
    ],
    '6': [
        ('GARAGE', 'BUREAU'),
        ('LINGERIE', 'GARAGE'),
        ('CHAMBRE ENFANT 11', 'HALL'),
        ('PORCHE 1', 'CELLIER'),
        ('WC', 'HALL 1')
    ],
}

N = 10


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

# Function to query GPT-4o with a text prompt and an image
# Written with help from https://github.com/openai/openai-cookbook/blob/main/examples/gpt4o/introduction_to_gpt4o.ipynb
def query_gpt4o_with_image_and_text(image_path, text_prompt):

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful navigation assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": text_prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.1,
    )

    text_response = response.choices[0].message.content
    return text_response

def process_images_and_prompts():

    for image_file in image_files:

        image_path = os.path.join(image_folder, image_file)
        
        #Loop through all trials
        #for key in plans.keys():
        key = image_file[:-4]

        for plan in plans[key]:

            start = plan[0]
            end = plan[1]

            prompt = prompt_A + start + prompt_B + end + prompt_C

            for n in range(3, N):

                #Call VLM
                text_response = query_gpt4o_with_image_and_text(image_path, prompt)

                # Write the text response to a new file
                filename = 'output/4room_GPT/' + key + '_' + start + '_' + end + '_' + 'trial' + str(n) + '.txt'
                with open(filename, 'w') as file:
                    file.write(text_response)

                print("Done with trial", n)

            print("Done with plan:", plan)

        print("Done with", image_file)

# Run the process
process_images_and_prompts()
