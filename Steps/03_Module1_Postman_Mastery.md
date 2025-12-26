## 🚀 Step 1: Set Up Your Workspace
### 1.1 Open Postman & Create Workspace
Open Postman (desktop app)

Click Workspaces in top-left corner

Click Create Workspace

Enter these details:

Name: API Testing Training

Visibility: Personal (default)

Description: For API testing course exercises

Click Create Workspace

### 1.2 Create New Collection
In your new workspace:

Click + button next to "Collections" or click New → Collection

Name it: GitHub API Tests

Click Create

✅ Checkpoint: You should see:

Workspace: "API Testing Training" (top-left)

Collection: "GitHub API Tests" (left sidebar)

## 🚀 Step 2: Configure Environment Variables
### 2.1 Create GitHub Environment
Click Environments in left sidebar (looks like eye icon)

Click + button

Name it: GitHub Training

Add these variables:

Variable	Initial Value	Current Value
base_url	https://api.github.com	(leave empty)
username	octocat	(leave empty)
token	your_token_here	(leave empty)
Click Save

### 2.2 Create GitHub Personal Access Token (PAT)
IMPORTANT: This token allows API access. Keep it secret!

Go to GitHub.com

Click your profile → Settings

Scroll to Developer settings (bottom-left)

Click Personal access tokens → Tokens (classic)

Click Generate new token → Generate new token (classic)

Fill in:

Note: Postman API Testing

Expiration: 30 days (for safety)

Select scopes: Check:

✅ repo (Full control of private repositories)

✅ user (Update ALL user data)

Click Generate token

