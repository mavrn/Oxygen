from Datatypes import String, Bool, Array
from interface import Interface


class Test:
    def __init__(self, name, inp, expected_output):
        self.name = name
        self.input = inp
        self.expected_output = expected_output

    def run(self):
        interface = Interface()
        try:
            actual_output = interface.run(self.input, return_out=True)
        except Exception as e:
            print("An exception occured during the test")
            print(e)
            return 2
        if actual_output == self.expected_output:
            print(f"{self.name} passed.")
            return 1
        else:
            print(f"{self.name} didnt pass.")
            print(f"Expected output: {self.expected_output}")
            print(f"Actual output: {actual_output}")
            return 0


class TestGroup:
    def __init__(self, tests):
        self.tests = tests
        self.test_count = len(self.tests)

    def run_tests(self):
        passed_tests = 0
        failed_tests = []
        exceptions = []
        print(f"Running {self.test_count} tests.")
        for i, test in enumerate(self.tests):
            print(f"Running test {i + 1}/{self.test_count}...")
            test_passed = test.run()
            if test_passed == 1:
                passed_tests += 1
            elif test_passed == 0:
                failed_tests.append(test.name)
            else:
                exceptions.append(test.name)
        print(f"Passed {passed_tests}/{self.test_count} tests.")
        print(f"Failed {len(failed_tests)}/{self.test_count} tests.")
        if len(failed_tests) > 0:
            out = "The following tests didn't pass: "
            for test_name in failed_tests:
                out += f"{test_name}, "
            print(out[:-2])
        print(f"{len(exceptions)}/{self.test_count} tests reached an exception.")
        if len(exceptions) > 0:
            out = "The following tests didn't pass: "
            for test_name in exceptions:
                out += f"{test_name}, "
            print(out[:-2])


t1 = "1 == (0.5 + 2 / 2^2)"
t2 = """fn get_c a b => sqrt(a^2+b^2)
get_c(3,4)
"""
t3 = """fn reverse boolean_value => !boolean_value
reverse(1==1)
"""
t4 = """fn is_in_range a b x => a<x<b
is_in_range(0, 5, 3)
is_in_range(-2, 2, -4)
"""
t5 = """fn divide_by_two x => x/2 if x%2 == 0 else x
12.divide_by_two
13.divide_by_two
"""
t6 = """fn fizz_buzz i => rep i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
10.fizz_buzz
"""
t7 = """fn bin_cof n k => n.factorial / (k.factorial * (n-k).factorial)
fn P p n x => bin_cof(n,x) * p^x * (1-p)^(n-x)
P(0.3, 20, 6)
"""
t8 = """x = 10
fn n a =>
return a == (x /2)<<
5.n
10.n
"""
t9 = """fn x a =>
p(a+1)
p(a+2)
return a-1<<
0.x
"""
t10 = """if False =>
x=0 <<
else =>
x=1 <<
x
"""
t11 = """fn fizz_buzz i => 
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
t12 = """fn x a =>
    return "Yes" if a else "False"
<<
True.x
"""
t13 = """fn x a =>
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
t14 = "6 if False else 5 if False else 4 if False else 3"
t15 = "x=4; x+2; x.sqrt"
t16 = """rep 2 as i =>
    i+1
    i/2
<<
"""
t17 = """if False =>
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
t18 = """
x = 2
y = 2x
"""
t19 = """fn fib n =>
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
t20 = """fn x a =>
    if a == 1 =>
        return 2
    <<
    return x(a-1)
<<
10.x
"""
t21= """x = [0,1,2,3,4,5,6]
[1,2,3,4,10,102].union(x)
[3,4,5,7].intersection(x)
fn y a => a^2
x.apply(y)
x >> x+1
"""
t22 = """fn x =>
return 0 <<
x
"""
t23= """fn sum_of_positive arr =>
return (arr >> 0 if x<0 else x).sum
<<
[0,1,2,3,4,5,-2].sum_of_positive
"""
t24= """fn get_neg num =>
return -abs(num)
<<
1.get_neg
-5.get_neg
0.get_neg
"""
t25= """\"hallo\".rev
"""
t26="""fn rem_chars str =>
res = ""
for i = 1, i<(str.l-1), i++ =>
res+=str[i]
<<
return res
<<
"remove these chars".rem_chars
"""
t27="""fn vowel_ct str =>
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
t28="""2x ? 10
10x - 20/19 ? 100
2y ?= 4
"""
t29="""
~test comment
100% + 20% ~this comment is a comment
2 * 20%
~~~ hi
"""
t30="""
x = [[0,1], [2,[3,4]]]
x[0]
x[1][0]
x[1][1][0]
"""
t31="""
10 >> x/2
"hallo" >> " " if x in "aeiou" else x
"lol" >> 1
"abcdefg" >> i
"""
t32 ="""fn add_spaces str => (str.arr >> x+" ").join
"hallo".add_spaces
"""
t33="""
"Remove all vowels" >> "" if x in "aeiou" else x
"""
t34="""fn x a =>
     odd_nums = a >> del if x%2==0
     a.diff(odd_nums)
     return odd_nums[0] if odd_nums.l == 1 else a[0]
