import os
import streamlit as st

from modules.transcription import transcribe_audio
from modules.semantic_analysis import calculate_similarity
from modules.audio_analysis import extract_audio_features, generate_waveform
from modules.filler_detection import detect_filler_words
from modules.scoring import calculate_final_score
from modules.report_generator import generate_pdf_report

st.set_page_config(
    page_title="VBCUA",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.write(
    "Upload your spoken explanation and get AI-based concept understanding feedback."
)

st.divider()

concept_name = st.text_input(
    "Enter Concept Name",
    placeholder="Example: Machine Learning"
)

reference_text = st.text_area(
    "Enter Reference Concept Explanation",
    placeholder="Example: Machine learning is a branch of AI that allows computers to learn from data..."
)

uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file is not None:
    st.subheader("Uploaded Audio")
    st.audio(uploaded_file)

if st.button("Analyse"):
    if uploaded_file is None:
        st.error("Please upload an audio file.")
    elif reference_text.strip() == "":
        st.error("Please enter reference concept explanation.")
    else:
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("data/waveforms", exist_ok=True)
        os.makedirs("data/reports", exist_ok=True)

        file_extension = uploaded_file.name.split(".")[-1]
        audio_path = os.path.join("data/uploads", f"uploaded_audio.{file_extension}")

        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.info("Transcribing audio using Whisper...")
        transcription = transcribe_audio(audio_path)
        st.success("Transcription completed.")

        st.info("Calculating semantic similarity...")
        similarity_score = calculate_similarity(transcription, reference_text)
        st.success("Semantic analysis completed.")

        st.info("Extracting audio features...")
        audio_features = extract_audio_features(audio_path)
        waveform_path = os.path.join("data/waveforms", "waveform.png")
        waveform_result = generate_waveform(audio_path, waveform_path)
        st.success("Audio feature extraction completed.")

        st.info("Detecting filler words...")
        filler_result = detect_filler_words(transcription)
        st.success("Filler word detection completed.")

        st.info("Calculating final score...")
        score_result = calculate_final_score(similarity_score, audio_features, filler_result)
        st.success("Final scoring completed.")

        report_path = os.path.join("data/reports", "vbcu_report.pdf")

        generate_pdf_report(
            report_path=report_path,
            concept_name=concept_name,
            reference_text=reference_text,
            transcription=transcription,
            similarity_score=similarity_score,
            audio_features=audio_features,
            filler_result=filler_result,
            score_result=score_result,
            waveform_path=waveform_path
        )

        st.divider()

        st.subheader("Final Analysis Summary")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Semantic Similarity", f"{similarity_score}%")

        with col2:
            st.metric("Audio Duration", f"{audio_features['duration']} sec")

        with col3:
            st.metric("Pause Ratio", f"{audio_features['pause_ratio']}%")

        with col4:
            st.metric("Filler Words", filler_result["total_filler_words"])

        with col5:
            st.metric("Final Score", f"{score_result['final_score']}%")

        st.subheader("Final Feedback")

        if score_result["final_score"] >= 80:
            st.success(score_result["final_feedback"])
        elif score_result["final_score"] >= 50:
            st.warning(score_result["final_feedback"])
        else:
            st.error(score_result["final_feedback"])

        st.subheader("Improvement Suggestions")
        for suggestion in score_result["suggestions"]:
            st.write("- " + suggestion)

        st.subheader("Download Report")

        with open(report_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name="vbcu_report.pdf",
                mime="application/pdf"
            )

        st.divider()

        col6, col7 = st.columns(2)

        with col6:
            st.subheader("Audio Feature Analysis")
            st.write("Audio Duration:", audio_features["duration"], "sec")
            st.write("Average RMS Energy:", audio_features["avg_rms"])
            st.write("Pause Ratio:", audio_features["pause_ratio"], "%")
            st.write("Voice Energy Level:", audio_features["confidence_level"])

            st.subheader("Filler Word Analysis")
            st.write("Total Filler Words:", filler_result["total_filler_words"])
            st.write("Detected Fillers:", filler_result["detected_fillers"])
            st.write("Feedback:", filler_result["filler_feedback"])

            st.subheader("Score Breakdown")
            st.write("Semantic Score:", score_result["semantic_score"])
            st.write("Pause Score:", score_result["pause_score"])
            st.write("Filler Score:", score_result["filler_score"])
            st.write("Energy Score:", score_result["energy_score"])

        with col7:
            st.subheader("Concept")
            st.write(concept_name)

            st.subheader("Uploaded Audio")
            st.audio(uploaded_file)

            st.subheader("Waveform Visualization")
            if waveform_result:
                st.image(waveform_result, caption="Uploaded Audio Waveform", use_container_width=True)
            else:
                st.warning("Waveform could not be generated because the audio file was empty or unreadable.")

        st.divider()

        st.subheader("Transcribed Explanation")
        st.write(transcription)

        st.subheader("Reference Concept Explanation")
        st.write(reference_text)