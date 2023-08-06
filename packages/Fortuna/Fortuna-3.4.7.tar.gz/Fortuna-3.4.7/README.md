# Fortuna: Random Value Generator
Fortuna's main goal is to provide a quick and easy way to build custom random-value generators.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Suggested Installation: `$ pip install Fortuna`

Installation on platforms other than MacOS may require building from source files.


### Documentation Table of Contents:
- Numeric Limits
- Project Definitions
- Random Value Generators
- Random Integer Generators
- Random Index Generators
- Random Float Generators
- Random Bool Generator
- Shuffle Algorithms
- Test Suite
- Test Suite Output
- Development Log
- Legal Information


##### Numeric Limits:
- Integer: 64 bit signed integer.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Minimum: -9223372036854775807
    - Maximum:  9223372036854775807
- Float: 64 bit double precision floating point.
    - Minimum: -1.7976931348623157e+308
    - Maximum:  1.7976931348623157e+308
    - Epsilon Below Zero: -5e-324
    - Epsilon Above Zero:  5e-324


##### Project Definitions:
- Value: Any python object: str, int, list and lambda to name a few.
- Callable: Any callable object, function, method or lambda.
- Sequence: Any object that can be converted into a list via `list(some_object)`.
    - List, Tuple, Set, etc...
    - Comprehensions and Generators that produce Sequences also qualify.
    - Classes that wrap a simple collection will take any Sequence or Array.
    - Functions that operate on a simple collection will require an Array.
- Array: List, tuple or any object that inherits from either.
    - Must be an object that is indexed like a list.
    - List comprehensions qualify as Arrays, but sets and list generators do not.
    - All Arrays are Sequences but not all Sequences are Arrays.
- Pair: Array of two Values.
- Table: Array of Pairs.
    - List of lists of two values each.
    - Tuple of tuples of two values each.
    - Generators that produce Tables also qualify.
    - The result of zip(list_1, list_2) also qualifies.
- Matrix: Dictionary of Arrays.
    - Generators or comprehensions that produces a Matrix also qualify.
