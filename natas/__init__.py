from .normalize import _normalize, set_spacy, wiktionary, _get_spacy
from .normalize import is_in_dictionary as _is_in_dictionary

def normalize_words(words, n_best=10, dictionary=None, all_candidates=True):
	return _normalize(words, "normalization.pt", n_best=n_best, dictionary=dictionary, all_candidates=all_candidates)

def is_correctly_spelled(word, dictionary=wiktionary, cache=True):
	return _is_in_dictionary(word.lower(), dictionary, _get_spacy(), cache)