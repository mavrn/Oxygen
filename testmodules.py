import unittest

from interface import Interface

input1 = "1 equals (0.5 + 2 / 2**2)"

input2 = """fn get_c a b => (a**2+b**2) sqrt
get_c(3,4)
"""

input3 = """fn negate boolean_value => !boolean_value
negate(1==1)
"""

input4 = """fn is_in_range a b x => a<x<b
is_in_range(0, 5, 3)
is_in_range(-2, 2, -4)
"""

input5 = """fn divide_by_two x => x/2 if x%2 == 0 else x
12 divide_by_two
13 divide_by_two
"""

input6 = """fn fizz_buzz i => rep i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
10.fizz_buzz
"""

input7 = """fn bin_cof n k => n.factorial / (k.factorial * (n-k).factorial)
fn P p n x => bin_cof(n,x) * p**x * (1-p)**(n-x)
P(0.3, 20, 6)
"""

input8 = """let x 10
fn n a =>
<- a == (x /2)<<
5 n
10 n
"""

input9 = """fn x a =>
out(a+1)
out(a+2)
<- a-1<<
0 x
"""

input10 = """x=-1
if False =>
x=0 <<
else =>
x=1 <<
x
"""

input11 = """fn fizz_buzz i => 
     for x=1, x<=i, x++ => 
             if x%3 == 0 and x%5 == 0 =>
                     out("FizzBuzz")
             <<
             or x%5 == 0 =>
                     out("Buzz")
             <<
             or x%3 == 0 =>
                     out("Fizz")
             <<
             else =>
                     out(x)
             <<
     <<
<<
10 fizz_buzz
"""

input12 = """fn x a =>
    <- "Yes" if a else "False"
<<
True x
"""

input13 = """fn x a =>
    if a > 10 => <- "Greater than 10"
    or a >= 0 => <- "Positive number"
    else => <- "Negative number"
<<
-1 x
2 x
11 x
"""

input14 = "6 if False else 5 if False else 4 if False else 3"

input15 = "x=4; x+2; x sqrt"

input16 = """rep 2 as i =>
    i+1
    i/2
<<
"""

input17 = """if False =>
    3
<<
or True =>
    4
<<
else =>
    5
<<
if False =>
    6
<<
else =>
    7
<<"""

input18 = """
x = 2
y = 2x
"""

input19 = """fn fib n =>
    if n == 1 => <- 0
    or n == 2 => <- 1
    else => <- fib(n-1) + fib(n-2)
<<
for i=1, i<=15, i++ =>
    out(i, i fib)
<<
"""

input20 = """fn x a =>
    if a == 1 =>
        <- 2
    <<
    <- x(a-1)
<<
10 x
"""

input21 = """x = [0,1,2,3,4,5,6]
[1,2,3,4,10,102] union(x)
[3,4,5,7] intersection(x)
fn y a => a**2
x apply(y)
x >> x+1
"""

input22 = """fn x =>
return 0 <<
x()
"""

input23 = """\"hallo\" reverse
"""

input24 = """2*x ? 10
10*x - 20/19 ? 100
2*y ?= 4
"""

input25 = """
~test comment
1+0.2 ~this comment is a comment
0.8/2
~~~ hi
"""

input26 = """
x = [[0,1], [2,[3,4]]]
x[0]
x[1][0]
x[1][1][0]
"""

input27 = """
"hallo" >> " " if x in "aeiou" else x
"lol" >> 1
"abcdefg" >> i
"""

input28 = """fn add_spaces str => (str asArr >> x+" ").join
"hallo" add_spaces
"""

input29 = """fn narc int => 
    spl = int asString asArr >> x asNum
    range = ([0]*10) >> i+1
    iter range as i=>
        sum = 0
        iter spl as x=>
            sum += x**i
        <<
        if sum == int => return True
    <<
    <- False
<<
153 narc out
371 narc out
4887 narc out"""

input30 = """y=0
fn x a =>
    y+=1
    "h" out
    <- "s"
<<
1 x
y
"""

#https://www.codewars.com/kata/5715eaedb436cf5606000381
codewars_input1 = """fn sum_of_positive arr =>
return (arr >> 0 if x<0 else x).sum
<<
[0,1,2,3,4,5,-2].sum_of_positive
"""

#https://www.codewars.com/kata/56dec885c54a926dcd001095
codewars_input2 = """fn get_neg num =>
return -abs(num)
<<
1.get_neg
-5.get_neg
0.get_neg
"""

#https://www.codewars.com/kata/56bc28ad5bdaeb48760009b0
codewars_input3 = """fn rem_chars str =>
res = ""
for i = 1, i<(str size -1), i++ =>
res+=str[i]
<<
<- res
<<
"remove these chars" rem_chars
"""

