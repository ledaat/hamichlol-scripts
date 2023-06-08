class TrieNode:
    def __init__(self):
        """
         Initialize the node's children and is_word attributes
        """
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        """
         Initialize the Trie object
        """
        self.root = TrieNode()

    def insert(self, word):
        """
         Convenience method for inserting a word into the trie.
         
         :param word: The word to insert into the trie. It must be a string
        """
        node = self.root
        # Add a node to the trie node.
        for char in word:
            # Add a new node to the trie.
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word):
        """
         Search the trie for a word.
         
         :param word: The word to search for. This can be any string.
         :returns: True if the word is found, False otherwise.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word


def generate_typos(word_list):
    """
     Generates typos based on a list of correct words.
     Typos are all strings with edit-distance of 1 which are not valid words themselves.
     
     :param word_list: list of words to generate typos from
     :returns: set of typos generated from the word_list
    """
    typos = set()
    candidate_chars = "אבּבגדהוזחטיכךלמםנןסעפףצץקרשׁשׂת"
    trie = Trie()

    # Build trie
    # Insert the word in the trie.
    for word in word_list:
        trie.insert(word)

    def generate_insertions(word):
        """
         Generate typos of insertion for a word.
         This is a generator function that iterates over the word.
         
         :param word: The word to generate insertions for. Should be a string
        """
        # Add all candidate characters to the trie.
        for i in range(len(word) + 1):
            # Add the candidate character to typos.
            for char in candidate_chars:
                typo = word[:i] + char + word[i:]
                # Add a typo to the trie if it doesn t already exist.
                if not trie.search(typo):
                    typos.add(typo)

    def generate_deletions(word):
        """
         Generate typos of deletion for a word.
         
         :param word: The word to be
        """
        # Add all the typos in the word to the typos list.
        for i in range(len(word)):
            typo = word[:i] + word[i + 1 :]
            # Add a typo to the list if it is not a valid word.
            if not trie.search(typo):
                typos.add(typo)

    def generate_substitutions(word):
        """
         Generate typos of substitutions for a word.
         
         :param word: Word to generate substitutions
        """
        # Add all candidate characters to the trie.
        for i in range(len(word)):
            # Add the candidate character to the typos.
            for char in candidate_chars:
                typo = word[:i] + char + word[i + 1 :]
                # Add a typo to the list if it is not a valid word.
                if typo != word and not trie.search(typo):
                    typos.add(typo)

    # Generates the insertions, deletions, and substitutions for each word.
    for word in word_list:
        generate_insertions(word)
        generate_deletions(word)
        generate_substitutions(word)

    return list(typos)


def main():
    """
     Generates typos based on words in words.txt and saves them to typos.txt.
     This is the main function.
    """
    # Open words file
    with open("words.txt", "r", encoding="utf-8") as file:
        word_list = [word.strip() for word in file]

    # Generate typos
    typos = generate_typos(word_list)

    # Save typos to file
    with open("typos.txt", "w", encoding="utf-8") as file:
        # Writes the typos to the file.
        for typo in typos:
            file.write(typo + "\n")

    print("Typos generated and saved to 'typos.txt'.")


# main function for the main module
if __name__ == "__main__":
    main()
