from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from reader import ReadingCompanionWorkflow

app = FastAPI()

DB_URL = "postgresql+psycopg2://ai:ai@localhost:5532/ai"
reading_workflow = ReadingCompanionWorkflow(db_url=DB_URL)

class QueryRequest(BaseModel):
    question: str
    pdf_url: HttpUrl

class SummaryRequest(BaseModel):
    pdf_url: HttpUrl

class UserPreferences(BaseModel):
    interests: List[str]
    reading_level: Optional[str] = "intermediate"
    focus_areas: Optional[List[str]] = []

class PersonalizedRequest(BaseModel):
    pdf_url: HttpUrl
    user_id: str
    preferences: Optional[UserPreferences] = None

@app.post("/process-pdf")
async def process_pdf(request: SummaryRequest):
    """Endpoint to pre-process a PDF"""
    try:
        agents = reading_workflow.process_book(str(request.pdf_url))
        return {
            "status": "success",
            "message": "PDF processed successfully",
            "pdf_url": str(request.pdf_url)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(query: QueryRequest):
    try:
        agents = reading_workflow.process_book(str(query.pdf_url))
        response = reading_workflow.get_response(agents["qa"], query.question)
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def get_summary(request: SummaryRequest):
    try:
        agents = reading_workflow.process_book(str(request.pdf_url))
        summary_prompt = """
        Please provide a comprehensive summary of the document including:
        1. Overview of the main content
        2. Key points and major arguments
        3. Important details and examples
        4. Conclusions or final thoughts
        
        Structure the summary in a clear, organized manner and ensure all major sections 
        of the document are covered. Include relevant headings or sections if applicable.
        """
        response = reading_workflow.get_response(agents["summary"], summary_prompt)
        return {"summary": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insights")
async def get_insights(request: SummaryRequest):
    try:
        agents = reading_workflow.process_book(str(request.pdf_url))
        # First get a summary to provide context
        summary_prompt = "Provide a brief overview of the document content"
        summary = reading_workflow.get_response(agents["summary"], summary_prompt)
        
        # Use the summary as context for insights
        insight_prompt = f"""
        Context of the document: {summary.content}

        Based on this document, please analyze and provide key insights including:
        1. Main themes and concepts
        2. Key arguments or points
        3. Notable findings or conclusions
        4. Important relationships or patterns
        5. Significant implications
        
        Please base all insights strictly on the document's content.
        """
        response = reading_workflow.get_response(agents["insight"], insight_prompt)
        return {"insights": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/personalized-insights")
async def get_personalized_insights(request: PersonalizedRequest):
    try:
        agents = reading_workflow.process_book(str(request.pdf_url))
        
        # Get document summary for context
        summary_prompt = "Provide a brief overview of the document content"
        summary = reading_workflow.get_response(agents["summary"], summary_prompt)
        
        # Create personalized prompt with context
        personalized_prompt = f"""
        Context of the document: {summary.content}

        User Interests: {request.preferences.interests if request.preferences else 'Not specified'}
        Reading Level: {request.preferences.reading_level if request.preferences else 'intermediate'}
        Focus Areas: {request.preferences.focus_areas if request.preferences and request.preferences.focus_areas else 'Not specified'}

        Based on the document and user preferences:
        1. Identify key insights that align with the user's interests
        2. Highlight sections particularly relevant to their focus areas
        3. Explain concepts at the appropriate reading level
        4. Make connections between the content and user's areas of interest
        5. Suggest specific areas for deeper exploration
        """
        
        response = reading_workflow.get_personalized_response(
            agents["insight"],
            personalized_prompt,
            request.user_id,
            request.preferences.interests if request.preferences else None
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reading-progress")
async def update_progress(
    user_id: str,
    section: str,
    progress: float
):
    try:
        return reading_workflow.reading_system.update_reading_progress(section, progress)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions/{user_id}")
async def get_suggestions(user_id: str):
    try:
        interests = reading_workflow.user_preferences.get(user_id, [])
        suggestions = reading_workflow.reading_system.get_section_suggestions(interests)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)