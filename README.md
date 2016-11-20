## Decision Tree Algorithm

This python application builds a decision tree from the flags dataset at the uci.edu datasets archive. http://archive.ics.uci.edu/ml/datasets/Flags. It creates a decision tree from the data and runs a few classification tests. This application is built for Dartmouth's Intro to Computation Neuroscience class, taught by Professor Granger.

## Algorithm Specifics

Again, this program implements the decision tree learning algorithm, which classifies instances of a dataset by traversing down a decision tree until reaching a leaf node, which provides the classification value. At each node, the classification algorithm tests an attribute of the instance, then traverses down the appropriate branch to the node which contains the value of the tested attribute. This step continues until we have reached a leaf node.

## Implementation

The algorithm is implemented in python, with a series of functions that 1. parse the input data 2. create subtrees 3. calculate entropy and 4. builds the entire tree and 5. classifies instances.

In general, the algorithm learns decision trees by constructing them top down. It decides which attribute to use at any certain level, where the the root is at level 0, it’s direct children at level1, and the children of those children at level 2 and so on and so forth. Each instance attribute is evaluated using a statistical test to determine how it classifies the training examples on its own. Then, a descendant of the root is selected and created for every possible value of the attribute. Then, the same test is used at each of the children node, where the training examples have been filtered, to select the next children.

To test the which attribute to test at each node in the tree, we need to select the attribute that is most useful for classifying the examples. We use a property, called information gain, that measures how well a given attribute separates the training examples according to their target classification. To this end, we use entropy, which measures the impurity of a collection of examples. Given a collection S, containing positive and negative examples of a target concept, the entropy of S relative to boolean classification is

Information gain is the expected reduction in entropy caused by partitioning the samples according to the attribute. Gain(S,A) is Entropy(S) - sum of values Sv over S * entropy(Sv)

Values(A) is set of all possible values for attribute A, and Sv is the subset of S for which attribute A has value v.

https://www.cs.princeton.edu/courses/archive/spring07/cos424/papers/mitchell-dectrees.pdf

## Data set

Provide code examples and explanations of how to get the project.

## Results

## Conclusions

Describe and show how to run the tests with code examples.

## References