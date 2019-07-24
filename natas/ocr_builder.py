from .normalize import is_in_dictionary, wiktionary, _get_spacy
import distance
from collections import defaultdict


def get_min_distance(word, words):
	min = 2000000
	min_word = ""
	for w in words:
		d = distance.levenshtein(w, word)
		if d < min:
			min = d
			min_word = w
	return min_word, min

def extract_parallel(seed_words, model, dictionary=wiktionary, lemmatize=True, use_freq=True, word_len=0, min_frequency=1000, cache=False, cache_name="ocr"):
	res = defaultdict(dict)
	for word in seed_words:
		if use_freq and seed_words[word] < min_frequency:
			continue
		word = word.strip().lower()
		if len(word) < word_len:
			continue
		errors = get_ocr_error_dict(word, model, dictionary, lemmatize=lemmatize, cache=cache,cache_name=cache_name)
		for correct in errors:
			res[correct].update(errors[correct])
	return res

def get_wv_normalization(word, model, dictionary, lemmatize=True, cache=True, cache_name="ocr"):
	res = get_ocr_error_dict(word,model, dictionary, lemmatize=lemmatize, cache=cache, cache_name=cache_name)
	for key, value in res.iteritems():
		if word in value and value[word] < 4:
			return key
	return ""

def get_ocr_error_dict(word, model, dictionary, lemmatize=True, cache=True, cache_name="ocr"):
	ocr_errors = []
	non_errors = [word]
	if lemmatize:
		spacy_nlp = _get_spacy()
	else:
		spacy_nlp = None
	try:
		pot_ocr_errors = model.most_similar(word)
	except:
		#word not in vocabulary
		return []

	for pot_ocr_error in pot_ocr_errors:
		pot_ocr_error = pot_ocr_error[0]
		if not is_in_dictionary(pot_ocr_error, dictionary, spacy_nlp, cache=cache, cache_name=cache_name,lemmatize=lemmatize):
			ocr_errors.append(pot_ocr_error)
		else:
			non_errors.append(pot_ocr_error)

	results = defaultdict(dict)
	for error in ocr_errors:
		w, d = get_min_distance(error, non_errors)
		results[w][error] = d
	return results

