import re
from edit_distance import editDistance

def getSentences(content):
    #Split content by sentence-ending punctuation: . ! ? ; : followed by space
    sentences = []
    split = re.split(r"([.!?;:\s]\s)", content)

    for i in range(len(split)):
        if (i%2 == 0 and (i+1 < len(split))):
            sentences.append(split[i] + split[i+1])
        if (i%2 ==0 and not(i+1 < len(split))):
            sentences.append(split[i])

    return sentences


def getWords(sentence):
    #Return list of all strings containing a-Z characters including - and '
    return re.findall(r"[a-zA-Z'-]+", sentence)


def spell_check(sentence, dictionary_words):

    for word in getWords(sentence):

        capitalized = word[0].isupper()

        #If word not recognized, notify and offer replacement or input
        if (word.lower() not in dictionary_words):

            new_word = word

            #Confirm error
            print("\n\n'"+word+"'", "was not recognized in: ", sentence)

            #If error, offer word suggestion
            suggestion = get_closest_word(word.lower(), dictionary_words)
            print("\nDid you mean", suggestion+"? [y/n]")

            response = getValidUserResponse(["y","n"])
            if (response == "quit"):
                return "~~~"+sentence

            if (response == "y"):
                new_word = suggestion

            #Otherwise, ask for what they meant
            else:
                print("\nWas this an error? [y/n]")

                response = getValidUserResponse(["y","n"])
                if (response == "quit"):
                    return "~~~"+sentence

                if (response == "n"):
                    continue

                response = input("\nWhat did you mean?")
                new_word = response

            #Replace word
            if (capitalized):
                new_word.capitalize()

            sentence = sentence.replace(word, new_word)

    return sentence


def recommend_synonyms(sentence, lg):

    for word in getWords(sentence):

        capitalized = word[0].isupper()

        #If word generic, offer a synonym
        if (isGeneric(word.lower(), lg)):

            print("\n\n'"+word+"'", "may be ineffective in:\n", sentence, "\nWould you like word recommendations? [y/n]")

            response = getValidUserResponse(["y","n"])
            if (response == "quit"):
                return "~~~"+sentence

            if (response == "n"):
                continue

            new_word = word

            #Get synonym recommendations in order of relevance
            recommendations = getSynonymRecommendations(word.lower(), sentence, lg)

            #Offer suggestion
            print("\n'" + recommendations[0]+"'", "may be the most effective word in this context. Would you like this replacement? [y/n]")

            response = getValidUserResponse(["y","n"])
            if (response == "quit"):
                return "~~~"+sentence

            #If approved, replace word
            if (response == "y"):

                new_word = recommendations[0]

            #Otherwise, offer all synonyms in order of relevance
            else:
                if (len(recommendations) > 1):
                    print("\nOther recommendations include:", recommendations[1:10])
                    print("\nWould you like to use one of these? [y/n]")
                else:
                    print("\nNo other recommendations")
                    continue

                response = getValidUserResponse(["y","n"])
                if (response == "quit"):
                    return "~~~"+sentence

                if (response == "n"):
                    continue

                print("Which one?")
                response = getValidUserResponse(recommendations)
                new_word = response

            #Replace word
            if (capitalized):
                new_word.capitalize()

            sentence = sentence.replace(word, new_word)

    return sentence


def getValidUserResponse(valid_responses):
    valid = False
    response = ''

    while (not valid):
        response = input()

        if (response in valid_responses or response == "quit"):
            valid = True
        else:
            print('Invalid response')

    return response


def get_closest_word(word, language_words):
    print('Getting suggestion...')
    suggestion = ""
    min = 10000000

    for w in language_words:
        distance = editDistance(word, w)
        if (distance < min):
            min = distance
            suggestion = w

    return suggestion


def getSynonymRecommendations(word, sentence, lg):

    synonyms = [w[1] for w in lg.edges(word, keys=True) if w[2] == "synonym"]


    recommendations = []

    for w in synonyms:
        relevance = getRelevance(w, sentence, lg)
        recommendations.append((relevance, w))

    recommendations.sort(reverse=True)

    return [r[1] for r in recommendations]


def isGeneric(word, lg, generic_threshold = 65):#Synonym count distribution: mean = 6.7, stdev = 14.5 (using ~4 std. deviations significance)

    synonyms = [s for s in lg.edges(word, keys=True) if s[2] == "synonym"]

    if (len(synonyms) > generic_threshold):
        return True

    return False


def getRelevance(word, sentence, lg):

    relavance_score = 0

    for w in getWords(sentence):
        w = w.lower()
        w_score = 0

        edge_data = lg.get_edge_data(word, w, key="co-occurance", default=None)

        if (edge_data != None):
            w_score = edge_data["count"]

        relavance_score += w_score ** 2

    return relavance_score