- Inclusive Range.
    - `[1, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Exclusive Range.
    - `(0, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Partial Ranges.
    - `[1, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
    - `(0, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Automatic Flattening.
    - All random value generators in Fortuna will recursively call or "flatten" callable objects returned from the dataset at call time.
    - Un-callable objects or those that require arguments will be returned in an uncalled state without error.
    - A callable that can be flattened is any class initializer, function, method or lambda so long as it requires no arguments, it will be automatically flattened.
    - Mixing callable objects with un-callable objects is fully supported, but it can be a bit messy.
    - Nested callable objects are fully supported. Because `lambda(lambda) -> lambda` fixes everything for arbitrary values of 'because', 'fixes' and 'everything'.
    - To disable automatic flattening, pass the optional keyword argument `flat=False`.


## Random Value Generators: Functional
`Fortuna.random_value(data: Array, flat=True) -> Value`
- @param data :: Array of Values.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Produces a random value from the list with a wide uniform distribution.

```python
from Fortuna import random_value


data = ("Apple", "Banana", "Cherry", "Grape", "Lime", "Orange")
print(random_value(data))  # prints a random value from the data, flat uniform distribution.
```

`Fortuna.cumulative_weighted_choice(weighted_table: Table, flat=True) -> Value`
- @param weighted_table :: Table of weighted Pairs. `[(1, "a"), (2, "b"), (3, "c")]`
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Produces a random value from the list with a custom distribution.

```python
from Fortuna import cumulative_weighted_choice


weighted_data = (
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
)
print(cumulative_weighted_choice(weighted_data))
# prints a random value from the data, with probability based on cumulative weight.
```

`Fortuna.lazy_cat(data, range_to=0, func=random_index, flat=True) -> Value`
- The lazy_cat function is a more general form of the QuantumMonty class.
- Features dependency injection instead of built-in methods.
- @param data :: Array of Values.
- @param range_to :: Default is zero. Must be equal to or less than the length of data, this represents the size of the output distribution. When range_to == 0, the total length of data is used instead. This argument is passed to the input function to get a valid index into the data. When range_to is negative the back of the data will be considered the starting point.
- @param func :: Optional. Default is random_index. This callable must follow the ZeroCool method specifications. All built-in ZeroCool methods qualify.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Returns a random value from the data using the function you specify at call time.

`Fortuna.truffle_shuffle(data: list, flat=True) -> Value`
- In-place micro-shuffled value generator. Modifies the list. It is recommended to shuffle the list conventionally once before a series of truffle_shuffles.
- @param data :: list of Values. Must be a mutable list. For best results, each Value should be unique and the number of Values should be more than just a few.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Random value from the list with a wide uniform distribution. The average width of the output sequence will naturally scale up with the size of the list.

**Wide Uniform Distribution**: *"Wide"* refers to the average distance between consecutive occurrences of the same value in the output sequence. The goal of this type of distribution is to keep the output sequence free of clumps or streaks, while maintaining randomness and uniform probability. This is not the same as a *flat uniform distribution*. The two distributions should be statistically similar for any given set, but the output sequence repetitiveness will be very different.


## Random Value Generators: Classes
### TruffleShuffle
`Fortuna.TruffleShuffle(data: Sequence, flat=True) -> Callable -> Value`
- In-place micro-shuffle. Non-destructive, copies the list_of_values.
- @param data :: Sequence of Values. Automatically shuffles once with Knuth B at instantiation.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Callable Instance.
    - @return :: Random value from the list with a wide uniform distribution, performs an internal micro-shuffle. Pop a Value for return then use front_poisson insert to randomly put it back near the front of the list. The relative width of the output sequence will naturally scale up with the size of the list.


#### TruffleShuffle, Basic Use
```python
from Fortuna import TruffleShuffle


list_of_values = [1, 2, 3, 4, 5, 6]
truffle_shuffle = TruffleShuffle(list_of_values)

print(truffle_shuffle())
```

#### Automatic Flattening
```python
from Fortuna import TruffleShuffle


auto_flat = TruffleShuffle([lambda: 1, lambda: 2, lambda: 3])
print(auto_flat())  # will print the value 1, 2 or 3.
# Note: the lambda will not be called until call time and stays dynamic for the life of the object.

un_flat = TruffleShuffle([lambda: 1, lambda: 2, lambda: 3], flat=False)
print(un_flat()())  # will print the value 1, 2 or 3, mind the double-double parenthesis

auto_un_flat = TruffleShuffle([lambda x: x, lambda x: x + 1, lambda x:  x + 2], flat=False)
# Note: flat=False is not required here because the lambdas can not be called without input x satisfied.
# It is still recommended to specify flat=False if non-flat output is intend.
print(auto_un_flat()(1))  # will print the value 1, 2 or 3, mind the double-double parenthesis

```


#### Mixing Static Objects with Callable Objects
```python
from Fortuna import TruffleShuffle


""" With automatic flattening active, lambda() -> int can be treated as an int. """
mixed_flat = TruffleShuffle([1, 2, lambda: 3])  # this is fine and works as intended.
print(mixed_flat())  # will print 1, 2 or 3

mixed_un_flat = TruffleShuffle([1, 2, lambda: 3], flat=False) # this pattern is not recommended.
print(mixed_flat())  # will print 1, 2 or "Function <lambda at some_address>"
# This pattern is not recommended because you wont know the nature of what you get back.
# This is almost always not what you want, and it can give rise to messy logic in other areas of your code.
```


#### Dynamic Strings
To successfully express a dynamic string, and keep it dynamic, at least one level of indirection is required. Without an indirection the f-string would collapse into a static string too soon.

```python
from Fortuna import TruffleShuffle, d


# d() is a simple dice function, d(n) -> [1, n] flat uniform distribution.
dynamic_strings = TruffleShuffle((
    # while the probability of all A == all B == all C, individual probabilities of each possible string will differ based on the number of possible outputs of each category.
    lambda: f"A{d(2)}",  # -> A1 - A2, each are twice as likely as any particular B, and three times as likely as any C.
    lambda: f"B{d(4)}",  # -> B1 - B4, each are half as likely as any particular A, and 3/2 as likely as any C.
    lambda: f"C{d(6)}",  # -> C1 - C6, each are 1/3 as likely as any particular A and 2/3 as likely of any B.
))

print(dynamic_strings())  # prints a random dynamic string, flattened at call time.

"""
Sample Distribution of 10,000 dynamic_strings():
    A1: 16.92%
    A2: 16.66%
    B1: 8.08%
    B2: 8.51%
    B3: 8.15%
    B4: 8.1%
    C1: 5.62%
    C2: 5.84%
    C3: 5.71%
    C4: 5.43%
    C5: 5.22%
    C6: 5.76%
"""
```


### QuantumMonty
`Fortuna.QuantumMonty(data: Sequence, flat=True) -> Callable -> Value`
- @param data :: Sequence of Values.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Callable Object with Monty Methods for producing various distributions of the data.
    - @return :: Random value from the data. The instance will produce random values from the list using the selected distribution model or "monty". The default monty is the Quantum Monty Algorithm.

```python
from Fortuna import QuantumMonty


list_of_values = [1, 2, 3, 4, 5, 6]
monty = QuantumMonty(list_of_values)

print(monty())               # prints a random value from the list_of_values.
                             # uses the default Quantum Monty Algorithm.

print(monty.flat_uniform())  # prints a random value from the list_of_values.
                             # uses the "uniform" monty: a flat uniform distribution.
                             # equivalent to random.choice(list_of_values).
```
The QuantumMonty class represents a diverse collection of strategies for producing random values from a sequence where the output distribution is based on the method you choose. Generally speaking, each value in the sequence will have a probability that is based on its position in the sequence. For example: the "front" monty produces random values where the beginning of the sequence is geometrically more common than the back. Given enough samples the "front" monty will always converge to a 45 degree slope down for any list of unique values.

There are three primary method families: linear, gaussian, and poisson. Each family has three base methods; 'front', 'middle', 'back', plus a 'quantum' method that incorporates all three base methods. The quantum algorithms for each family produce distributions by overlapping the probability waves of the other methods in their family. The Quantum Monty Algorithm incorporates all nine base methods.

```python
import Fortuna


monty = Fortuna.QuantumMonty(
    ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
)

# Each of the following methods will return a random value from the sequence.
# Each method has its own unique distribution model for the same data set.

""" Flat Base Case """
monty.flat_uniform()             # Flat Uniform Distribution

""" Geometric Positional """
monty.front_linear()        # Linear Descending, Triangle
monty.middle_linear()       # Linear Median Peak, Equilateral Triangle
monty.back_linear()         # Linear Ascending, Triangle
monty.quantum_linear()      # Linear Overlay, 3-way monty.

""" Gaussian Positional """
monty.front_gauss()         # Front Gamma
monty.middle_gauss()        # Scaled Gaussian
monty.back_gauss()          # Reversed Gamma
monty.quantum_gauss()       # Gaussian Overlay, 3-way monty.

""" Poisson Positional """
monty.front_poisson()       # 1/4 Mean Poisson
monty.middle_poisson()      # 1/2 Mean Poisson
monty.back_poisson()        # 3/4 Mean Poisson
monty.quantum_poisson()     # Poisson Overlay, 3-way monty.

""" Quantum Monty Algorithm """
monty()                     # Quantum Monty Algorithm, 9-way monty.
monty.quantum_monty()
```

### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values.

The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

#### Cumulative Weight Strategy
`Fortuna.CumulativeWeightedChoice(weighted_table: Table, flat=True) -> Callable -> Value`
- @param weighted_table :: Table of weighted pairs.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Callable Instance
    - @return :: Random value from the weighted_table, distribution based on the weights of the values.

_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cum_weighted_choice = CumulativeWeightedChoice([
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),  # same as relative weight 4 because 30 - 26 = 4
])

print(cum_weighted_choice())  # prints a weighted random value
```

#### Relative Weight Strategy
`Fortuna.RelativeWeightedChoice(weighted_table: Table) -> Callable -> Value`
- @param weighted_table :: Table of weighted pairs.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Callable Instance
    - @return :: Random value from the weighted_table, distribution based on the weights of the values.

```python
from Fortuna import RelativeWeightedChoice


population = ["Apple", "Banana", "Cherry", "Grape", "Lime", "Orange"]
rel_weights = [7, 4, 2, 10, 3, 4]
rel_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))

