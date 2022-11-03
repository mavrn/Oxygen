import unittest

from interface import Interface

input1 = "1 == (0.5 + 2 / 2^2)"
input2 = """fn get_c a b => sqrt(a^2+b^2)
get_c(3,4)
"""
input3 = """fn reverse boolean_value => !boolean_value
reverse(1==1)
"""
input4 = """fn is_in_range a b x => a<x<b
is_in_range(0, 5, 3)
is_in_range(-2, 2, -4)
"""
input5 = """fn divide_by_two x => x/2 if x%2 == 0 else x
12.divide_by_two
13.divide_by_two
"""
input6 = """fn fizz_buzz i => rep i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
10.fizz_buzz
"""
input7 = """fn bin_cof n k => n.factorial / (k.factorial * (n-k).factorial)
fn P p n x => bin_cof(n,x) * p^x * (1-p)^(n-x)
P(0.3, 20, 6)
"""
input8 = """x = 10
fn n a =>
return a == (x /2)<<
5.n
10.n
"""
input9 = """fn x a =>
p(a+1)
p(a+2)
return a-1<<
0.x
"""
input10 = """if False =>
x=0 <<
else =>
x=1 <<
x
"""
input11 = """fn fizz_buzz i => 
     for x=1, x<=i, x++ => 
             if x%3 == 0 and x%5 == 0 =>
                     p("FizzBuzz")
             <<
             or x%5 == 0 =>
                     p("Buzz")
             <<
             or x%3 == 0 =>
                     p("Fizz")
             <<
             else =>
                     p(x)
             <<
     <<
<<
10.fizz_buzz
"""
input12 = """fn x a =>
    return "Yes" if a else "False"
<<
True.x
"""
input13 = """fn x a =>
    if a > 10 =>
        return "Greater than 10"
    <<
    or a >= 0 =>
        return "Positive number"
    <<
    else =>
        return "Negative number"
    <<
<<
-1.x
2.x
11.x
"""
input14 = "6 if False else 5 if False else 4 if False else 3"
input15 = "x=4; x+2; x.sqrt"
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
    if n == 1 =>
        return 0
    <<
    or n == 2 =>
        return 1
    <<
    else =>
        return fib(n-1) + fib(n-2)
    <<
<<
for i=1, i<=15, i++ =>
    p(i, i.fib)
<<
"""
input20 = """fn x a =>
    if a == 1 =>
        return 2
    <<
    return x(a-1)
<<
10.x
"""
input21 = """x = [0,1,2,3,4,5,6]
[1,2,3,4,10,102].union(x)
[3,4,5,7].intersection(x)
fn y a => a^2
x.apply(y)
x >> x+1
"""
input22 = """fn x =>
return 0 <<
x()
"""
input23 = """fn sum_of_positive arr =>
return (arr >> 0 if x<0 else x).sum
<<
[0,1,2,3,4,5,-2].sum_of_positive
"""
input24 = """fn get_neg num =>
return -abs(num)
<<
1.get_neg
-5.get_neg
0.get_neg
"""
input25 = """\"hallo\".rev
"""
input26 = """fn rem_chars str =>
res = ""
for i = 1, i<(str.l-1), i++ =>
res+=str[i]
<<
return res
<<
"remove these chars".rem_chars
"""
input27 = """fn vowel_ct str =>
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
input28 = """2x ? 10
10x - 20/19 ? 100
2y ?= 4
"""
input29 = """
~test comment
1+0.2 ~this comment is a comment
0.8/2
~~~ hi
"""
input30 = """
x = [[0,1], [2,[3,4]]]
x[0]
x[1][0]
x[1][1][0]
"""
input31 = """
"hallo" >> " " if x in "aeiou" else x
"lol" >> 1
"abcdefg" >> i
"""
input32 = """fn add_spaces str => (str.arr >> x+" ").join
"hallo".add_spaces
"""
input33 = """
"Remove all vowels" >> "" if x in "aeiou" else x
"""
input34 = """fn x a =>
     odd_nums = a >> del if x%2==0
     a.difference(odd_nums)
     return odd_nums[0] if odd_nums.l == 1 else a[0]
<<
[160, 3, 1719, 19, 11, 13, -21].x
"""
input35 = """fn repl str =>
     str >>> "" if not (x in alphabet)
     return str.nummap().join(" ")
<<
"The sunset sets at twelve o' clock.".repl
"""
input36 = """fn order str =>
    a = str.split()
    new =[""]*a.l
    iter a as i, word =>
        num = 0
        for char in word =>
            if char in numbers => num = char.n
        <<
        new[num-1] = word
    <<
    return new.join(" ")
<<
p("4of Fo1r pe6ople g3ood th5e the2".order)"""
input37 = """fn uni str =>
    new = [str[0]]
    iter str =>
            if _x != new[-1] and _i >0 =>
                    new+=_x
            <<
    <<
    return new
<<
"AAAABBBCCDAABBB".uni.p
[1,2,2,3,3].uni.p
"""
input38 = """fn narc int => 
    spl = int.s.arr >> x.n
    range = ([0]*10) >> i+1
    iter range as i=>
        sum = 0
        iter spl as x=>
            sum += x^i
        <<
        if sum == int => return True
    <<
    return False
<<
153.narc.p
371.narc.p
4887.narc.p"""
input39 = """fn score st => (st.capitalize.nummap >> x.n).sum
fn highest str => 
    h = ""
    hs = 0
    iter str.split() =>
        sc = _x.score
        if sc > hs =>
            hs = sc
            h = _x
        <<
    <<
    return h
<<
'what time are we climbing up the volcano'.highest"""
input40 = """fn countzeroes arr =>
    zeroes = arr.count(0)
    arr >>> del if x == 0
    rep zeroes => arr += 0
    return arr
<<
[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9].countzeroes.p"""
input41 = """fn val str =>
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
input42 = """fn uniquecheck arr =>
    arr.sort()
    for i=1, i<arr.l, i++ =>
        if i!=arr[i-1] => return False
    <<
    return True
