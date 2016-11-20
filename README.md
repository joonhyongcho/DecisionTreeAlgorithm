## Decision Tree Algorithm

This python application builds a decision tree from the flags dataset at the uci.edu datasets archive. http://archive.ics.uci.edu/ml/datasets/Flags. It creates a decision tree from the data and runs a few classification tests. This application is built for Dartmouth's Intro to Computation Neuroscience class, taught by Professor Granger.

## Installation

To run the visualization components of the program, you must install the PIL library, which can be installed by running `pip install image` on the terminal. You must have `pip` installed in order to retrieve PIL. You may find that pip does not install the PIL library properly, in which case you should run `python -m pip install image`, which will install the libraries in the folder of your default python interpreter.

## Algorithm Specifics

Again, this program implements the decision tree learning algorithm, which classifies instances of a dataset by traversing down a decision tree until reaching a leaf node, which provides the classification value. At each node, the classification algorithm tests an attribute of the instance, then traverses down the appropriate branch to the node which contains the value of the tested attribute. This step continues until we have reached a leaf node.

## Implementation

The algorithm is implemented in python, and the program runs in two steps: Build the decision tree, then classify instances of the data set.

### Building the Decision Tree

The algorithms recursively constructs the decision tree from top to bottom, starting from the root, which looks at all of the rows in the dataset. At each iteration of the `buildTree` method, the algorithm calculates the attribute that would "best" split the current rows. In this dataset, each column represents a different attribute. The column number, the attribute represented at that column, and possible values, which are represented by numbers in the dataset, are listed below:
1. age of the patient: (1) young, (2) pre-presbyopic, (3) presbyopic
2. spectacle prescription:  (1) myope, (2) hypermetrope
3. astigmatic:     (1) no, (2) yes
4. tear production rate:  (1) reduced, (2) normal

And so, `buildTree` will determine whether to split the current data by tear production rate or age of the patient. After deciding which attribute to use, the algorithm then splits the data into disjoint sets, where each set shares the same value for that attribute. It then runs `buildTree` on each set and adds the resulting subtrees to the children array of the current decision node.

The "best" split of the data is determined by a statistical property called *information gain*. It measures how well a given attribute separates the training examples according to a target classification. The target classification in our case is whether the patient should be fitted with 1. hard contact lenses 2. soft contact lenses or 3. no lenses at all. Information gain relies on entropy, which measures the "impurity" of a collection of examples. More information on entropy can be found here[!https://en.wikipedia.org/wiki/Entropy_(information_theory)].

Entropy is calculated by the equation:
![description](entropy.png)


To test the which attribute to test at each node in the tree, we need to select the attribute that is most useful for classifying the examples. We use a property, called information gain, that measures how well a given attribute separates the training examples according to their target classification. To this end, we use entropy, which measures the impurity of a collection of examples. Given a collection S, containing positive and negative examples of a target concept, the entropy of S relative to boolean classification is

Information gain is the expected reduction in entropy caused by partitioning the samples according to the attribute. Gain(S,A) is Entropy(S) - sum of values Sv over S * entropy(Sv)

Values(A) is set of all possible values for attribute A, and Sv is the subset of S for which attribute A has value v.

In the future, this could be made more generic, but the program is specific to the flag dataset because a lot of the printing methods utilize a predetermine dictionary that maps column indices to certain real life values based on the value. For example, the dictionary includes the entry:  5: [English, Spanish, French, German, Slavic, Other Indo-European, Chinese, Arabic, Japanese/Turkish/Finnish/Magyar, Others]. This could be made more generic as to parse all dataset.names.txt files.

https://www.cs.princeton.edu/courses/archive/spring07/cos424/papers/mitchell-dectrees.pdf

## Data set

Provide code examples and explanations of how to get the project.

## Results

## Conclusions

Describe and show how to run the tests with code examples.

## References