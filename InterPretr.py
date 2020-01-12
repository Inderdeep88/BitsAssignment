import sys
from collections import deque

class interPretr:
    vertices = []
    edges = []
    transRelation = []
    fullPath = []

    min = sys.maxint
    parent = []

    def findLanguage(self, lang):
        for k in self.vertices:
            if(k.data == lang):
                return k
        return None

    def findCandidate(self, cand):
        for k in self.vertices:
            if(k.data == cand):
                return k
        return None

    def readeInputFile(self, inputFile):

        # Open file
        fileHandler = open(inputFile, "r")

        # Get list of all lines in file
        listOfLines = fileHandler.readlines()

        # Close file
        fileHandler.close()

        for line in listOfLines:
            candidate = None
            language = None
            relation1 = None
            relation2 = None

            i = 0

            list = line.replace("\n", "").split("/")

            for item in list:

                if (i == 0):
                    candidate = self.findCandidate(item.strip())
                    if candidate is None:
                        candidate = vertex(len(self.vertices), item.strip(), False)
                        self.vertices.append(candidate)
                        self.edges.append([])
                        for indx in range(0, len(self.vertices) - 1):
                            self.edges[len(self.vertices) - 1].append(None)
                        for indx in range(0, len(self.vertices)):
                            self.edges[indx].append(None)
                else:
                    language = self.findLanguage(item.strip())
                    if language is None:
                        language = vertex(len(self.vertices), item.strip(), True)
                        self.vertices.append(language)
                        self.edges.append([])
                        for indx in range(0, len(self.vertices) - 1):
                            self.edges[len(self.vertices) - 1].append(None)
                        for indx in range(0, len(self.vertices)):
                            self.edges[indx].append(None)

                    relation1 = edge(candidate, language, "speaks")
                    relation2 = edge(language, candidate, "spokenBy")
                    self.edges[candidate.index][language.index] = relation1
                    self.edges[language.index][candidate.index] = relation2

                i = i + 1
        return None

    def showAll(self):
        candidateList, languageList = self.bsf(self.vertices[0])

        fileHandler = open("outputPS7.txt", "w")

        fileHandler.write("--------Function showAll--------\n")
        fileHandler.write("Total no. of candidates: %d \n" %len(candidateList))
        fileHandler.write("Total no. of languages: %d \n" %len(languageList))

        fileHandler.write("\nList of candidates:\n")
        for candidate in candidateList:
            fileHandler.write("%s\n" %candidate)

        fileHandler.write("\nList of languages:\n")
        for language in languageList:
            fileHandler.write("%s\n" %language)

        fileHandler.write("-----------------------------------------")

        fileHandler.close()
        return None

    def findDirectTranslator(self, langA, langB):
        source = self.findLanguage(langA)
        target = self.findLanguage(langB)

        candidateList = self.bfsDirectTrans(source, target)

        print("findDirectTranslator candidateList : ", candidateList)
        return None

    def findTransRelation(self, langA, langB):
        source = self.findLanguage(langA)
        target = self.findLanguage(langB)

        candidateList = self.bfsDirectTrans(source, target)

        if len(candidateList) != 0:
            for candidate in candidateList:
                list = []
                list.append(source.data)
                list.append(candidate)
                list.append(target.data)
                self.transRelation.append(list)
        else:
            visited = [False] * len(self.vertices)
            path = []
            self.dfsTransRelation(source, target, visited, path, self.min)

        print("findTransRelation path : ",self.transRelation)
        return None

    def findTransRelationTry(self, langA):
        source = self.findLanguage(langA)

        visited = [False] * len(self.vertices)
        path = []
        self.dfsTransRelationTry(source, visited, path)

        self.fullPath.sort(key=len)
        k=0
        for l1 in self.fullPath:
            foundPath = True
            print "checking list ",k
            for item in self.vertices:
                if(item.langFlag is True) and (item.data not in l1):
                    print "exit for ",item.data
                    print "list ", l1
                    foundPath = False
                    break
            if foundPath is True:
                print l1
            k=k+1
        / Users / b0213314 / PycharmProjects / Assigment_7 / inputPS7.txt
