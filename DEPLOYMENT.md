# Hack2Skill Submission Guide

## 1. GitHub

Create a **public** GitHub repository named:

`the-blind-spot`

Upload all project files.

Do not upload `.env` or your real API key.

## 2. Gemini API key

Get a Gemini API key from Google AI Studio and configure it as the `GEMINI_API_KEY` environment variable.

## 3. Cloud Run

Install/authenticate the Google Cloud CLI, select your project, then from this project directory run:

```bash
gcloud run deploy the-blind-spot \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_KEY
```

Cloud Run should return a public service URL.

Test the URL before submitting.

## 4. LinkedIn

Publish a post describing:
- The Blind Spot
- The problem it solves
- Your tech stack
- A short demo/result

Copy the URL of the LinkedIn post.

## 5. Hack2Skill form

Submit:

### Public GitHub Repository Link
Your public repository URL.

### Deployed Link - Cloud Run URL
Your Cloud Run service URL.

### LinkedIn Post
Your LinkedIn post URL.

## Final test

Verify all three links before clicking Submit.
