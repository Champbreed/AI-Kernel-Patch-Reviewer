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

def generate_policy_payload(security_request: str) -> dict:
    """Constructs the API payload for K8s configuration and policy generation."""
    
    # System instruction guides the LLM to act as a K8s Security Expert
    system_prompt = (
        "You are a Kubernetes Security Architect specializing in hardening deployments. "
        "The user will provide a high-level security requirement. You MUST generate two outputs: "
        "1) A complete, hardened Kubernetes Deployment YAML that satisfies the request. "
        "2) A summary of the rule implemented, suitable for a policy engine (e.g., OPA or Kube-bench). "
        "Generate the findings in the exact JSON format specified in the schema."
    )

    # User query includes the policy to be enforced
    user_query = (
        "Based on the following security requirement, generate a hardened Kubernetes Deployment YAML "
        "for a basic Nginx container, and summarize the enforcement rule:\n\n"
        f"SECURITY REQUIREMENT: {security_request}"
    )

    # Define the strict JSON schema for the output report
    # The YAML content will be returned as a string inside the JSON object
    policy_schema = {
        "type": "OBJECT",
        "properties": {
            "policy_summary": {
                "type": "STRING", 
                "description": "A concise, single-sentence summary of the security rule that was enforced (e.g., 'All containers must run as non-root user and use read-only filesystems')."
            },
            "hardened_kubernetes_yaml": {
                "type": "STRING", 
                "description": "The complete, hardened Kubernetes Deployment YAML, including securityContext fields to meet the requirement. MUST be a valid YAML string."
            }
        },
        "required": ["policy_summary", "hardened_kubernetes_yaml"]
    }

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": policy_schema
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
            response.raise_for_status()

            result = response.json()
            
            if (result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts')):
                
                json_text = result['candidates'][0]['content']['parts'][0]['text']
                return json.loads(json_text)
            
            print(f"Attempt {attempt + 1}: API response received but no valid content found. Retrying...")
            time.sleep(2 ** attempt)
        
        except requests.exceptions.HTTPError as e:
            print(f"Attempt {attempt + 1}: HTTP error occurred: {e}. Retrying...")
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Attempt {attempt + 1}: An unexpected error occurred: {e}. Retrying...")
            time.sleep(2 ** attempt)

    print("--- [FAILURE] Max retries reached. Could not complete API call. ---")
    return {}

def main():
    """Main function to run the K8s security policy generator."""
    if not API_KEY:
        print("--- [ERROR] GEMINI_API_KEY not found. Please ensure your .env file is configured. ---")
        return
        
    try:
        # 1. Read the policy request from the file
        request_filepath = 'security_request.txt'
        with open(request_filepath, 'r') as f:
            security_request = f.read().strip()
        
        print(f"--- Analyzing Security Request: '{security_request}' ---")
        
        # 2. Generate the API payload and get structured JSON analysis
        analysis_results = call_gemini_api(generate_policy_payload(security_request))
        
        if not analysis_results:
             print("--- [FAILURE] Analysis failed to produce results. ---")
             return
        
        policy_summary = analysis_results.get('policy_summary', 'N/A')
        k8s_yaml = analysis_results.get('hardened_kubernetes_yaml', '')

        # 3. Save the generated YAML and Policy Summary to separate files
        yaml_filename = 'hardened_deployment.yaml'
        policy_filename = 'enforcement_policy_summary.txt'

        with open(yaml_filename, 'w') as f:
            f.write(k8s_yaml)
            
        with open(policy_filename, 'w') as f:
            f.write(f"Policy Enforced: {policy_summary}\n\nGenerated for: Nginx-Deployment")
            
        print("\n--- AI-Driven Kubernetes Hardener Report ---")
        print(f"[SUCCESS] Policy Summary: {policy_summary}")
        print(f"[OUTPUT 1] Hardened K8s Deployment YAML saved to '{yaml_filename}'.")
        print(f"[OUTPUT 2] Policy Summary saved to '{policy_filename}'.")
        print("-" * 60)
        
    except FileNotFoundError:
        print(f"--- [ERROR] File not found: '{request_filepath}'. Ensure 'security_request.txt' exists. ---")
    except Exception as e:
        print(f"--- [CRITICAL ERROR] Failed to run generator: {e} ---")

if __name__ == "__main__":
    main()
