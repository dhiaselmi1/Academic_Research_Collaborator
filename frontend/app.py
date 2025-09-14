import streamlit as st
import requests
import json
from typing import Dict, Any, List
import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Academic Research Collaborator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-fill {
        height: 20px;
        background-color: #1f77b4;
        transition: width 0.3s ease;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"status": "error", "message": str(e)}


def display_progress_bar(progress_data: Dict):
    """Display research progress"""
    if not progress_data:
        return

    completed = sum(progress_data.values())
    total = len(progress_data)
    percentage = (completed / total * 100) if total > 0 else 0

    st.markdown("### Research Progress")

    # Overall progress bar
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {percentage}%"></div>
    </div>
    <p style="text-align: center;">{percentage:.1f}% Complete ({completed}/{total} tasks)</p>
    """, unsafe_allow_html=True)

    # Individual progress items
    col1, col2, col3 = st.columns(3)

    with col1:
        status = "✅" if progress_data.get('literature_review_completed', False) else "⏳"
        st.markdown(f"**Literature Review** {status}")

    with col2:
        status = "✅" if progress_data.get('hypothesis_validated', False) else "⏳"
        st.markdown(f"**Hypothesis Validation** {status}")

    with col3:
        status = "✅" if progress_data.get('draft_polished', False) else "⏳"
        st.markdown(f"**Draft Polishing** {status}")


def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Academic Research Collaborator</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")

        # API Health Check
        if st.button("🔍 Check API Status"):
            health = make_api_request("/health")
            if health.get("status") == "healthy":
                st.success("✅ API is running")
            else:
                st.error("❌ API is down")

        st.markdown("---")

        # Memory Management
        st.subheader("💾 Memory Management")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📋 View Memory"):
                st.session_state.show_memory = True

        with col2:
            if st.button("🗑️ Clear Memory"):
                result = make_api_request("/memory", method="DELETE")
                if result.get("status") == "success":
                    st.success("Memory cleared!")
                    st.rerun()

        st.markdown("---")

        # Research Progress
        progress_result = make_api_request("/research-progress")
        if progress_result.get("status") == "success":
            progress_data = progress_result.get("progress", {})
            display_progress_bar(progress_data)

    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔬 Research Setup",
        "📖 Literature Review",
        "💡 Hypothesis Validation",
        "✍️ Draft Polishing",
        "📊 Dashboard"
    ])

    with tab1:
        research_setup_tab()

    with tab2:
        literature_review_tab()

    with tab3:
        hypothesis_validation_tab()

    with tab4:
        draft_polishing_tab()

    with tab5:
        dashboard_tab()

    # Show memory if requested
    if st.session_state.get('show_memory', False):
        show_memory_modal()


def research_setup_tab():
    """Research setup and input tab"""
    st.header("🔬 Research Setup")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Research Question")
        research_question = st.text_area(
            "Enter your research question:",
            height=100,
            placeholder="What is the impact of social media on academic performance among university students?"
        )

        st.subheader("Citations & Sources")
        citations_text = st.text_area(
            "Enter your citations (one per line):",
            height=200,
            placeholder="""Smith, J. (2023). Social Media and Academic Performance. Journal of Education, 45(2), 123-145.
Johnson, A. (2022). Digital Distractions in Higher Education. Educational Psychology Review, 34(3), 567-589."""
        )

        st.subheader("Research Notes")
        notes_text = st.text_area(
            "Enter your research notes (one per line):",
            height=150,
            placeholder="""Initial observation: Students spend average 3.5 hours daily on social media
