import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def audit_infrastructure():
    filepath = 'test_plan.txt'
    try:
        with open(filepath, 'r') as f:
            plan_data = f.read()
    except FileNotFoundError:
        print("Error: test_plan.txt not found.")
        return

    prompt = f"Analyze this Terraform Plan for cost and security. Return JSON: {plan_data}"

    print("--- [PHASE 3] Initiating FinOps Audit (Gemini 3 + Retry Logic) ---")

    # 🛠️ RETRY LOGIC: Try up to 3 times with a delay
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=prompt
            )

            with open('infrastructure_audit_report.json', 'w') as f:
                f.write(response.text)

            print("\n--- Infrastructure Audit Result ---")
            print(response.text)
            return # Success! Exit the function.

        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                wait_time = (attempt + 1) * 5  # Waits 5s, then 10s
                print(f"[!] Server Overloaded. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Audit failed: {e}")
                break

    print("❌ Critical: Could not reach Gemini 3 after 3 attempts.")

if __name__ == "__main__":
    audit_infrastructure()
