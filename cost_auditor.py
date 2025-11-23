import requests
import json
import os
import time
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
MAX_RETRIES = 5

def generate_analysis_payload(plan_diff: str) -> dict:
    """Constructs the API payload for the IaC change analysis."""
    
    # The system instruction guides the LLM to act as a dual FinOps/Security Analyst
    system_prompt = (
        "You are a specialized DevSecOps and FinOps analyst. Your task is to analyze the "
        "raw Terraform Plan diff provided below. You must identify all changes, categorize the "
        "type of infrastructure change (Add, Update, Destroy), provide a high-level cost "
        "forecast for the changes, and flag any unexpected or risky 'drift' from security standards. "
        "Generate the findings in the exact JSON format specified in the schema."
    )

    # The user query provides the content
    user_query = (
        "Analyze the following Terraform Plan output. Provide a summary, cost impact, and security "
        "notes based on the changes.\n\n---\n"
        f"{plan_diff}\n---"
    )

    # Define the strict JSON schema for the output report
    analysis_schema = {
        "type": "OBJECT",
        "properties": {
            "summary": {"type": "STRING", "description": "A high-level summary of the resources being added, modified, or destroyed."},
            "cost_impact": {"type": "STRING", "description": "A financial forecast for the infrastructure changes (e.g., '$500 Monthly Increase', '$100 Monthly Reduction', 'Minimal Change')."},
            "critical_changes_found": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "resource_name": {"type": "STRING"},
                        "change_type": {"type": "STRING", "description": "ADD, UPDATE, or DESTROY"},
                        "risk_or_cost_note": {"type": "STRING", "description": "Note on security drift or significant cost implication."}
                    }
                }
            }
        },
        "required": ["summary", "cost_impact", "critical_changes_found"]
    }

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": analysis_schema
        }
    }
    return payload

def call_gemini_api(payload: dict) -> dict:
    """Calls the Gemini API with exponential backoff for resilience."""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                API_URL, 
                headers={'Content-Type': 'application/json'}, 
                data=json.dumps(payload)
            )
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            
            if (result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts')):
                
                json_text = result['candidates'][0]['content']['parts'][0]['text']
                return json.loads(json_text)
            
            print(f"Attempt {attempt + 1}: API response received but no valid content found.")
            time.sleep(2 ** attempt)
        
        except requests.exceptions.HTTPError as e:
            print(f"Attempt {attempt + 1}: HTTP error occurred: {e}. Retrying...")
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Attempt {attempt + 1}: An unexpected error occurred: {e}. Retrying...")
            time.sleep(2 ** attempt)

    print("--- [FAILURE] Max retries reached. Could not complete API call. ---")
    return {}

def print_audit_summary(results: dict):
    """Prints the combined audit summary in a human-readable format."""
    print("\n--- AI-Driven IaC Cost and Drift Analyzer Report ---")
    if not results:
        print("[FAILURE] No analysis results available.")
        return

    print(f"\n[SUMMARY]: {results.get('summary', 'N/A')}")
    
    # Emphasize the FinOps forecast
    print(f"\n[FINOPS COST FORECAST]:")
    print(f"  --> {results.get('cost_impact', 'N/A')}")
    
    # Show the critical changes and security/drift notes
    print(f"\n[DEVOPS DRIFT/RISK NOTES] (Total Critical Changes: {len(results.get('critical_changes_found', []))}):")
    for change in results.get('critical_changes_found', []):
        print(f"  - RESOURCE: {change.get('resource_name', 'N/A')} ({change.get('change_type', 'N/A')})")
        print(f"    NOTE: {change.get('risk_or_cost_note', 'No note provided.')}")
    print("-" * 60)

def main():
    """Main function to run the IaC cost and drift auditor."""
    if not API_KEY:
        print("--- [ERROR] GEMINI_API_KEY not found. Please ensure your .env file is configured. ---")
        return
        
    try:
        # 1. Read the Terraform plan diff from the file
        diff_filepath = 'terraform_plan_diff.txt'
        with open(diff_filepath, 'r') as f:
            plan_diff = f.read()
        
        print(f"--- Analyzing Terraform Plan Diff file: {diff_filepath} ({len(plan_diff)} bytes) ---")
        
        # 2. Generate the API payload and get structured JSON analysis
        analysis_results = call_gemini_api(generate_analysis_payload(plan_diff))
        
        # 3. Save the raw JSON output (for integration into other tools)
        output_filename = 'cost_drift_report.json'
        with open(output_filename, 'w') as f:
            json.dump(analysis_results, f, indent=2)
            
        print(f"\n[SUCCESS] Structured JSON report saved to '{output_filename}'.")
        
        # 4. Print a human-readable summary
        print_audit_summary(analysis_results)
        
    except FileNotFoundError:
        print(f"--- [ERROR] File not found: '{diff_filepath}'. Ensure 'terraform_plan_diff.txt' exists. ---")
    except Exception as e:
        print(f"--- [CRITICAL ERROR] Failed to run auditor: {e} ---")

if __name__ == "__main__":
    main()