<<
[160, 3, 1719, 19, 11, 13, -21].x
"""
t35="""fn repl str =>
     str >>> "" if not (x in alphabet)
     return str.nummap().join(" ")
<<
"The sunset sets at twelve o' clock.".repl
"""
t36="""fn order str =>
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
t37="""fn uni str =>
    new = [str[0]]
    iter str =>
            if _x != new[-1] and _i >0 =>
                    new+=_x
            <<
    <<
    return new
<<
'AAAABBBCCDAABBB'.uni.p
[1,2,2,3,3].uni.p"""
t38="""fn narc int => 
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
t39="""fn score st => (st.capitalize.nummap >> x.n).sum
fn highes str => 
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
'what time are we climbing up the volcano'.highes"""
t40="""fn spl arr =>
    zeroes = arr.count(0)
    arr >>> del if x == 0
    rep zeroes => arr += 0
    return arr
<<
[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9].spl.p"""


test1 = Test("Test 1", t1, ["True"])
test2 = Test("Test 2", t2, ["5"])
test3 = Test("Test 3", t3, ["False"])
test4 = Test("Test 4", t4, ["True", "False"])
test5 = Test("Test 5", t5, ["6", "13"])
test6 = Test("Test 6", t6, ["FizzBuzz", "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz"])
test7 = Test("Test 7", t7, ["0.19163898275344238"])
test8 = Test("Test 8", t8, ["10", "Warning: Built-in function n has been overridden.", "True", "False"])
test9 = Test("Test 9", t9, ["1", "2", "-1"])
test10 = Test("Test 10", t10, ["1", "1"])
test11 = Test("Test 11", t11, ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz"])
test12 = Test("Test 12", t12, ["Yes"])
test13 = Test("Test 13", t13, ["Negative number", "Positive number", "Greater than 10"])
test14 = Test("Test 14", t14, ["3"])
test15 = Test("Test 15", t15, ["4", "6", "2"])
test16 = Test("Test 16", t16, ["1", "0", "2", "0.5"])
test17 = Test("Test 17", t17, ["4", "7"])
test18 = Test("Test 18", t18, ["2", "4"])
test19 = Test("Test 19", t19, ["1 0", "2 1", "3 1", "4 2", "5 3", "6 5",
                               "7 8", "8 13", "9 21", "10 34", "11 55",
                               "12 89", "13 144", "14 233", "15 377"])
test20 = Test("Test 20", t20, ["2"])
test21 = Test("Test 21", t21, ["[0, 1, 2, 3, 4, 5, 6]", "[1, 2, 3, 4, 10, 102, 0, 5, 6]","[3, 4, 5]","[0, 1, 4, 9, 16, 25, 36]","[1, 2, 5, 10, 17, 26, 37]"])
test22 = Test("Test 22", t22, ["0"])
test23 = Test("Test 23", t23, ["15"])
test24 = Test("Test 24", t24, ["-1", "-5", "0"])
test25 = Test("Test 25", t25, ["ollah"])
test26 = Test("Test 26", t26, ["emove these char"])
test27 = Test("Test 27", t27, ["3", "7"])
test28 = Test("Test 28", t28, ["5", "10.105263157894736", "2"])
test29 = Test("Test 29", t29, ["1.2", "0.4"])
test30 = Test("Test 30", t30, ["[[0, 1], [2, [3, 4]]]", "[0, 1]", "2", "3"])
test31 = Test("Test 31", t31, ["5", "h ll ", "111", "0123456"])
test32 = Test("Test 32", t32, ["h a l l o "])
test33 = Test("Test 33", t33, ["Rmv ll vwls"])
test34 = Test("Test 34", t34, ["160"])
test35 = Test("Test 35", t35, ["20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"])
test36 = Test("Test 36", t36, ["Fo1r the2 g3ood 4of th5e pe6ople"])
test37 = Test("Test 37", t37, ["[A, B, C, D, A, B]", "[1, 2, 3]"])
test38 = Test("Test 38", t38, ["True", "True", "False"])
test39 = Test("Test 39", t39, ["volcano"])
test40 = Test("Test 40", t40, ["[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"])

tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15,
         test16, test17, test18, test19, test20, test21,test22, test23, test24, test25, test26, test27, test28, test29, test30,
         test31, test32, test33, test34, test35, test36, test37, test38, test39, test40]

test_group = TestGroup(tests)