#{
#	"pos tagging": ["DET", "NOUN", "ADP", "DET", "NOUN", "VERB", "DET", "NOUN", "NOUN", "PUNCT"],
#	"dependency": ["det", "nsubj", "prep", "det", "pobj", "ROOT", "det", "compound", "dobj", "punct"], 
#	"compression": ["unknownnnnnnnnnnn"], 
#	"label": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#	"text": ["the", "person", "at", "the", "office", "signed", "the", "marriage", "certificate", "."]
#}


#python -m spacy.en.download all
import csv
import spacy
import json

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

def clean_data(data):
	tag_data = []
	story_data = []
	for d in data:
		for dd in d[1:]:
			tag_data.append(dd)
		story_data.append(" ".join(d[1:]))
	return tag_data, story_data

def construct_new_dataset(data):
	nlp = spacy.load('en')
	array = []
	for d in data:
		tokenized_data = nlp(d)
		data_dict = {}
		pos_tagging = []
		dependency = []
		compression = ["unknownnnnnnnnnnn"]
		label = []
		text = []
		for token in tokenized_data:
			label.append(0)
			text.append(token.string.lower())
			dependency.append(token.dep_)
			pos_tagging.append(token.pos_)
		data_dict["pos tagging"] = pos_tagging
		data_dict["dependency"] = dependency
		data_dict["compression"] = compression
		data_dict["label"] = label
		data_dict["text"] = text
		array.append(json.dumps(data_dict))
	return array

nlp = spacy.load('en')
data = merge_data("./data/2016.csv","./data/2017.csv")
tag_data, story_data = clean_data(data)

# skeleton
array = construct_new_dataset(tag_data)

array_train_lens = int(len(story_data) * 0.8 * 5)
array_valid_lens = int(len(story_data) * 0.1 * 5)

train_lens = int(len(story_data) * 0.8)
valid_lens = int(len(story_data) * 0.1)

train_sc_array = array[:array_train_lens]
valid_sc_array = array[array_train_lens:array_train_lens+array_valid_lens]
test_sc_array = array[array_train_lens+array_valid_lens:]

train_story_array = story_data[:train_lens]
valid_story_array = story_data[train_lens:train_lens+valid_lens]
test_story_array = story_data[train_lens+valid_lens:]

with open ("./new_data/train_sc.txt", 'w') as file:
	for a in train_sc_array:
		file.write(str(a) + "\n")
with open ("./new_data/valid_sc.txt", 'w') as file:
	for a in valid_sc_array:
		file.write(str(a) + "\n")
with open ("./new_data/test_sc.txt", 'w') as file:
	for a in test_sc_array:
		file.write(str(a) + "\n")


with open ("./new_data/train_process.txt", 'w') as file:
	for a in train_story_array:
		tokenized_data = nlp(a)
		out_str = ""
		for t in tokenized_data:
			out_str += t.string.lower().strip() + " "
		file.write(out_str + "\n")

with open ("./new_data/valid_process.txt", 'w') as file:
	for a in valid_story_array:
		tokenized_data = nlp(a)
		out_str = ""
		for t in tokenized_data:
			out_str += t.string.lower().strip() + " "
		file.write(out_str + "\n")

with open ("./new_data/test_process.txt", 'w') as file:
	for a in test_story_array:
		tokenized_data = nlp(a)
		out_str = ""
		for t in tokenized_data:
			out_str += t.string.lower().strip() + " "
		file.write(out_str + "\n")


