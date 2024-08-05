import os
import json
import base64
from anthropic import Anthropic

# Set your Anthropic API key
with open("api_key.txt", "r") as file:
    anthropic_api_key = file.read().strip()

# Anthropic client
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
anthropic_client = Anthropic()

# Folder to images dataset
image_folder = 'updated_v2'

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

prompt_B = ", then go to "

prompt_C = ", then arrive at " 

prompt_D = """. The only doors which exist are represented as yellow rectangles and labeled with  'D(N)' distinct positive integers(1,2,3...N). A plan consists of a sequence of the following actions:
 
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
    "simple1": [
        ('CH.3', 'CH.2', 'CH.1'), 
        ('CUISINE', 'CH.2', 'CH.1'), 
        ('CUISINE', 'CH.3', 'SEJOUR'), 
        ('CUISINE', 'SEJOUR', 'CH.2'), 
        ('CH.1', 'CH.2', 'SEJOUR')
    ],
    "simple2": [
        ('CH.1', 'CH.2', 'BAINS'), 
        ('BAINS', 'CUISINE', 'CH.2'), 
        ('BAINS', 'CUISINE', 'GARAGE'), 
        ('BAINS', 'CUISINE', 'CH.1'), 
        ('CH.2', 'HALL', 'GARAGE')
    ],
    "simple3": [
        ('TERRASSE COUVERTE', 'CH. PARENTS', 'CUISINE'), 
        ('CH. PARENTS', 'CUISINE', 'DOUCHE'), 
        ('DOUCHE', 'TERRASSE COUVERTE', 'CELLIER'), 
        ('TERRASSE COUVERTE', 'CH. PARENTS', 'DOUCHE'), 
        ('CELLIER', 'DOUCHE', 'TERRASSE COUVERTE')
    ],
     "medium1": [
        ('DEGT.', 'CH.2', 'CH.1'), 
        ('PORCHE', 'CH.1', 'CH.2'), 
        ('CH.1', 'CELLIER', 'BAINS'), 
        ('DEGT.', 'CUISINE', 'SEJOUR'), 
        ('DEGT.', 'PORCHE', 'CUISINE')
    ],
    "medium2": [
        ('HALL', 'CELLIER', 'GARAGE'), 
        ('BAINS', 'CHAMBRE 2', 'WC'), 
        ('CHAMBRE 1', 'BAINS', 'GARAGE'), 
        ('HALL', 'CHAMBRE 1', 'CHAMBRE 2'), 
        ('CHAMBRE 3', 'BAINS', 'HALL')
    ],
    "medium3": [
        ('HALL', 'GARAGES', 'CHAMBRE 1'), 
        ('CHAMBRE 1', 'HALL', 'CELLIER'), 
        ('DOUCHE', 'CHAMBRE 1', 'HALL'), 
        ('CHAMBRE 1', 'CELLIER', 'GARAGES'), 
        ('CUISINE', 'DOUCHE', 'HALL')
    ],
     "complex1": [
        ('CUISINE', 'CELLIER', 'GARAGE'), 
        ('CUISINE', 'PORCHE', 'BAINS'), 
        ('CHAMBRE 2', 'PORCHE', 'BAINS'), 
        ('CELLIER', 'HALL', 'CHAMBRE 1'), 
        ('GARAGE', 'CHAMBRE 1', 'CHAMBRE 2')
    ],
    "complex2": [
        ('CHAMBRE 2', 'GARAGE', 'CELLIER'), 
        ('CHAMBRE 1', 'TERRASSE COUVERTE', 'HALL'), 
        ('CHAMBRE 2', 'HALL', 'PORCHE'), 
        ('CHAMBRE 2', 'GARAGE', 'CHAMBRE 1'), 
        ('CHAMBRE 2', 'WC', 'GARAGE')
    ],
    "complex3": [
        ('CHAMBRE ENFANT 1', 'BAINS', 'CHAMBRE PARENTS'), 
        ('GARAGE', 'CELLIER', 'WC'), 
        ('BAINS', 'CHAMBRE ENFANT 2', 'GARAGE'), 
        ('BAINS', 'CHAMBRE ENFANT 1', 'CHAMBRE ENFANT 2'), 
        ('BUREAU', 'HALL', 'CHAMBRE ENFANT 1')
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

def query_anthropic_with_image_and_text(image_path, text_prompt):
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

    response = anthropic_client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=message_list
    )

    return response.content[0].text

def process_images_and_prompts():
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)

        key = image_file[:-4]
        
        
        if key not in plans:
            continue

        for plan in plans[key]:
            start = plan[0]
            middle = plan[1]
            end = plan[2]

            prompt = prompt_A + start + prompt_B + middle + prompt_C + end + prompt_D

            for n in range(N):
                # Call VLM
                text_response = query_anthropic_with_image_and_text(image_path, prompt)

                # Write the text response to a new file
                filename = 'output/v2_results_3point_claude/' + key + '_' + start + '_' + middle + '_' + end + '_' + 'trial' + str(n) + '.txt'
                with open(filename, 'w') as file:
                    file.write(text_response)

                print("Done with trial", n)

            print("Done with plan:", plan)

        print("Done with", image_file)

# Run the process
process_images_and_prompts()
