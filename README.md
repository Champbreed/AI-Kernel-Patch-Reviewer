AI-Driven DevSecOps Automation Portfolio
​Applicant: Simon Essien (champbreed1@gmail.com)
GitHub Repository: [https://github.com/Champbreed/AI-Kernel-Patch-Reviewer]
Domain Focus: Advanced DevSecOps and FinOps Automation via Generative AI (Google Gemini) and Python.

​This portfolio showcases four distinct, innovative projects that leverage Large Language Models (LLMs) to automate security, 
compliance, and cost optimization across the full stack—from core Linux kernel code to modern Cloud-Native infrastructure. T
he core principle demonstrated is converting unstructured technical output into actionable, structured data (JSON Schema) for pipeline consumption.

​🧭 Table of Contents

​Setup & Environment
​Project 1: Kernel Patch Reviewer (Linux Security)
​Project 2: Terraform Security Auditor (IaC Security)
​Project 3: IaC Cost and Drift Analyzer (FinOps)
​Project 4: K8s Policy & Config Hardener (Policy-as-Code)

​1. ⚙ Setup & Environment

​All tools are built in Python 3 and designed to run within a standard virtual environment.

 step                                         command                                             purpose
________________________________________________________________________________________________________________________________


1. Clone & Navigate              git clone [Your Repo URL]; cd [Repo Name]              Fetches the code and enters the project 
                                                                                        directory.
_________________________________________________________________________________________________________________________________

2. Activate Venv                python3 -m venv venv; source venv/bin/activate          Creates and activates an isolated 
                                                                                        environment. 

_________________________________________________________________________________________________________________________________

3. Install Deps                   pip install requests python-dotenv                    Installs necessary libraries for API commu-
                                                                                        nication and secret loading.

__________________________________________________________________________________________________________________________________

4. Configure API Key            echo 'GEMINI_API_KEY="YOUR_KEY_HERE"' > .env            Sets the credential securely (The .env file 
                                                                                        is excluded from Git via .gitignore).

___________________________________________________________________________________________________________________________________






2.  🛡  Project 1: AI-Driven Kernel Patch Reviewer

               Metric                                                        Details
___________________________________________________________________________________________________________________________________

A.         What It Does                                             Automated Vulnerability Triage for Linux Patches. Analyzes raw Git
                                                                   diffs/patches from Linux kernel repositories (e.g., net-next.git).
___________________________________________________________________________________________________________________________________

B.       How It Works                                              The script (patch_analyzer.py) sends raw C code/patch diffs to 
                                                                  the LLM, enforcing a strict JSON Schema to return a structured 
                                                                  finding (Severity, Issue, Remediation) rather than just free text
___________________________________________________________________________________________________________________________________

C.   Relevance to Linux/Open Source                                Kernel Contribution Acceleration: Proves capability in handling
                                                                  complex C code structures and identifying critical vulnerabilities
                                                                  (like Use-After-Free) at the earliest stage, significantly reducing
                                                                  the security review overhead for kernel maintainers.
___________________________________________________________________________________________________________________________________

D.     Run Command                                                   python3
                                                                    patch_analyzer.py
___________________________________________________________________________________________________________________________________








3. ☁  Project 2: AI-Driven Terraform Security Auditor

                    Metric                                                 Details
___________________________________________________________________________________________________________________________________

A.             What It Does                                        Shift-Left IaC Security Gating. Performs static analysis on
                                                                  Infrastructure as Code (IaC) written in Terraform HCL to check for
                                                                  compliance and common cloud risks.
___________________________________________________________________________________________________________________________________

B.            How It Works                                         The script (terraform_auditor.py) reads the IaC file 
                                                                   (test_infra.tf) and instructs the AI to generate a structured
                                                                   audit report, categorized by severity, risk, and containing
                                                                   executable remediation steps.
___________________________________________________________________________________________________________________________________

C.    Relevance to DevSecOps                                      Security Compliance: Creates a vital security check before cloud 
                                                                  infrastructure is deployed. This is a foundational DevSecOps
                                                                  practice essential for ensuring baseline security posture 
                                                                  in any cloud environment.
___________________________________________________________________________________________________________________________________

D.          Run Command                                                        python3
                                                                         terraform_auditor.py

___________________________________________________________________________________________________________________________________









4. 💰 Project 4: AI-Driven K8s Policy & Configuration Hardener


___________________________________________________________________________________________________________________________________

                     Metric                                 Details
__________________________________________________________________________________________________________________________________


A.                 What It Does                         DevSecOps & FinOps Integration. Provides a dual security and financial impact
                                                        audit by analyzing the raw text output of a complex terraform plan diff.
___________________________________________________________________________________________________________________________________


B.               How It Works                           The script (cost_auditor.py) leverages the AI's contextual reasoning to 
                                                        synthesize the plan's changes, producing a structured report that includes 
                                                        a Cost Forecast (budget impact) and Security Drift Notes (e.g., unauthorized
                                                        resource exposure).
___________________________________________________________________________________________________________________________________

C.       Relevance to Strategy                          Operational Excellence: This project demonstrates high-level strategic
                                                        thinking by bridging technical deployment risk with business profitability 
                                                        and cost governance (FinOps), a non-negotiable requirement for modern, 
                                                        large-scale cloud organizations.

___________________________________________________________________________________________________________________________________

D.              Run Command                                python3 
                                                         cost_auditor.py

___________________________________________________________________________________________________________________________________







5.   🔑 Project 4: AI-Driven K8s Policy & Configuration Hardener

___________________________________________________________________________________________________________________________________

                 Metric                       Details

___________________________________________________________________________________________________________________________________

A.         What It Does                Natural Language to Policy-as-Code Automation. Automates the creation of hardened Kubernetes
                                       YAML configurations and their corresponding security enforcement policies from simple 
                                       English requirements.
__________________________________________________________________________________________________________________________________

B.         How It Works                The script (k8s_policy_generator.py) takes a high-level policy (e.g., "All containers must 
                                       run as non-root") and outputs two critical, structured artifacts: 1) The hardened K8s
                                       Deployment YAML, and 2) A concise Policy Summary suitable for external policy engines like 
                                       OPA Gatekeeper.
__________________________________________________________________________________________________________________________________

C.      Relevance to Cloud-Native      Governance and Compliance: Solves the complexity of cloud-native security by automating the
                                       creation of both the secure artifact and the rule required to enforce that artifact, 
                                       establishing repeatable, auditable governance in a Kubernetes cluster.
__________________________________________________________________________________________________________________________________

D.         Run Command                       python3
                                         k8s_policy_generator.py
___________________________________________________________________________________________________________________________________


All project files, including Python scripts, test inputs, and JSON/YAML outputs, are included in the repository for full functional verification.

