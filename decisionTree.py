from __future__ import print_function
from math import log
from collections import deque

# These arrays convert the number values in the data set to the Attributes they describe in English
lenseAttributes = [
    ("Age of Patient", ["Young", "Pre-presbyopic", "Presbyopic"]),
    ("Spectacle Prescription", ["Myope", "Hypermetrope"]),
    ("Astigmatic", ["No", "Yes"]),
    ("Tear Production Rate", ["Reduced", "Normal"])
]

classAttribute = ["Hard", "Soft", "Not Fitted"]

# Decision Node class
class DNode:
  def __init__(self,col=-1,value=None,results=None,children=None):
    self.col=col
    self.value=value
    self.results=results
    self.children = children

# parseTextToArray parses the flagdata file and converts integer stings to integers
def parseTextToArray():

    res = []
    for line in open("lenses.data.txt", "r"):
        line = line.split()
        line = [int(attr) if any(char.isdigit() for char in attr) else attr for attr in line]
        res.append(line)
    return res

# divideSetByAllValues creates maps values to the rows that contain that value for a given column
def divideSetByCol(rows, column):
    valueMap = {}

    for row in rows:
        if row[column] in valueMap:
            valueMap[row[column]].append(row)
        else:
            valueMap[row[column]] = [row]

    return valueMap

# calculateEntropy calculates the entropy for the rows grouping by certain column
def calculateEntropy(rows, col):
    entropy = 0.0
    classMap = divideSetByCol(rows, col)

    for label in classMap:
        proportion = float(len(classMap[label]))/len(rows)
        entropy -= proportion*log(proportion, 2)

    return entropy

# divideRowsByClass divides rows by classification
def divideRowsByClass(rows, classIdx):
    return divideSetByCol(rows, classIdx)

# buildTree recursively builds tree nodes by measuring information gain
def buildTree(rows, classIdx):
    if len(rows) == 0:
        return DNode()

    currentScore = calculateEntropy(rows, classIdx)

    bestGain = 0.0
    bestCriteria = None
    bestSets=None

    for col in range(len(rows[0])):
        # skip the class
        if col == classIdx:
            continue

        attrMap = divideSetByCol(rows, col)
        gain = currentScore

        for attr in attrMap:
            proportion = float(len(attrMap[attr])) / len(rows)
            gain -= proportion * calculateEntropy(attrMap[attr], classIdx)

        if gain > bestGain:
            bestGain = gain
            bestCriteria = col
            bestSets = attrMap

    if bestGain > 0:
        children = []
        for value in bestSets:
            childNode = buildTree(bestSets[value], classIdx)
            childNode.value = value
            children.append(childNode)
        return DNode(col=bestCriteria, children=children)
    else:
        return DNode(results=divideRowsByClass(rows, classIdx))

# classify classifies an instance using the given decision tree
def classify(instance,tree):
    if tree.results!=None:
        return tree.results.keys()[0]
    else:
        value = instance[tree.col]
        print("Checking attribute " +str(lenseAttributes[tree.col][0]) + " and val is " + str(lenseAttributes[tree.col][1][value-1]))
        for child in tree.children:
            if child.value == value:
                return classify(instance, child)

    return None

def printTree(tree,indent=''):
    if tree.results!=None:
        for key in tree.results:
            print("Class: " + str(classAttribute[key-1]))
    else:
        print("Check Attribute: " + str(lenseAttributes[tree.col][0]))
        if tree.children:
            for child in tree.children:
                print(indent + " " + "if " + str(lenseAttributes[tree.col][1][child.value-1]), end=" ")
                printTree(child,indent+'  ')

data = parseTextToArray()
# Exclude individual ids
data = [data[i][1:] for i in range(len(data))]
tree = buildTree(data, len(data[0]) - 1)
printTree(tree)
print(classAttribute[classify([2,  1,  1,  2,  2], tree)- 1])
