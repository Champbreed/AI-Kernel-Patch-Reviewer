import subprocess
import time
import os

def run_audit(script_name, description):
    print(f"\n[🚀] STAGE: {description}")
    print("-" * 60)
    try:
        # Runs the script and captures output
        result = subprocess.run(['python3', script_name], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"[!] Warning in {script_name}: {result.stderr}")
    except Exception as e:
        print(f"[❌] Failed to run {script_name}: {e}")
    print("-" * 60)
    time.sleep(1) # Small pause for visual effect in demo video

def main():
    os.system('clear')
    print("=" * 60)
    print("🛡️  SENTINELS OF GEMINI: AUTONOMOUS DEVSECOPS DASHBOARD")
    print("   Powered by Gemini 3 Flash Preview")
    print("=" * 60)

    # 1. Infrastructure Audit
    run_audit("cost_auditor.py", "Infrastructure FinOps & Security Audit")

    # 2. Kernel Patch Analysis
    run_audit("patch_analyzer.py", "Linux Kernel Memory Safety Analysis")

    # 3. K8s Hardening
    run_audit("k8s_policy_generator.py", "Kubernetes Security Policy Generation")

    print("\n[🏁] ALL AUDITS COMPLETE.")
    print("Files Generated: infrastructure_audit_report.json, analysis_results.json, hardened_deployment.yaml")
    print("=" * 60)

if __name__ == "__main__":
    main()
