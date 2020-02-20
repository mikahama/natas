from mikatools import *
import os

def main():
	url = "https://github.com/mikahama/natas/raw/master/natas/models/"
	models = ["normalization_brnn_latech19.pt", "normalization.pt", "ocr_ranlp19.pt", "ocr.pt"]
	model_path = script_path("models")
	if not os.path.exists(model_path):
		os.mkdir(model_path)
	for i, model in enumerate(models):
		print("Downloading", i+1, "out of", len(models) )
		download_file(url + model, script_path("models/" + model), show_progress=True)

if __name__== "__main__":
  main()