<<
fn check sudoku =>
    column = [0]*9
    grid = [0]*9
    count = 0

    for row in sudoku =>
        if not uniquecheck(row) => return False
    <<
    for i=0, i<9, i++ =>
        for x=0, x<9, x++ =>
            column[x] = sudoku[x][i]
        <<
        if not uniquecheck(column) => return False
    <<
    for i=0, i<9, i+=3 =>
        for x=0, x<9, x+=3 =>
            for o=0, o<3, o++ =>
                for k=0, k<3, k++ =>
                    grid[count] = sudoku[i+k][x+o]
                    count++
                <<
            <<
            if not uniquecheck(grid) => return False
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
input43 = """fn remspace str => str >> del if x == " "
"8 j 8   mBliB8g  imjB8B8  jl  B".remspace
"8 8 Bi fk8h B 8 BB8B B B  B888 c hl8 BhB fd".remspace
"""
input44 = """
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
stripcomments("apples, pears # and bananas\ngrapes\nbananas !apples", ["#", "!"])
stripcomments("a #b\nc\nd $e f g", ["#", "$"])"""
input45 = """
fn nextbigger num =>
    allnums = (num.s.permutations >> n(x.join)).sort()
    return -1 if allnums.posof(num) == (allnums.l-1) else allnums[allnums.posof(num)+1]
<<
12.nextbigger
518.nextbigger
2017.nextbigger
9.nextbigger"""
input46 = """fn wordcount text =>
    arr = split(lower(text >> " " if x not in alphabet))
    return arr.mostcommon >> x[0]
<<
"DDD e e e e ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e".wordcount.p
"""
input47 = """fn multpossibilities n k =>
    results = []
    arr = [0]*n >> i+1
    combs = arr.multicombinations(k)
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
    return results.l
<<
multpossibilities(24,2).p
multpossibilities(100,1).p
multpossibilities(20,3).p
"""
input48 = """y=0
fn x a =>
    y+=1
    "h".p
    return "s"
<<
1.x
y
"""

output1 = ['True']
output2 = ['5']
output3 = ['False']
output4 = ['True', 'False']
output5 = ['6', '13']
output6 = ['"FizzBuzz"', '1', '2', '"Fizz"', '4', '"Buzz"', '"Fizz"', '7', '8', '"Fizz"']
output7 = ['0.19163898275344238']
output8 = ['10', '"Warning: Built-in function n has been overridden."', 'True', 'False']
output9 = ['1', '2', '-1']
output10 = ['1', '1']
output11 = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz']
output12 = ['"Yes"']
output13 = ['"Negative number"', '"Positive number"', '"Greater than 10"']
output14 = ['3']
output15 = ['4', '6', '2']
output16 = ['1', '0', '2', '0.5']
output17 = ['4', '7']
output18 = ['2', '4']
output19 = ['1 0', '2 1', '3 1', '4 2', '5 3', '6 5', '7 8', '8 13', '9 21', '10 34', '11 55', '12 89', '13 144',
            '14 233', '15 377']
output20 = ['2']
output21 = ['[0, 1, 2, 3, 4, 5, 6]', '[1, 2, 3, 4, 10, 102, 0, 5, 6]', '[3, 4, 5]', '[0, 1, 4, 9, 16, 25, 36]',
            '[1, 2, 5, 10, 17, 26, 37]']
