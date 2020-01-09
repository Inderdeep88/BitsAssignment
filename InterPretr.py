
class interPretr:
    vertices=[]
    edges=[]

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


# Open file
fileHandler = open("inputPS7.txt", "r")

# Get list of all lines in file
listOfLines = fileHandler.readlines()
candidateList=[]
languageList=[]

graph=interPretr()

for line in listOfLines:
    candidate = None
    language = None
    relation1 = None
    relation2 = None

    i = 0

    list=line.replace("\n","").split("/")

    for item in list:

        if(i == 0):
            if item.strip() not in candidateList:
                candidateList.append(item.strip())
                candidate = vertex(len(graph.vertices),item.strip(),False)
                graph.vertices.append(candidate)
                graph.edges.append([])
                for indx in range(0,len(graph.vertices)-1):
                    graph.edges[len(graph.vertices)-1].append(None)
                for indx in range(0,len(graph.vertices)):
                    graph.edges[indx].append(None)
            else:
                candidate = graph.findCandidate(item.strip())
        else:
            if item.strip() not in languageList:
                languageList.append(item.strip())
                language = vertex(len(graph.vertices),item.strip(),True)
                graph.vertices.append(language)
                graph.edges.append([])
                for indx in range(0,len(graph.vertices)-1):
                    graph.edges[len(graph.vertices)-1].append(None)
                for indx in range(0, len(graph.vertices)):
                    graph.edges[indx].append(None)
            else:
                language = graph.findLanguage(item.strip())
            relation1 = edge(candidate, language, "speaks")
            relation2 = edge(language, candidate, "spokenBy")
            graph.edges[candidate.index][language.index]=relation1
            graph.edges[language.index][candidate.index] = relation2

        i=i+1


# Close file
fileHandler.close()

print("candidate:",candidateList)
print("language:",languageList)

for i in range(0,len(graph.edges)):
    l2 = len(graph.edges[i])
    for j in range(0,l2):
        if (graph.edges[i][j] != None):
            print (graph.edges[i][j].src.data + " " + graph.edges[i][j].rel + " " + graph.edges[i][j].dest.data)
    print

