from .base import BaseAgent
from typing import Dict, Any, List
import datetime


class DraftPolisherAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_name = "Draft Polisher Agent"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process draft polishing request"""
        draft_text = input_data.get('draft_text', '')
        polish_type = input_data.get('polish_type',
                                     'comprehensive')  # comprehensive, grammar, structure, clarity, citations
        target_audience = input_data.get('target_audience', 'academic')

        # Load current memory
        memory = self.load_memory()

        # Polish the draft
        polished_result = self._polish_draft(draft_text, polish_type, target_audience, memory)

        # Store polished draft in memory
        draft_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original_draft": draft_text,
            "polished_draft": polished_result['polished_text'],
            "polish_type": polish_type,
            "improvements_made": polished_result['improvements'],
            "word_count_original": len(draft_text.split()),
            "word_count_polished": len(polished_result['polished_text'].split())
        }
        memory['drafts'].append(draft_entry)
        memory['progress']['draft_polished'] = True

        # Save updated memory
        self.save_memory(memory)

        return {
            "status": "success",
            "agent": self.agent_name,
            "original_text": draft_text,
            "polished_text": polished_result['polished_text'],
            "improvements": polished_result['improvements'],
            "quality_score": polished_result['quality_score'],
            "suggestions": polished_result['suggestions']
        }

    def _polish_draft(self, draft_text: str, polish_type: str, target_audience: str, memory: Dict[str, Any]) -> Dict[
        str, Any]:
        """Polish draft based on specified type and audience"""

        # Get research context from memory
        research_context = self._build_research_context(memory)

        polish_prompts = {
            'comprehensive': self._get_comprehensive_polish_prompt,
            'grammar': self._get_grammar_polish_prompt,
            'structure': self._get_structure_polish_prompt,
            'clarity': self._get_clarity_polish_prompt,
            'citations': self._get_citations_polish_prompt
        }

        prompt_func = polish_prompts.get(polish_type, polish_prompts['comprehensive'])
        prompt = prompt_func(draft_text, target_audience, research_context)

        response = self.generate_response(prompt)

        # Extract improvements and suggestions
        improvements = self._extract_improvements(response)
        suggestions = self._extract_suggestions(response)
        quality_score = self._assess_quality_score(draft_text, response)

        # Extract polished text (simplified - assumes it's in the response)
        polished_text = self._extract_polished_text(response, draft_text)

        return {
            'polished_text': polished_text,
            'improvements': improvements,
            'suggestions': suggestions,
            'quality_score': quality_score
        }

    def _build_research_context(self, memory: Dict[str, Any]) -> str:
        """Build context from research memory"""
        context_parts = []

        if memory.get('research_question'):
            context_parts.append(f"Research Question: {memory['research_question']}")

        if memory.get('literature_reviews'):
            latest_review = memory['literature_reviews'][-1].get('review', '')
            context_parts.append(f"Literature Context: {latest_review[:300]}...")

        if memory.get('hypotheses'):
            latest_hypothesis = memory['hypotheses'][-1].get('hypothesis', '')
            context_parts.append(f"Research Hypothesis: {latest_hypothesis}")

        return "\n".join(context_parts)

    def _get_comprehensive_polish_prompt(self, draft_text: str, target_audience: str, research_context: str) -> str:
        return f"""
        As an expert academic editor, comprehensively polish this research draft:

        TARGET AUDIENCE: {target_audience}

        RESEARCH CONTEXT:
        {research_context}

        DRAFT TO POLISH:
        {draft_text}

        Provide comprehensive editing focusing on:

        1. STRUCTURE & ORGANIZATION
        - Logical flow of arguments
        - Clear paragraph transitions
        - Appropriate section organization
        - Strong introduction and conclusion

        2. CLARITY & READABILITY
        - Sentence structure and variety
        - Word choice and precision
        - Elimination of jargon (where appropriate)
        - Active vs passive voice optimization

        3. ACADEMIC STYLE
        - Formal academic tone
        - Objective language
        - Proper terminology usage
        - Citation integration

        4. ARGUMENT STRENGTH
        - Logical reasoning
        - Evidence presentation
        - Counter-argument consideration
        - Conclusion support

        Please provide:
        - The polished version of the text
        - List of major improvements made
        - Specific suggestions for further enhancement
        - Quality assessment (1-10 scale)

        Format your response with clear sections: POLISHED TEXT, IMPROVEMENTS MADE, SUGGESTIONS, QUALITY SCORE
        """

    def _get_grammar_polish_prompt(self, draft_text: str, target_audience: str, research_context: str) -> str:
        return f"""
        Focus specifically on grammar, punctuation, and language mechanics for this academic text:

        DRAFT:
        {draft_text}

        Correct and improve:
        1. Grammar errors
        2. Punctuation mistakes
        3. Spelling errors
        4. Sentence fragments or run-ons
        5. Subject-verb agreement
        6. Tense consistency
        7. Word usage and precision

        Provide the corrected text and list all corrections made.
        Format: CORRECTED TEXT, CORRECTIONS MADE
        """

    def _get_structure_polish_prompt(self, draft_text: str, target_audience: str, research_context: str) -> str:
        return f"""
        Focus on improving the structural organization of this academic text:

        RESEARCH CONTEXT:
        {research_context}

        DRAFT:
        {draft_text}

        Improve:
        1. Overall document structure
        2. Paragraph organization
        3. Topic sentences
        4. Transitions between ideas
        5. Logical flow of arguments
        6. Section balance

        Provide restructured text and explain structural improvements.
        Format: RESTRUCTURED TEXT, STRUCTURAL IMPROVEMENTS
        """

    def _get_clarity_polish_prompt(self, draft_text: str, target_audience: str, research_context: str) -> str:
        return f"""
        Enhance clarity and readability for {target_audience} audience:

        DRAFT:
        {draft_text}

        Focus on:
        1. Simplifying complex sentences
        2. Clarifying ambiguous statements
        3. Improving word choice
        4. Reducing redundancy
        5. Enhancing precision
        6. Making arguments more explicit

        Provide clarified text and list clarity improvements.
        Format: CLARIFIED TEXT, CLARITY IMPROVEMENTS
        """

    def _get_citations_polish_prompt(self, draft_text: str, target_audience: str, research_context: str) -> str:
        return f"""
        Focus on improving citation integration and academic referencing:

        RESEARCH CONTEXT:
        {research_context}

        DRAFT:
        {draft_text}

        Improve:
        1. Citation integration into text flow
        2. Proper attribution of ideas
        3. Balance of cited vs original content
        4. Citation formatting consistency
        5. Source variety and quality
        6. Avoiding over-citation or under-citation

        Provide improved text with better citation integration.
        Format: IMPROVED TEXT, CITATION IMPROVEMENTS
        """

    def _extract_improvements(self, response: str) -> List[str]:
        """Extract list of improvements from response"""
        improvements = []
        lines = response.split('\n')
        in_improvements_section = False

        for line in lines:
            if 'IMPROVEMENTS' in line.upper() or 'CORRECTIONS' in line.upper():
                in_improvements_section = True
                continue
            elif line.strip() and line.strip().startswith(('POLISHED', 'SUGGESTIONS', 'QUALITY')):
                in_improvements_section = False
            elif in_improvements_section and line.strip():
                if line.strip().startswith(('-', '*', '•')) or any(num in line[:3] for num in ['1.', '2.', '3.']):
                    improvements.append(line.strip())

        return improvements[:10]  # Limit to 10 improvements

    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract suggestions from response"""
        suggestions = []
        lines = response.split('\n')
        in_suggestions_section = False

        for line in lines:
            if 'SUGGESTIONS' in line.upper():
                in_suggestions_section = True
                continue
            elif line.strip() and line.strip().startswith('QUALITY'):
                in_suggestions_section = False
            elif in_suggestions_section and line.strip():
                if line.strip().startswith(('-', '*', '•')) or any(num in line[:3] for num in ['1.', '2.', '3.']):
                    suggestions.append(line.strip())

        return suggestions[:5]  # Limit to 5 suggestions

    def _assess_quality_score(self, original_text: str, polished_response: str) -> float:
        """Assess quality improvement score"""
        # Simplified scoring based on response content
        if 'excellent' in polished_response.lower() or 'high quality' in polished_response.lower():
            return 9.0
        elif 'good' in polished_response.lower() or 'well' in polished_response.lower():
            return 7.5
        elif 'improvement' in polished_response.lower():
            return 6.0
        else:
            return 7.0  # Default score

    def _extract_polished_text(self, response: str, original_text: str) -> str:
        """Extract polished text from response"""
        lines = response.split('\n')
        polished_lines = []
        in_polished_section = False

        for line in lines:
            if any(marker in line.upper() for marker in
                   ['POLISHED TEXT', 'CORRECTED TEXT', 'RESTRUCTURED TEXT', 'CLARIFIED TEXT', 'IMPROVED TEXT']):
                in_polished_section = True
                continue
            elif line.strip() and any(
                    marker in line.upper() for marker in ['IMPROVEMENTS', 'CORRECTIONS', 'SUGGESTIONS', 'QUALITY']):
                in_polished_section = False
            elif in_polished_section and line.strip():
                polished_lines.append(line)

        polished_text = '\n'.join(polished_lines).strip()
        return polished_text if polished_text else original_text

    def compare_versions(self, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two versions of a draft"""
        prompt = f"""
        Compare these two versions of an academic text and provide analysis:

        VERSION 1:
        {version1}

        VERSION 2:
        {version2}

        Analyze:
        1. Key differences
        2. Improvements in version 2
        3. Any potential losses
        4. Overall recommendation
        5. Quality comparison (rate each version 1-10)

        Provide detailed comparison analysis.
        """

        analysis = self.generate_response(prompt)
        return {
            "comparison_analysis": analysis,
            "version1_length": len(version1.split()),
            "version2_length": len(version2.split()),
            "timestamp": datetime.datetime.now().isoformat()
        }