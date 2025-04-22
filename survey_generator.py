##Set Parameters
import pandas as pd
import requests
import json
import re
import os

# Variables for local LLM Studio server instance
# GPT4ALL_API_URL = "http://localhost:1234/v1/chat/completions"
GPT4ALL_API_URL = "https://7cc2-129-130-19-169.ngrok-free.app/v1/chat/completions"
API_HEADERS = {"Content-Type": "application/json"}



generic_template = pd.read_csv('./output/GenericSurvey.csv')


low_match_csv_path = "output/low_matched_survey_questions.csv"
medium_match_csv_path = "./output/medium_matched_survey_questions.csv"
high_match_csv_path = "./output/high_matched_survey_questions.csv"
# load matches
high_df = pd.read_csv(high_match_csv_path);
medium_df = pd.read_csv(medium_match_csv_path);
low_df = pd.read_csv(low_match_csv_path);



def generate_survey_json(questions):
    # Convert the list of questions into a formatted string.
    # Each question is prefixed with a hyphen for clarity.
    question_list_str = "\n".join(f"- {q}" for q in questions)
    
    prompt = [
        { 
          "role": "system", 
          "content": (
              "You are an AI that rewrites survey questions into a more generic, "
              "broadly applicable format. Make them concise while preserving key context. "
              "Analyze the following list of questions, avoid redundancy, and generate a minimal set "
              "of generic questions that cover the diverse topics present."
          )
        },
        { 
          "role": "user", 
          "content": (
              "Generate an array of generic survey questions based on the following list of questions. "
              "For each generic question, generate a set of clear, concise multiple-choice answer options. \n\n"
              "**DO NOT include explanations, comments, notes, hints, or any extra text. "
              "Return ONLY a valid JSON array.**\n\n"
              "**Strict JSON Output Format (DO NOT MODIFY):**\n"
              "[\n"
              "  {\n"
              "    \"group\": \"Refined group/category of question e.g perception, maitenence, security,parks and recreation, satisfaction etc.\",\n"
              "    \"question\": \"Your rephrased generic question\",\n"
              "    \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\", \"Option 5\"]\n"
              "  },\n"
              "  { ... }, ...\n"
              "]\n\n"
              "**Input Questions:**\n"
              f"{question_list_str}"
          )
        }
    ]
    payload = {
            "model": "llama-3.2-3b-instruct",
            "messages": prompt,
            "temperature": 0.7,
            # "max_tokens": -1,
        }
    try:
        response = requests.post(GPT4ALL_API_URL, headers=API_HEADERS, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad status codes.
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]

        # Extract either a JSON array or JSON object using regex.
        json_match = re.search(r'(\[.*\]|\{.*\})', response_text, re.DOTALL)
        if json_match:
            json_output = json_match.group(0).strip()
            data = json.loads(json_output)
            return data
        else:
            print(f"❌ Invalid JSON response: {response_text}")
            return None

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error generating survey JSON: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"❌ JSON decoding error: {json_err}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error generating survey JSON: {e}")
        return None
    
def generate_new_questions(questions):
    new_questions_data = []
    llm_response = generate_survey_json(questions)
    for new_question_data in llm_response:
        new_questions_data.append({
            "question_group": new_question_data.get("group"),
            "generic_question": new_question_data.get("question"),
            # "question_tail_prompt": None,
            **{f"option_{i+1}": new_question_data["options"][i] if i < len(new_question_data["options"]) else None for i in range(7)}
        })
    return new_questions_data




def update_survey(row):
    generic_template = pd.read_csv('./output/GenericSurvey.csv')
    print("Row",row)
    new_questions_df = pd.DataFrame([row])
    print("new_questions_df", new_questions_df)
    # Append the new questions to the generic survey template.
    updated_survey_df = pd.concat([generic_template, new_questions_df], ignore_index=True)
    # Save the updated template.
    updated_survey_path = "./output/GenericSurvey.csv"
    updated_survey_df.to_csv(updated_survey_path, index=False)
    return True
