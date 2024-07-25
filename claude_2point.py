import os
import json
import base64
from anthropic import Anthropic

# Set your Anthropic API key
api_key_file = open("api_key.txt", "r+")
API_KEY = api_key_file.read().strip()
api_key_file.close()

os.environ["ANTHROPIC_API_KEY"] = API_KEY
client = Anthropic()

# Folder to images dataset
image_folder = 'floorplan_dataset_v4'

# Output folder for JSON plans from VLM
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

Remember - the door symbol can overlap with the boundaries or common spaces. Remember to only use the generated door room connections for making the action plan.  Double-check if each action is necessary and correct for traversal to the end goal. Common spaces (eg Hall) and larger rooms may have multiple instances of the same labels to help you understand their boundaries.

Important: The doors close after every GoThrough(x) action. Carefully inspect the floor plan image to ensure the correct correspondence between doors and rooms. Prioritize providing a correct path over the shortest path. Make sure the path avoids any unnecessary doors or rooms. If any unnecessary doors or rooms are included, silently correct the plan before providing the final sequence. Give the final path in a json format.

Remember to make explicit connections for each door,then make a step by step solution for each navigation and ONLY use the door-room connections to generate the navigation path. 
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
MODEL_NAME = "claude-3-5-sonnet-20240620"
MAX_TOKENS = 2048

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        return base64_string

def query_claude_with_image_and_text(image_path, text_prompt):
    media_type = f"image/{image_path.split('.')[-1]}"
    
    message_list = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image", 
                    "source": {
                        "type": "base64", 
                        "media_type": media_type, 
                        "data": get_base64_encoded_image(image_path)
                    }
                },
                {"type": "text", "text": text_prompt}
            ]
        }
    ]

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=message_list
    )

    return response.content[0].text

def process_images_and_prompts():
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
        key = image_file[:-4]

        for plan in plans[key]:
            start, end = plan

            prompt = prompt_A + start + prompt_B + end + prompt_C

            for n in range(N):
                # Call Claude API
                text_response = query_claude_with_image_and_text(image_path, prompt)

                # Write the text response to a new file
                filename = f'output/v4_results_2point_claude/{key}_{start}_{end}_trial{n}.txt'
                with open(filename, 'w') as file:
                    file.write(text_response)

                print(f"Done with trial {n}")
                

            print(f"Done with plan: {plan}")
            

        print(f"Done with {image_file}")

# Run the process
process_images_and_prompts()