##### NOTE #####
# This code is correct, i.e., it produces correct ans for all testcases of below challenge -
# https://www.hackerrank.com/challenges/determining-dna-health/problem
# But, in few testcases, RUNTIME ERROR occurs due to high memory consumption.
# Also, in few testcases, TIMEOUT occurs.

##### FUTURE TASKS #####
# Optimise code for reducing time & space complexity

##### REFERENCE #####
# https://cp-algorithms.com/string/aho_corasick.html


K = 26  # Alphabet size

class TrieNode():
    def __init__(self, par=None, parChID=None):
        self.nxt = [None] * K   # To store next edges from current node (for a char) in Trie
        self.leafPatIDs = []    # If current node is not leaf ==> 'leafPatIDs' will be empty list; otherwise, it will contain "indices of ALL patterns in pats[]" represented by current node (NOTE - "indices of ALL patterns" because pats[] can contain repeating pattern strings)
        self.par = par          # To store parent node of current node
        self.parChID = parChID  # To store char ID of edge joining parent node & current node
        self.sfxLink = None     # To store suffix link of current node
        self.extLink = None     # To store exit link of current node
        self.goto = [None] * K  # To memoise the goto node after the 1st call to goto(curNode, chID) occurs for current node


class TrieAutomaton():
    def __init__(self, pats):
        self.trie = [TrieNode()]    # 'trie' is a list of 'TrieNode's (if we build 'trie' as a tree instead, with one node pointing to other, the calculation of suffix links & exit links will each take O(K*m) time instead of O(m), where m = no. of nodes (or, states) in Trie Automaton)
        
        for p in range(len(pats)):
            par = 0
            for ch in pats[p]:
                chID = ord(ch) - ord('a')
                if (self.trie[par].nxt[chID] is None):
                    nxt = len(self.trie)    # The ID of the new node which we will create in next step
                    self.trie.append(TrieNode(par, chID))
                    self.trie[par].nxt[chID] = nxt  # The newly created node is assigned as the next edge of 'par' node (for transition with 'chID') in Trie
                par = self.trie[par].nxt[chID]
            self.trie[par].leafPatIDs.append(p)    # Now, 'par' is a leaf node. So, append the pattern IDs to the 'leafPatIDs' list of 'par' node
            
        # Base case for Trie root (required to terminate the goto(0, chID) call; otherwise, the call will go into infinite loop - see comment in goto())
        for k in range(K):
            if (self.trie[0].nxt[k] is None):
                self.trie[0].nxt[k] = 0
            
        self.buildSuffixLinks()
        self.buildExitLinks()
        
        
    def buildSuffixLinks(self):
        for node in range(len(self.trie)):
            self.createSuffixLink(node)

    def createSuffixLink(self, node):
        if (self.trie[node].sfxLink is None):
            # Base case for Trie root and its immediate children
            # NOTE - Base case is required for immediate children of root, otherwise suffix link of immediate children (say, 'immChild') will turn out to be 'immChild' itself, which is wrong.
            if (node == 0) or (self.trie[node].par == 0):
                self.trie[node].sfxLink = 0
            else:
                par = self.trie[node].par
                parChID = self.trie[node].parChID
                sfxLinkPar = self.createSuffixLink(par)
                self.trie[node].sfxLink = self.goto(sfxLinkPar, parChID)

        return self.trie[node].sfxLink

        
    def goto(self, node, chID):
        if (self.trie[node].goto[chID] is None):
            if (self.trie[node].nxt[chID] is None): # This condition becomes FALSE due to base case of 'nxt' param for Trie root, thus preventing the goto(0, chID) call going into infinite loop.
                sfxLink = self.trie[node].sfxLink
                if (sfxLink is None):   # This check is required because: during suffix link creation of node A, goto() is called, which in turn calls goto() with suffix link of another node B. Since, we still might be in the process of creation of suffix links, it's possible that suffix link of node B hasn't been calculated yet (thus a value of 'None'). Passing this un-calculated suffix link (i.e., 'None') to goto() will raise error in the 1st if condition (since, node will be 'None' & self.trie[None] will yield TypeError). So, before passing any suffix link to goto(), we must ensure that suffix link is not 'None'.
                    sfxLink = self.createSuffixLink(node)
                self.trie[node].goto[chID] = self.goto(sfxLink, chID)
            else:
                self.trie[node].goto[chID] = self.trie[node].nxt[chID]
            
        return self.trie[node].goto[chID]


    def buildExitLinks(self):
        for node in range(len(self.trie)):
            self.createExitLink(node)
            
    def createExitLink(self, node):
        if (self.trie[node].extLink is None):
            # Note - 'extLink' of Trie root is None, which is already set to 'None'
            if (node > 0):
                sfxLink = self.trie[node].sfxLink   # Note - even if the current node is a leaf node, the exit link is calculated by traversing the suffix links (rather than assigning the current node itself as the exit link)
                if (self.trie[sfxLink].leafPatIDs):
                    self.trie[node].extLink = sfxLink
                else:
                    self.trie[node].extLink = self.createExitLink(sfxLink)
            
        return self.trie[node].extLink


def recordPatOccur(c, leafPatIDs):
    for leafPatID in leafPatIDs:
        occurID = c - len(pats[leafPatID]) + 1
        patOccurID[leafPatID].append(occurID)


def Aho_Corasick_search_all_pats(pats, txt):
    trieAuto = TrieAutomaton(pats)

    par = 0
    for c in range(len(txt)):
        chID = ord(txt[c]) - ord('a')
        cur = trieAuto.goto(par, chID)

        # If 'cur' node is a leaf node (i.e., string corresponding to 'cur' node matches >= 1 patterns in pats[]), record the occurrence locations of patterns
        recordPatOccur(c, trieAuto.trie[cur].leafPatIDs)

        # Matching patterns can also be found by traversing the exit links of 'cur' node.
        extLink = trieAuto.trie[cur].extLink
        while extLink:
            recordPatOccur(c, trieAuto.trie[extLink].leafPatIDs)
            extLink = trieAuto.trie[extLink].extLink
        
        par = cur


if __name__ == '__main__':
    pats = input().split()		# Space separated patterns to be searched in text
    txt = input()

    patOccurID = {}
    for patID in range(len(pats)):
        patOccurID[patID] = []

    Aho_Corasick_search_all_pats(pats, txt)

    print('Each pattern occurs in the text at following indices -')
    print('Pattern  -->  Occurs at')
    for patID in range(len(pats)):
        print('%s  -->  ' % pats[patID], end='')
        print(patOccurID[patID])
