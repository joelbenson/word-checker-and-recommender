import re
import networkx as nx
from languageUtils import getSentences, getWords, spell_check, recommend_synonyms, getValidUserResponse
from languageGraphUtils import read_lg
import time

def main():

    #Get file path from user
    file = None
    filepath = input('What is the filepath to your document?')

    #Try opening file
    try:
        file = open(filepath)
        content = file.read()

    except FileNotFoundError:
        print('Unable to find document. Make sure the filepath is correct and try again.')
        return -1

    #Open the language graph
    print("\nOpening dictionary...\nThis process will take about 5 minutes.")
    time.sleep(2)
    print("\n\nIn the meantime, here is how the program works: While scanning through your document, the scanner will look for unrecognized expressions and generic words. You will be offered word fixes and replacements which you can accept or reject. If you accept, the word will automatically be replaced in your file. You can quit and save at any point by responding to a prompt with 'quit'.")
    lg = read_lg("data/english_word_graph.lg")

    dictionary_words = lg.nodes

    edited_content = ""
    user_quit = False

    #Check each sentence in order
    for sentence in getSentences(content):

        if (not user_quit):

            sentence = spell_check(sentence, dictionary_words)

            if (sentence[0:3] == "~~~"):
                user_quit = True
                sentence = sentence[3:]


        if (not user_quit):

            sentence = recommend_synonyms(sentence, lg)

            if (sentence[0:3] == "~~~"):
                user_quit = True
                sentence = sentence[3:]

        edited_content += "".join(sentence)

    file.close()

    print("\nWould you like to save your changes? [y/n]")
    response = getValidUserResponse(["y", "n"])

    if (response == "y"):
        #Write new contents back to file
        file = open(filepath, 'w')
        file.write(edited_content)
        file.close()

        print("Changes saved to file.")

    else:
        print("File closed without saving changes.")


    return 0


if __name__ == '__main__':
    main()
