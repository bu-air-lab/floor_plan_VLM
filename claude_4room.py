import os
import base64
import time
import random
from anthropic import Anthropic

# Set your Anthropic API key
with open("api_key.txt", "r") as api_key_file:
    API_KEY = api_key_file.read().strip()

os.environ["ANTHROPIC_API_KEY"] = API_KEY
client = Anthropic()

# Folder to images dataset
image_folder = 'maps/sparse_labels'

# Output folder for JSON plans from VLM
output_folder = 'output/4room_claude_sparse'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

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

MODEL_NAME = "claude-3-5-sonnet-20240620"
MAX_TOKENS = 2048

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def query_claude_with_image_and_text(image_path, text_prompt, max_retries=5, initial_delay=1):
    retries = 0
    while retries < max_retries:
        try:
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
        except Exception as e:
            retries += 1
            if retries == max_retries:
                print(f"Max retries reached for query. Error: {e}")
                return None
            delay = initial_delay * (2 ** retries) + random.uniform(0, 1)
            print(f"Error: {e}. Retrying in {delay:.2f} seconds...")
            time.sleep(delay)

def process_images_and_prompts():
    for image_file in image_files:      
        image_path = os.path.join(image_folder, image_file)
        
        key = image_file[:-4]

        if key not in plans:
            print(f"No plan found for image {image_file}. Skipping.")
            continue

        for plan in plans[key]:
            start, end = plan

            prompt = prompt_A + start + prompt_B + end + prompt_C

            for n in range(N):
                # Call Claude API
                text_response = query_claude_with_image_and_text(image_path, prompt)

                if text_response is None:
                    print(f"Failed to get response for {image_file}, plan {plan}, trial {n}")
                    continue

                # Write the text response to a new file
                filename = f'{output_folder}/{key}_{start}_{end}_trial{n}.txt'
                with open(filename, 'w') as file:
                    file.write(text_response)

                print(f"Done with trial {n}")                   
                
            print(f"Done with plan: {plan}")
            
        print(f"Done with {image_file}")

# Run the process
process_images_and_prompts()
print("Done with processing all images.")