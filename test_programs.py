test1 = "1 == (0.5 + 2 / 2^2)"
test2 = """fn get_c a b => sqrt(a^2+b^2)
get_c(3,4)
"""
test3 = """fn reverse boolean_value => !boolean_value
reverse(1==1)
"""
test4 = """fn is_in_range a b x => a<x<b
is_in_range(0, 5, 3)
is_in_range(-2, 2, -4)
"""
test5 = """fn divide_by_two x => x/2 if x%2 == 0 else x
divide_by_two.12
divide_by_two.13
"""
test6 = """fn fizz_buzz i => rep i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
fizz_buzz.10
"""
test7 = """fn bin_cof n k => factorial.n / (factorial.k * factorial(n-k))
fn P p n x => bin_cof(n,x) * p^x * (1-p)^(n-x)
P(0.3, 20, 6)
"""