#https://www.codewars.com/kata/54ff3102c1bad923760001f3
codewars_input4 = """fn vowel_ct str =>
ct = 0
for c in str =>
if c in "aeiou" => 
ct++
<<
<<
return ct
<<
"hallo test".vowel_ct
"haaaloooo".vowel_ct
"""

#https://www.codewars.com/kata/52fba66badcd10859f00097e
codewars_input5 = """
"Remove all vowels" >> "" if x in "aeiou" else x
"""

#https://www.codewars.com/kata/5526fc09a1bbd946250002dc
codewars_input6 = """fn x a =>
     odd_nums = a >> del if x%2==0
     a difference(odd_nums)
     <- odd_nums[0] if odd_nums size == 1 else a[0]
<<
[160, 3, 1719, 19, 11, 13, -21] x
"""

#https://www.codewars.com/kata/546f922b54af40e1e90001da
codewars_input7 = """fn repl str =>
     str >>> del if x not in ALPHABET
     <- str.numMap().join(" ")
<<
"The sunset sets at twelve o' clock." repl
"""

#https://www.codewars.com/kata/55c45be3b2079eccff00010f
codewars_input8 = """fn order str =>
    a = str split
    new =[""]* a size
    iter a as i, word =>
        num = 0
        for char in word =>
            if char in NUMBERS => num = char asNum
        <<
        new[num-1] = word
    <<
    return new join(" ")
<<
"4of Fo1r pe6ople g3ood th5e the2" order out"""

#https://www.codewars.com/kata/54e6533c92449cc251001667
codewars_input9 = """fn uni str =>
    new = [str[0]]
    str ->
            if iterelem != new[-1] and itercounter >0 =>
                    new+=iterelem
            <<
    <<
    return new
<<
"AAAABBBCCDAABBB".uni.out
[1,2,2,3,3].uni.out
"""

#https://www.codewars.com/kata/57eb8fcdf670e99d9b000272/
codewars_input10 = """fn score st => (st.capitalize.numMap >> x asNum).sum
fn highest str => 
    h = ""
    hs = 0
    str split ->
        sc = iterelem score
        if sc > hs =>
            hs = sc
            h = iterelem
        <<
    <<
    return h
<<
'what time are we climbing up the volcano' highest"""

#https://www.codewars.com/kata/52597aa56021e91c93000cb0
codewars_input11 = """fn countzeroes arr =>
    zeroes = arr.count(0)
    arr >>> del if x == 0
    rep zeroes => arr += 0
    return arr
<<
[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9].countzeroes.out"""

#https://www.codewars.com/kata/52774a314c2333f0a7000688
codewars_input12 = """fn val str =>
    open = 0
    iter str as i, char =>
        if char == "(" => open +=1
        or char == ")" =>
            if open <= 0 => return False
            else => open -= 1
        <<
    <<
    return open == 0
<<
"(())((()())())".val
"(".val
")(()))".val
")))(((".val
"""

#https://www.codewars.com/kata/529bf0e9bdf7657179000008
codewars_input13 = """fn uniquecheck arr =>
    arr sort
    for i=1, i<arr size, i++ =>
        if i!=arr[i-1] => return False
    <<
    return True
<<
fn check sudoku =>
    column = [0]*9
    grid = [0]*9
    count = 0

    for row in sudoku =>
        if not row clone uniquecheck => return False
    <<
    for i=0, i<9, i++ =>
        for x=0, x<9, x++ =>
            column[x] = sudoku[x][i]
        <<
        if not column clone uniquecheck => return False
    <<
    for i=0, i<9, i+=3 =>
        for x=0, x<9, x+=3 =>
            for o=0, o<3, o++ =>
                for k=0, k<3, k++ =>
                    grid[count] = sudoku[i+k][x+o]
                    count++
                <<
            <<
            if not grid clone uniquecheck => return False
            grid = [0]*9
            count = 0
        <<
    <<
    return True
<<
[[5, 3, 4, 6, 7, 8, 9, 1, 2],
[6, 7, 2, 1, 9, 5, 3, 4, 8],
[1, 9, 8, 3, 4, 2, 5, 6, 7],
[8, 5, 9, 7, 6, 1, 4, 2, 3],
[4, 2, 6, 8, 5, 3, 7, 9, 1],
[7, 1, 3, 9, 2, 4, 8, 5, 6],
[9, 6, 1, 5, 3, 7, 2, 8, 4],
[2, 8, 7, 4, 1, 9, 6, 3, 5],
[3, 4, 5, 2, 8, 6, 1, 7, 9]].check
[[5, 3, 4, 6, 7, 8, 9, 1, 2],
[6, 7, 2, 1, 9, 0, 3, 4, 8],
[1, 0, 0, 3, 4, 2, 5, 6, 0],
[8, 5, 9, 7, 6, 1, 0, 2, 0],
[4, 2, 6, 8, 5, 3, 7, 9, 1],
[7, 1, 3, 9, 2, 4, 8, 5, 6],
[9, 0, 1, 5, 3, 7, 2, 1, 4],
[2, 8, 7, 4, 1, 9, 6, 3, 5],
[3, 0, 0, 4, 8, 1, 1, 7, 9]].check
"""

