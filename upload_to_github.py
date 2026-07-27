import os
import base64
import requests

# Configuration
GITHUB_REPO = "Rudra1234-hack/AI_RESUME_BUILDER"

def should_exclude(path):
    exclusions = [
        'db.sqlite3', '.git', '__pycache__', '.gemini', 
        '.agents', 'venv', 'env', '.vscode', '.idea',
        'staticfiles', 'media'
    ]
    for ex in exclusions:
        if f"{os.sep}{ex}{os.sep}" in path or path.startswith(f"{ex}{os.sep}") or path == ex:
            return True
    return False

def upload_file(file_path, token):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path.replace(os.sep, '/')}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Read and encode file content
    try:
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Get SHA if file already exists (to overwrite it)
    sha = None
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json().get("sha")

    payload = {
        "message": f"Upload {file_path} via API",
        "content": content
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print(f"Successfully uploaded: {file_path}")
        return True
    else:
        print(f"Failed to upload {file_path}: {r.status_code} - {r.text}")
        return False

def main():
    print("=== GitHub Direct Uploader ===")
    print(f"Target Repo: {GITHUB_REPO}")
    print("\nTo upload, you need a GitHub Personal Access Token (PAT).")
    print("Create one at: https://github.com/settings/tokens (classic PAT with 'repo' scope).")
    
    token = input("\nEnter your GitHub Personal Access Token: ").strip()
    if not token:
        print("Token is required.")
        return

    files_to_upload = []
    for root, dirs, files in os.walk("."):
        # Modify dirs in-place to avoid searching excluded folders
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        
        for file in files:
            full_path = os.path.relpath(os.path.join(root, file), ".")
            if not should_exclude(full_path) and not file.endswith('.pyc'):
                files_to_upload.append(full_path)

    print(f"\nFound {len(files_to_upload)} files to upload.")
    confirm = input("Do you want to proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Upload cancelled.")
        return

    success_count = 0
    for file_path in files_to_upload:
        if upload_file(file_path, token):
            success_count += 1
            
    print(f"\nFinished! Successfully uploaded {success_count}/{len(files_to_upload)} files.")

if __name__ == "__main__":
    main()