print(rel_weighted_choice())  # prints a weighted random value
```

### FlexCat
`Fortuna.FlexCat(dict_of_lists: Matrix, key_bias="front_linear", val_bias="truffle_shuffle", flat=True) -> Callable -> Value`
- @param dict_of_lists :: Keyed Matrix of Value Sequences.
- @parm key_bias :: String indicating the name of the algorithm to use for random key selection.
- @parm val_bias :: String indicating the name of the algorithm to use for random value selection.
- @param flat :: Bool. Default: True. Option to flatten callable values. Automatic Flattening.
- @return :: Callable Instance
    - @param cat_key :: Optional. Default is None. Key selection by name. If specified, this will override the key_bias for a single call.
    - @return :: Value. Returns a random value generated with val_bias from a random sequence generated with key_bias.

FlexCat is like a two dimensional QuantumMonty, or a QuantumMonty of QuantumMonty\.

The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections. The algorithm specified for selecting a key need not be the same as the one for selecting values. An optional key may be provided at call time to bypass the random key selection. Keys passed in this way must exactly match a key in the Matrix.

By default, FlexCat will use key_bias="front" and val_bias="truffle_shuffle", this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle the sequence values. This config is known as TopCat, it produces a descending-step, micro-shuffled distribution sequence. Many other combinations are available.

Algorithmic Options: _See QuantumMonty & TruffleShuffle for more details._
- "front_linear", Linear Descending
- "middle_linear", Linear Median Peak
- "back_linear", Linear Ascending
- "quantum_linear", Linear 3-way monty
- "front_gauss", Gamma Descending
- "middle_gauss", Scaled Gaussian
- "back_gauss", Gamma Ascending
- "quantum_gauss", Gaussian 3-way monty
- "front_poisson", Front 1/3 Mean Poisson
- "middle_poisson", Middle Mean Poisson
- "back_poisson", Back 1/3 Mean Poisson
- "quantum_poisson", Poisson 3-way monty
- "quantum_monty", Quantum Monty Algorithm, 9-way monty
- "flat_uniform", uniform flat distribution
- "truffle_shuffle", TruffleShuffle, wide uniform distribution

```python
from Fortuna import FlexCat


matrix_data = {
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}
flex_cat = FlexCat(matrix_data, key_bias="front_linear", val_bias="flat_uniform")

