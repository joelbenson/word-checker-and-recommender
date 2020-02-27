import re
import networkx as nx
from utils import getSentences, getWords, spell_check, synonym_check

def main():

    #Get file path from user
    file = None
    filepath = input('What is the filepath to your document?')

    #Try opening file
    try:
        content = open(filepath).read()
    except FileNotFoundError:
        print('Unable to find document. Make sure the filepath is correct and try again.')
        return -1

    #Open the language graph
    print('Opening document and dictionary...')
    language_graph = nx.read_gml('data/language_graph.gml')
    dictionary_words = language_graph.nodes

    edited_content = ""

    #Check each sentence in order
    for sentence in getSentences(content):
        sentence = spell_check(sentence, language_words)
        # sentence = synonym_check(sentence, language_graph)
        edited_content += "".join(sentence)

    #Write new contents back to file
    open(filepath, 'w').write(new_content)

    return 0




if __name__ == '__main__':
    main()
