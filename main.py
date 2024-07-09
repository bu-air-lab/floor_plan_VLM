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
image_folder = 'yellow_labelled_areas'

#Output folder for JSON plans from VLM
output_folder = 'output'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of image files
image_files = sorted([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])



prompt_A = """I am a robot that cannot go through walls and must use doors to navigate. This is the floor plan of the building I am in right now (provided as an image). You are a navigation agent, and your task is to give me a detailed, efficient navigation plan that strictly follows a sequence of actions to achieve the navigation task: Begin in the """ 

prompt_B = " and arrive at the " 


prompt_C = """. The only doors which exist are represented as yellow rectangles and labeled as D1-D(n). A plan consists of a sequence of the following actions:
 
ApproachDoor(x): Move in front of door x.
OpenDoor(x): Open door x.
GoThrough(x): Move through open door x to the location on the other side.

Include only the necessary doors that are part of the path being used, and do not mention doors that won't be traversed even if they are in the path. 

Explicit Room and Door Descriptions: Alongside the image, make a clear list of all rooms and doors with their connections - for your reference. 

Remember - the door symbol can overlap with the boundaries or common spaces.

Important: Carefully inspect the floor plan image to ensure the correct correspondence between doors and rooms. Prioritize providing a correct path over the shortest path. Make sure the path avoids any unnecessary doors or rooms. If any unnecessary doors or rooms are included, silently correct the plan before providing the final sequence. Verify the plan's accuracy before finalizing your response. Give the final path in a json format.

"""


# Define the plans
plans = {
    'simple1': [
        ('CH.3', 'CH.1'),
        ('SEJOUR', 'CUISINE'),
        ('CH.2', 'SEJOUR'),
        ('CH.1', 'CH.2'),
        ('CUISINE', 'CH.3')
    ],
    'simple2': [
        ('CH.1', 'GARAGE'),
        ('BAINS', 'HALL'),
        ('GARAGE', 'CH.2'),
        ('HALL', 'CUISINE'),
        ('CUISINE', 'CH.1')
    ],
    'simple3': [
        ('CUISINE', 'DOUCHE'),
        ('CELLIER', 'CH. PARENTS'),
        ('TERRASSE COUVERTE', 'CUISINE'),
        ('DOUCHE', 'CELLIER'),
        ('CH. PARENTS', 'TERRASSE COUVERTE')
    ],
    'medium1': [
        ('CELLIER', 'WC'),
        ('SEJOUR', 'CH.1'),
        ('CUISINE', 'CH.2'),
        ('DEGT.', 'PORCHE'),
        ('WC', 'BAINS')
    ],
    'medium2': [
        ('GARAGE', 'BAINS'),
        ('CHAMBRE 1', 'HALL'),
        ('CELLIER', 'CHAMBRE 3'),
        ('BAINS', 'PORCHE'),
        ('WC', 'CHAMBRE 2')
    ],
    'medium3': [
        ('GARAGES', 'CELLIER'),
        ('DOUCHE', 'CHAMBRE 1'),
        ('CELLIER', 'HALL'),
        ('WC', 'CUISINE'),
        ('CHAMBRE 1', 'GARAGES')
    ],
    'complex1': [
        ('GARAGE', 'CHAMBRE 2'),
        ('CELLIER', 'WC'),
        ('BAINS', 'TERRASSE COUVERTE'),
        ('CHAMBRE 1', 'TERRASSE COUVERTE'),
        ('CUISINE', 'CHAMBRE 1')
    ],
    'complex2': [
        ('GARAGE', 'BAINS'),
        ('CELLIER', 'HALL'),
        ('CHAMBRE 2', 'WC'),
        ('PORCHE', 'CUISINE'),
        ('CHAMBRE 1', 'TERRASSE COUVERTE')
    ],
    'complex3': [
        ('PORCHE', 'LINGERIE'),
        ('BUREAU', 'BAINS'),
        ('CHAMBRE PARENTS', 'CELLIER'),
        ('GARAGE', 'CHAMBRE ENFANT 1'),
        ('HALL', 'CHAMBRE ENFANT 2')
    ]
}

N = 3


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

            for n in range(N):

                #Call VLM
                text_response = query_gpt4o_with_image_and_text(image_path, prompt)

                # Write the text response to a new file
                filename = 'output/yellow_labelled/' + key + '_' + start + '_' + end + '_' + 'trial' + str(n) + '.txt'
                with open(filename, 'w') as file:
                    file.write(text_response)

                print("Done with trial", n)

            print("Done with plan:", plan)

        print("Done with", image_file)

# Run the process
process_images_and_prompts()
