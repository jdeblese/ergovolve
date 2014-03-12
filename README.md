ergovolve
=========

Genetic-algorithm based optimizer for finding the best set of keycaps for a given set of Ergodox layouts

Makes use of DEAP, and of the conventions established in the Ergodox firmware for key names. Because
this software uses these names as unique names for keycaps, it currently does not support any non-ANSI
keys, apart from the layer switch keys for which an arbitrary convention was selected. This should not
be too difficult to expand upon, however.

The solver is based on the knapsack example of DEAP, with a new fitness and crossover function. It
attempts to optimize two variables:

* Maximises minimum % coverage, by taking as fitness to maximize the min() of the % coverage of the
  proposed set over all given layouts.

* Minimize set length, by taking as fitness to minimize the max() of the number of extraneous keys in the
  proposed set over all given layouts.

This should guarantee that at least the most common keys are covered, and that every set is at least
partially covered, without trying to cover them all at the cost of adding many keys.
