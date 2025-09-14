from .base import BaseAgent

# Import agent classes with proper names
try:
    from .literature_review_agent import LiteratureReviewAgent
except ImportError:
    # Try with spaces in filename
    try:
        from importlib import import_module
        lit_module = import_module('agents.Literature Review Agent')
        LiteratureReviewAgent = lit_module.LiteratureReviewAgent
    except ImportError:
        print("Could not import LiteratureReviewAgent")
        LiteratureReviewAgent = None

try:
    from .hypothesis_validator_agent import HypothesisValidatorAgent
except ImportError:
    # Try with spaces in filename
    try:
        from importlib import import_module
        hyp_module = import_module('agents.Hypothesis Validator Agent')
        HypothesisValidatorAgent = hyp_module.HypothesisValidatorAgent
    except ImportError:
        print("Could not import HypothesisValidatorAgent")
        HypothesisValidatorAgent = None

try:
    from .draft_polisher_agent import DraftPolisherAgent
except ImportError:
    # Try with spaces in filename
    try:
        from importlib import import_module
        draft_module = import_module('agents.Draft Polisher Agent')
        DraftPolisherAgent = draft_module.DraftPolisherAgent
    except ImportError:
        print("Could not import DraftPolisherAgent")
        DraftPolisherAgent = None

__all__ = ['BaseAgent', 'LiteratureReviewAgent', 'HypothesisValidatorAgent', 'DraftPolisherAgent']