#https://www.codewars.com/kata/57eae20f5500ad98e50002c5
codewars_input14 = """fn remspace str => str >> del if x == " "
"8 j 8   mBliB8g  imjB8B8  jl  B".remspace
"8 8 Bi fk8h B 8 BB8B B B  B888 c hl8 BhB fd".remspace
"""

#https://www.codewars.com/kata/51c8e37cee245da6b40000bd
codewars_input15 = """
fn stripcomments str delimiters =>
    lines = str.split("\n")
    newlines = []
    iter lines as line =>
        newline = ""
        iter line as char =>
            if char in delimiters => break
            else => newline += char
        <<
        newlines += newline.strip
    <<
    return newlines.join("\n")
<<
stripcomments("apples, pears \# and bananas\ngrapes\nbananas !apples", ["\#", "!"])
stripcomments("a \#b\nc\nd $e f g", ["\#", "$"])"""

#https://www.codewars.com/kata/55983863da40caa2c900004e
codewars_input16 = """
fn nextbigger num =>
    allnums = (num.s.permutations >> n(x.join)).sort()
    return -1 if allnums.posof(num) == (allnums.l-1) else allnums[allnums.posof(num)+1]
<<
12.nextbigger
518.nextbigger
2017.nextbigger
9.nextbigger"""

#https://www.codewars.com/kata/51e056fe544cf36c410000fb
codewars_input17 = """fn wordcount text =>
    arr = split(lower(text >> " " if x not in ALPHABET))
    return arr mostCommon >> x[0]
<<
"DDD e e e e ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e".wordcount.out
"""

#https://www.codewars.com/kata/5f1891d30970800010626843
codewars_input18 = """fn multpossibilities n k =>
    results = []
    arr = [0]*n >> i+1
    combs = arr.multiCombinations(k)
    iter combs as comb =>
        res = 1
        iter comb as num =>
            res *= num
        <<
        if res == n =>
            iter comb.permutations as perm =>
                if perm not in results =>
                    results += perm
                <<
            <<
        <<
    <<
    return results size
<<
multpossibilities(24,2).out
multpossibilities(100,1).out
multpossibilities(20,3).out
"""

#https://www.codewars.com/kata/520446778469526ec0000001
codewars_input19 = """
fn same_structure_as original other =>
    if original type != other type != "Array" or original size != other size=>
        return False<<
    rep original size as i =>
        if type(original[i]) == "Array" and not same_structure_as(original[i], other[i])=>
            return False<<
    <<
    return True
<<
same_structure_as([ 1, 1, 1 ], [ 2, 2, 2 ]).out
same_structure_as([ 1, [ 1, 1 ] ], [ 2, [ 2, 2 ] ] ).out
same_structure_as([ 1, [ 1, 1 ] ], [ [ 2, 2 ], 2 ] ).out
same_structure_as([ 1, [ 1, 1 ] ], [ [ 2 ], 2 ] ).out
same_structure_as([ [ [ ], [ ] ] ], [ [ [ ], [ ] ] ] ).out
same_structure_as([ [ [ ], [ ] ] ], [ [ 1, 1 ] ] ).out"""

#https://www.codewars.com/kata/5264d2b162488dc400000001
codewars_input20 = """fn rev_5 str =>
    return (str split >> x reverse if x size >= 5) join(" ")
<<
"Hey fellow warriors".rev_5
"This is a test".rev_5
"This is another test".rev_5
"""

#https://www.codewars.com/kata/541c8630095125aba6000c00
codewars_input21 = """fn sum_of_digits num => sum(num asString asArr >> x asNum)
16.sum_of_digits.out
493193.sum_of_digits.out
fn root_sum num => 
    let res num.sum_of_digits
    return res if res asString size == 1 else res.root_sum
<<
493193.root_sum
132189.root_sum
"""

#https://www.codewars.com/kata/54bf1c2cd5b56cc47f0007a1
codewars_input22 = """fn duplicates str =>
    let dup_sum 0
    iter str as x =>
        if str count(x) > 1 =>
            str removeAll(x)
            dup_sum++
        <<
    <<
    return dup_sum
<<
"Indivisibilities".duplicates
"abcde".duplicates
"""

