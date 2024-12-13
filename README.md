# Expert_matcher
Expert Matcher leverages LLM and NLP techniques to identify and rank experts based on a project description. It analyzes input data, matches it with expert profiles, and evaluates relevance by skills, experience, and industry fit. The tool provides ranked results with clear justifications, ensuring accuracy,and efficiency in decision-making.

# Requirements and project set up
1) Create a virtual environment with base extension Python 3.12 
   command: conda create -p venv python==3.12
2) Activate the virtual environment using the command "conda activate venv"
3) Install the dependencies provided in requirements.txt by command pip install -r requirements.txt"
# Overview
This project addresses the challenge of identifying and ranking the 100 most relevant experts based on a candidate description. By combining traditional semantic similarity methods with the power of large language models (LLMs), this tool ensures precision, scalability, and detailed ranking explanations.

The approach consists of two stages:
1) Initial Filtering using cosine similarity on embeddings to identify the top 20 resumes.
2) Advanced Scoring by leveraging an LLM to generate relevance scores and explanations for the filtered resumes.

# Project Objectives
The tool is designed to:
Identify relevant experts from a pool of resumes based on a candidate description.
Rank experts with relevance scores from the LLM.
Provide justifications for the ranking, including specific matched skills and qualifications.
Approach
1. Resume Processing
Extract text from resumes (PDF format) using PyPDFLoader.
Ensure clean and structured text data for analysis.
2. Filtering with Semantic Similarity
Convert the candidate description and resume content into high-dimensional embeddings using Sentence Transformers (all-MiniLM-L6-v2).
Compute cosine similarity between the description and each resume.
Select the top 20 resumes based on the highest similarity scores for further evaluation.
3. Advanced Scoring with LLM
Pass the top 20 resumes and the candidate description to a Large Language Model (e.g., OpenAI GPT or similar).
The LLM evaluates each resume against the description to generate:
A relevance score (on a scale of 0–100).
A detailed explanation for the score, highlighting matched skills, qualifications, and experiences.
4. Ranking and Justification
Rank the 20 resumes based on LLM-generated scores.
Provide an output JSON with detailed explanations for the ranking.

# Technologies Used
Programming Language: Python
Libraries and Tools:
PyPDFLoader: Extract text from PDF resumes.
Sentence Transformers: Generate embeddings for semantic similarity.
Cosine Similarity (from scikit-learn): Filter top candidates.
Large Language Model (LLM): Perform advanced scoring and generate explanations.
JSON: Structured input/output data.


