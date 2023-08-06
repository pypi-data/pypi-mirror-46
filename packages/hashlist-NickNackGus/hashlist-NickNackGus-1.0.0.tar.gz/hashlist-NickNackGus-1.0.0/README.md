# HashList

This is a package for a list that can display the minimal differences between instances of this type.

This is best demonstrated with Python's go-to metasyntatic values:

```python
menu = [
    HashList(['egg', 'bacon']),
    HashList(['egg', 'sausage', 'bacon']),
    HashList(['egg', 'spam']),
    HashList(['egg', 'bacon', 'spam']),
    HashList(['egg', 'bacon', 'sausage', 'spam']),
    HashList(['spam', 'bacon', 'sausage', 'spam']),
    HashList(['spam', 'egg', 'spam', 'spam', 'bacon', 'spam']),
    HashList(['spam', 'spam', 'spam', 'egg', 'spam']),
    HashList(['spam', 'spam', 'spam', 'spam', 'spam', 'spam', 'baked beans', 'spam', 'spam', 'spam', 'spam']),
    HashList(['lobster thermidor aux crevettes with a mornay sauce, garnished with truffle pâté and a fried egg on top', 'spam'])
]

# Header
end = ', '
for i in range(len(menu)):
    if i == len(menu) - 1:
        end = ': '
    print('Combo {}'.format(i), end=end)
print("Item")
print("-" * 100)

# Table of indicies
for entry in menu[0].diff(menu[1:]):
    end = ', '
    for i in range(len(entry['matches'])):
        match = entry['matches'][i]
        if i == len(entry['matches']) - 1:
            end = ': '
        print('{!r:>7}'.format(match), end=end)
    print(entry['item'])
```

Output:
```
Combo 0, Combo 1, Combo 2, Combo 3, Combo 4, Combo 5, Combo 6, Combo 7, Combo 8, Combo 9: Item
----------------------------------------------------------------------------------------------------
      0,       0,       0,       0,       0,    None,       1,       3,    None,    None: egg
      1,       2,    None,       1,       1,       1,       4,    None,    None,    None: bacon
   None,       1,    None,    None,       2,       2,    None,    None,    None,    None: sausage
   None,    None,       1,       2,       3,       0,       0,       0,       0,       1: spam
   None,    None,    None,    None,    None,       3,       2,       1,       1,    None: spam
   None,    None,    None,    None,    None,    None,       3,       2,       2,    None: spam
   None,    None,    None,    None,    None,    None,       5,       4,       3,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,       4,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,       5,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,       6,    None: baked beans
   None,    None,    None,    None,    None,    None,    None,    None,       7,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,       8,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,       9,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,      10,    None: spam
   None,    None,    None,    None,    None,    None,    None,    None,    None,       0: lobster thermidor aux crevettes with a mornay sauce, garnished with truffle pâté and a fried egg on top
```

