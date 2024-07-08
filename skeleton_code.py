import os
import openai
import json

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY_HERE'

# Define paths to the image and prompt folders
image_folder = '/path/to/images'
prompt_folder = '/path/to/prompts'
output_folder = '/path/to/output'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of image and prompt files
image_files = sorted([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])
prompt_files = sorted([f for f in os.listdir(prompt_folder) if os.path.isfile(os.path.join(prompt_folder, f))])

# Function to read the content of a text file
def read_prompt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading prompt file {file_path}: {e}")
        return None

# Function to read image data
def read_image(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading image file {file_path}: {e}")
        return None

# Function to process images and prompts with OpenAI API
def process_images_and_prompts():
    for image_file, prompt_file in zip(image_files, prompt_files):
        image_path = os.path.join(image_folder, image_file)
        prompt_path = os.path.join(prompt_folder, prompt_file)
        
        # Read the prompt text
        prompt_text = read_prompt(prompt_path)
        if prompt_text is None:
            continue
        
        # Read the image file
        image_data = read_image(image_path)
        if image_data is None:
            continue
        
        # Run the prompt and image through the OpenAI API
        try:
            response = openai.Image.create(
                prompt=prompt_text,
                image=image_data
            )
            
            # Save the full JSON response to a file
            output_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_response.json")
            with open(output_path, 'w') as output_file:
                json.dump(response, output_file, indent=4)
            
            print(f"Processed image {image_file} and prompt {prompt_file}, response saved to {output_path}")
        except openai.error.OpenAIError as e:
            print(f"API request failed for image {image_file} and prompt {prompt_file}: {e}")

# Run the process
process_images_and_prompts()
