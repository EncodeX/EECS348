from __future__ import print_function
import math
import random


class Bayes_Classifier:

    train_docs = []
    dictionary = {}
    f_proportion = []
    word_score_dict = [{}, {}]

    stop_words = set(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is', 'isnt', 'it', 'its', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off',
                      'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'were', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves'])

    def __init__(self):
        return

    def read_file(self, filename):
        result = []

        with open(filename, 'rt') as f:
            lines = f.readlines()

        for line in lines:
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            fields = line.split('|')
            doc = []
            doc.append(int(fields[0]))                 # document ID
            doc.append(0 if fields[1] is '1' else 1)   # document sentiment
            fields[2] = fields[2].replace('.', '')
            fields[2] = fields[2].replace(',', '')
            fields[2] = fields[2].replace('!', '')
            fields[2] = fields[2].replace('?', '')
            fields[2] = fields[2].replace(')', '')
            fields[2] = fields[2].replace('(', '')
            fields[2] = fields[2].replace(')', '')
            fields[2] = fields[2].replace('-', '')
            fields[2] = fields[2].replace(':', '')
            fields[2] = fields[2].replace('$', '')
            fields[2] = fields[2].replace('\'', '')
            s_list = fields[2].lower().split(' ')
            sentences = []
            for word in s_list:
                if len(word) == 0:
                    continue
                if word in self.stop_words:
                    continue
                sentences.append(word)
            doc.append(sentences)                      # document sentences
            result.append(doc)

        return result

    def train(self, filename):
        # code to be completed by students to extract features from
        # training file, and to train naive bayes classifier.

        # Read File into [document:[sentence]]
        self.train_docs = self.read_file(filename)

        # Read all words and collect the proportion of words corresponding
        # to the f-score,
        # f: f-score, w: word, s: sentence
        # Calculate P(fi | wj), P(fi), P(wj), P(wj | fi)
        scores_count = [0, 0]
        for doc in self.train_docs:
            # doc[0]: id, doc[1]: f_score
            for word in doc[2]:
                if self.dictionary.has_key(word):
                    self.dictionary[word][0] = self.dictionary[word][0] + 1
                    if doc[1] == 0:
                        self.dictionary[word][1][0] += 1
                    else:
                        self.dictionary[word][1][1] += 1
                else:
                    if doc[1] == 0:
                        self.dictionary[word] = [1, [1, 0]]
                    else:
                        self.dictionary[word] = [1, [0, 1]]
                scores_count[doc[1]] = scores_count[doc[1]] + 1

        words_count = float(scores_count[0] + scores_count[1])

        self.f_proportion.append(
            math.log10(scores_count[0]) if scores_count[0] != 0 else 0 -
            math.log10(words_count))    # P(f0)
        self.f_proportion.append(
            math.log10(scores_count[1]) if scores_count[1] != 0 else 0 -
            math.log10(words_count))    # P(f1)

        for word, wordInfo in self.dictionary.iteritems():
            f0 = wordInfo[1][0]
            f1 = wordInfo[1][1]
            f_total = float(f0 + f1)
            p_f0_word = math.log10(f0) if f0 != 0 else 0 - \
                math.log10(f_total)   # P(f0 | wj)
            p_f1_word = math.log10(f1) if f1 != 0 else 0 - \
                math.log10(f_total)   # P(f1 | wj)
            p_word = math.log10(f_total) - math.log10(words_count)  # P(wj)
            self.word_score_dict[0][word] = p_f0_word + \
                p_word - self.f_proportion[0]
            self.word_score_dict[1][word] = p_f1_word + \
                p_word - self.f_proportion[1]
        return

    def classify(self, filename):
        # code to be completed by student to classifier reviews
        # in file using naive bayes classifier previously trains.
        # member function must return a list of predicted
        # classes with '5' = positive and '1' = negative
        result = []
        test_docs = self.read_file(filename)
        for doc in test_docs:
            doc_f0 = self.f_proportion[0]
            doc_f1 = self.f_proportion[1]
            for word in doc[2]:
                if self.dictionary.has_key(word):
                    doc_f0 += self.word_score_dict[0][word]
                    doc_f1 += self.word_score_dict[1][word]
            result.append('1' if doc_f0 > doc_f1 else '5')
            # print(result, doc_f0, doc_f1)
            # break

        return result
