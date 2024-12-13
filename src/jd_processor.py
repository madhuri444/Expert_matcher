import os
from dotenv import load_dotenv
from groq import Groq
from docx import Document  # To read Word documents

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# System prompt to guide the LLM
system_prompt = """
You are an expert in analyzing job descriptions and extracting key information.
Your task is to extract the following key aspects from any given job description:
1. Job Title
2. Required Skills
3. Key Responsibilities
4. Qualifications
5. Experience Level (e.g., entry-level, mid-level, senior-level)
6. Industry
7. Location

Return strictly json  structure nothing else
Dont return these ``` in json file


"""

def extract_key_aspects(jd_text):
    """
    Extract key aspects from a job description using Groq LLM.
    
    Args:
        jd_text (str): The job description text.
    
    Returns:
        str: Extracted key aspects in JSON format.
    """
    # Prompt Groq LLM to analyze the job description
    response = groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",  # Groq model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": jd_text},
        ]
    )

    # Extract response content
    return response.choices[0].message.content

def read_word_document(file_path):
    """
    Read text content from a Word (.docx) document.
    
    Args:
        file_path (str): Path to the Word document.
    
    Returns:
        str: Text content of the document.
    """
    doc = Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return "\n".join(content)

def process_jd_folder(folder_path, output_folder):
    """
    Process all Word job description files in a folder, extract key aspects, and save results.
    
    Args:
        folder_path (str): Path to the folder containing job descriptions.
        output_folder (str): Path to the folder where extracted key aspects will be saved.
    """
    # Ensure the output folder exists
    #os.makedirs(output_folder, exist_ok=True)
    # if not os.path.isdir(output_folder):
    #     os.makedirs(output_folder, exist_ok=True)
    # Iterate over all .docx files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".docx"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            
            # Read the JD text from the Word document
            jd_text = read_word_document(file_path)
            
            # Extract key aspects using Groq
            key_aspects = extract_key_aspects(jd_text)
            
            # Save the extracted key aspects to a JSON file
            #output_file = os.path.splitext(file_name)[0] + "_key_aspects.json"
            # output_path = os.path.join(output_folder, output_file)
            # print(output_path)
            
            with open(output_folder, "w") as f:
                f.write(key_aspects)
            
            print(f"Key aspects saved to: {output_folder}")

