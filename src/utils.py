import re
import unicodedata


def slugfy(text):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    normalized_text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    )
    lowercase_text = normalized_text.lower()
    alphanumeric_text = re.sub(r"[^a-z0-9\s-]", "", lowercase_text)
    slug = re.sub(r"\s+", "-", alphanumeric_text).strip("-_")
    return slug