#https://www.codewars.com/kata/55bf01e5a717a0d57e0000ec
codewars_input23 = """fn persistent_bugger num =>
    let ct 0
    while num asString size > 1 =>
        new = 1
        iter num asString asArr as x => new *= x asNum
        num = new
        ct++
    <<
    return ct
<<
39.persistent_bugger
999.persistent_bugger
"""

#https://www.codewars.com/kata/517abf86da9663f1d2000003
codewars_input24 = """fn camel_case str => 
    let a str split("_", "-")
    let res a[0]
    iter a[1:a size] as x =>
        res += x capitalize<<
    return res
<<
"the-stealth-warrior".camel_case
"The_Stealth_Warrior".camel_case
"""

#https://www.codewars.com/kata/585d7d5adb20cf33cb000235
codewars_input25 = """fn unique_number array =>
    array ->
        if array count(iterelem) == 1 => <- iterelem
    <<
<<
[ 1, 1, 1, 2, 1, 1 ].unique_number.out
[ 0, 0, 0.55, 0, 0 ].unique_number.out
"""

#https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7
codewars_input26 = """fn xy array x y =>
    return 0 if (x<0 or x>=array[0] size or y<0 or y>=array size) else array[y][x]
<<

fn field_validator f =>
    for y=0,y<f.size,y++ =>
        for x=0,x<f[y].size,x++ =>
            if (xy(f, x, y) == 1) =>
                v = xy(f, x, y-1) != 0 or xy(f, x, y+1) != 0
                h = xy(f, x-1, y) != 0 or xy(f, x+1, y) != 0
                if h and v => return false
                if v => f[y][x] = -1
                if (xy(f, x-1, y-1) != 0 or xy(f, x+1, y-1) != 0 or xy(f, x+1, y+1) != 0 or xy(f, x-1, y+1) != 0) =>
                    return False<<
            <<
        <<
    <<
    ship_counts = [0, 4, 3, 2, 1]
    for y=0, y<f.size, y++ =>
        for x=0, x<f[y].size, x++ =>
            if (xy(f, x, y) == 1) =>
                len = 1
                while (xy(f, ++x, y) == 1) => len++
                if len > 4 => return False
                ship_counts[len]--
            <<
        <<
    <<
    for x=0, x<f[0].size, x++ =>
        for y=0, y<f.size, y++ =>
            if (xy(f, x, y) == -1) =>
                len = 1
                while (xy(f, x, ++y) == -1) => len++
                if len > 4 => return False
                ship_counts[len]--
            <<
        <<
    <<
    iter ship_counts as count => if count != 0 => return False
    return True
<<
[[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
[1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]].field_validator.out
[[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
[1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]].field_validator.out
[[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0]].field_validator.out
"""

#https://www.codewars.com/kata/534e01fbbb17187c7e0000c6
codewars_input27 = """fn spiralize size =>
    spiral = [[0] * size]*size
    pos_x = pos_y = 0
    direction = 'right'
    while True =>
        spiral[pos_y][pos_x] = 1
        if direction == 'right' =>
            if (pos_x + 1) < size =>
                if (pos_x + 2) < size =>
                    if spiral[pos_y][pos_x + 2] == 1 =>
                        direction = 'down'
                        pos_y += 1
                        if (spiral[pos_y][pos_x-1] != 0 or spiral[pos_y][pos_x+1] != 0 or spiral[pos_y+1][pos_x] != 0)=> break
                    <<
                    else=> pos_x += 1
                <<
                else=> pos_x += 1
            <<
            else=> direction = 'down'
        <<

        or direction == 'down' =>
            if (pos_y + 1) < size =>
                if (pos_y + 2) < size =>
                    if spiral[pos_y + 2][pos_x] == 1 =>
                        direction = 'left'
                        pos_x -= 1
                        if (spiral[pos_y-1][pos_x] != 0 or spiral[pos_y+1][pos_x] != 0 or spiral[pos_y][pos_x-1] != 0) => break
                    <<
                    else => pos_y += 1
                <<
                else => pos_y += 1
            <<
            else => direction = 'left'
        <<

        or direction == 'left' =>
            if (pos_x - 1) >= 0 =>
                if (pos_x - 2) >= 0 =>
                    if spiral[pos_y][pos_x - 2] == 1 =>
                        direction = 'up'
                        pos_y -= 1
                        if (spiral[pos_y][pos_x-1] != 0 or spiral[pos_y][pos_x+1] != 0 or spiral[pos_y-1][pos_x] != 0) => break
                    <<
                    else => pos_x -= 1
                <<
                else =>  pos_x -= 1
            <<
            else => direction = 'up'
        <<

        or direction == 'up' =>
            if (pos_y - 1) >= 0 =>
                if (pos_y - 2) >= 0 =>
                    if spiral[pos_y - 2][pos_x] == 1 =>
                        direction = 'right'
                        pos_x += 1
                        if (spiral[pos_y-1][pos_x] != 0 or spiral[pos_y+1][pos_x] != 0 or spiral[pos_y][pos_x+1] != 0) => break
                    <<
                    else => pos_y -= 1
                <<
                else => pos_y -= 1
            <<
            else => direction = 'right'
        <<
    <<
    return spiral
<<
7.spiralize
"""

