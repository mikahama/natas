from mikatools import script_path, json_load
from itertools import islice, repeat
import configargparse as cfargparse
import spacy
import os
from onmt_runner import Translator

wiktionary = None

def load_wiktionary():
	global wiktionary
	if wiktionary is not None:
		return
	try:
		wiktionary = set([x.lower() for x in json_load(script_path("wiktionary_lemmas.json"))])
	except:
		print("run python -m natas.download")
		wiktionary = []

is_in_data_cache = {"ceec_eng":{}, "ocr_fin":{}}

def set_spacy(nlp):
	models["spacy"] = nlp

def _get_spacy():
	if "spacy" not in models:
		try:
			models["spacy"] = spacy.load('en_core_web_md')
		except IOError:
			raise Exception("Spacy model was not loaded! Run: python -m spacy download en_core_web_md")
	return models["spacy"]

def split_corpus(f, shard_size):
    if shard_size <= 0:
        yield f
    else:
        while True:
            shard = list(islice(f, shard_size))
            if not shard:
                break
            yield shard

models = {}

def is_in_dictionary(word, correct_lemmas, spacy_nlp, cache=True, cache_name="ceec_eng", lemmatize=True):
	if correct_lemmas is None:
		load_wiktionary()
		correct_lemmas = wiktionary
	if cache and word in is_in_data_cache:
		return is_in_data_cache["ceec_eng"][word]
	if word in correct_lemmas:
		is_in_data_cache["ceec_eng"][word] = True
		return True
	if not lemmatize:
		is_in_data_cache["ceec_eng"][word] = False
		return False
	try:
		res = spacy_nlp(word)
		if len(res) > 1:
			is_in_data_cache["ceec_eng"][word] = False
			return False
		lemma = res[0].lemma_
	except:
		is_in_data_cache["ceec_eng"][word] = False
		return False
	if lemma in correct_lemmas:
		is_in_data_cache["ceec_eng"][word] = True
		return True
	is_in_data_cache["ceec_eng"][word] = False
	return False

def _dict_filter(results, dictionary, all_candidates=True, correct_spelling_cache=True):
	output = []
	nlp = _get_spacy()

	for word in results:
		cor = []
		for candidate in word:
			score = None
			if isinstance(candidate, list):
				score = candidate[1]
				candidate = candidate[0]
			candidate = candidate.replace(" ", "")
			if is_in_dictionary(candidate, dictionary, nlp, correct_spelling_cache):
				if score is not None:
					cor.append([candidate, score])
				else:
					cor.append(candidate)
				if not all_candidates:
					break
		output.append(cor)
	return output

class opennmt_opts(cfargparse.ArgumentParser):
	"""docstring for opennmt_opts"""
	def __init__(self, model, **kwargs):
		self.models = [model]
		for k, v in kwargs.items():
			setattr(self,k,v)

class fake_stream(object):
	"""docstring for fake_stream"""
	def __init__(self):
		self.lines = []
		self.scores = []

	def write(self, line):
		self.lines.append(line)

	def close(self):
		pass
	def flush(self):
		pass

	def __repr__(self):
		return "\n".join(self.lines)

	def load_scores(self, translated):
		self.scores = [[score.item() for score in score_set] for score_set in translated[0]]

	def get_lines(self):
		return str(self).split("\n")

	def get_scores(self):
		return self.scores

def _chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

def _parse_fake_stream(stream, n_best=10):
	parts = stream.get_lines()
	k = n_best + 1
	del parts[k-1::k]
	return _chunks(parts, n_best)

def _default_kwargs(words=None,n_best=10):
	return {"tgt_prefix":False,"fp32":False,"int8":False, "ban_unk_token":False, "random_sampling_topp":0.0,"avg_raw_probs":False,"batch_size":30,"attn_debug":False,"src":words,"tgt":None,"alpha":0.0,"beta":-0.0,"length_penalty":"none","coverage_penalty":"none","gpu":-1,"n_best":n_best,"min_length":0,"max_length":100,"ratio":-0.0,"beam_size":5,"random_sampling_topk":0,"random_sampling_temp":1.0,"stepwise_penalty":False,"dump_beam":"","block_ngram_repeat":0,"ignore_when_blocking":[],"replace_unk":True,"phrase_table":"","data_type":"text","verbose":False,"report_bleu":False,"report_rouge":False,"report_time":False,"seed":829,"shard_size":0}


def _load_model(name):
	model_path = script_path("models/" + name)
	if not os.path.exists(model_path):
		model_path = name
	m = Translator.load(model_path)
	models[name] = m

def _give_model(name):
	if name not in models:
		_load_model(name)
	return models[name]

def _split_words(words):
	return [" ".join(x.lower()) for x in words]

def call_onmt(words, model_name, n_best=10, return_scores=False):
	model = _give_model(model_name)
	tss = model.translate_many(words, n_best=n_best, return_scores=return_scores)
	res = []
	for ts in tss:
		if not isinstance(ts, list):
			ts = [ts]
		if return_scores is True:
			res.append([[t.text, t.score] for t in ts])
		else:
			res.append(ts)
	return res

def _normalize(words, model_name, n_best=5, dictionary=None, all_candidates=True, correct_spelling_cache=True, return_scores=False):
	res = call_onmt(_split_words(words), model_name, n_best=n_best, return_scores=return_scores)
	if dictionary is None:
		load_wiktionary()
		dictionary = wiktionary
	res = _dict_filter(res, dictionary, all_candidates=all_candidates, correct_spelling_cache=correct_spelling_cache)
	return res


