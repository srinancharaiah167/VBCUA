def calculate_final_score(similarity_score, audio_features, filler_result):
    pause_ratio = audio_features["pause_ratio"]
    avg_rms = audio_features["avg_rms"]
    filler_count = filler_result["total_filler_words"]

    # 1. Semantic score
    semantic_score = similarity_score

    # 2. Pause score
    # Less pause ratio means better score
    pause_score = max(0, 100 - pause_ratio)

    # 3. Filler score
    # Each filler word reduces 5 marks, maximum penalty 40
    filler_penalty = min(filler_count * 5, 40)
    filler_score = max(0, 100 - filler_penalty)

    # 4. Voice energy score
    if avg_rms >= 0.05:
        energy_score = 100
    elif avg_rms >= 0.02:
        energy_score = 75
    elif avg_rms > 0:
        energy_score = 50
    else:
        energy_score = 0

    # Final weighted score
    final_score = (
        semantic_score * 0.60 +
        pause_score * 0.15 +
        filler_score * 0.15 +
        energy_score * 0.10
    )

    final_score = round(final_score, 2)

    if final_score >= 80:
        final_feedback = "Excellent Concept Understanding and Clear Communication"
    elif final_score >= 65:
        final_feedback = "Good Understanding with Minor Improvements Needed"
    elif final_score >= 50:
        final_feedback = "Moderate Understanding; Improve Clarity and Fluency"
    else:
        final_feedback = "Needs Improvement in Concept Explanation and Speech Delivery"

    suggestions = []

    if similarity_score < 50:
        suggestions.append("Improve conceptual accuracy by covering the core definition, examples, and applications.")
    elif similarity_score < 80:
        suggestions.append("Your concept explanation is partially correct. Add more key points and examples.")

    if pause_ratio > 40:
        suggestions.append("Reduce long pauses and practice explaining the topic in a continuous flow.")

    if filler_count > 5:
        suggestions.append("Reduce filler words such as um, uh, like, actually, and basically.")

    if avg_rms < 0.02:
        suggestions.append("Speak louder and more clearly to improve voice confidence.")

    if not suggestions:
        suggestions.append("Good performance. Continue practicing with more advanced concepts.")

    return {
        "semantic_score": round(semantic_score, 2),
        "pause_score": round(pause_score, 2),
        "filler_score": round(filler_score, 2),
        "energy_score": round(energy_score, 2),
        "final_score": final_score,
        "final_feedback": final_feedback,
        "suggestions": suggestions
    }