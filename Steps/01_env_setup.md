## Step 1: Set Up VS Code Environment
Open VS Code

Open your API_Testing folder: File → Open Folder

Open a terminal: Terminal → New Terminal (PowerShell will open)

Check Python is installed:

```
python --version
```
You should see Python 3.x.x

## Step 2: Install Python Dependencies in VS Code Terminal
In the VS Code PowerShell terminal:

 Navigate to your API_Testing folder if not already there
cd C:\path\to\your\API_Testing

 Create requirements.txt file (copy the content I provided earlier)
 Then install:
```
pip install -r requirements.txt
```
 Or install individually:
```
pip install requests pytest python-dotenv
```

## Step 3: Complete the Repository Structure
In your API_Testing folder, create this structure:
```
  API_Testing/  
├── README.md                    (you already have this)  
├── requirements.txt             (create this with dependencies list)  
├── .env                         (for API keys - add to .gitignore!)  
├── .gitignore                   (important for secrets)  
│  
├── module-01-postman-mastery/  
│   ├── README.md  
│   ├── exercises/  
│   └── screenshots/             (optional, for documentation)  
│  
├── module-02-python-automation/  
│   ├── README.md  
│   ├── tests/  
│   ├── utilities/  
│   └── data/  
│  
├── postman/  
│   └── collections/             (for exported Postman collections)  
│  
└── test-data/  
    ├── csv/  
    └── json/  
```
How to create in VS Code:
```
# In VS Code terminal (PowerShell):
New-Item .env
New-Item .gitignore
```
```
mkdir module-02-python-automation
mkdir module-02-python-automation/tests
mkdir module-02-python-automation/utilities
mkdir module-02-python-automation/data
```

## Step 3.1 Setup venv

```
# 1. Navigate to your API_Testing folder
cd C:\Users\YourName\API_Testing

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
.\venv\Scripts\Activate.ps1

# 4. Create folder structure
mkdir module-01-postman-mastery, module-01-postman-mastery/exercises, module-01-postman-mastery/screenshots
mkdir module-02-python-automation, module-02-python-automation/tests, module-02-python-automation/utilities, module-02-python-automation/data
mkdir postman, test-data

# 5. Create files
New-Item .env
New-Item .gitignore
New-Item requirements.txt

# 6. Add content to requirements.txt (copy from earlier)
# 7. Install packages
pip install -r requirements.txt

# 8. Verify installation
python --version
pip list
```
---
Update Structure and Update .gitignore to include venv:
---
Update .gitignore
```
git init
git add .
git commit -m
```
  ---
  ### Complete Git setup
  ```
  # Initialize git repository
git init
# Add all files (except those in .gitignore)
git add .
# Commit with message
git commit -m "Initial setup: API Testing training repository"
# Connect to GitHub (after creating repo on GitHub.com)
git remote add origin https://github.com/roberthpchao/API_Testing.git
# Rename branch to main
git branch -M main
# Push to GitHub
git push -u origin main
```
---
Quick verification
```
# See what's been committed
git log --oneline
# Check status
git status
# See remote connections
git remote -v
```