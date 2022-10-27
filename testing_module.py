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
        else:
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
#x=[0,1]
#fn y a => a+1
#x.apply(y)
t22 = """fn x =>
return 0
<<
x
"""
t23= """fn sum_of_positive arr =>
return (arr >> 0 if x<0 else x).sum
<<
[0,1,2,3,4,5,-2].sum_of_positive
"""
t24= """fn get_neg num =>
return -num.abs
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
vowel_ct."hallo test"
vowel_ct."haaaloooo"
"""

test1 = Test("Test 1", t1, ["True"])
test2 = Test("Test 2", t2, ["5"])
test3 = Test("Test 3", t3, ["False"])
test4 = Test("Test 4", t4, ["True", "False"])
test5 = Test("Test 5", t5, ["6", "13"])
test6 = Test("Test 6", t6, ["FizzBuzz", "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz"])
test7 = Test("Test 7", t7, ["0.19163898275344238"])
test8 = Test("Test 8", t8, ["10", "True", "False"])
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
test22 = Test("Test22", t22, ["0"])

tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15,
         test16, test17, test18, test19, test20, test21,test22]

test_group = TestGroup(tests)