flex_cat()  # returns a "flat_uniform" random value from a random "front_linear" weighted category.
flex_cat("Cat_B")  # returns a "flat_uniform" random value specifically from the "Cat_B" sequence.
```

### Random Integer Generators
`Fortuna.random_below(number: int) -> int`
- @param number :: Any Integer
- @return :: Returns a random integer in the range...
    - `random_below(number) -> [0, number)` for positive values.
    - `random_below(number) -> (number, 0]` for negative values.
    - `random_below(0) -> 0` Always returns zero when input is zero
- Flat uniform distribution.


`Fortuna.random_int(left_limit: int, right_limit: int) -> int`
- @param left_limit :: Any Integer
- @param right_limit :: Any Integer
- @return :: Returns a random integer in the range [left_limit, right_limit]
    - `random_int(1, 10) -> [1, 10]`
    - `random_int(10, 1) -> [1, 10]` same as above.
    - `random_int(A, B)` Always returns A when A == B
- Flat uniform distribution.


`Fortuna.random_range(start: int, stop: int = 0, step: int = 1) -> int`
- @param start :: Required starting point.
    - `random_range(0) -> [0]`
    - `random_range(10) -> [0, 10)` from 0 to 9. Same as `Fortuna.random_index(N)`
    - `random_range(-10) -> [-10, 0)` from -10 to -1. Same as `Fortuna.random_index(-N)`
- @param stop :: Zero by default. Optional range bound. With at least two arguments, the order of the first two does not matter.
    - `random_range(0, 0) -> [0]`
    - `random_range(0, 10) -> [0, 10)` from 0 to 9.
    - `random_range(10, 0) -> [0, 10)` same as above.
- @param step :: One by default. Optional step size.
    - `random_range(0, 0, 0) -> [0]`
    - `random_range(0, 10, 2) -> [0, 10) by 2` even numbers from 0 to 8.
    - The sign of the step parameter controls the phase of the output. Negative stepping will flip the inclusively.
    - `random_range(0, 10, -1) -> (0, 10]` starts at 10 and ranges down to 1.
    - `random_range(10, 0, -1) -> (0, 10]` same as above.
    - `random_range(10, 10, 0) -> [10]` a step size or range size of zero always returns the first parameter.
- @return :: Returns a random integer in the range [A, B) by increments of C.
- Flat uniform distribution.


`Fortuna.d(sides: int) -> int`
- Represents a single roll of a given size die.
- @param sides :: Any Integer. Represents the size or number of sides, most commonly six.
- @return :: Returns a random integer in the range [1, sides].
- Flat uniform distribution.


`Fortuna.dice(rolls: int, sides: int) -> int`
- Represents the sum of multiple rolls of the same size die.
- @param rolls :: Any Integer. Represents the number of times to roll the die.
- @param sides :: Any Integer. Represents the die size or number of sides, most commonly six.
- @return :: Returns a random integer in range [X, Y] where X = rolls and Y = rolls * sides.
- Geometric distribution based on the number and size of the dice rolled.
- Complexity scales primarily with the number of rolls, not the size of the dice.


`Fortuna.plus_or_minus(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Flat uniform distribution.


`Fortuna.plus_or_minus_linear(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Linear geometric, 45 degree triangle distribution centered on zero.


`Fortuna.plus_or_minus_gauss(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Stretched gaussian distribution centered on zero.


### Random Index, ZeroCool Specification
ZeroCool Methods are used by lazy_cat via dependency injection to generate random indices with any distribution.

ZeroCool methods must have the following properties:
- Any distribution model is acceptable.
- The method or function takes exactly one parameter.
- The method returns a random int in range `[0, N)` for positive values of N
- The method returns a random int in range `[N, 0)` for negative values of N.
    - This symmetry matches how python will naturally index a list from the back for negative index values or from the front for positive index values.

ZeroCool functions often have an interesting limit as size goes to zero. ZeroCool does not place requirements the output of this input limit. At higher levels of abstraction, inside classes that employ ZeroCool methods- zero is always a sentinel to indicate the full range. In that case the length of the list is sent to the ZeroCool method, not zero. However for those who enjoy thinking a little deeper, consider the following:

If given the fact that an empty range is never an option, we could design a better solution than failure for input zero. Calculus might suggest that both infinity and negative infinity are equally viable output for an input limit of zero, but both are inappropriate for indexing a list. However, if we map infinity to the back of the list and minus infinity to the front of the list, then the following might hold: `random_index(0) -> [-1, 0]`. This "Top or Bottom" solution is not required for a method to be ZeroCool compatible, it is just an interesting option. Other valid possibilities include: always return None or 0 or -1 or throw an exception or spawn nasal demons, however none of these seem terribly helpful or useful. At least the Top/Bottom solution accurately reflects the "off by one" symmetry of the domain mapping that defines ZeroCool methods in general.


```python
from Fortuna import random_index


some_list = [i for i in range(100)]

print(some_list[random_index(10)])  # prints one of the first 10 items of some_list, [0, 9]
print(some_list[random_index(-10)])  # prints one of the last 10 items of some_list, [90, 99]
```
### ZeroCool Methods
`Fortuna.random_index(size: int) -> int` Flat uniform distribution

`Fortuna.front_gauss(size: int) -> int` Gamma Distribution: Front Peak

`Fortuna.middle_gauss(size: int) -> int` Stretched Gaussian Distribution: Median Peak

`Fortuna.back_gauss(size: int) -> int` Gamma Distribution: Back Peak

`Fortuna.quantum_gauss(size: int) -> int` Quantum Gaussian: Three-way Monty

`Fortuna.front_poisson(size: int) -> int` Poisson Distribution: Front 1/3 Peak

`Fortuna.middle_poisson(size: int) -> int` Poisson Distribution: Middle Peak

`Fortuna.back_poisson(size: int) -> int` Poisson Distribution: Back 1/3 Peak

`Fortuna.quantum_poisson(size: int) -> int` Quantum Poisson: Three-way Monty

`Fortuna.front_geometric(size: int) -> int` Linear Geometric: 45 Degree Front Peak

`Fortuna.middle_geometric(size: int) -> int` Linear Geometric: 45 Degree Middle Peak

`Fortuna.back_geometric(size: int) -> int` Linear Geometric: 45 Degree Back Peak

`Fortuna.quantum_geometric(size: int) -> int` Quantum Geometric: Three-way Monty

`Fortuna.quantum_monty(size: int) -> int` Quantum Monty: Twelve-way Monty

```python
from Fortuna import front_gauss, middle_gauss, back_gauss, quantum_gauss


some_list = [i for i in range(100)]

# Each of the following prints one of the first 10 items of some_list with the appropriate distribution
print(some_list[front_gauss(10)])
print(some_list[middle_gauss(10)])
print(some_list[back_gauss(10)])
print(some_list[quantum_gauss(10)])

# Each of the following prints one of the last 10 items of some_list with the appropriate distribution
print(some_list[front_gauss(-10)])  
print(some_list[middle_gauss(-10)])  
print(some_list[back_gauss(-10)])  
print(some_list[quantum_gauss(-10)])  

```

### Random Float Generator
`Fortuna.canonical() -> float`
- @return :: random float in range [0.0, 1.0), flat uniform.


`Fortuna.random_float(a: Float, b: Float) -> Float`
- @param a :: Float
- @param b :: Float
- @return :: random Float in range [a, b), flat uniform distribution.


### Random Truth Generator
`Fortuna.percent_true(truth_factor: Float = 50.0) -> bool`
- @param truth_factor :: The probability of True as a percentage. Default is 50 percent.
- @return :: Produces True or False based on the truth_factor.
    - Always returns False if num is 0 or less
    - Always returns True if num is 100 or more.


### Shuffle Algorithms
`Fortuna.shuffle(array: list) -> None`
- Knuth B shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.

`Fortuna.knuth(array: list) -> None`
- Knuth A shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.

`Fortuna.fisher_yates(array: list) -> None`
- Fisher-Yates shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.


### Test Suite
`Fortuna.distribution_timer(func: staticmethod, *args, num_cycles=100000, **kwargs) -> None`

`Fortuna.quick_test(cycles=10000) -> None`


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine

Random Values:

Base Case
Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 968 nano seconds
Raw Samples: 1, 1, 8, 5, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4891
 Std Deviation: 2.8891721862139264
Distribution of 100000 Samples:
 0: 10.227%
 1: 9.973%
 2: 10.042%
 3: 9.97%
 4: 9.868%
 5: 9.756%
 6: 10.093%
 7: 10.037%
 8: 10.061%
 9: 9.973%

Output Distribution: random_value([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 156 nano seconds
Raw Samples: 9, 5, 5, 0, 8
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5156
 Std Deviation: 2.8774962447349686
Distribution of 100000 Samples:
 0: 10.154%
 1: 9.952%
 2: 9.946%
 3: 9.939%
 4: 10.03%
 5: 9.935%
 6: 10.036%
 7: 10.082%
 8: 9.926%
 9: 10.0%

Output Analysis: TruffleShuffle(some_list)
Typical Timing: 343 nano seconds
Raw Samples: 4, 3, 2, 1, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5134
 Std Deviation: 2.8675499514868834
Distribution of 100000 Samples:
 0: 9.871%
 1: 9.932%
 2: 10.034%
 3: 10.021%
 4: 10.135%
 5: 9.983%
 6: 10.005%
 7: 9.924%
 8: 10.099%
 9: 9.996%

Output Distribution: truffle_shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 218 nano seconds
Raw Samples: 6, 0, 4, 1, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5223
 Std Deviation: 2.8794672846178195
Distribution of 100000 Samples:
 0: 9.972%
 1: 10.019%
 2: 9.981%
 3: 9.994%
 4: 10.019%
 5: 9.988%
 6: 10.062%
 7: 10.067%
 8: 9.958%
 9: 9.94%

Output Analysis: QuantumMonty(some_list)
Typical Timing: 343 nano seconds
Raw Samples: 0, 4, 5, 4, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5211
 Std Deviation: 2.8703621178988525
Distribution of 100000 Samples:
 0: 10.888%
 1: 8.9%
 2: 8.926%
 3: 9.634%
 4: 11.515%
 5: 11.606%
 6: 9.707%
 7: 8.95%
 8: 8.949%
 9: 10.925%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], zero_cool=<built-in function quantum_monty>)
Typical Timing: 281 nano seconds
Raw Samples: 1, 5, 9, 7, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4934
 Std Deviation: 2.872904766639475
Distribution of 100000 Samples:
 0: 10.948%
 1: 8.853%
 2: 9.014%
 3: 9.752%
 4: 11.595%
 5: 11.47%
 6: 9.654%
 7: 8.9%
 8: 8.964%
 9: 10.85%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], cum_weights=[1, 10, 100, 1000])
