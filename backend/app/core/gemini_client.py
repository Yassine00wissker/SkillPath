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


def build_gemini_prompt(goal: str, competences: List[str], interests: List[str], candidates: List[Dict]) -> str:
    """
    Build Gemini prompt for skillpath generation using the template from prompt.txt.
    
    Args:
        goal: User's goal (free text)
        competences: List of current skills
        interests: List of interests
        candidates: List of job/formation candidates with id, type, title, description, skills
    """
    competences_json = json.dumps(competences)
    interests_json = json.dumps(interests)
    
    # Format candidates
    candidates_list = []
    for c in candidates[:30]:  # Limit to 30 candidates
        candidate_obj = {
            "id": c.get("id"),
            "type": c.get("type", "formation"),
            "title": c.get("title", c.get("titre", "")),
            "description": (c.get("description") or "")[:200],
            "skills": c.get("requirements", c.get("skills", []))
        }
        candidates_list.append(candidate_obj)
    
    candidates_json = json.dumps(candidates_list, indent=2)
    
    prompt = f"""System: You are an assistant that outputs ONLY valid JSON.

User: Given the following user inputs and candidate items, produce a single JSON object representing an AI-generated "skillpath" (a practical roadmap for the user). Do not include any extra text, commentary, or explanation — ONLY JSON.

User profile:
{{
  "goal": "{goal}",
  "competences": {competences_json},
  "interests": {interests_json}
}}

Candidates:
{candidates_json}

Task:
- Produce JSON with this schema:
{{
  "title": "<compact 5-8 word title>",
  "summary": "<1-2 sentence summary>",
  "steps": [
    {{
      "id": "step-1",
      "title": "short title",
      "duration_weeks": 1-12,
      "progress_estimate": "text (e.g., 'beginner->intermediate')",
      "resources": [
        {{"type":"formation"|"job"|"external", "id": <int or null>, "titre": "<title or null>", "url": "<if external or null>", "score": 0.0-1.0}}
      ],
      "explanation": "<<=20 words>"
    }},
    ...
  ],
  "recommended_jobs": [{{"id":int,"titre":"", "score":0.0-1.0, "match_reason":"<=20 words"}}],
  "recommended_formations": [{{"id":int,"titre":"", "score":0.0-1.0, "match_reason":"<=20 words"}}]
}}

Rules:
1) Return only JSON that strictly follows the schema.
2) Use IDs from Candidates when referencing formations/jobs. If you add external resources, set id=null and provide URL.
3) Use scores between 0.0 and 1.0.
4) Steps should be 3-7 items long, ordered sequentially.
5) Keep fields concise.
6) If unsure, return an empty array rather than text.

End."""
    
    return prompt


async def send_skillpath_request(prompt: str) -> Dict:
    """
    Send a skillpath request to Gemini API and return the response.
    
    Returns:
        Parsed JSON response from Gemini with skillpath structure
    """
    if MOCK_MODE:
        # Return deterministic mock response for testing
        return {
            "title": "Become Backend Developer",
            "summary": "A structured path to master backend development with Python and FastAPI.",
            "steps": [
                {
                    "id": "step-1",
                    "title": "Learn Python basics",
                    "duration_weeks": 2,
                    "progress_estimate": "beginner->intermediate",
                    "resources": [
                        {"type": "formation", "id": 1, "titre": "Python Fundamentals", "url": None, "score": 0.9},
                        {"type": "external", "id": None, "titre": "Python Official Docs", "url": "https://docs.python.org", "score": 0.8}
                    ],
                    "explanation": "Master Python fundamentals before moving to frameworks"
                },
                {
                    "id": "step-2",
                    "title": "Learn FastAPI framework",
                    "duration_weeks": 3,
                    "progress_estimate": "intermediate->advanced",
                    "resources": [
                        {"type": "formation", "id": 2, "titre": "FastAPI for Beginners", "url": None, "score": 0.95}
                    ],
                    "explanation": "Build REST APIs with FastAPI"
                }
            ],
            "recommended_jobs": [
                {"id": 1, "titre": "Backend Developer", "score": 0.95, "match_reason": "Perfect match for Python backend skills"}
            ],
            "recommended_formations": [
                {"id": 1, "titre": "Python Fundamentals", "score": 0.9, "match_reason": "Essential foundation for backend development"}
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


# Keep the old function for backward compatibility
async def send_to_gemini(prompt: str) -> Dict:
    """
    Send a prompt to Gemini API and return the response.
    
    Returns:
        Parsed JSON response from Gemini
    """
    return await send_skillpath_request(prompt)


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

