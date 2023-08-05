# pymutation
Python library for calculating permutations and combinations

Example:
```python
from pymutation import pymutation
# A reading list contains 11 novels and 5 mysteries.
books = ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'M', 'M', 'M', 'M', 'M']
# In how many different ways could a student select
# a. a novel or a mystery?
print(pymutation(books, [lambda x: x == 'N' or x == 'M'])) # 16
# b. a novel and then a mystery?
print(pymutation(books, ['N', 'M'])) # 55
# c. a mystery and then another mystery?
print(pymutation(books, ['M', 'M'])) # 20
```
