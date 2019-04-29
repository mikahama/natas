from .normalize import _normalize, set_spacy

def normalize_words(words):
	return _normalize(words, "normalization.pt")

