import subprocess
import json

# Get user input
project_type = input("Enter Project Type: ")
artifact_id = input("Enter Library Name: ")
group_id = input("Enter Group ID (press enter if none): ")
version = input("Enter Library Version: ")

# Build command based on user input
if group_id == "":
    command = f"srcclr lookup --type {project_type} --coord1 {artifact_id} --version {version} --json"
else:
    command = f"srcclr lookup --type {project_type} --coord1 {artifact_id} --coord2 {group_id} --version {version} --json"

# Run command and parse output as JSON
print("\nGathering information about library...")
result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
data = json.loads(result.stdout)

# Extract relevant data and print in table format
library_name = data["records"][0]["libraries"][0]["name"]
combined_coord_version = f"{artifact_id} v{version}"
latest_version = data["records"][0]["libraries"][0]["latestRelease"]
print("\nSummary:")
print("========")
print(f"Library Scanned: {combined_coord_version}")
print(f"Latest Version: {latest_version}\n")

# Extract Vulnerability Information
vulnerabilities = data["records"][0]["vulnerabilities"]
if len(vulnerabilities) > 0:
    print("\nVulnerabilities Information:")
    print("============================")
    for i, vuln in enumerate(vulnerabilities, start=1):
        print("\nVulnerability {i}:")
        print(f"CVE: {vuln['cve']} - {vuln['title']}")
        print(f"Description: {vuln['overview']}")
        print(f"CVSS v3 Score: {vuln['cvss3Score']}")
else:
    print("\nNo Vulnerabilities Found.")
