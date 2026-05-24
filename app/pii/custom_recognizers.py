import re 
from presidio_analyzer import Pattern, PatternRecognizer


# Pattern tuning to catch common profile and porfile-like URLs
LINKEDIN_PATTERN = r"(?:https?://)?(?:www\.)?linkedin\.com/(?:in|pub|company)/[A-Za-z0-9\-\_\.\/]+"
GITHUB_PATTERN = r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9\-\_]+(?:/[A-Za-z0-9\-\_]+)?"
PORTFOLIO_HOSTS = [
    r"(?:https?://)?(?:www\.)?behance\.net/[A-Za-z0-9\-\_]+",
    r"(?:https?://)?(?:www\.)?dribbble\.com/[A-Za-z0-9\-\_]+",
    r"(?:https?://)?(?:www\.)?medium\.com/@[A-Za-z0-9\-\_]+",
    r"(?:https?://)?(?:www\.)?[A-Za-z0-9\-\_]+\.dev",
    r"(?:https?://)?(?:www\.)?[A-Za-z0-9\-\_]+\.me",
    r"(?:https?://)?(?:www\.)?[A-Za-z0-9\-\_]+\.io",
]

class LinkedInRecognizer(PatternRecognizer):
    """
    Recognizer for LinkedIn, GitHub, and portfolio URLs.
    Returns entity_type 'URL' with a custom score and context.
    """

    def __init__(self):
        patterns = [
            Pattern("LINKEDIN", LINKEDIN_PATTERN, 0.95),
            Pattern("GITHUB", GITHUB_PATTERN, 0.95),
        ]
        # add portfolio hosts
        for i, p in enumerate(PORTFOLIO_HOSTS):
            patterns.append(Pattern(f"PORTFOLIO_{i}", p, 0.9))

        # Use a generic name 'URL' so anonymizer rules can be shared
        super().__init__(supported_entity="URL", patterns=patterns, name="LinkedProfileRecognizer")