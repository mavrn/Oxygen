from Datatypes import String, Bool
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
divide_by_two.12
divide_by_two.13
"""
t6 = """fn fizz_buzz i => rep i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
fizz_buzz.10
"""
t7 = """fn bin_cof n k => factorial.n / (factorial.k * factorial(n-k))
fn P p n x => bin_cof(n,x) * p^x * (1-p)^(n-x)
P(0.3, 20, 6)
"""
t8 = """x = 10
fn n a =>
return a == (x /2)<<
n.5
n.10
"""
t9 = """fn x a =>
print(a+1)
print(a+2)
return a-1<<
x.0
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
                     print("FizzBuzz")
             <<
             or x%5 == 0 =>
                     print("Buzz")
             <<
             or x%3 == 0 =>
                     print("Fizz")
             <<
             else =>
                     print(x)
             <<
     <<
<<
fizz_buzz.10
"""
t12 = """fn x a =>
    return "Yes" if a else "False"
<<
x.True
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
x.-1
x.2
x.11
"""
t14 = "6 if False else 5 if False else 4 if False else 3"
t15 = "x=4; x+2; sqrt.x"
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
    print(i, fib.i)
<<
"""
t20 = """fn x a =>
    if a == 1 =>
        return 2
    <<
    return x(a-1)
<<
x.10
"""

test1 = Test("Test 1", t1, [Bool(True)])
test2 = Test("Test 2", t2, [5.0])
test3 = Test("Test 3", t3, [Bool(False)])
test4 = Test("Test 4", t4, [Bool(True), Bool(False)])
test5 = Test("Test 5", t5, [6.0, 13.0])
test6 = Test("Test 6", t6, [String("FizzBuzz"), 1.0, 2.0, String("Fizz"), 4.0, String("Buzz"), String("Fizz"), 7.0,
                            8.0, String("Fizz")])
test7 = Test("Test 7", t7, [0.19163898275344238])
test8 = Test("Test 8", t8, [10.0, Bool(True), Bool(False)])
test9 = Test("Test 9", t9, [String(1), String(2), -1.0])
test10 = Test("Test 10", t10, [1.0, 1.0])
test11 = Test("Test 11", t11, [String(1), String(2), String("Fizz"), String(4), String("Buzz"), String("Fizz"),
                               String(7), String(8), String("Fizz"), String("Buzz")])
test12 = Test("Test 12", t12, [String("Yes")])
test13 = Test("Test 13", t13, [String("Negative number"), String("Positive number"), String("Greater than 10")])
test14 = Test("Test 14", t14, [3.0])
test15 = Test("Test 15", t15, [4.0, 6.0, 2.0])
test16 = Test("Test 16", t16, [1.0, 0.0, 2.0, 0.5])
test17 = Test("Test 17", t17, [4.0, 7.0])
test18 = Test("Test 18", t18, [2.0, 4.0])
test19 = Test("Test 19", t19, [String("1 0"), String("2 1"), String("3 1"), String("4 2"), String("5 3"), String("6 5"),
                               String("7 8"), String("8 13"), String("9 21"), String("10 34"), String("11 55"),
                               String("12 89"), String("13 144"), String("14 233"), String("15 377")])
test20 = Test("Test 20", t20, [2.0])

tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15,
         test16, test17, test18, test19, test20]
test_group = TestGroup(tests)