Typical Timing: 1687 nano seconds
Raw Samples: [18], [24], [18], [18], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6984
 Std Deviation: 2.1671887575176907
Distribution of 100000 Samples:
 18: 89.796%
 24: 9.156%
 30: 0.961%
 36: 0.087%

Output Analysis: CumulativeWeightedChoice(zip(cum_weights, population))
Typical Timing: 250 nano seconds
Raw Samples: 18, 18, 18, 18, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6498
 Std Deviation: 2.048653132661993
Distribution of 100000 Samples:
 18: 89.885%
 24: 9.127%
 30: 0.892%
 36: 0.096%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], weights=[1, 9, 90, 900])
Typical Timing: 2125 nano seconds
Raw Samples: [18], [18], [18], [18], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.627
 Std Deviation: 2.0275310326130205
Distribution of 100000 Samples:
 18: 90.158%
 24: 8.859%
 30: 0.875%
 36: 0.108%

Output Analysis: RelativeWeightedChoice(zip(rel_weights, population))
Typical Timing: 250 nano seconds
Raw Samples: 18, 18, 18, 18, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6696
 Std Deviation: 2.1141624365882645
Distribution of 100000 Samples:
 18: 89.979%
 24: 9.018%
 30: 0.899%
 36: 0.104%

Output Analysis: FlexCat(some_matrix, key_bias="flat_uniform", val_bias="flat_uniform")
Typical Timing: 437 nano seconds
Raw Samples: 100, 3, 1, 2, 200
Statistics of 10000 Samples:
 Minimum: 1
 Median: 20
 Maximum: 400
 Mean: 91.6
 Std Deviation: 128.46102297367221
Distribution of 100000 Samples:
 1: 8.395%
 2: 8.283%
 3: 8.349%
 4: 8.276%
 10: 8.353%
 20: 8.326%
 30: 8.343%
 40: 8.402%
 100: 8.31%
 200: 8.29%
 300: 8.37%
 400: 8.303%

Output Distribution: flex_cat({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40], 'C': [100, 200, 300, 400]})
Typical Timing: 781 nano seconds
Raw Samples: 3, 10, 200, 30, 100
Statistics of 10000 Samples:
 Minimum: 1
 Median: 30
 Maximum: 400
 Mean: 92.5135
 Std Deviation: 129.31396687114966
Distribution of 100000 Samples:
 1: 8.311%
 2: 8.329%
 3: 8.421%
 4: 8.47%
 10: 8.127%
 20: 8.307%
 30: 8.39%
 40: 8.252%
 100: 8.316%
 200: 8.342%
 300: 8.244%
 400: 8.491%


Random Integers:

Base Case
Output Distribution: Random.randrange(10)
Typical Timing: 875 nano seconds
Raw Samples: 3, 8, 3, 5, 4
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5388
 Std Deviation: 2.8785279488508064
Distribution of 100000 Samples:
 0: 10.082%
 1: 9.921%
 2: 9.918%
 3: 9.904%
 4: 10.152%
 5: 9.839%
 6: 9.982%
 7: 10.016%
 8: 10.035%
 9: 10.151%

Output Distribution: random_below(10)
Typical Timing: 62 nano seconds
Raw Samples: 5, 9, 6, 1, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4703
 Std Deviation: 2.8435060159328422
Distribution of 100000 Samples:
 0: 10.092%
 1: 10.035%
 2: 9.856%
 3: 10.12%
 4: 9.996%
 5: 10.042%
 6: 10.024%
 7: 9.911%
 8: 9.938%
 9: 9.986%

Output Distribution: random_index(10)
Typical Timing: 62 nano seconds
Raw Samples: 2, 7, 8, 2, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5277
 Std Deviation: 2.8727787933984024
Distribution of 100000 Samples:
 0: 10.005%
 1: 10.092%
 2: 9.944%
 3: 10.006%
 4: 10.014%
 5: 10.012%
 6: 9.955%
 7: 10.084%
 8: 9.829%
 9: 10.059%

Output Distribution: random_range(10)
Typical Timing: 93 nano seconds
Raw Samples: 3, 8, 5, 6, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4916
 Std Deviation: 2.8815550968144956
Distribution of 100000 Samples:
 0: 10.017%
 1: 9.908%
 2: 10.027%
 3: 10.054%
 4: 10.092%
 5: 10.03%
 6: 10.1%
 7: 9.838%
 8: 9.991%
 9: 9.943%

Output Distribution: random_below(-10)
Typical Timing: 93 nano seconds
Raw Samples: 0, -5, -5, -4, -7
Statistics of 10000 Samples:
 Minimum: -9
 Median: -4
 Maximum: 0
 Mean: -4.4984
 Std Deviation: 2.8729119029793146
Distribution of 100000 Samples:
 -9: 9.997%
 -8: 9.93%
 -7: 10.077%
 -6: 10.044%
 -5: 10.04%
 -4: 10.186%
 -3: 10.018%
 -2: 9.913%
 -1: 9.881%
 0: 9.914%

Output Distribution: random_index(-10)
Typical Timing: 77 nano seconds
Raw Samples: -4, -2, -4, -3, -6
Statistics of 10000 Samples:
 Minimum: -10
 Median: -5
 Maximum: -1
 Mean: -5.4809
 Std Deviation: 2.8591349487678133
