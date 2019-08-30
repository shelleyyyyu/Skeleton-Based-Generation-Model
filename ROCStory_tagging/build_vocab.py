import csv
import spacy
from tqdm import tqdm
from tqdm._tqdm import trange


def load_csv(filename):
    with open(filename, 'r') as File:
        stories = []
        lines = csv.reader(File)
        for line in lines:
            stories.append(line[1:])
    return stories[1:] 

def merge_data(file1, file2):
    data1 = load_csv(file1)
    data2 = load_csv(file2)
    merge_data = data1 + data2
    return merge_data

def wordcount(strl_ist):
	count_dict = {}
	for str in strl_ist:
		if str in count_dict.keys():
			count_dict[str] = count_dict[str] + 1
		else:
			count_dict[str] = 1
		count_list = sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
	return count_list


data = merge_data("./data/2016.csv","./data/2017.csv")

words = []
nlp = spacy.load('en')
print("----------------HERE 1----------------")
count_dict = {}
for sid, stories in enumerate(data):
	print("sid: %d" %sid)
	for s in stories:
		tokenized_data = nlp(s)
		for token in tokenized_data:
			w = token.string
			if w in count_dict.keys():
				count_dict[w] = count_dict[w] + 1
			else:
				count_dict[w] = 1
print("----------------HERE 2----------------")
count_list = sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
print("----------------HERE 3----------------")

with open("./new_data/vocab.txt", 'w') as file:
	for c in count_list:
		file.write(str(c[0]) + " " + str(c[1]) +'\n')