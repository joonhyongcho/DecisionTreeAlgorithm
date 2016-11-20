# religion of country from size and colours in flag
# http://gabrielelanaro.github.io/blog/2016/03/03/decision-trees.html
# http://www.patricklamle.com/Tutorials/Decision%20tree%20python/tuto_decision%20tree.html
#
class decisionnode:
  def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
    self.col=col
    self.value=value
    self.results=results
    self.tb=tb
    self.fb=fb

def parseTextToArray():

    res = []
    for line in open("flagSmall.txt", "r"):
        line = line.strip()
        line = line.split(",")
        line = [int(attr) if any(char.isdigit() for char in attr) else attr for attr in line]
        res.append(line)
    return res

def divideSet(rows, column, value):
    splitFunction = None

    if isinstance(value, int) or isinstance(value, float):
        splitFunction = lambda row:row[column] >= value
    else:
        splitFunction = lambda row:row[column] == value

    set1 = [row for row in rows if splitFunction(row)]
    set2 = [row for row in rows if not splitFunction(row)]
    return (set1, set2)

def entropy(rows):
    from math import log
    log2 = lambda x:log(x) / log(2)
    results = uniqueCounts(rows)
    entr = 0.0
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent = ent-p*log2(p)
    return ent
def uniqueCounts(rows, idx):
    results = {}
    for row in rows:
        r = row[idx]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

def buildTree(rows, scoref=entropy):
    if len(rows) == 0:
        return decisionnode()
    currentScore = scoref(rows)

    bestGain = 0.0
    bestCriteria = None
    bestSets=None

    columnCount = len(rows[0]) - 1

    for col in range(0, columnCount):
        global columnValues
        columnValues = {}
        for row in rows:
            columnValues[row[col]] = 1
        for value in volumn_values.keys():
            set1, set2 = divideSet(rows, col, value)
            p = float(len(set1))/len(rows)
            gain = currentScore - p *scoref(set1) - (1-p)* scoref(set2)

            if gain > bestGain and len(set1) > 0 and  len(set2) > 0:
                bestGain = gain
                bestCriteria = (col, value)
                bestSets = (set1, set2)
        if bestGain > 0:
            truBranch = buildTree(bestSets[0])
            falseBranch = buildTree(bestSets[1])
            return decisionnode(col=bestCriteria[0], value=bestCriteria[1], tb=TruBranch, fb=FalseBranch)
        else:
            return decisionnode(results=uniqueCounts(rows))
def classify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        branch=None
    if isinstance(v,int) or isinstance(v,float):
        if v>=tree.value: branch=tree.tb
        else: branch=tree.fb
    else:
        if v==tree.value: branch=tree.tb
        else: branch=tree.fb
    return classify(observation,branch)

print(any(char.isdigit() for char in 'Afghanistan'))
print(any(char.isdigit() for char in "American-Samoa"))
data = parseTextToArray()
print(uniqueCounts(data, 6))
set1, set2 = divideSet(data, 6, 4)
print(set1)
print(set2)