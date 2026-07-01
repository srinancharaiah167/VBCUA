from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_pdf_report(
    report_path,
    concept_name,
    reference_text,
    transcription,
    similarity_score,
    audio_features,
    filler_result,
    score_result,
    waveform_path
):
    doc = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("Voice-Based Concept Understanding Analyser Report", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Concept Name:</b>", styles["Heading2"]))
    story.append(Paragraph(concept_name if concept_name else "Not Provided", styles["BodyText"]))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("<b>Final Feedback:</b>", styles["Heading2"]))
    story.append(Paragraph(score_result["final_feedback"], styles["BodyText"]))
    story.append(Spacer(1, 0.15 * inch))

    score_data = [
        ["Metric", "Value"],
        ["Semantic Similarity", f"{similarity_score}%"],
        ["Audio Duration", f"{audio_features['duration']} sec"],
        ["Pause Ratio", f"{audio_features['pause_ratio']}%"],
        ["Average RMS Energy", str(audio_features["avg_rms"])],
        ["Voice Energy Level", audio_features["confidence_level"]],
        ["Filler Words", str(filler_result["total_filler_words"])],
        ["Final Score", f"{score_result['final_score']}%"]
    ]

    table = Table(score_data, colWidths=[2.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(Paragraph("<b>Evaluation Metrics:</b>", styles["Heading2"]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Score Breakdown:</b>", styles["Heading2"]))
    breakdown_text = f"""
    Semantic Score: {score_result['semantic_score']}<br/>
    Pause Score: {score_result['pause_score']}<br/>
    Filler Score: {score_result['filler_score']}<br/>
    Energy Score: {score_result['energy_score']}
    """
    story.append(Paragraph(breakdown_text, styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Improvement Suggestions:</b>", styles["Heading2"]))
    for suggestion in score_result["suggestions"]:
        story.append(Paragraph(f"- {suggestion}", styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Filler Word Analysis:</b>", styles["Heading2"]))
    story.append(Paragraph(f"Detected Fillers: {filler_result['detected_fillers']}", styles["BodyText"]))
    story.append(Paragraph(f"Feedback: {filler_result['filler_feedback']}", styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Waveform Visualization:</b>", styles["Heading2"]))
    try:
        waveform_image = Image(waveform_path, width=6 * inch, height=2.2 * inch)
        story.append(waveform_image)
    except Exception:
        story.append(Paragraph("Waveform image could not be added.", styles["BodyText"]))

    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Transcribed Explanation:</b>", styles["Heading2"]))
    story.append(Paragraph(transcription if transcription else "No transcription available.", styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Reference Concept Explanation:</b>", styles["Heading2"]))
    story.append(Paragraph(reference_text if reference_text else "No reference text provided.", styles["BodyText"]))

    doc.build(story)

    return report_path