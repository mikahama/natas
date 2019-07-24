from .normalize import _normalize, set_spacy, wiktionary, _get_spacy
from .normalize import is_in_dictionary as _is_in_dictionary
from .ocr_builder import get_wv_normalization

class W2VException(Exception):
	pass

def normalize_words(words, n_best=10, dictionary=None, all_candidates=True, correct_spelling_cache=True):
	return _normalize(words, "normalization.pt", n_best=n_best, dictionary=dictionary, all_candidates=all_candidates,correct_spelling_cache=correct_spelling_cache)

def ocr_correct_words(words, n_best=10, dictionary=None, all_candidates=True, hybrid=False, hybrid_w2v_model=None,correct_spelling_cache=True):
	if hybrid is True and hybrid_w2v_model is None:
		raise W2VException("W2V model not specified")
	norms = _normalize(words, "ocr.pt", n_best=n_best, dictionary=dictionary, all_candidates=all_candidates,correct_spelling_cache=correct_spelling_cache)
	if hybrid:
		for i, l in enumerate(norms):
			if len(l) == 0:
				w2v_norm = get_wv_normalization(words[i], hybrid_w2v_model, dictionary, cache=correct_spelling_cache)
				if len(w2v_norm) > 0:
					l.append(w2v_norm)
		return norms
	else:
		return norms

def is_correctly_spelled(word, dictionary=wiktionary, cache=True):
	return _is_in_dictionary(word.lower(), dictionary, _get_spacy(), cache)