Distribution of 100000 Samples:
 -10: 10.083%
 -9: 9.951%
 -8: 9.93%
 -7: 9.92%
 -6: 10.08%
 -5: 9.871%
 -4: 10.125%
 -3: 9.924%
 -2: 10.031%
 -1: 10.085%

Output Distribution: random_range(-10)
Typical Timing: 93 nano seconds
Raw Samples: -7, -10, -5, -6, -10
Statistics of 10000 Samples:
 Minimum: -10
 Median: -5
 Maximum: -1
 Mean: -5.4819
 Std Deviation: 2.869267443018506
Distribution of 100000 Samples:
 -10: 10.093%
 -9: 9.862%
 -8: 9.8%
 -7: 10.061%
 -6: 9.983%
 -5: 10.011%
 -4: 10.114%
 -3: 10.032%
 -2: 10.05%
 -1: 9.994%

Base Case
Output Distribution: Random.randrange(1, 10)
Typical Timing: 1093 nano seconds
Raw Samples: 7, 6, 1, 7, 2
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.0296
 Std Deviation: 2.5789511315443514
Distribution of 100000 Samples:
 1: 11.122%
 2: 10.889%
 3: 11.206%
 4: 11.188%
 5: 11.201%
 6: 11.076%
 7: 11.197%
 8: 10.929%
 9: 11.192%

Output Distribution: random_range(1, 10)
Typical Timing: 93 nano seconds
Raw Samples: 7, 8, 4, 9, 4
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.9909
 Std Deviation: 2.57186287306765
Distribution of 100000 Samples:
 1: 11.094%
 2: 11.044%
 3: 11.094%
 4: 11.201%
 5: 11.222%
 6: 11.191%
 7: 11.008%
 8: 11.036%
 9: 11.11%

Output Distribution: random_range(10, 1)
Typical Timing: 93 nano seconds
Raw Samples: 7, 3, 3, 8, 1
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.0066
 Std Deviation: 2.572706419674072
Distribution of 100000 Samples:
 1: 10.986%
 2: 11.113%
 3: 11.134%
 4: 11.168%
 5: 11.068%
 6: 11.167%
 7: 11.008%
 8: 11.293%
 9: 11.063%

Base Case
Output Distribution: Random.randint(-5, 5)
Typical Timing: 1156 nano seconds
Raw Samples: -1, 0, 4, 5, 5
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0002
 Std Deviation: 3.157055061234436
Distribution of 100000 Samples:
 -5: 9.102%
 -4: 9.141%
 -3: 9.057%
 -2: 9.053%
 -1: 9.07%
 0: 9.164%
 1: 9.152%
 2: 9.009%
 3: 8.973%
 4: 8.98%
 5: 9.299%

Output Distribution: random_int(-5, 5)
Typical Timing: 62 nano seconds
Raw Samples: -5, -2, 3, 3, 4
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0275
 Std Deviation: 3.1569828007197636
Distribution of 100000 Samples:
 -5: 9.064%
 -4: 9.09%
 -3: 9.121%
 -2: 8.997%
 -1: 8.971%
 0: 9.051%
 1: 9.067%
 2: 9.171%
 3: 9.166%
 4: 9.098%
 5: 9.204%

Base Case
Output Distribution: Random.randrange(1, 20, 2)
Typical Timing: 1312 nano seconds
Raw Samples: 7, 7, 17, 7, 1
Statistics of 10000 Samples:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 9.9952
 Std Deviation: 5.725666361702239
Distribution of 100000 Samples:
 1: 9.906%
 3: 10.007%
 5: 9.983%
 7: 10.104%
 9: 9.904%
 11: 9.857%
 13: 10.189%
 15: 10.072%
 17: 9.894%
 19: 10.084%

Output Distribution: random_range(1, 20, 2)
Typical Timing: 93 nano seconds
Raw Samples: 5, 9, 17, 5, 5
Statistics of 10000 Samples:
 Minimum: 1
 Median: 11
 Maximum: 19
 Mean: 9.9968
 Std Deviation: 5.752086439705247
Distribution of 100000 Samples:
 1: 9.914%
 3: 10.006%
 5: 9.886%
 7: 10.018%
 9: 9.925%
 11: 9.966%
 13: 10.019%
 15: 10.145%
 17: 9.933%
 19: 10.188%

Output Distribution: random_range(1, 20, -2)
Typical Timing: 93 nano seconds
Raw Samples: 10, 2, 18, 14, 2
Statistics of 10000 Samples:
 Minimum: 2
 Median: 10
 Maximum: 20
 Mean: 10.9788
 Std Deviation: 5.7683687440902025
Distribution of 100000 Samples:
 2: 10.044%
 4: 9.879%
 6: 10.007%
 8: 9.98%
 10: 10.08%
 12: 10.023%
 14: 9.859%
 16: 10.105%
 18: 10.003%
 20: 10.02%

Output Distribution: d(10)
Typical Timing: 62 nano seconds
Raw Samples: 6, 10, 7, 9, 2
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4967
 Std Deviation: 2.8835777451043705
Distribution of 100000 Samples:
 1: 10.026%
 2: 9.996%
 3: 9.964%
 4: 10.198%
 5: 9.894%
 6: 9.991%
 7: 9.872%
 8: 10.076%
 9: 9.965%
 10: 10.018%

Output Distribution: dice(3, 6)
Typical Timing: 93 nano seconds
Raw Samples: 12, 8, 13, 7, 11
Statistics of 10000 Samples:
 Minimum: 3
 Median: 10
 Maximum: 18
 Mean: 10.471
 Std Deviation: 2.9748687339777597
Distribution of 100000 Samples:
 3: 0.453%
 4: 1.395%
 5: 2.83%
 6: 4.589%
 7: 7.007%
 8: 9.817%
 9: 11.488%
 10: 12.468%
 11: 12.613%
 12: 11.453%
 13: 9.797%
 14: 6.932%
 15: 4.476%
 16: 2.781%
 17: 1.417%
 18: 0.484%

Output Distribution: ability_dice(4)
Typical Timing: 218 nano seconds
Raw Samples: 11, 9, 12, 17, 11
Statistics of 10000 Samples:
 Minimum: 3
 Median: 12
 Maximum: 18
 Mean: 12.2368
 Std Deviation: 2.8474087401799846
