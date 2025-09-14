from .base import BaseAgent
from typing import Dict, Any, List
import datetime


class LiteratureReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_name = "Literature Review Agent"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process literature review request"""
        research_question = input_data.get('research_question', '')
        citations = input_data.get('citations', [])
        notes = input_data.get('notes', [])

        # Load current memory
        memory = self.load_memory()

        # Update memory with new input
        if research_question:
            memory['research_question'] = research_question
        if citations:
            memory['citations'].extend(citations)
        if notes:
            memory['notes'].extend(notes)

        # Generate literature review
        review = self._generate_literature_review(research_question, citations, notes)

        # Store the review in memory
        review_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "review": review,
            "sources_analyzed": len(citations)
        }
        memory['literature_reviews'].append(review_entry)
        memory['progress']['literature_review_completed'] = True

        # Save updated memory
        self.save_memory(memory)

        return {
            "status": "success",
            "agent": self.agent_name,
            "review": review,
            "sources_analyzed": len(citations),
            "recommendations": self._generate_recommendations(research_question, citations)
        }

    def _generate_literature_review(self, research_question: str, citations: List[str], notes: List[str]) -> str:
        """Generate comprehensive literature review"""
        prompt = f"""
        As an expert academic researcher, conduct a comprehensive literature review based on the following:

        Research Question: {research_question}

        Available Citations/Sources:
        {chr(10).join([f"- {citation}" for citation in citations])}

        Research Notes:
        {chr(10).join([f"- {note}" for note in notes])}

        Please provide a structured literature review that includes:
        1. Thematic analysis of the existing literature
        2. Identification of research gaps
        3. Key findings and patterns
        4. Methodological approaches used in the field
        5. Theoretical frameworks identified
        6. Areas of consensus and disagreement
        7. Implications for the current research question

        Format the review in clear sections with proper academic structure.
        """

        return self.generate_response(prompt)

    def _generate_recommendations(self, research_question: str, citations: List[str]) -> List[str]:
        """Generate recommendations for further research"""
        prompt = f"""
        Based on the research question: "{research_question}" and the analyzed sources, 
        provide 5 specific recommendations for:
        1. Additional sources to search for
        2. Research methodologies to consider
        3. Key authors or researchers to investigate
        4. Databases or repositories to explore
        5. Theoretical frameworks to examine

        Provide each recommendation as a clear, actionable bullet point.
        """

        response = self.generate_response(prompt)
        # Parse response into list (simplified parsing)
        recommendations = [line.strip() for line in response.split('\n') if line.strip() and (
                    '1.' in line or '2.' in line or '3.' in line or '4.' in line or '5.' in line)]
        return recommendations[:5]  # Limit to 5 recommendations

    def analyze_source_quality(self, citations: List[str]) -> Dict[str, Any]:
        """Analyze the quality and relevance of sources"""
        prompt = f"""
        Analyze the following academic sources for quality and relevance:

        {chr(10).join([f"- {citation}" for citation in citations])}

        Provide assessment on:
        1. Source credibility (journal impact, publisher reputation)
        2. Relevance to research area
        3. Publication recency
        4. Methodological rigor (if discernible from citation)
        5. Citation diversity (different perspectives, methodologies)

        Rate overall source quality on a scale of 1-10 and provide specific feedback.
        """

        analysis = self.generate_response(prompt)
        return {
            "analysis": analysis,
            "sources_count": len(citations),
            "timestamp": datetime.datetime.now().isoformat()
        }