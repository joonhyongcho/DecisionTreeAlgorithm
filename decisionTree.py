from __future__ import print_function
from math import log
from collections import deque
from PIL import Image,ImageDraw

# religion of country from size and colours in flag
# http://gabrielelanaro.github.io/blog/2016/03/03/decision-trees.html
# http://www.patricklamle.com/Tutorials/Decision%20tree%20python/tuto_decision%20tree.html
#
#

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

def divideRowsByClass(rows, classIdx):
    return divideSetByCol(rows, classIdx)

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

def classify(observation,tree):
    if tree.results!=None:
        return tree.results.keys()[0]
    else:
        value = observation[tree.col]
        print("Checking attribute " +str(lenseAttributes[tree.col][0]) + " and val is " + str(lenseAttributes[tree.col][1][value-1]))
        for child in tree.children:
            if child.value == value:
                return classify(observation, child)

    return None

def getwidth(tree):
    queue = deque()
    queue.append((tree, 0))
    maxLevel = 0
    currLevel = 0
    maxWidth = 0
    currWidth = 0

    while queue:
        currTup = queue.popleft()
        node = currTup[0]
        level = currTup[1]

        if level != currLevel and currWidth > maxWidth:
            maxWidth = currWidth
            maxLevel = currLevel
        elif level != currLevel:
            currLevel = level
            currWidth = 1
        else:
            currWidth += 1

        if node.children:
            for child in node.children:
                queue.append((child, level + 1))

    return maxWidth

def getdepth(tree):
    queue = deque()
    queue.append((tree, 0))

    maxLevel = 0

    while queue:
        currTup = queue.popleft()
        node = currTup[0]
        level = currTup[1]

        if level > maxLevel:
            maxLevel = level

        if node.children:
            for child in node.children:
                queue.append((child, level + 1))

    return maxLevel

def drawtree(tree,jpeg='tree.jpg'):
    w = getwidth(tree) * 100
    h = getdepth(tree) * 100 + 120

    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')

def drawnode(draw,tree,x,y):
    if tree.results==None:
        # Get the width of each branch
        widths = []
        for child in tree.chidren:
            widths.append(getwidth(child) * 100)
        sumWidths = sum(widths)
        # w1=getwidth(tree.fb)*100
        # w2=getwidth(tree.tb)*100

        # Determine the total space required by this node
        spaces = []
        # for width in widths:
            # if len(widths) % 2:


        left=x-(sumWidths)/len(sumWidths)
        right=x+(sumWidths)/len(sumWidths)

        # Draw the condition string
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

        # Draw links to the branches
        for width in tree.children:
            draw.line((x,y, left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))

        # Draw the branch nodes
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
        txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
        draw.text((x-20,y),txt,(0,0,0))

def printTree(tree,indent=''):
    if tree.results!=None:
        for key in tree.results:
            print("Class: " + str(classAttribute[key-1]))
    else:
        print("Check Attribute: " + str(lenseAttributes[tree.col][0]))
        if tree.children:
            for child in tree.children:
                print(indent + " " + "if " + str(lenseAttributes[tree.col][1][child.value-1]), end=" ")
                # print(indent + " " + "if " + str(lenseAttributes[child.col][1][child.value-1]), end= " ")
                printTree(child,indent+'  ')

data = parseTextToArray()
# Exclude individual ids
data = [data[i][1:] for i in range(len(data))]
tree = buildTree(data, len(data[0]) - 1)
printTree(tree)
print(classAttribute[classify([2,  1,  1,  2,  2], tree)- 1])
