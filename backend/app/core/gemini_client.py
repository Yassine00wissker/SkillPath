import os
import json
import httpx
from typing import Dict, Optional, List
from fastapi import HTTPException, status

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
# Use gemini-1.5-flash (faster) or gemini-1.5-pro (more capable)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


def build_gemini_prompt(user: Dict, candidates: List[Dict], task: str = "enhance") -> str:
    """
    Create a prompt template for Gemini.
    
    Args:
        user: User profile with competence, interests, etc.
        candidates: List of job/formation candidates
        task: "enhance" (rank existing) or "generate" (suggest new)
    """
    user_profile = f"""
User profile:
- Name: {user.get('nom', '')} {user.get('prenom', '')}
- Email: {user.get('email', '')}
- Competence: {user.get('competence', [])}
- Interests: {user.get('interests', [])}
"""
    
    if task == "enhance":
        candidates_text = "\n".join([
            f"- {c.get('type', 'unknown')}: {c.get('title', '')} (ID: {c.get('id', '')}) - {c.get('description', '')[:100]}"
            for c in candidates[:50]  # Limit to 50 candidates
        ])
        
        prompt = f"""System: You are an assistant that outputs ONLY valid JSON. Do not include any markdown formatting, code blocks, or explanations outside the JSON.

User: Here is a user profile and a list of candidates.

{user_profile}

Candidates (jobs/formations):
{candidates_text}

Task: Rank the candidates by relevance to this user. For each candidate return:
- id: the candidate ID
- type: "job" or "formation"
- score: a relevance score between 0.0 and 1.0
- explanation: a short explanation (maximum 20 words)

Return a JSON object with this exact structure:
{{"jobs": [{{"id": <int>, "type": "job", "score": <0.0-1.0>, "explanation": "<text>"}}], "formations": [{{"id": <int>, "type": "formation", "score": <0.0-1.0>, "explanation": "<text>"}}]}}

Return ONLY the JSON object, nothing else."""
    
    else:  # generate
        prompt = f"""System: You are an assistant that outputs ONLY valid JSON. Do not include any markdown formatting, code blocks, or explanations outside the JSON.

User: Here is a user profile.

{user_profile}

Task: Generate job and course suggestions based on this user's skills and interests. For each suggestion return:
- title: a job title or course name
- type: "job" or "formation"
- score: a relevance score between 0.0 and 1.0
- explanation: why this is relevant (maximum 20 words)
- description: a brief description

Return a JSON object with this exact structure:
{{"jobs": [{{"title": "<text>", "type": "job", "score": <0.0-1.0>, "explanation": "<text>", "description": "<text>"}}], "formations": [{{"title": "<text>", "type": "formation", "score": <0.0-1.0>, "explanation": "<text>", "description": "<text>"}}]}}

Return ONLY the JSON object, nothing else."""
    
    return prompt


async def send_to_gemini(prompt: str) -> Dict:
    """
    Send a prompt to Gemini API and return the response.
    
    Returns:
        Parsed JSON response from Gemini
    """
    if MOCK_MODE:
        # Return deterministic mock response for testing
        return {
            "jobs": [
                {"id": 1, "type": "job", "score": 0.95, "explanation": "Perfect match for Python backend skills"},
                {"id": 2, "type": "job", "score": 0.75, "explanation": "Good fit for full stack development"}
            ],
            "formations": [
                {"id": 1, "type": "formation", "score": 0.90, "explanation": "Covers FastAPI and SQL topics"},
                {"id": 2, "type": "formation", "score": 0.80, "explanation": "Advanced Python programming course"}
            ]
        }
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY not configured"
        )
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Gemini API error: {response.text}"
                )
            
            data = response.json()
            
            # Extract text from Gemini response
            if "candidates" in data and len(data["candidates"]) > 0:
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Try to extract JSON from the response
                # Remove markdown code blocks if present
                text_content = text_content.strip()
                if text_content.startswith("```"):
                    # Remove markdown code blocks
                    lines = text_content.split("\n")
                    text_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
                
                # Parse JSON
                try:
                    result = json.loads(text_content)
                    return result
                except json.JSONDecodeError:
                    # Try to find JSON object in the text
                    start = text_content.find("{")
                    end = text_content.rfind("}") + 1
                    if start >= 0 and end > start:
                        result = json.loads(text_content[start:end])
                        return result
                    else:
                        raise ValueError("No valid JSON found in response")
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Invalid response from Gemini API"
                )
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Gemini API request timeout"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Gemini API: {str(e)}"
        )