#https://www.codewars.com/kata/5279f6fe5ab7f447890006a7
codewars_input28 = """fn pick_peaks array =>
    result = {"pos" > [], "peaks" > []}
    pos = 0
    iter 1:(array size -1) as i =>
        if array[i] != array[pos] => pos = i
        if pos and array[pos-1] < array[pos] > array[i+1] =>
            result["pos"] += pos
            result["peaks"] += array[pos]
        <<
    <<
    <- result
<<
[3, 2, 3, 6, 4, 1, 2, 3, 2, 1, 2, 3].pick_peaks
[1, 2, 2, 2, 1].pick_peaks
"""

#https://www.codewars.com/kata/51ba717bb08c1cd60f00002f
codewars_input29 = """fn range_extraction a =>
    let result ""
    let tmp []
    iter a as e =>
        if not tmp or abs(e-tmp[-1]) == 1 => tmp += e
        else =>
            if tmp size >= 3 =>
                result += tmp[0] asString + "-" + tmp[-1] asString + ","
            <<
            else =>
                iter tmp as t =>
                    result += t asString + ","
                <<
            <<
            tmp = [e]
        <<
    <<
    if tmp size >= 3 =>
        result += tmp[0] asString + "-" + tmp[-1] asString + ","
    <<
    else =>
        iter tmp as t =>
            result += t asString + ","
        <<
    <<
    return result [0:-1]
<<

[-10, -9, -8, -6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20] range_extraction
"""


