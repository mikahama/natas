from mikatools import *

def main():
	url = "https://github.com/mikahama/natas/raw/master/natas/models/"
	models = ["normalization_brnn_latech19.pt", "normalization.pt", "ocr_ranlp19.pt", "ocr.pt"]
	for i, model in enumerate(models):
		print("Downloading", i+1, "out of", len(models) )
		download_file(url + model, script_path("models/" + model), show_progress=True)

if __name__== "__main__":
  main()