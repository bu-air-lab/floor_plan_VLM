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
GoTo(x): Move to location x. This action only works when no doors are in the way.

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
        ('SEJOUR', 'CAVE'),
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
        ('BAINS', 'SEJOUR'),
        ('CHAMBRE 1', 'TERRASSE COUVERTE'),
        ('CUISINE', 'REPAS')
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


#prompt_files = sorted([f for f in os.listdir(prompt_folder) if os.path.isfile(os.path.join(prompt_folder, f))])

# Function to read the content of a text file
# def read_prompt(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             return file.read()
#     except Exception as e:
#         print(f"Error reading prompt file {file_path}: {e}")
#         return None

# Function to read image data
# def read_image(file_path):
#     try:
#         with open(file_path, 'rb') as file:
#             return file.read()
#     except Exception as e:
#         print(f"Error reading image file {file_path}: {e}")
#         return None

# Function to process images and prompts with OpenAI API
# def process_images_and_prompts():
#     for image_file, prompt_file in zip(image_files, prompt_files):
#         image_path = os.path.join(image_folder, image_file)
#         prompt_path = os.path.join(prompt_folder, prompt_file)
        
#         # Read the prompt text
#         prompt_text = read_prompt(prompt_path)
#         if prompt_text is None:
#             continue
        
#         # Read the image file
#         image_data = read_image(image_path)
#         if image_data is None:
#             continue
        
#         # Run the prompt and image through the OpenAI API
#         try:
#             response = openai.Image.create(
#                 prompt=prompt_text,
#                 image=image_data
#             )
            
#             # Save the full JSON response to a file
#             output_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_response.json")
#             with open(output_path, 'w') as output_file:
#                 json.dump(response, output_file, indent=4)
            
#             print(f"Processed image {image_file} and prompt {prompt_file}, response saved to {output_path}")
#         except openai.error.OpenAIError as e:
#             print(f"API request failed for image {image_file} and prompt {prompt_file}: {e}")

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
        temperature=0.0,
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

            #Call VLM
            text_response = query_gpt4o_with_image_and_text(image_path, prompt)
            #print(prompt, image_path, text_response)

            #Write json plan output by VLM to json file
            # Find the start and end of the JSON snippet
            json_start = text_response.find('{')
            json_end = text_response.rfind('}') + 1

            # Extract the JSON snippet
            json_snippet = text_response[json_start:json_end]
            print(text_response)
            print(json_snippet)

            # Load the JSON to validate it (optional but recommended)
            json_data = json.loads(json_snippet)

            # Write the JSON snippet to a new file
            filename = 'output/yellow_labelled/' + key + '_' + start + '_' + end + '.json'
            with open(filename, 'w') as file:
                json.dump(json_data, file, indent=4)

            print("Done with plan:", plan)
        print("Done with", image_file)
        zz

            

        # # Read the prompt text
        # prompt_text = read_prompt(prompt_path)
        # if prompt_text is None:
        #     continue
        
        # # Read the image file
        # image_data = read_image(image_path)
        # if image_data is None:
        #     continue
        
        # # Run the prompt and image through the OpenAI API
        # try:
        #     response = openai.Image.create(
        #         prompt=prompt_text,
        #         image=image_data
        #     )
            
        #     # Save the full JSON response to a file
        #     output_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_response.json")
        #     with open(output_path, 'w') as output_file:
        #         json.dump(response, output_file, indent=4)
            
        #     print(f"Processed image {image_file} and prompt {prompt_file}, response saved to {output_path}")
        # except openai.error.OpenAIError as e:
        #     print(f"API request failed for image {image_file} and prompt {prompt_file}: {e}")

# Run the process
process_images_and_prompts()