Hypothesis: Negative correlation between social media usage and GPA
Key variables: Usage time, GPA, study habits"""
        )

    with col2:
        st.subheader("📊 Current Status")

        # Get current memory
        memory_result = make_api_request("/memory")
        if memory_result.get("status") == "success":
            memory = memory_result.get("memory", {})

            # Display metrics
            st.markdown(f"""
            <div class="metric-card">
                <h4>📝 Research Question</h4>
                <p>{memory.get('research_question', 'Not set')[:100]}{('...' if len(memory.get('research_question', '')) > 100 else '')}</p>
            </div>
            <div class="metric-card">
                <h4>📚 Citations</h4>
                <p>{len(memory.get('citations', []))} sources</p>
            </div>
            <div class="metric-card">
                <h4>📋 Notes</h4>
                <p>{len(memory.get('notes', []))} entries</p>
            </div>
            """, unsafe_allow_html=True)

    # Save research setup
    if st.button("💾 Save Research Setup", type="primary"):
        citations = [cite.strip() for cite in citations_text.split('\n') if cite.strip()]
        notes = [note.strip() for note in notes_text.split('\n') if note.strip()]

        if research_question.strip():
            with st.spinner("Saving research setup..."):
                result = make_api_request("/literature-review", method="POST", data={
                    "research_question": research_question,
                    "citations": citations,
                    "notes": notes
                })

                if result.get("status") == "success":
                    st.success("✅ Research setup saved successfully!")
                    st.info("You can now proceed to Literature Review tab.")
                else:
                    st.error("Failed to save research setup")
        else:
            st.warning("Please enter a research question")


def literature_review_tab():
    """Literature review analysis tab"""
    st.header("📖 Literature Review")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Conduct Literature Review")

        # Option to add more sources
        additional_citations = st.text_area(
            "Add additional citations (optional):",
            height=100,
            placeholder="New citations to include in the review..."
        )

        additional_notes = st.text_area(
            "Add additional notes (optional):",
            height=100,
            placeholder="Additional research notes..."
        )

        if st.button("🔍 Conduct Literature Review", type="primary"):
            additional_citations_list = [cite.strip() for cite in additional_citations.split('\n') if cite.strip()]
            additional_notes_list = [note.strip() for note in additional_notes.split('\n') if note.strip()]

            with st.spinner("Conducting literature review... This may take a moment."):
                result = make_api_request("/literature-review", method="POST", data={
                    "research_question": "",  # Will use stored question
                    "citations": additional_citations_list,
                    "notes": additional_notes_list
                })

                if result.get("status") == "success":
                    st.success("✅ Literature review completed!")
                    st.session_state.literature_review_result = result
                else:
                    st.error("Failed to conduct literature review")

        # Source Quality Analysis
        st.markdown("---")
        st.subheader("📊 Source Quality Analysis")

        if st.button("Analyze Source Quality"):
            # Get citations from memory
            memory_result = make_api_request("/memory")
            if memory_result.get("status") == "success":
                citations = memory_result.get("memory", {}).get("citations", [])

                if citations:
                    with st.spinner("Analyzing source quality..."):
                        result = make_api_request("/analyze-sources", method="POST", data={
                            "citations": citations
                        })

                        if result.get("status") == "success":
                            st.session_state.source_analysis = result.get("analysis")
                else:
                    st.warning("No citations found. Please add sources in Research Setup.")

    with col2:
        st.subheader("📋 Review Results")

        # Display literature review results
        if 'literature_review_result' in st.session_state:
            result = st.session_state.literature_review_result

            with st.expander("📖 Literature Review", expanded=True):
                st.write(result.get("review", ""))

            with st.expander("💡 Recommendations"):
                recommendations = result.get("recommendations", [])
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")

            st.metric("Sources Analyzed", result.get("sources_analyzed", 0))

        # Display source analysis
        if 'source_analysis' in st.session_state:
            analysis = st.session_state.source_analysis

            with st.expander("📊 Source Quality Analysis", expanded=True):
                st.write(analysis.get("analysis", ""))


def hypothesis_validation_tab():
    """Hypothesis validation tab"""
    st.header("💡 Hypothesis Validation")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Enter Your Hypothesis")

        hypothesis = st.text_area(
            "Research Hypothesis:",
            height=120,
            placeholder="Students who spend more than 4 hours daily on social media will have significantly lower GPAs compared to those who spend less than 2 hours daily."
        )

        if st.button("🔬 Validate Hypothesis", type="primary"):
            if hypothesis.strip():
                with st.spinner("Validating hypothesis... This may take a moment."):
                    result = make_api_request("/validate-hypothesis", method="POST", data={
                        "hypothesis": hypothesis,
                        "research_question": ""  # Will use stored question
                    })

                    if result.get("status") == "success":
                        st.success("✅ Hypothesis validation completed!")
                        st.session_state.validation_result = result
                    else:
                        st.error("Failed to validate hypothesis")
            else:
                st.warning("Please enter a hypothesis")

        st.markdown("---")
        st.subheader("🎲 Generate Alternative Hypotheses")

        context = st.text_area(
            "Additional context (optional):",
            height=80,
            placeholder="Any specific context or constraints for generating alternatives..."
        )

        if st.button("Generate Alternatives"):
            # Get research question from memory
            memory_result = make_api_request("/memory")
            if memory_result.get("status") == "success":
                research_question = memory_result.get("memory", {}).get("research_question", "")

                if research_question:
                    with st.spinner("Generating alternative hypotheses..."):
                        result = make_api_request("/generate-alternatives", method="POST", data={
                            "research_question": research_question,
                            "context": context
                        })

                        if result.get("status") == "success":
                            st.session_state.alternatives = result.get("alternative_hypotheses", [])
                else:
                    st.warning("No research question found. Please set up your research first.")

    with col2:
        st.subheader("📊 Validation Results")

        # Display validation results
        if 'validation_result' in st.session_state:
            result = st.session_state.validation_result
            validation = result.get("validation", {})

            # Overall score
            score = validation.get("overall_score", 0)
            assessment = validation.get("assessment", "Unknown")

            st.metric("Overall Score", f"{score:.1f}/10", assessment)

            with st.expander("📋 Detailed Analysis", expanded=True):
                st.write(validation.get("detailed_analysis", ""))

            with st.expander("💡 Improvement Recommendations"):
                recommendations = result.get("recommendations", [])
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")

        # Display alternative hypotheses
        if 'alternatives' in st.session_state:
            st.subheader("🎲 Alternative Hypotheses")

            alternatives = st.session_state.alternatives
            for i, alt in enumerate(alternatives, 1):
                with st.expander(f"Alternative {i}"):
                    st.write(alt)


def draft_polishing_tab():
    """Draft polishing tab"""
    st.header("✍️ Draft Polishing")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Submit Your Draft")

        draft_text = st.text_area(
            "Paste your draft text:",
            height=300,
            placeholder="Paste your academic draft here for polishing..."
        )

        # Polish options
        col_a, col_b = st.columns(2)

        with col_a:
            polish_type = st.selectbox(
                "Polish Type:",
                ["comprehensive", "grammar", "structure", "clarity", "citations"],
                help="Choose the type of polishing you want"
            )

        with col_b:
            target_audience = st.selectbox(
                "Target Audience:",
                ["academic", "general", "undergraduate", "graduate", "professional"],
                help="Choose your target audience"
            )

        if st.button("✨ Polish Draft", type="primary"):
            if draft_text.strip():
                with st.spinner("Polishing draft... This may take a moment."):
                    result = make_api_request("/polish-draft", method="POST", data={
                        "draft_text": draft_text,
                        "polish_type": polish_type,
                        "target_audience": target_audience
                    })

                    if result.get("status") == "success":
                        st.success("✅ Draft polished successfully!")
                        st.session_state.polish_result = result
                        st.session_state.original_draft = draft_text
                    else:
                        st.error("Failed to polish draft")
            else:
                st.warning("Please enter draft text")

        # Draft comparison
        st.markdown("---")
        st.subheader("📊 Compare Draft Versions")

        if 'polish_result' in st.session_state:
            if st.button("Compare Original vs Polished"):
                original = st.session_state.get('original_draft', '')
                polished = st.session_state.polish_result.get('polished_text', '')

                with st.spinner("Comparing versions..."):
                    result = make_api_request("/compare-drafts", method="POST", data={
                        "version1": original,
                        "version2": polished
                    })

                    if result.get("status") == "success":
                        st.session_state.comparison_result = result.get("comparison")

    with col2:
        st.subheader("✨ Polished Results")

        # Display polishing results
        if 'polish_result' in st.session_state:
            result = st.session_state.polish_result

            # Quality score
            quality_score = result.get("quality_score", 0)
            st.metric("Quality Score", f"{quality_score:.1f}/10")

            # Polished text
            with st.expander("📝 Polished Text", expanded=True):
                polished_text = result.get("polished_text", "")
                st.text_area("", value=polished_text, height=200, disabled=True)

                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.write("Text ready for copying:")
                    st.code(polished_text)

            # Improvements
            with st.expander("🔧 Improvements Made"):
                improvements = result.get("improvements", [])
                for imp in improvements:
                    st.write(f"• {imp}")

            # Suggestions
            with st.expander("💡 Suggestions for Further Improvement"):
                suggestions = result.get("suggestions", [])
                for sugg in suggestions:
                    st.write(f"• {sugg}")

        # Display comparison results
        if 'comparison_result' in st.session_state:
            comparison = st.session_state.comparison_result

            with st.expander("📊 Version Comparison", expanded=True):
                st.write(comparison.get("comparison_analysis", ""))

                col_x, col_y = st.columns(2)
                with col_x:
                    st.metric("Original Length", f"{comparison.get('version1_length', 0)} words")
                with col_y:
                    st.metric("Polished Length", f"{comparison.get('version2_length', 0)} words")


def dashboard_tab():
    """Research dashboard tab"""
    st.header("📊 Research Dashboard")

    # Get research progress
    progress_result = make_api_request("/research-progress")

    if progress_result.get("status") == "success":
        data = progress_result

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Completion", f"{data.get('completion_percentage', 0):.1f}%")

        with col2:
            st.metric("Citations", data.get('total_citations', 0))

        with col3:
            st.metric("Reviews", data.get('total_reviews', 0))

        with col4:
            st.metric("Drafts", data.get('total_drafts', 0))

        # Research question
        st.subheader("🎯 Current Research Question")
        research_q = data.get('research_question', 'No research question set')
        st.info(research_q)

        # Detailed progress
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📋 Task Progress")
            progress = data.get('progress', {})

            for task, completed in progress.items():
                status = "✅ Complete" if completed else "⏳ Pending"
                task_name = task.replace('_', ' ').title()
                st.write(f"**{task_name}**: {status}")

        with col_right:
            st.subheader("📈 Research Statistics")

            stats_data = [
                ("Literature Reviews", data.get('total_reviews', 0)),
                ("Hypotheses Validated", data.get('total_hypotheses', 0)),
                ("Draft Versions", data.get('total_drafts', 0)),
                ("Research Notes", data.get('total_notes', 0))
            ]

            for stat_name, stat_value in stats_data:
                st.write(f"**{stat_name}**: {stat_value}")

        # Export functionality
        st.markdown("---")
        st.subheader("📤 Export Research Data")

        if st.button("📥 Export All Data"):
            result = make_api_request("/export-research")

            if result.get("status") == "success":
                export_data = result.get("export_data", {})

                # Convert to JSON string for download
                json_string = json.dumps(export_data, indent=2, ensure_ascii=False)

                st.download_button(
                    label="💾 Download Research Data (JSON)",
                    data=json_string,
                    file_name=f"research_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

                st.success("✅ Research data ready for download!")


def show_memory_modal():
    """Show memory content in modal"""
    st.subheader("💾 Memory Content")

    memory_result = make_api_request("/memory")

    if memory_result.get("status") == "success":
        memory = memory_result.get("memory", {})

        # Display memory as JSON
        st.json(memory)
    else:
        st.error("Failed to load memory")

    if st.button("Close"):
        st.session_state.show_memory = False
        st.rerun()


if __name__ == "__main__":
    # Initialize session state
    if 'show_memory' not in st.session_state:
        st.session_state.show_memory = False

    main()