COPY THE TOKEN IMMEDIATELY (you won't see it again!)

Go back to Postman

### 2.3 Update Environment with Your Token
In Postman, click the Environments dropdown (top-right)

Select GitHub Training

Click the environment name to edit

Update variables:

username: Your GitHub username (not email)

token: Paste your GitHub token

Click Save

✅ Checkpoint:

Environment selected: "GitHub Training" (top-right dropdown)

Variables should show your username and token (token is masked)

## 🚀 Step 3: Create Your First Request
### 3.1 Create GET User Request
In your "GitHub API Tests" collection:

Click ⋮ (three dots) → Add request

Or click + in the collection

Configure request:

Method: GET (default)

URL: {{base_url}}/users/{{username}}

Type {{ and Postman will suggest variables

Name: Get User Profile

Add Headers:
Click Headers tab, add:

```
Key: Authorization
Value: Bearer {{token}}

Key: Accept
Value: application/vnd.github.v3+json
```
This is GitHub's API versioning header. Here's why it matters:
GitHub has multiple API versions: v3 (REST), v4 (GraphQL), etc.
By default, they might serve you the latest version
If you don't specify, your tests could break when GitHub updates their API
application/vnd.github.v3+json explicitly says: "Give me v3 in JSON format"
```
Key: User-Agent
Value: PostmanRuntime/7.26.8
```
Many APIs require User-Agent (GitHub requires it!)
It identifies who's making the request
Helps API providers: Track usage, Contact you if there are issues, Block malicious bots
PostmanRuntime is Postman's standard User-Agent
The version can be anything reasonable
Without User-Agent, some APIs will reject your request or rate-limit you more aggressively.

### 3.2 Send & Verify
Click Send (blue button) You should see: Status: 200 OK
Response body (JSON with user data)
Time: Less than 1000ms
Check the response includes your GitHub profile

✅ Checkpoint: Successful 200 response with your user data.

## 🚀 Step 4: Add Pre-request Script
### 4.1 Add Script to Log Details
Click Pre-request Script tab

Add this JavaScript:

### javascript
```
// Log request details before sending
console.log("=== REQUEST DETAILS ===");
console.log("Endpoint:", pm.request.url);
console.log("Method:", pm.request.method);
console.log("Environment:", pm.environment.name);
console.log("Timestamp:", new Date().toISOString());
console.log("======================");

// Validate environment variables
if (!pm.environment.get("token")) {
    console.error("ERROR: GitHub token is missing!");
    postman.setNextRequest(null); // Stop execution
}

if (!pm.environment.get("username")) {
    console.error("ERROR: Username is missing!");
    postman.setNextRequest(null);
}
```
### 4.2 Test the Script
Open Postman Console:
View → Show Postman Console (or Ctrl+Alt+C)
Send request again
Check console for logs

✅ Checkpoint: Console shows your request details.
---
## 🚀 Step 5: Add Comprehensive Tests
### 5.1 Add Test Script
into Post-response

### javascript
```
// ===== TEST 1: Response Status =====
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// ===== TEST 2: Response Time =====
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// ===== TEST 3: Headers Validation =====
pm.test("Content-Type header is present", function () {
    pm.response.to.have.header("Content-Type");
});

pm.test("Content-Type is application/json", function () {
    pm.expect(pm.response.headers.get("Content-Type"))
      .to.include("application/json");
});

// ===== TEST 4: JSON Schema Validation =====
pm.test("Response has correct JSON schema", function () {
    const schema = {
        "type": "object",
        "properties": {
            "login": {"type": "string"},
            "id": {"type": "number"},
            "node_id": {"type": "string"},
            "avatar_url": {"type": "string"},
            "type": {"type": "string"},
            "name": {"type": "string"},
            "company": {"type": ["string", "null"]},
            "blog": {"type": ["string", "null"]},
            "location": {"type": ["string", "null"]},
            "email": {"type": ["string", "null"]},
            "hireable": {"type": ["boolean", "null"]},
            "bio": {"type": ["string", "null"]},
            "public_repos": {"type": "number"},
            "followers": {"type": "number"},
            "following": {"type": "number"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        },
        "required": ["login", "id", "node_id", "avatar_url", "type"]
    };
    
    pm.response.to.have.jsonSchema(schema);
});

// ===== TEST 5: Business Logic Validation =====
pm.test("User type is 'User' or 'Organization'", function () {
    const response = pm.response.json();
    const validTypes = ["User", "Organization"];
    pm.expect(validTypes).to.include(response.type);
});

pm.test("User has non-negative follower count", function () {
    const response = pm.response.json();
    pm.expect(response.followers).to.be.at.least(0);
});

pm.test("Created date is before updated date", function () {
    const response = pm.response.json();
    const created = new Date(response.created_at);
    const updated = new Date(response.updated_at);
    pm.expect(created.getTime()).to.be.lessThan(updated.getTime());
});

// ===== TEST 6: Extract Data for Future Requests =====
const responseJson = pm.response.json();
pm.environment.set("user_id", responseJson.id);
pm.environment.set("avatar_url", responseJson.avatar_url);
pm.environment.set("public_repos_count", responseJson.public_repos);

console.log("Extracted user_id:", responseJson.id);
console.log("Public repos:", responseJson.public_repos);
```
---
### 5.2 Run Tests
Send request

Check Test Results tab (next to "Body")

Should see: 9/9 tests passed

✅ Checkpoint: All 9 tests pass.

## 🚀 Step 6: Save Your Work
### 6.1 Export Collection

Click ⋮ next to "GitHub API Tests" collection

Export

Choose Collection v2.1 (recommended)

Export

Save to your project folder: API_Testing/postman/

Name: github-api-training.json

### 6.2 Export Environment
Click ⋮ next to "GitHub Training" environment

Export

Save to same folder

Name: github-training-environment.json

⚠️ WARNING: This contains your token! Add to .gitignore:
Add this line to your .gitignore:

text
# Postman environment files with secrets
*.postman_environment.json
##🚀 Step 7: Create Your Module 1 README
In your module-01-postman-mastery/ folder, create README.md:

## markdown
# Module 1: Postman Mastery - COMPLETED

### ✅ What You've Accomplished

### 1. Workspace & Collection Setup
- Created "API Testing Training" workspace
- Created "GitHub API Tests" collection

### 2. Environment Configuration
- Created "GitHub Training" environment
- Set up variables: `base_url`, `username`, `token`
- Generated GitHub Personal Access Token

### 3. First API Request
- Created GET request to `{{base_url}}/users/{{username}}`
- Added proper headers (Authorization, Accept, User-Agent)
- Successfully received 200 response

### 4. Pre-request Script
- Added logging for request details
- Implemented environment validation
- Used Postman Console for debugging

### 5. Comprehensive Testing
- Implemented 9 different tests including:
  - Status code validation
  - Response time checks
  - Header validation
  - JSON schema validation
  - Business logic tests
  - Data extraction for future requests

### 6. Export & Save
- Exported collection to `postman/github-api-training.json`
- Exported environment (securely)
- Updated `.gitignore` to protect secrets

## 📁 Files Created
- `postman/github-api-training.json` - Collection export
- Screenshots in `screenshots/` folder (optional)

## 🔍 Key Learnings
1. **Environment Variables**: Keep sensitive data out of requests
2. **Pre-request Scripts**: Automate setup and validation
3. **Test Scripts**: Go beyond status codes to business logic
4. **JSON Schema**: Validate response structure
5. **Security**: Never commit tokens to version control

## 🚀 Next Steps
Proceed to [Module 2: Python Automation](../module-02-python-automation/)
📊 Verification Checklist
Before moving on, verify:

Postman workspace created

GitHub PAT generated and working

GET request returns 200 with your data

Pre-request script logs to console

All 9 tests pass

Collection exported to JSON

.gitignore updated to exclude environment files

Module 1 README created

Files committed to Git

💡 Troubleshooting Tips
Issue: "401 Unauthorized"

Token expired? Generate new one

Wrong token format? Use Bearer {{token}}

Token missing scopes? Regenerate with repo and user

Issue: Tests failing

Check console for errors

Verify response structure matches schema

Adjust response time threshold if needed

Issue: Variables not working

Check environment is selected (top-right dropdown)

Ensure variable names match exactly {{base_url}}