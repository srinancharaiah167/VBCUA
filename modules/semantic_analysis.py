from sentence_transformers import SentenceTransformer, util

_model = None

def load_sentence_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def calculate_similarity(user_text, reference_text):
    model = load_sentence_model()

    user_embedding = model.encode(user_text, convert_to_tensor=True)
    reference_embedding = model.encode(reference_text, convert_to_tensor=True)

    similarity = util.cos_sim(user_embedding, reference_embedding)

    similarity_score = float(similarity[0][0]) * 100

    return round(similarity_score, 2)