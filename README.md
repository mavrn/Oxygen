# **A simple interactive interpreter written in python**


## Syntax explanation



**Note: The `>` at the beginning of the line will indicate user input, the following line will be the interpreter
output.**

### **Declaring Variables**

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

### **Operations**

---

The interpreter will understand the following operations:

- Add, Subtract, Multiply, Divide with the common operators
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

### **Functions**

---

Functions are declared using the keyword `fn`, the identifier, the arguments listed with spaces inbetween, <br>
the operator =>
and the function body.
> Declaring the function "add" that takes two arguments and returns the sum:

```python
> fn add x y => x + y
```

Functions are called using the identifier and the respective arguments in brackets; separated by commas.
> Calling the "add" function:

```python
> sum = add(7, 3)
10
```

Alternatively, if the function takes exactly one argument, it is also callable with the identifier, a period, and the
argument.

```python
> fn add_two x => x + 2
> add_two.2
4
```

If there is a name conflict between a function variable and a global variable, the function variable will take
precedence
(emulating local and global scope).

```python
> x = 5
> add_two(4)
6
```

### **Built-in functions**

---

Currently, there are the following usable built-in functions:

- `sqrt` (square root)
- `sin`, `cos`, `tan`
- `asin`, `acos`, `atan`
- `abs`
- `factorial`

They are called just like normal functions: `keyword.factor` or `keyword(expression)`

*Example:*

```python
> sqrt.81
9
> sqrt(80+1)
9
```

### **Output**

---

Output for a valid expression will be the result of the expression.<br>
Output for a valid function declaration will be an nothing. <br>
Output for input consisting entirely of whitespace will be nothing. <br>
A warning will be displayed if the user tries to override a built-in function.

### **Errors**

---

Exceptions will be thrown for invalid Expressions. <br>
*Some examples*:

```
> 4 + (4 + 1
SyntaxError: Expected a closing parenthesis.
> y + 1
NameError: Name "y" is not defined.
> fn add a b => a + b
> add(5)
SyntaxError: Expected 2 arguments, got 1.
> fn add a b = a + b
SyntaxError: Expected "=>"
```

## **Functionality**

Here's a quick summary on how it works: <br>
First, the **lexer** will convert the input string into a list of `tokens`. I used `namedtuples` for that. <br>
Then, the **parser** will recursively go over these tokens and put them into defined nodes (also `namedtuples`),
following the common order. <br>
Lastly, the generated tree of operations will be recursively evaluated in the **interpreter**. <br>

#### Example input:

```python
x = 5 + 1
```

#### **Lexer** output:

```python
[token(type='IDENTIFIER', value='x'), token(type='EQUALS', value=None), token(type='NUMBER', value=5.0), token(type='PLUS_SIGN', value=None), token(type='NUMBER', value=1.0)]
```

#### **Parser** output:

```python
AssignNode(identifier='x', value=AddNode(a=5.0, b=1.0))
```

#### **Interpreter** output:

```
6
```