Distribution of 100000 Samples:
 3: 0.084%
 4: 0.316%
 5: 0.769%
 6: 1.697%
 7: 2.933%
 8: 4.72%
 9: 6.995%
 10: 9.361%
 11: 11.448%
 12: 12.809%
 13: 13.474%
 14: 12.302%
 15: 9.934%
 16: 7.344%
 17: 4.208%
 18: 1.606%

Output Distribution: plus_or_minus(5)
Typical Timing: 62 nano seconds
Raw Samples: 1, 0, -2, 3, -2
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0009
 Std Deviation: 3.1746979479481303
Distribution of 100000 Samples:
 -5: 9.192%
 -4: 9.093%
 -3: 9.109%
 -2: 8.89%
 -1: 9.147%
 0: 9.161%
 1: 9.198%
 2: 8.966%
 3: 9.15%
 4: 9.017%
 5: 9.077%

Output Distribution: plus_or_minus_linear(5)
Typical Timing: 93 nano seconds
Raw Samples: 2, -2, 1, 0, 1
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0211
 Std Deviation: 2.422775634304055
Distribution of 100000 Samples:
 -5: 2.793%
 -4: 5.572%
 -3: 8.374%
 -2: 11.105%
 -1: 13.807%
 0: 16.696%
 1: 13.89%
 2: 11.09%
 3: 8.369%
 4: 5.474%
 5: 2.83%

Output Distribution: plus_or_minus_gauss(5)
Typical Timing: 93 nano seconds
Raw Samples: 0, 1, 2, -2, 0
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.01
 Std Deviation: 1.22443861626155
Distribution of 100000 Samples:
 -5: 0.075%
 -4: 0.493%
 -3: 2.347%
 -2: 7.618%
 -1: 16.213%
 0: 46.682%
 1: 16.069%
 2: 7.514%
 3: 2.426%
 4: 0.489%
 5: 0.074%


Random Floats:

Output Distribution: canonical()
Typical Timing: 62 nano seconds
Raw Samples: 0.8032432867451378, 0.13240479678379335, 0.815017476807797, 0.6641213383500574, 0.039539996186494314
Statistics of 10000 Samples:
 Minimum: 1.347565414983829e-05
 Median: (0.5009154651318495, 0.500921347727443)
 Maximum: 0.9999893644576607
 Mean: 0.4989486975362023
 Std Deviation: 0.2881492123930689
Post-processor Distribution of 100000 Samples using round method:
 0: 49.857%
 1: 50.143%

Output Distribution: random_float(0.0, 10.0)
Typical Timing: 46 nano seconds
Raw Samples: 5.057696525384957, 4.795383809802452, 6.526723283418038, 4.811609146396875, 1.4122312982707788
Statistics of 10000 Samples:
 Minimum: 5.128355005912331e-05
 Median: (4.977158246101063, 4.977536448081229)
 Maximum: 9.999572952842357
 Mean: 4.981970298699068
 Std Deviation: 2.893918935030247
Post-processor Distribution of 100000 Samples using floor method:
 0: 10.228%
 1: 10.086%
 2: 9.919%
 3: 10.022%
 4: 9.838%
 5: 10.014%
 6: 9.89%
 7: 9.886%
 8: 10.03%
 9: 10.087%


Random Booleans:

Output Distribution: percent_true(33.33)
Typical Timing: 46 nano seconds
Raw Samples: True, False, False, False, False
Statistics of 10000 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.3292
 Std Deviation: 0.46994621494857736
Distribution of 100000 Samples:
 False: 66.611%
 True: 33.389%


Shuffle Performance Tests:

Base Case: random.shuffle(some_list_100)
Typical Timing: 67531 nano seconds

fisher_yates(some_list_100)
Typical Timing: 6952 nano seconds

knuth(some_list_100)
Typical Timing: 6937 nano seconds

shuffle(some_list_100)
Typical Timing: 3968 nano seconds

-------------------------------------------------------------------------
Total Test Time: 3.183 seconds

