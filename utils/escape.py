import re

to_escape = r'_*\[\]()~`>#+-=|{}.!'


def escape(text: str) -> str:
    return re.sub(f'([{re.escape(to_escape)}])', r'\\\1', text)
