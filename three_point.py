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

prompt_B = ", then go to "

prompt_C = ", then arrive at " 


prompt_D = """. The only doors which exist are represented as yellow rectangles and labeled as D1-D(n). A plan consists of a sequence of the following actions:
 
ApproachDoor(x): Move in front of door x.
OpenDoor(x): Open door x.
GoThrough(x): Move through open door x to the location on the other side.

Include only the necessary doors that are part of the path being used, and do not mention doors that won't be traversed even if they are in the path. 

Explicit Room and Door Descriptions: Alongside the image, make a clear list of all rooms and doors with their connections - for your reference. 

Remember - the door symbol can overlap with the boundaries or common spaces.

Important: The doors close after every GoThrough(x) action. Carefully inspect the floor plan image to ensure the correct correspondence between doors and rooms. Prioritize providing a correct path over the shortest path. Make sure the path avoids any unnecessary doors or rooms. If any unnecessary doors or rooms are included, silently correct the plan before providing the final sequence. Verify the plan's accuracy before finalizing your response. Give the final path in a json format.

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
    "medium1": [
        ('DEGT.', 'CH.2', 'CH.1'), 
        ('PORCHE', 'CH.1', 'CH.2'), 
        ('CH.1', 'CELLIER', 'BAINS'), 
        ('DEGT.', 'CUISINE', 'SEJOUR'), 
        ('DEGT.', 'PORCHE', 'CUISINE')
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
    ],
    "simple2": [
        ('CH.1', 'CH.2', 'BAINS'), 
        ('BAINS', 'CUISINE', 'CH.2'), 
        ('BAINS', 'CUISINE', 'GARAGE'), 
        ('BAINS', 'CUISINE', 'CH.1'), 
        ('CH.2', 'HALL', 'GARAGE')
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
    "simple3": [
        ('TERRASSE COUVERTE', 'CH. PARENTS', 'CUISINE'), 
        ('CH. PARENTS', 'CUISINE', 'DOUCHE'), 
        ('DOUCHE', 'TERRASSE COUVERTE', 'CELLIER'), 
        ('TERRASSE COUVERTE', 'CH. PARENTS', 'DOUCHE'), 
        ('CELLIER', 'DOUCHE', 'TERRASSE COUVERTE')
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

		if(key == 'simple2'):

			for plan in plans[key]:

				start = plan[0]
				middle = plan[1]
				end = plan[2]

				prompt = prompt_A + start + prompt_B + middle + prompt_C + end + prompt_D

				for n in range(N):

					#Call VLM
					text_response = query_gpt4o_with_image_and_text(image_path, prompt)

					# Write the text response to a new file
					filename = 'output/yellow_labelled/3_point_navigation/' + key + '_' + start + '_' + middle + '_' + end + '_' + 'trial' + str(n) + '.txt'
					with open(filename, 'w') as file:
						file.write(text_response)

					print("Done with trial", n)

				print("Done with plan:", plan)

			print("Done with", image_file)

# Run the process
process_images_and_prompts()