output1 = ['True']
output2 = ['5']
output3 = ['False']
output4 = ['True', 'False']
output5 = ['6', '13']
output6 = ['"FizzBuzz"', '1', '2', '"Fizz"', '4', '"Buzz"', '"Fizz"', '7', '8', '"Fizz"']
output7 = ['0.19163898275344238']
output8 = ['10', 'True', 'False']
output9 = ['1', '2', '-1']
output10 = ['-1', '1', '1']
output11 = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz']
output12 = ['"Yes"']
output13 = ['"Negative number"', '"Positive number"', '"Greater than 10"']
output14 = ['3']
output15 = ['4', '6', '2']
output16 = ['1', '0', '2', '0.5']
output17 = ['4', '7']
output18 = ['2', '4']
output19 = ['1 0', '2 1', '3 1', '4 2', '5 3', '6 5', '7 8', '8 13', '9 21', '10 34', '11 55', '12 89', '13 144', '14 233', '15 377']
output20 = ['2']
output21 = ['[0, 1, 2, 3, 4, 5, 6]', '[1, 2, 3, 4, 10, 102, 0, 5, 6]', '[3, 4, 5]', '[0, 1, 4, 9, 16, 25, 36]','[1, 2, 5, 10, 17, 26, 37]']
output22 = ['0']
output23 = ['"ollah"']
output24 = ['5', '10.105263157894736', '2']
output25 = ['1.2', '0.4']
output26 = ['[[0, 1], [2, [3, 4]]]', '[0, 1]', '2', '3']
output27 = ['"h ll "', '"111"', '"0123456"']
output28 = ['"h a l l o "']
output29 = ['True', 'True', 'False']
output30 = ['0', 'h', '"s"', '1']
codewars_output1 = ['15']
codewars_output2 = ['-1', '-5', '0']
codewars_output3 = ['"emove these char"']
codewars_output4 = ['3', '7']
codewars_output5 = ['"Rmv ll vwls"']
codewars_output6 = ['160']
codewars_output7 = ['"20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"']
codewars_output8 = ['Fo1r the2 g3ood 4of th5e pe6ople']
codewars_output9 = ['["A", "B", "C", "D", "A", "B"]', '[1, 2, 3]']
codewars_output10 = ['"volcano"']
codewars_output11 = ['[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]']
codewars_output12 = ['True', 'False', 'False', 'False']
codewars_output13 = ['True', 'False']
codewars_output14 = ['"8j8mBliB8gimjB8B8jlB"', '"88Bifk8hB8BB8BBBB888chl8BhBfd"']
codewars_output15 = ['"apples, pears\ngrapes\nbananas"', '"a\nc\nd"']
codewars_output16 = ['21', '581', '2071', '-1']
codewars_output17 = ['["e", "ddd", "aa"]']
codewars_output18 = ['8', '1', '18']
codewars_output19 = ['True', 'True', 'False', 'False', 'True', 'False']
codewars_output20 = ['"Hey wollef sroirraw"', '"This is a test"','"This is rehtona test"']
codewars_output21 = ['7', '29', '2', '6']
codewars_output22 = ['2', '0']
codewars_output23 = ['3', '4']
codewars_output24 = ['"theStealthWarrior"', '"TheStealthWarrior"']
codewars_output25 = ['2', '0.55']
codewars_output26 = ["True", "False", "True"]
codewars_output27 = ['[[1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]']
codewars_output28 = ['{"pos" > [3, 7], "peaks" > [6, 3]}','{"pos" > [1], "peaks" > [2]}']
codewars_output29 = ['"-10--8,-6,-3-1,3-5,7-11,14,15,17-20"']


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.interface = Interface(debug=False, quit_after_exceptions=True, printall=True)

    def test1(self):
        self.assertEqual(self.interface.run(input1, return_out=True), output1)

    def test2(self):
        self.assertEqual(self.interface.run(input2, return_out=True), output2)

    def test3(self):
        self.assertEqual(self.interface.run(input3, return_out=True), output3)

    def test4(self):
        self.assertEqual(self.interface.run(input4, return_out=True), output4)

    def test5(self):
        self.assertEqual(self.interface.run(input5, return_out=True), output5)

    def test6(self):
        self.assertEqual(self.interface.run(input6, return_out=True), output6)

    def test7(self):
        self.assertEqual(self.interface.run(input7, return_out=True), output7)

    def test8(self):
        self.assertEqual(self.interface.run(input8, return_out=True), output8)

    def test9(self):
        self.assertEqual(self.interface.run(input9, return_out=True), output9)

    def test10(self):
        self.assertEqual(self.interface.run(input10, return_out=True), output10)

    def test11(self):
        self.assertEqual(self.interface.run(input11, return_out=True), output11)

    def test12(self):
        self.assertEqual(self.interface.run(input12, return_out=True), output12)

    def test13(self):
        self.assertEqual(self.interface.run(input13, return_out=True), output13)

    def test14(self):
        self.assertEqual(self.interface.run(input14, return_out=True), output14)

    def test15(self):
        self.assertEqual(self.interface.run(input15, return_out=True), output15)

    def test16(self):
        self.assertEqual(self.interface.run(input16, return_out=True), output16)

    def test17(self):
        self.assertEqual(self.interface.run(input17, return_out=True), output17)

    def test18(self):
        self.assertEqual(self.interface.run(input18, return_out=True), output18)

    def test19(self):
        self.assertEqual(self.interface.run(input19, return_out=True), output19)

    def test20(self):
        self.assertEqual(self.interface.run(input20, return_out=True), output20)

    def test21(self):
        self.assertEqual(self.interface.run(input21, return_out=True), output21)

    def test22(self):
        self.assertEqual(self.interface.run(input22, return_out=True), output22)

    def test23(self):
        self.assertEqual(self.interface.run(input23, return_out=True), output23)

    def test24(self):
        self.assertEqual(self.interface.run(input24, return_out=True), output24)

    def test25(self):
        self.assertEqual(self.interface.run(input25, return_out=True), output25)

    def test26(self):
        self.assertEqual(self.interface.run(input26, return_out=True), output26)

    def test27(self):
        self.assertEqual(self.interface.run(input27, return_out=True), output27)

    def test28(self):
        self.assertEqual(self.interface.run(input28, return_out=True), output28)

    def test29(self):
        self.assertEqual(self.interface.run(input29, return_out=True), output29)

    def test30(self):
        self.assertEqual(self.interface.run(input30, return_out=True), output30)

    def test_codewars1(self):
        self.assertEqual(self.interface.run(codewars_input1, return_out=True), codewars_output1)

    def test_codewars2(self):
        self.assertEqual(self.interface.run(codewars_input2, return_out=True), codewars_output2)

    def test_codewars3(self):
        self.assertEqual(self.interface.run(codewars_input3, return_out=True), codewars_output3)

    def test_codewars4(self):
        self.assertEqual(self.interface.run(codewars_input4, return_out=True), codewars_output4)

    def test_codewars5(self):
        self.assertEqual(self.interface.run(codewars_input5, return_out=True), codewars_output5)

    def test_codewars6(self):
        self.assertEqual(self.interface.run(codewars_input6, return_out=True), codewars_output6)

    def test_codewars7(self):
        self.assertEqual(self.interface.run(codewars_input7, return_out=True), codewars_output7)

    def test_codewars8(self):
        self.assertEqual(self.interface.run(codewars_input8, return_out=True), codewars_output8)

    def test_codewars9(self):
        self.assertEqual(self.interface.run(codewars_input9, return_out=True), codewars_output9)

    def test_codewars10(self):
        self.assertEqual(self.interface.run(codewars_input10, return_out=True), codewars_output10)

    def test_codewars11(self):
        self.assertEqual(self.interface.run(codewars_input11, return_out=True), codewars_output11)

    def test_codewars12(self):
        self.assertEqual(self.interface.run(codewars_input12, return_out=True), codewars_output12)

    def test_codewars13(self):
        self.assertEqual(self.interface.run(codewars_input13, return_out=True), codewars_output13)

    def test_codewars14(self):
        self.assertEqual(self.interface.run(codewars_input14, return_out=True), codewars_output14)

    def test_codewars15(self):
        self.assertEqual(self.interface.run(codewars_input15, return_out=True), codewars_output15)

    def test_codewars16(self):
        self.assertEqual(self.interface.run(codewars_input15, return_out=True), codewars_output15)

    def test_codewars17(self):
        self.assertEqual(self.interface.run(codewars_input17, return_out=True), codewars_output17)

    def test_codewars18(self):
        self.assertEqual(self.interface.run(codewars_input18, return_out=True), codewars_output18)

    def test_codewars19(self):
        self.assertEqual(self.interface.run(codewars_input19, return_out=True), codewars_output19)

    def test_codewars20(self):
        self.assertEqual(self.interface.run(codewars_input20, return_out=True), codewars_output20)

    def test_codewars21(self):
        self.assertEqual(self.interface.run(codewars_input21, return_out=True), codewars_output21)

    def test_codewars22(self):
        self.assertEqual(self.interface.run(codewars_input22, return_out=True), codewars_output22)

    def test_codewars23(self):
        self.assertEqual(self.interface.run(codewars_input23, return_out=True), codewars_output23)

    def test_codewars24(self):
        self.assertEqual(self.interface.run(codewars_input24, return_out=True), codewars_output24)

    def test_codewars25(self):
        self.assertEqual(self.interface.run(codewars_input25, return_out=True), codewars_output25)

    def test_codewars26(self):
        self.assertEqual(self.interface.run(codewars_input26, return_out=True), codewars_output26)

    def test_codewars27(self):
        self.assertEqual(self.interface.run(codewars_input27, return_out=True), codewars_output27)

    def test_codewars28(self):
        self.assertEqual(self.interface.run(codewars_input28, return_out=True), codewars_output28)

    def test_codewars29(self):
        self.assertEqual(self.interface.run(codewars_input29, return_out=True), codewars_output29)

    def test_math(self):
        self.assertEqual(self.interface.run(
            "100.sqrt.factorial",
            return_out=True, ),
            ["3628800"])

    def test_bool(self):
        self.assertEqual(self.interface.run(
            "bool(0);bool(10==10)",
            return_out=True, ),
            ["False", "True"])

    def test_midn(self):
        self.assertEqual(self.interface.run(
            "midnight(1,0,-1)",
            return_out=True, ),
            ["[1, -1]"])

    def test_leet(self):
        self.assertEqual(self.interface.run(
            "'Hallo'.leet",
            return_out=True, ),
            ['"|-|4ll0"'])

    def test_type(self):
        self.assertEqual(self.interface.run(
            "type('str');type(0);type([]);type(True)",
            return_out=True, ),
            ['"String"', '"Number"', '"Array"', '"Bool"'])

    def test_arr(self):
        self.assertEqual(self.interface.run(
            "'hallo' asArr",
            return_out=True, ),
            ['["h", "a", "l", "l", "o"]'])

    def test_apply(self):
        self.assertEqual(self.interface.run(
            'fn x a => a+10;[0,1,2].apply(x)',
            return_out=True, ),
            ['[10, 11, 12]'])

    def test_append(self):
        self.assertEqual(self.interface.run(
            'x = [0].append(1);x+2;x+=3;x',
            return_out=True, ),
            ['[0, 1]', '[0, 1, 2]', '[0, 1, 3]', '[0, 1, 3]'])

    def test_union(self):
        self.assertEqual(self.interface.run(
            '[0,1,2].union([2,3,4])',
            return_out=True, ),
            ['[0, 1, 2, 3, 4]'])

    def test_intersection(self):
        self.assertEqual(self.interface.run(
            '[0,1,2].intersection([1,2,3])',
            return_out=True, ),
            ['[1, 2]'])

    def test_join(self):
        self.assertEqual(self.interface.run(
            '["h", "a"].join(" ");["h", "o"].join',
            return_out=True, ),
            ['"h a"', '"ho"'])

    def test_rev(self):
        self.assertEqual(self.interface.run(
            '"xa".reverse;[0,1].reverse',
            return_out=True, ),
            ['"ax"', '[1, 0]'])

    def test_sum(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3].sum',
            return_out=True, ),
            ['6'])

    def test_slice(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3,4].slice(1,3);"hallo"[0:5:2]',
            return_out=True, ),
            ['[1, 2]', '"hlo"'])

    def test_minmax(self):
        self.assertEqual(self.interface.run(
            '[0,2,3,4,5,100,2,101,-3].min;[0,2,3,4,5,100,2,101,-3].max',
            return_out=True, ),
            ['-3', '101'])

    def test_conv(self):
        self.assertEqual(self.interface.run(
            '10.asString;type(10.asString);"10".asNum',
            return_out=True, ),
            ['"10"', '"String"', '10'])

    def test_split(self):
        self.assertEqual(self.interface.run(
            '"h a".split',
            return_out=True, ),
            ['["h", "a"]'])

    def test_difference(self):
        self.assertEqual(self.interface.run(
            'difference([0,1,2,3], [0,1,2])',
            return_out=True, ),
            ['[3]'])

    def test_count(self):
        self.assertEqual(self.interface.run(
            '[0,0,1,2].count(0);"hallo".count("l", "h")',
            return_out=True, ),
            ['2', '3'])

    def test_nummap(self):
        self.assertEqual(self.interface.run(
            '"hallo".numMap',
            return_out=True, ),
            ['[8, 1, 12, 12, 15]'])

    def test_upper_lower_capitalize(self):
        self.assertEqual(self.interface.run(
            '"hAlLo".lower;"halLo".upper;"hALLO".capitalize',
            return_out=True, ),
            ['"hallo"', '"HALLO"', '"Hallo"'])

    def test_strip(self):
        self.assertEqual(self.interface.run(
            '"h f    ".strip;"jk".strip("k")',
            return_out=True, ),
            ['"h f"', '"j"'])

    def test_replace(self):
        self.assertEqual(self.interface.run(
            '[0,1].replace(0,2)',
            return_out=True, ),
            ['[2, 1]'])

    def test_isupper_islower_iscapitalized(self):
        self.assertEqual(self.interface.run(
            '"hallo".isLower;"Hallo".isUpper;"Hallo".isCapitalized',
            return_out=True, ),
            ['True', 'False', 'True'])

    def test_sort(self):
        self.assertEqual(self.interface.run(
            '[1,0,-1].sort',
            return_out=True, ),
            ['[-1, 0, 1]'])

    def test_posof(self):
        self.assertEqual(self.interface.run(
            '"hallo".posOf("o")',
            return_out=True, ),
            ['4'])

    def test_combinations_allcombinations_multicombinations_permutations_mostcommon(self):
        self.assertEqual(self.interface.run(
            'x="ha";"hal".combinations(2);x.allCombinations;x.multiCombinations;x.permutations;x.mostCommon(1)',
            return_out=True, ),
            ['"ha"', '[["h", "a"], ["h", "l"], ["a", "l"]]', '[[], ["h"], ["a"], ["h", "a"]]',
             '[["h", "h"], ["h", "a"], ["a", "a"]]', '[["h", "a"], ["a", "h"]]', '[["h", 1]]'])

    def test_removeduplicates(self):
        self.assertEqual(self.interface.run(
            '[0,0,1].removeDuplicates',
            return_out=True, ),
            ['[0, 1]'])

    def test_range(self):
        self.assertEqual(self.interface.run(
            '1:10:3',
            return_out=True, ),
            ['[1, 4, 7]'])

    def test_slices(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3,4,5][1:-1:2]',
            return_out=True, ),
            ['[1, 3]'])

    def test_iter(self):
        self.assertEqual(self.interface.run(
            'iter 1:6:3 => iterelem',
            return_out=True, ),
            ['1', '4'])

    def test_deleteat_pop(self):
        self.assertEqual(self.interface.run(
            'range(0,2)',
            return_out=True, ),
            ['[0, 1]'])

    def test_if_without_else(self):
        self.assertEqual(self.interface.run(
            'x = 1 if False;x;[0,1,2] >> -1 if x==0',
            return_out=True, ),
            ['[-1, 1, 2]'])

def main():
    unittest.main()


if __name__ == "__main__":
    main()
