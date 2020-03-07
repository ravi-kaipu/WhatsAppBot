import json
import random
import time
import re

class ChatBot(object):
    def __init__(self):
        self.json_data = None

    def get_data(self):
        with open("training_set.json") as fp:
            self.json_data = dict(json.loads(fp.read()))

    @staticmethod
    def filter_words(words):
        return words

    @staticmethod
    def get_rank1(question, words):
        question = question.lower()
        count = 0
        quest = question
        for word in words:
            if word in quest:
                count += 1
                try:
                    ind = quest.index(word)
                except:
                    continue
                else:
                    quest = quest[ind+len(word):]
        return count

    @staticmethod
    def get_rank(question, words):
        count = 0
        ft = False
        for i in range(len(words)):
            subst = ""
            firsttime = False
            if not ft:
                words = words
                ft = True
            else:
                words = words[:-1]
            for word in words:
                if not firsttime:
                    subst = "({})".format(word)
                    firsttime = True
                else:
                    subst += "\s*({})".format(word)

            expression = r'{}'.format(subst)
            ms = re.match(expression, question)
            if ms:
                count += 1
        return count

    @staticmethod
    def select_question(question, ranks):
        if len(ranks) == 0:
            return None
        if len(ranks) > 1:
            #TODO: max with regular expression check
            return ranks[0][1]
        else:
            return ranks[0][1]

    def choose_answer(self, question, ranks):
        quest = self.select_question(question, ranks)
        if quest:
            #if len(quest) < len(question):
            #    return None
            fields = self.json_data[quest]
            return fields["replies"][0]
        return None

    def estimate_answer(self, question):
        self.get_data()
        question = question.lower()
        question = re.sub(r'[^\w\s]','',question)
        words = question.split()
        all_questions = self.json_data
        ranks = []
        prev_rank = 0
        for quest in all_questions:
            rank = self.get_rank(quest, words)
            if rank != 0 and rank >= prev_rank:
                if rank == prev_rank:
                    ranks.append((rank, quest))
                else:
                    ranks = [(rank, quest)]
                prev_rank = rank

        answer = self.choose_answer(question, ranks)
        if not answer:
            return ""
        return answer.capitalize()

    def run(self):
        self.get_data()
        while True:
            question = input("Ask me:")
            print(question, "--->", self.estimate_answer(question))
