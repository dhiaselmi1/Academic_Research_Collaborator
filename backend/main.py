from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

from agents.base import BaseAgent
from agents import LiteratureReviewAgent, HypothesisValidatorAgent, DraftPolisherAgent

app = FastAPI(title="Academic Research Collaborator API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
literature_agent = LiteratureReviewAgent()
hypothesis_agent = HypothesisValidatorAgent()
draft_agent = DraftPolisherAgent()


# Pydantic models for request/response
class ResearchInput(BaseModel):
    research_question: Optional[str] = ""
    citations: Optional[List[str]] = []
    notes: Optional[List[str]] = []


class HypothesisInput(BaseModel):
    hypothesis: str
    research_question: Optional[str] = ""


class DraftInput(BaseModel):
    draft_text: str
    polish_type: Optional[str] = "comprehensive"  # comprehensive, grammar, structure, clarity, citations
    target_audience: Optional[str] = "academic"


class AlternativeHypothesesInput(BaseModel):
    research_question: str
    context: Optional[str] = ""


class SourceAnalysisInput(BaseModel):
    citations: List[str]


class ComparisonInput(BaseModel):
    version1: str
    version2: str


@app.get("/")
async def root():
    return {"message": "Academic Research Collaborator API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": ["literature_review", "hypothesis_validator", "draft_polisher"]}


@app.get("/memory")
async def get_memory():
    """Get current memory state"""
    try:
        base_agent = BaseAgent()
        memory = base_agent.load_memory()
        return {"status": "success", "memory": memory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading memory: {str(e)}")


@app.delete("/memory")
async def clear_memory():
    """Clear memory store"""
    try:
        memory_path = "memory/memory_store.json"
        if os.path.exists(memory_path):
            os.remove(memory_path)
        return {"status": "success", "message": "Memory cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")


@app.post("/literature-review")
async def conduct_literature_review(input_data: ResearchInput):
    """Conduct literature review analysis"""
    try:
        if literature_agent is None:
            raise HTTPException(status_code=503, detail="Literature Review Agent not available")

        result = literature_agent.process({
            "research_question": input_data.research_question,
            "citations": input_data.citations,
            "notes": input_data.notes
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Literature review error: {str(e)}")


@app.post("/analyze-sources")
async def analyze_source_quality(input_data: SourceAnalysisInput):
    """Analyze quality of research sources"""
    try:
        if literature_agent is None:
            raise HTTPException(status_code=503, detail="Literature Review Agent not available")

        result = literature_agent.analyze_source_quality(input_data.citations)
        return {"status": "success", "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Source analysis error: {str(e)}")


@app.post("/validate-hypothesis")
async def validate_hypothesis(input_data: HypothesisInput):
    """Validate research hypothesis"""
    try:
        if hypothesis_agent is None:
            raise HTTPException(status_code=503, detail="Hypothesis Validator Agent not available")

        result = hypothesis_agent.process({
            "hypothesis": input_data.hypothesis,
            "research_question": input_data.research_question
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hypothesis validation error: {str(e)}")


@app.post("/generate-alternatives")
async def generate_alternative_hypotheses(input_data: AlternativeHypothesesInput):
    """Generate alternative hypotheses"""
    try:
        if hypothesis_agent is None:
            raise HTTPException(status_code=503, detail="Hypothesis Validator Agent not available")

        alternatives = hypothesis_agent.generate_alternative_hypotheses(
            input_data.research_question,
            input_data.context
        )
        return {
            "status": "success",
            "research_question": input_data.research_question,
            "alternative_hypotheses": alternatives
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alternative generation error: {str(e)}")


@app.post("/polish-draft")
async def polish_draft(input_data: DraftInput):
    """Polish academic draft"""
    try:
        if draft_agent is None:
            raise HTTPException(status_code=503, detail="Draft Polisher Agent not available")

        result = draft_agent.process({
            "draft_text": input_data.draft_text,
            "polish_type": input_data.polish_type,
            "target_audience": input_data.target_audience
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Draft polishing error: {str(e)}")


@app.post("/compare-drafts")
async def compare_draft_versions(input_data: ComparisonInput):
    """Compare two versions of a draft"""
    try:
        if draft_agent is None:
            raise HTTPException(status_code=503, detail="Draft Polisher Agent not available")

        result = draft_agent.compare_versions(input_data.version1, input_data.version2)
        return {"status": "success", "comparison": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Draft comparison error: {str(e)}")


@app.get("/research-progress")
async def get_research_progress():
    """Get overall research progress"""
    try:
        base_agent = BaseAgent()
        memory = base_agent.load_memory()
        progress = memory.get('progress', {})

        # Calculate completion percentage
        completed_tasks = sum(progress.values())
        total_tasks = len(progress)
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "status": "success",
            "progress": progress,
            "completion_percentage": round(completion_percentage, 2),
            "research_question": memory.get('research_question', ''),
            "total_citations": len(memory.get('citations', [])),
            "total_notes": len(memory.get('notes', [])),
            "total_reviews": len(memory.get('literature_reviews', [])),
            "total_hypotheses": len(memory.get('hypotheses', [])),
            "total_drafts": len(memory.get('drafts', []))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Progress tracking error: {str(e)}")


@app.get("/export-research")
async def export_research_data():
    """Export all research data"""
    try:
        base_agent = BaseAgent()
        memory = base_agent.load_memory()

        # Format export data
        export_data = {
            "export_timestamp": "2024-01-01T00:00:00",  # Current timestamp would be better
            "research_summary": {
                "question": memory.get('research_question', ''),
                "total_sources": len(memory.get('citations', [])),
                "progress": memory.get('progress', {})
            },
            "literature_reviews": memory.get('literature_reviews', []),
            "hypotheses": memory.get('hypotheses', []),
            "drafts": memory.get('drafts', []),
            "citations": memory.get('citations', []),
            "notes": memory.get('notes', [])
        }

        return {"status": "success", "export_data": export_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)