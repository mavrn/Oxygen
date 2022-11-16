# **Oxygen Guide**

## **Installation**
---

To run the program, simply clone the repository (or download the source code) and run main.py with Python 3.10+. <br>
You will need [numpy](https://pypi.org/project/numpy/) v1.22.1+ and [matplotlib](https://pypi.org/project/matplotlib/)
v3.5.1+ for plotting purposes. <br>
Alternatively, you can put the Oxygen directory in the C:\Program Files Directory and then add that directory to your PATH, enabling you to run Oxygen with the "oxy" command from anywhere in CMD. <br>("python main.py" gets replaced by "oxy")

While "oxy" opens the Oxygen interpreter, you can also specify any file to be opened as an argument.

Example:
`oxy program.oxy`

After that, you can add any of these arguments:

| Argument              | Function                                                                                 | Default  |
|-----------------------|------------------------------------------------------------------------------------------|----------|
| fallthrough | Interpreter: Will quit the program if an exception occurs. Might be more stable and less error-prone. | False
| debug                 | In addition to the expression result, will print the output of both Lexer and Parser     | False    |
| printall                   | When running a file, will print the output of every line, as opposed to only `out` calls               | True for the interpreter; False for running a file    |

Examples: <br>
`oxy fallthrough`<br>
`oxy program.oxy printall debug`

<br>

## **Quick Guide**
---

<br>

### **Operations**

---

```
>> 3+3
6
>> 1+6*4
25
>> 2**3
8
```
### **Variables**

---

```
>> x = 10
10
>> x = y = 5
5
>> y
5
>> let x 9
9
>> x *= 2
18
>> x++
18
>> x
19
>> ++x
20
>> x = 5+(y=10)
15
>> y
10
>> 2y
20
```

### **Conditions**

---

```
>> x = True
True
>> x = 2 > 3
False
>> x = not 0
True
>> 10 equals 10
True
>> True or False
True
>> True and False
False
>> 3<5<6
True
>> 5==5==5
True
```

```
>> if True => out("is true")
is true
>> if 3 smaller 2 => out("three is smaller than two")
.. or 3 equals 2 => out("three is equal to two")
.. else => out("three is bigger than two")
three is bigger than two
>> 8 if 3<10 else 10
8
>> x = False
False
>> y = 10 if x else 5
5
```

### **Arrays**

---

```
>> arr = [0,1,2,3,4]
[0, 1, 2, 3, 4]
>> arr append: 6
[0, 1, 2, 3, 4, 6]
>> arr >> x+1
[1, 2, 3, 4, 5, 7]
>> arr
[0, 1, 2, 3, 4, 6]
>> arr >>> x+2
[2, 3, 4, 5, 6, 8]
>> arr
[2, 3, 4, 5, 6, 8]
>> arr at: 1
3
>> arr[0]
2
>> arr last
8
>> x = arr pop
8
>> 1 in arr
False
>> arr sum
20
>> arr intersection: [2, 3, 10] join
"23"
>> [9, 16, 100] foreach: sqrt
3
4
10
>> [0,3,4,-4,9,-1] detect: afn a => a<0
-4
>> [0,3,4,-4] select: afn a => a>0
[3, 4]
>> [-1, 1, -9] apply: afn a => a abs if a > -5 else a
[1, 1, -9]
>> [3, 4, 5, 6, 7, 8] >> del if x%2 != 0
[4, 6, 8]
```
### **Strings**
---
```
>> x = "hello world"
"hello world"
>> x >> x+" "
"h e l l o  w o r l d "
>> x startswith "h"
True
>> x isLower
True
>> x split
["hello", "world"]
>>x find: "l"
2
```
### **Hashstrings**
---
```
>> x = ["t", "e", "s", "t"]
["t", "e", "s", "t"]
>> "this is a #x join#"
"this is a test"
```
### **Dictionaries**
---
```
>> x = {0> "zero", 1> "one"}
{0 > "zero", 1 > "one"}
>> x hasValue: "zero"
True
>> x size
2
>> x keys
[0, 1]
>> x get: 0
"zero"
>> x[1]
"one"
```

### **Functions**
---


```
>> fn add x y => x + y
>> sum = add(7, 3)
10
>> sum = 7 add: 3
10
>> sum = 7 add(3)
10
>> fn add_ten x =>
..      getScope() out
..      getFields(getScope()) out
..      "called function" out
..      return x+10
.. <<
>> 5 add_ten
global >> add_ten
{"x" > 5}
called function
15
>> x = afn a => a/2
>> 10 x
5
>> fn x =>
..      <- 10 
.. <<
>> x()
10
```

### **Loops**
---

```python
>> x = 0
>> rep 2 => x += 2
2
4
>> 
>> rep 3 => iterelem
0
1
2
>> rep 3 as i => i / 2
0
0.5
1
```

```
>> for x=0, x<5, x++ => x
0
1
2
3
4
```
```
>> iter [0,1] => iterelem + 1
1
2
>> iter [10, 11] =>
..  "counter is at #itercounter#; element is #iterelem#"
.. <<
"counter is at 0; element is 10"
"counter is at 1; element is 11"
>> iter [10, 11] as i, x=>
..  "counter is at #i#, element is #x#"
.. <<
"counter is at 0; element is 10"
"counter is at 1; element is 11"
>> [11, 12] -> iterelem
11
12
```
```
>> x = 0
0
>> while x<=2 => x+=1
1
2
3
>> while True =>
..      if x>4 => break
..      x+=1<<
4
5
```

### **Statement seperators**
---

```
>> x = 4; x + 2; x sqrt
4
6
2
```
### **Ranges**
---
```
>> 1..4
[1, 2, 3]
>> 1..10..2
[1, 3, 5, 7, 9]
>> iter 10..13 => iterelem
10
11
12
```

### **Change**
---
```
>> let x 0
0
>> change("let", "#")
>> #x 2
2
>> change("fn", "define")
>> define x a b => a*b
>> x(3,4)
12
```

### **Plotting**

---
```python
>> fn f x => 0.5 * x^3 + 2 * x^2
>> plot(f, -4, 2)
``` 

![img.png](plotted_function.png)


### **Simple Linear Equation Solving**

---

```python
>> 2x - 3 ? 5
4
>> x/10 ?= 2
20
>> x
20
```

### **Comments**

---

```
>> x = 0 ~setting x to 0
0
>> x += 1 ~adding 1 to x
1
```

### **Errors**

---

```
>> 4 + (4 + 1
SyntaxError: Expected a closing parenthesis.
>> y + 1
NameError: Name "y" is not defined.
>> fn add a b => a + b
>> add(5)
SyntaxError: Expected 2 arguments, got 1.
>> x = 2
>> x()
TypeError: float object is not callable
>> fn add a b = a + b
SyntaxError: Expected "=>"
```

## **Code examples**
---

For a more extensive list of more complex examples, check testmodules.py.

> Evaluating an expression and comparing it to 1

```
>> 1 == (0.5 + 2 / 2^2)
True
```

> Defining a function which can calculate c in a triangle according to the theorem of pythagoras

```
>> fn get_c a b => sqrt(a^2+b^2)
>> get_c(3,4)
5
```

> Defining a function which takes the arguments a, b and x and returns True if x is between a and b (and vice versa)

```
>> fn is_in_range a b x => a<x<b
>> is_in_range(0, 5, 3)
True
>> is_in_range(-2, 2, -4)
False
```

> Coding FizzBuzz

```
>> fn fizz_buzz i => 
..      for x=1, x<=i, x++ => 
..              if x%3 == 0 and x%5 == 0 =>
..                      print("FizzBuzz")
..              <<
..              or x%5 == 0 =>
..                      print("Buzz")
..              <<
..              or x%3 == 0 =>
..                      print("Fizz")
..              <<
..              else =>
..                      print(x)
..              <<
..      <<
.. <<
>> fizz_buzz.10
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
```

> Utilizing recursion to calculate the fibonacci sequence

```
fn fib n =>
    if n equals 1 =>
        return 0
    <<
    or n equals 2 =>
        return 1
    <<
    else =>
        return fib(n-1) + fib(n-2)
    <<
<<

1..16 ->
    out(iterelem, fib.iterelem)
<<
1 0
2 1
3 1
4 2
5 3
6 5
7 8
8 13
9 21
10 34
11 55
12 89
13 144
14 233
15 377
```

> Calculating P in a binomial distribution

```
>> fn bin_cof n k => factorial.n / (factorial.k * factorial(n-k))
>> fn P p n x => bin_cof(n,x) * p^x * (1-p)^(n-x)
>> P(0.3, 20, 6)
0.19163898275344238
```
 > Getting the first non-repating character in a string
```
>> fn first_non_repeating_character str =>
..    iter str => if str lower count: (iterelem lower) smaller 2 => <-iterelem 
.. <<
>> "sTreSS" first_non_repeating_character out
T
```

> Getting the next bigger number arrangable with the digits of a number
```
>> fn nextbigger num =>
..     allnums = (num asString permutations >> x join asNum) sort
..     return -1 if allnums find: num equals (allnums size-1) else allnums[allnums find: num +1]
.. <<
>> 12 nextbigger
21
>> 518 nextbigger
581
>> 2017 nextbigger
2071
```

> Writing a function that removes whitespace
```
fn remspace str => str >> del if x=" "
"    remove  these spaces" remspace
"removethesespaces"
```

## **Methodology**
---

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