#        print("findTransRelation path : ",self.transRelation)
        return None

    def displayHireList(self):
        mincost = 0
        for indx in range(0,len(self.vertices)):
            self.parent.append(indx)
        edge_count = 0
        while (edge_count < len(self.vertices) - 1):
            a = -1
            b = -1
            for i in range(0, len(self.vertices)):
                for j in range(0, len(self.vertices)):
                    if (self.find(i) != self.find(j)):
                        a = i
                        b = j
            self.union1(a, b)
            edge_count = edge_count + 1
            print("Edge ", edge_count, a, b)
            mincost = mincost + 1
            print("Minimum cost=", mincost)
        return None

    def union1(self, i, j):
        a = self.find(i)
        b = self.find(j)
        self.parent[a] = b
        return None

    # Find set of vertex i
    def find(self, i):
        while (self.parent[i] != i):
            i = self.parent[i]
        return i

    def bsf(self, start):
        graphLength = len(self.vertices)
        candidateList = []
        languageList = []
        q = deque()
        visited = [False] * graphLength

        q.append(start)
        visited[start.index] = True

        while(q):
            node = q.popleft()
            if(node.langFlag == False):
                candidateList.append(node.data)
            else:
                languageList.append(node.data)
            for indx in range(0, graphLength):
                if (self.edges[node.index][indx] is not None) and (visited[indx] == False):
                    q.append(self.vertices[indx])
                    visited[indx] = True
        return candidateList, languageList

    def bfsDirectTrans(self, start, target):
        graphLength = len(self.vertices)
        candidateList = []
        q = deque()
        visited = [False] * graphLength

        q.append(start)
        visited[start.index] = True

        while(q):
            node = q.popleft()

            for indx in range(0, graphLength):
                if (self.edges[node.index][indx] is not None) and (visited[indx] == False):
                    if (self.edges[node.index][indx].rel == "spokenBy" ) :
                        q.append(self.vertices[indx])
                        visited[indx] = True
                    else:
                        if (self.vertices[indx].data == target.data):
                            candidateList.append(node.data)
                            break
        return candidateList

    def dfsTransRelation(self, start, target, visited, path, min):
        graphLength = len(self.vertices)
        path.append(start.data)
        visited[start.index] = True

        if start.data == target.data:
            self.transRelation.append(list(path))
            self.min = len(path)
        else:
            for indx in range(0, graphLength):
                if (self.edges[start.index][indx] is not None) and (visited[indx] is False and len(path) < self.min):
                    self.dfsTransRelation(self.vertices[indx], target, visited, path, min)
        path.pop()
        visited[start.index]=False
        return None

    def dfsTransRelationTry(self, start, visited, path):
        graphLength = len(self.vertices)
        path.append(start.data)
        visited[start.index] = True

        self.fullPath.append(list(path))

        for indx in range(0, graphLength):
            if (self.edges[start.index][indx] is not None) and (visited[indx] is False):
                self.dfsTransRelationTry(self.vertices[indx], visited, path)

        path.pop()
        visited[start.index]=False
        return None

    def displayCandidates(self, lang):
        candidateList = self.findCandidateForLanguage(lang)
        print("candidateList : ", candidateList)
        return None

    def findCandidateForLanguage(self,lang):
        candidateList = []
        language = self.findLanguage(lang)
        if language is not None:
            for indx in range(0,len(self.vertices)):
                edge=self.edges[language.index][indx]
                if((edge is not None) and edge.rel == "spokenBy"):
                    candidateList.append(self.vertices[indx].data)
        return candidateList

class vertex:
    def __init__(self, index, data, langFlag):
        self.index = index
        self.data = data
        self.langFlag = langFlag

class edge:
    def __init__(self, src, dest, rel):
        self.src = src
        self.dest = dest
        self.rel = rel


def main():
    graph = interPretr()
    graph.readeInputFile("inputPS7.txt")
    graph.showAll()
    graph.displayCandidates("Gujarati")
    graph.findDirectTranslator("English","Hindi")
    graph.findTransRelation("Bengali","Tamil")
   # graph.displayHireList()
    graph.findTransRelationTry("English")

if __name__ == "__main__":
    main()

#
# for i in range(0,len(graph.edges)):
#     l2 = len(graph.edges[i])
#     for j in range(0,l2):
#         if (graph.edges[i][j] != None):
#             print (graph.edges[i][j].src.data + " " + graph.edges[i][j].rel + " " + graph.edges[i][j].dest.data)
#     print

