import os
import json
import pandas as pd
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# System prompt for ranking resumes
system_prompt = """
You are an expert in analyzing resumes based on job descriptions.
For each resume, assign:
1. A relevance score (0-100).
2. Matched technical skills. Eg(Python, Machine learning)
3. Industry experience (number of years)
4. Qualification(Educational background eg: Masters, bachelors)
5. A detailed explanation of why the resume matches the job description.


Return strictly json  structure nothing else
Dont return these ``` in json file
"""

def read_resumes_from_folder(folder_path):
    resumes = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file_name))
            documents = loader.load()
            content = " ".join([doc.page_content for doc in documents])
            resumes.append({"file_name": file_name, "content": content})
    return resumes

def generate_embeddings(text_list, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    return model.encode(text_list)

def initial_filtering(jd_text, resumes, top_n=20):
    jd_embedding = generate_embeddings([jd_text])[0]
    resume_texts = [resume["content"] for resume in resumes]
    resume_embeddings = generate_embeddings(resume_texts)

    similarity_scores = cosine_similarity([jd_embedding], resume_embeddings)[0]
    for i, score in enumerate(similarity_scores):
        resumes[i]["similarity_score"] = score

    return sorted(resumes, key=lambda x: x["similarity_score"], reverse=True)[:top_n]

def rank_with_llm(jd_text, resumes):
    resumes_text = "\n\n".join([f"Resume {i+1}:\n{resume['content']}" for i, resume in enumerate(resumes)])
    prompt = f"{system_prompt}\n\nJob Description:\n{jd_text}\n\nResumes:\n{resumes_text}"
    
    response = groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def process_resumes(jd_file, resumes_folder, output_file, top_n=20):
    with open(jd_file, "r") as f:
        #content = f.read()
        jd_key_aspects = json.load(f) # Assuming the first JD is used for simplicity

    jd_text = (
        f"Job Title: {jd_key_aspects['Job Title']}\n"
        f"Required Skills: {', '.join(jd_key_aspects['Required Skills'])}\n"
        f"Key Responsibilities: {', '.join(jd_key_aspects['Key Responsibilities'])}\n"
        f"Qualifications: {', '.join(jd_key_aspects['Qualifications'])}\n"
        f"Industry: {jd_key_aspects['Industry']}\n"
        f"Experience Level: {jd_key_aspects['Experience Level']}\n"
    )

    resumes = read_resumes_from_folder(resumes_folder)
    top_resumes = initial_filtering(jd_text, resumes, top_n=top_n)
    ranked_resumes = rank_with_llm(jd_text, top_resumes)

    with open(output_file, "w") as f:
        #ranked_resumes = json.load(ranked_resumes)
        print(type(ranked_resumes))
        output = json.loads(ranked_resumes)
        json.dump(output, f, indent=4)
    print(f"Ranked resumes saved to {output_file}")
