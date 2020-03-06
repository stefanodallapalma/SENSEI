from modules.software_quality.projects.known_datasets.DUTADataset import DUTADataset
from utils.FileUtils import load_json, save_json
import os

if __name__ == "__main__":
    dataset = DUTADataset()
    pages_path = "../resources/raw/"

    duta1 = load_json(os.path.join(dataset.path, "Duta1.json"))
    duta2 = load_json(os.path.join(dataset.path, "Duta2.json"))
    duta = []

    for i in range(len(duta1)):
        page1 = duta1[i]
        page2 = duta2[i]

        if all(page1[key] is None for key in ("number_links", "number_of_words", "min_words_in_sentence",
                                             "max_words_in_sentence", "bitcoin", "deep_web")):
            duta.append(page2)
        else:
            duta.append(page1)

    save_json(os.path.join(dataset.path, "Duta.json"), duta)