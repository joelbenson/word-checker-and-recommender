import re
from editDistance import editDistance

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

        #If word not recognized, notify and offer replacement or input
        if (word not in language_words):
            new_word = ""

            #Confirm error
            print("'"+word+"'", "was not recognized in: ", sentence)

            #If error, offer word suggestion
            suggestion = get_closest_word(word, language_words)
            print("Did you mean", suggestion+"? [y/n]")

            response = getValidUserResponse(["y","n"])

            if (response == "y"):
                new_word = suggestion

            #Otherwise, ask for what they meant
            else:
                print("\nWas this an error? [y/n]")

                response = getValidUserResponse(["y","n"])

                if (response == "n"):
                    continue

                response = input("What did you mean?")
                new_word = response

            #Replace word
            sentence = sentence.replace(word, new_word)

    return sentence

def synonym_check(sentence, language_graph):
    return

def getValidUserResponse(valid_responses):
    valid = False
    response = ''

    while (not valid):
        response = input()

        if (response in valid_responses):
            valid = True
        else:
            print('Invalid response')

    return response

def get_closest_word(word, language_words):
    print('Getting suggestion')
    suggestion = ""
    min = 10000000

    for w in language_words:
        distance = editDistance(word, w)
        if (distance < min):
            min = distance
            suggestion = w
    return suggestion
