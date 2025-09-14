from .base import BaseAgent
from typing import Dict, Any, List
import datetime


class HypothesisValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_name = "Hypothesis Validator Agent"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process hypothesis validation request"""
        hypothesis = input_data.get('hypothesis', '')
        research_question = input_data.get('research_question', '')

        # Load current memory
        memory = self.load_memory()

        # Use stored research question if not provided
        if not research_question:
            research_question = memory.get('research_question', '')

        # Validate hypothesis
        validation_result = self._validate_hypothesis(hypothesis, research_question, memory)

        # Store validation in memory
        validation_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "hypothesis": hypothesis,
            "validation": validation_result,
            "research_question": research_question
        }
        memory['hypotheses'].append(validation_entry)
        memory['progress']['hypothesis_validated'] = True

        # Save updated memory
        self.save_memory(memory)

        return {
            "status": "success",
            "agent": self.agent_name,
            "hypothesis": hypothesis,
            "validation": validation_result,
            "recommendations": self._generate_improvement_recommendations(hypothesis, validation_result)
        }

    def _validate_hypothesis(self, hypothesis: str, research_question: str, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Validate hypothesis against research standards"""
        literature_context = ""
        if memory.get('literature_reviews'):
            latest_review = memory['literature_reviews'][-1].get('review', '')
            literature_context = f"Based on literature review: {latest_review[:500]}..."

        prompt = f"""
        As an expert research methodologist, validate the following hypothesis:

        Research Question: {research_question}
        Hypothesis: {hypothesis}

        {literature_context}

        Evaluate the hypothesis on the following criteria (score 1-10 for each):

        1. CLARITY: Is the hypothesis clearly stated and unambiguous?
        2. TESTABILITY: Can this hypothesis be empirically tested?
        3. SPECIFICITY: Is the hypothesis specific enough to guide research design?
        4. RELEVANCE: Does it directly address the research question?
        5. ORIGINALITY: Does it contribute new knowledge to the field?
        6. FEASIBILITY: Is it realistic to test with available resources/methods?
        7. THEORETICAL GROUNDING: Is it based on existing theory or evidence?

        For each criterion, provide:
        - Score (1-10)
        - Brief justification
        - Specific suggestions for improvement if score < 7

        Also provide:
        - Overall assessment (Strong/Moderate/Weak)
        - Key strengths
        - Major weaknesses
        - Suggested revisions
        """

        response = self.generate_response(prompt)

        # Parse the response to extract scores (simplified parsing)
        overall_score = self._calculate_overall_score(response)

        return {
            "detailed_analysis": response,
            "overall_score": overall_score,
            "assessment": self._get_assessment_level(overall_score),
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _calculate_overall_score(self, analysis: str) -> float:
        """Extract and calculate overall score from analysis"""
        # Simplified scoring - in production, you'd want more sophisticated parsing
        scores = []
        lines = analysis.split('\n')
        for line in lines:
            if any(criterion in line.upper() for criterion in
                   ['CLARITY', 'TESTABILITY', 'SPECIFICITY', 'RELEVANCE', 'ORIGINALITY', 'FEASIBILITY', 'THEORETICAL']):
                # Look for numbers in the line
                import re
                numbers = re.findall(r'\b([1-9]|10)\b', line)
                if numbers:
                    scores.append(int(numbers[0]))

        return sum(scores) / len(scores) if scores else 5.0

    def _get_assessment_level(self, score: float) -> str:
        """Convert score to assessment level"""
        if score >= 8:
            return "Strong"
        elif score >= 6:
            return "Moderate"
        else:
            return "Weak"

    def _generate_improvement_recommendations(self, hypothesis: str, validation_result: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for hypothesis improvement"""
        prompt = f"""
        Based on the hypothesis validation, provide 5 specific, actionable recommendations 
        to improve this hypothesis:

        Original Hypothesis: {hypothesis}
        Assessment Level: {validation_result.get('assessment', 'Unknown')}
        Overall Score: {validation_result.get('overall_score', 0)}

        Focus on:
        1. Improving clarity and specificity
        2. Enhancing testability
        3. Strengthening theoretical foundation
        4. Addressing feasibility concerns
        5. Increasing research impact

        Provide each recommendation as a clear, actionable statement.
        """

        response = self.generate_response(prompt)
        recommendations = [line.strip() for line in response.split('\n') if
                           line.strip() and any(num in line for num in ['1.', '2.', '3.', '4.', '5.'])]
        return recommendations[:5]

    def generate_alternative_hypotheses(self, research_question: str, context: str = "") -> List[str]:
        """Generate alternative hypotheses for the research question"""
        memory = self.load_memory()
        literature_context = ""
        if memory.get('literature_reviews'):
            latest_review = memory['literature_reviews'][-1].get('review', '')
            literature_context = f"Literature context: {latest_review[:500]}..."

        prompt = f"""
        Generate 3 alternative, well-formed hypotheses for this research question:

        Research Question: {research_question}
        Additional Context: {context}
        {literature_context}

        Each hypothesis should be:
        - Testable and specific
        - Theoretically grounded
        - Different from each other in approach/focus
        - Feasible to investigate

        Format each hypothesis clearly and provide brief rationale for each.
        """

        response = self.generate_response(prompt)
        # Parse alternatives (simplified)
        alternatives = []
        lines = response.split('\n')
        current_hypothesis = ""
        for line in lines:
            if line.strip() and ('Hypothesis' in line or line.startswith(('1.', '2.', '3.'))):
                if current_hypothesis:
                    alternatives.append(current_hypothesis.strip())
                current_hypothesis = line
            elif line.strip() and current_hypothesis:
                current_hypothesis += " " + line
        if current_hypothesis:
            alternatives.append(current_hypothesis.strip())

        return alternatives[:3]