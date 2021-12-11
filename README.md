# **A simple interactive interpreter written in python**


## Syntax explanation



**Note: The `>` at the beginning of the line will indicate user input, the following line will be the interpreter
output.**

### Declaring Variables

---

Integers and floats are assigned with the identifier on the left, and the value on the right. Example:

```python
> x = 3
3
```

Nested and chained assignments are also possible:

```python
> x = y = 3
3
> x = 5 + (y=4)
9
> y
4
```

### Operations

---

The interpreter will understand the following operations:

- Add, Subtract, Multiplicate, Divide with the common operators
- Modulus with %
- Exponentiate with ^
- Brackets

Operator precedence will follow the common order:

```python
> x = 2+3*4
14
> x = (2+3)*4
20
```

### Keywords

---

Currently, there are the following usable keywords:

- `sqrt` (square root)
- `sin`, `cos`, `tan`
- `factorial`

Keywords can be used in two ways: `keyword.factor` or `keyword(expression)`

*Example:*

```python
> sqrt.81
9
> sqrt(80+1)
9
```

### Functions

---

Functions are declared using the keyword `fn`, the identifier, the arguments listed with spaces between, the operator =>
and the function body.
> Declaring the function "add" that takes two arguments and returns the sum:

```python
fn add x y => x + y
```

Functions are called using the identifier and the respective arguments in brackets; seperated by commas.
> Calling the "add" function:

```python
sum = add(7+3)
10
```

### Output

---

Output for a valid function declaration will be an empty string. <br>
Output for a valid expression will be the result of the expression.<br>
Output for input consisting entirely of whitespace will be nothing.

### Errors

---

Exceptions will be thrown for invalid Expressions. <br>
*Some examples*:

```
> 4 + (4 + 1
SyntaxError: Expected a closing parenthesis.
> y + 1
NameError: Name "y" is not defined.
> 81.sqrt
SyntaxError: Wrong use of keyword sqrt.
> fn add a b = a + b
SyntaxError: Expected "=>"
```

## Functionality


Here's a quick summary on how it works: <br>
First, the **lexer** will convert the input string into a list of `tokens`. I used `namedtuples` for that. <br>
Then, the **parser** will recursively go over these tokens and put them in defined nodes (also `namedtuples`), following
the common order. <br>
Lastly, the generated tree of operations will be recusively evaluated in the **interpreter**. <br>

##### Example input:

```python
x = 5 + 1
```

##### Lexer output:

```python
[token(type='IDENTIFIER', value='x'), token(type='EQUALS', value=None), token(type='NUMBER', value=5.0), token(type='PLUS_SIGN', value=None), token(type='NUMBER', value=1.0)]
```

##### Parser output:

```python
AssignNode(identifier='x', value=AddNode(a=5.0, b=1.0))
```

##### Interpreter output:

```
6
```
