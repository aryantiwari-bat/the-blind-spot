# The Blind Spot

**The Blind Spot** is an AI-powered critical-thinking assistant for the Hack2Skill challenge.

It does not make decisions for users. Instead, it helps users identify:
- Potential blind spots
- Unstated assumptions
- Missing factors
- Conflicting considerations
- Questions worth exploring
- Information that should be verified

## Tech Stack

- Python
- Flask
- Google Gemini API
- HTML/CSS/JavaScript
- Docker
- Google Cloud Run

## Run locally

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key:

Linux/macOS:
```bash
export GEMINI_API_KEY="YOUR_KEY"
```

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

4. Start:

```bash
python app.py
```

5. Open `http://localhost:8080`

If no API key is configured, the app uses a local fallback analysis so the UI can still be demonstrated.

## Deploy to Cloud Run

Google Cloud Run supports deploying a Python Flask service from source.

After authenticating with Google Cloud CLI and selecting your project:

```bash
gcloud run deploy the-blind-spot --source . --region asia-south1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=YOUR_KEY
```

For a production submission, prefer storing the API key in Secret Manager rather than putting it directly in a shell history or source file.

## Important

Never commit your real Gemini API key to GitHub.