output22 = ['0']
output23 = ['15']
output24 = ['-1', '-5', '0']
output25 = ['"ollah"']
output26 = ['"emove these char"']
output27 = ['3', '7']
output28 = ['5', '10.105263157894736', '2']
output29 = ['1.2', '0.4']
output30 = ['[[0, 1], [2, [3, 4]]]', '[0, 1]', '2', '3']
output31 = ['"h ll "', '"111"', '"0123456"']
output32 = ['"h a l l o "']
output33 = ['"Rmv ll vwls"']
output34 = ['160']
output35 = ['"20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"']
output36 = ['Fo1r the2 g3ood 4of th5e pe6ople']
output37 = ['["A", "B", "C", "D", "A", "B"]', '[1, 2, 3]']
output38 = ['True', 'True', 'False']
output39 = ['"volcano"']
output40 = ['[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]']
output41 = ['True', 'False', 'False', 'False']
output42 = ['True', 'False']
output43 = ['"8j8mBliB8gimjB8B8jlB"', '"88Bifk8hB8BB8BBBB888chl8BhBfd"']
output44 = ['"apples, pears\ngrapes\nbananas"', '"a\nc\nd"']
output45 = ['21', '581', '2071', '-1']
output46 = ['["e", "ddd", "aa"]']
output47 = ['8', '1', '18']
output48 = ['0', 'h', '"s"', '1']


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.interface = Interface(debug=False, quit_after_exceptions=True, printall=True)

    def test1(self):
        self.assertEqual(self.interface.run(input1, return_out=True), output1)

    def test2(self):
        self.assertEqual(self.interface.run(input2, return_out=True), output2)

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

    def test31(self):
        self.assertEqual(self.interface.run(input31, return_out=True), output31)

    def test32(self):
        self.assertEqual(self.interface.run(input32, return_out=True), output32)

    def test33(self):
        self.assertEqual(self.interface.run(input33, return_out=True), output33)

    def test34(self):
        self.assertEqual(self.interface.run(input34, return_out=True), output34)

    def test35(self):
        self.assertEqual(self.interface.run(input35, return_out=True), output35)

    def test36(self):
        self.assertEqual(self.interface.run(input36, return_out=True), output36)

    def test37(self):
        self.assertEqual(self.interface.run(input37, return_out=True), output37)

    def test38(self):
        self.assertEqual(self.interface.run(input38, return_out=True), output38)

    def test39(self):
        self.assertEqual(self.interface.run(input39, return_out=True), output39)

    def test40(self):
        self.assertEqual(self.interface.run(input40, return_out=True), output40)

    def test41(self):
        self.assertEqual(self.interface.run(input41, return_out=True), output41)

    def test42(self):
        self.assertEqual(self.interface.run(input42, return_out=True), output42)

    def test43(self):
        self.assertEqual(self.interface.run(input43, return_out=True), output43)

    def test44(self):
        self.assertEqual(self.interface.run(input44, return_out=True), output44)

    def test45(self):
        self.assertEqual(self.interface.run(input44, return_out=True), output44)

    def test46(self):
        self.assertEqual(self.interface.run(input46, return_out=True), output46)

    def test47(self):
        self.assertEqual(self.interface.run(input47, return_out=True), output47)

    def test48(self):
        self.assertEqual(self.interface.run(input48, return_out=True), output48)

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
            "midn(1,0,-1)",
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
            "'hallo'.arr",
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
            '"xa".rev;[0,1].rev',
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
            '10.s;type(10.s);"10".n',
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
            '"hallo".nummap',
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
            '"hallo".islower;"Hallo".isupper;"Hallo".iscapitalized',
            return_out=True, ),
            ['True', 'False', 'True'])

    def test_sort(self):
        self.assertEqual(self.interface.run(
            '[1,0,-1].sort',
            return_out=True, ),
            ['[-1, 0, 1]'])

    def test_posof(self):
        self.assertEqual(self.interface.run(
            '"hallo".posof("o")',
            return_out=True, ),
            ['4'])

    def test_combinations_allcombinations_multicombinations_permutations_mostcommon(self):
        self.assertEqual(self.interface.run(
            'x="ha";"hal".combinations(2);x.allcombinations;x.multicombinations;x.permutations;x.mostcommon(1)',
            return_out=True, ),
            ['"ha"', '[["h", "a"], ["h", "l"], ["a", "l"]]', '[[], ["h"], ["a"], ["h", "a"]]',
             '[["h", "h"], ["h", "a"], ["a", "a"]]', '[["h", "a"], ["a", "h"]]', '[["h", 1]]'])

    def test_removeduplicates(self):
        self.assertEqual(self.interface.run(
            '[0,0,1].removeduplicates',
            return_out=True, ),
            ['[0, 1]'])

    def test_range(self):
        self.assertEqual(self.interface.run(
            '1:10:3',
            return_out=True, ),
            ['[1, 4, 7]'])

    def test_deleteat_pop(self):
        self.assertEqual(self.interface.run(
            'x=[0,1,2,3];x.deleteAt(0);x.pop(0)',
            return_out=True, ),
            ['[0, 1, 2, 3]', '1'])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
