# Google Cloud Service Account Setup

## This directory should contain your Google Cloud service account key

### Required Files:

- `service-account-key.json` - Your Google Cloud service account credentials

### How to get Google Cloud credentials:

1. **Go to Google Cloud Console**

   - Visit: https://console.cloud.google.com/

2. **Create a new project** (or use existing)

   - Project ID: `ai-accelerate-hackathon`

3. **Enable required APIs:**

   ```
   - Vertex AI API
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API
   - Cloud Translation API (optional)
   ```

4. **Create Service Account:**

   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Name: `ai-accelerate-service-account`
   - Roles needed:
     - Vertex AI User
     - Cloud Speech Client
     - Cloud Text-to-Speech Client
     - Storage Object Viewer (if using Cloud Storage)

5. **Generate Key:**
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Save as `service-account-key.json` in this directory

### Security Note:

- Never commit `service-account-key.json` to version control
- This file is already in .gitignore
- For production, use environment-based authentication

### Environment Variables:

After placing the service account key, set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/service-account-key.json"
```

Or update the .env file with the correct path.