```


## Fortuna Development Log
##### Fortuna 3.4.7
- Bug fix for analytic_continuation.

##### Fortuna 3.4.6
- Docs Update

##### Fortuna 3.4.5
- Docs Update
- Range Tests Added, see extras folder.

##### Fortuna 3.4.4
- ZeroCool Algorithm Bug Fixes
- Typos Fixed

##### Fortuna 3.4.3
- Docs Update

##### Fortuna 3.4.2
- Typos Fixed

##### Fortuna 3.4.1
- Major Bug Fix: random_index()

##### Fortuna 3.4.0 - internal
- ZeroCool Poisson Algorithm Family Updated

##### Fortuna 3.3.8 - internal
- Docs Update

##### Fortuna 3.3.7
- Fixed Performance Bug: ZeroCool Linear Algorithm Family

##### Fortuna 3.3.6
- Docs Update

##### Fortuna 3.3.5
- ABI Updates
- Bug Fixes

##### Fortuna 3.3.4
- Examples Update

##### Fortuna 3.3.3
- Test Suite Update

##### Fortuna 3.3.2 - internal
- Documentation Update

##### Fortuna 3.3.1 - internal
- Minor Bug Fix

##### Fortuna 3.3.0 - internal
- Added `plus_or_minus_gauss(N: int) -> int` random int in range [-N, N] Stretched Gaussian Distribution

##### Fortuna 3.2.3
- Small Typos Fixed

##### Fortuna 3.2.2
- Documentation update.

##### Fortuna 3.2.1
- Small Typo Fixed

##### Fortuna 3.2.0
- API updates:
    - QunatumMonty.uniform -> QunatumMonty.flat_uniform
    - QunatumMonty.front -> QunatumMonty.front_linear
    - QunatumMonty.middle -> QunatumMonty.middle_linear
    - QunatumMonty.back -> QunatumMonty.back_linear
    - QunatumMonty.quantum -> QunatumMonty.quantum_linear
    - randindex -> random_index
    - randbelow -> random_below
    - randrange -> random_range
    - randint   -> random_int

##### Fortuna 3.1.0
- `discrete()` has been removed, see Weighted Choice.
- `lazy_cat()` added.
- All ZeroCool methods have been raised to top level API, for use with lazy_cat()

##### Fortuna 3.0.1
- minor typos.

##### Fortuna 3.0.0
- Storm 2 Rebuild.

##### Fortuna 2.1.1
- Small bug fixes.
- Test updates.

##### Fortuna 2.1.0, Major Feature Update
- Fortuna now includes the best of RNG and Pyewacket.

##### Fortuna 2.0.3
- Bug fix.

##### Fortuna 2.0.2
- Clarified some documentation.

##### Fortuna 2.0.1
- Fixed some typos.

##### Fortuna 2.0.0b1-10
- Total rebuild. New RNG Storm Engine.

##### Fortuna 1.26.7.1
- README updated.

##### Fortuna 1.26.7
- Small bug fix.

##### Fortuna 1.26.6
- Updated README to reflect recent changes to the test script.

##### Fortuna 1.26.5
- Fixed small bug in test script.

##### Fortuna 1.26.4
- Updated documentation for clarity.
- Fixed a minor typo in the test script.

##### Fortuna 1.26.3
- Clean build.

##### Fortuna 1.26.2
- Fixed some minor typos.

##### Fortuna 1.26.1
- Release.

##### Fortuna 1.26.0 beta 2
- Moved README and LICENSE files into fortuna_extras folder.

##### Fortuna 1.26.0 beta 1
- Dynamic version scheme implemented.
- The Fortuna Extension now requires the fortuna_extras package, previously it was optional.

##### Fortuna 1.25.4
- Fixed some minor typos in the test script.

##### Fortuna 1.25.3
- Since version 1.24 Fortuna requires Python 3.7 or higher. This patch corrects an issue where the setup script incorrectly reported requiring Python 3.6 or higher.

##### Fortuna 1.25.2
- Updated test suite.
- Major performance update for TruffleShuffle.
- Minor performance update for QuantumMonty & FlexCat: cycle monty.

##### Fortuna 1.25.1
- Important bug fix for TruffleShuffle, QuantumMonty and FlexCat.

##### Fortuna 1.25
- Full 64bit support.
- The Distribution & Performance Tests have been redesigned.
- Bloat Control: Two experimental features have been removed.
    - RandomWalk
    - CatWalk
- Bloat Control: Several utility functions have been removed from the top level API. These function remain in the Fortuna namespace for now, but may change in the future without warning.
    - stretch_bell, internal only.
    - min_max, not used anymore.
    - analytic_continuation, internal only.
    - flatten, internal only.

##### Fortuna 1.24.3
- Low level refactoring, non-breaking patch.

##### Fortuna 1.24.2
- Setup config updated to improve installation.

##### Fortuna 1.24.1
- Low level patch to avoid potential ADL issue. All low level function calls are now qualified.

##### Fortuna 1.24
- Documentation updated for even more clarity.
- Bloat Control: Two naïve utility functions that are no longer used in the module have been removed.
    - n_samples -> use a list comprehension instead. `[f(x) for _ in range(n)]`
    - bind -> use a lambda instead. `lambda: f(x)`

##### Fortuna 1.23.7
- Documentation updated for clarity.
- Minor bug fixes.
- TruffleShuffle has been redesigned slightly, it now uses a random rotate instead of swap.
- Custom `__repr__` methods have been added to each class.

##### Fortuna 1.23.6
- New method for QuantumMonty: quantum_not_monty - produces the upside down quantum_monty.
- New bias option for FlexCat: not_monty.

##### Fortuna 1.23.5.1
- Fixed some small typos.

##### Fortuna 1.23.5
- Documentation updated for clarity.
- All sequence wrappers can now accept generators as input.
- Six new functions added:
    - random_float() -> float in range [0.0..1.0) exclusive, uniform flat distribution.
    - percent_true_float(num: float) -> bool, Like percent_true but with floating point precision.
    - plus_or_minus_linear_down(num: int) -> int in range [-num..num], upside down pyramid.
    - plus_or_minus_curve_down(num: int) -> int in range [-num..num], upside down bell curve.
    - mostly_not_middle(num: int) -> int in range [0..num], upside down pyramid.
    - mostly_not_center(num: int) -> int in range [0..num], upside down bell curve.
- Two new methods for QuantumMonty:
    - mostly_not_middle
    - mostly_not_center
- Two new bias options for FlexCat, either can be used to define x and/or y axis bias:
    - not_middle
    - not_center

##### Fortuna 1.23.4.2
- Fixed some minor typos in the README.md file.

##### Fortuna 1.23.4.1
- Fixed some minor typos in the test suite.

##### Fortuna 1.23.4
- Fortuna is now Production/Stable!
- Fortuna and Fortuna Pure now use the same test suite.

##### Fortuna 0.23.4, first release candidate.
- RandomCycle, BlockCycle and TruffleShuffle have been refactored and combined into one class: TruffleShuffle.
- QuantumMonty and FlexCat will now use the new TruffleShuffle for cycling.
- Minor refactoring across the module.

##### Fortuna 0.23.3, internal
- Function shuffle(arr: list) added.

##### Fortuna 0.23.2, internal
- Simplified the plus_or_minus_curve(num: int) function, output will now always be bounded to the range [-num..num].
- Function stretched_bell(num: int) added, this matches the previous behavior of an unbounded plus_or_minus_curve.

##### Fortuna 0.23.1, internal
- Small bug fixes and general clean up.

##### Fortuna 0.23.0
- The number of test cycles in the test suite has been reduced to 10,000 (down from 100,000). The performance of the pure python implementation and the c-extension are now directly comparable.
- Minor tweaks made to the examples in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.22.2, experimental features
- BlockCycle class added.
- RandomWalk class added.
- CatWalk class added.

##### Fortuna 0.22.1
- Fortuna classes no longer return lists of values, this behavior has been extracted to a free function called n_samples.

##### Fortuna 0.22.0, experimental features
- Function bind added.
- Function n_samples added.

##### Fortuna 0.21.3
- Flatten will no longer raise an error if passed a callable item that it can't call. It correctly returns such items in an uncalled state without error.
- Simplified `.../fortuna_extras/fortuna_examples.py` - removed unnecessary class structure.

##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Function flatten added.
- Flatten: The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random_value()
- Added Base Case for randint()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna

##### Dice 0.1.x - 0.9.x
- Experimental Phase


## Legal Information
Fortuna © 2019 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>
