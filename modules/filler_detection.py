import re

def detect_filler_words(text):
    filler_words = [
        "um",
        "uh",
        "like",
        "actually",
        "basically",
        "you know",
        "i mean",
        "so",
        "well"
    ]

    text_lower = text.lower()

    detected_fillers = {}
    total_count = 0

    for filler in filler_words:
        pattern = r"\b" + re.escape(filler) + r"\b"
        matches = re.findall(pattern, text_lower)

        if matches:
            detected_fillers[filler] = len(matches)
            total_count += len(matches)

    if total_count == 0:
        filler_feedback = "Excellent speech clarity. No major filler words detected."
    elif total_count <= 3:
        filler_feedback = "Good speech flow. Very few filler words detected."
    elif total_count <= 7:
        filler_feedback = "Moderate filler usage. Try to reduce hesitation words."
    else:
        filler_feedback = "High filler word usage. Practice speaking more clearly and directly."

    return {
        "total_filler_words": total_count,
        "detected_fillers": detected_fillers,
        "filler_feedback": filler_feedback
    }