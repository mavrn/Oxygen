import unittest
from interface import Interface
import timeit


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.interface = Interface(debug=False, quit_after_exceptions=True, printall=True, autoid=True)

    def test_math(self):
        self.assertEqual(self.interface.run(
            "100 sqrt factorial",
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
            "'Hallo' leet",
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
            'fn x a => a+10;[0,1,2] apply: x',
            return_out=True, ),
            ['[10, 11, 12]'])

    def test_append(self):
        self.assertEqual(self.interface.run(
            'x = [0] append: 1;x+2;x+=3;x',
            return_out=True, ),
            ['[0, 1]', '[0, 1, 2]', '[0, 1, 3]', '[0, 1, 3]'])

    def test_union(self):
        self.assertEqual(self.interface.run(
            '[0,1,2] union([2,3,4])',
            return_out=True, ),
            ['[0, 1, 2, 3, 4]'])

    def test_intersection(self):
        self.assertEqual(self.interface.run(
            '[0,1,2] intersection([1,2,3])',
            return_out=True, ),
            ['[1, 2]'])

    def test_join(self):
        self.assertEqual(self.interface.run(
            '["h", "a"] join(" ");["h", "o"] join',
            return_out=True, ),
            ['"h a"', '"ho"'])

    def test_rev(self):
        self.assertEqual(self.interface.run(
            '"xa" reverse;[0,1] reverse',
            return_out=True, ),
            ['"ax"', '[1, 0]'])

    def test_sum(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3] sum',
            return_out=True, ),
            ['6'])

    def test_slice(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3,4] slice(1,3);"hallo"[0..5..2]',
            return_out=True, ),
            ['[1, 2]', '"hlo"'])

    def test_minmax(self):
        self.assertEqual(self.interface.run(
            '[0,2,3,4,5,100,2,101,-3] min;[0,2,3,4,5,100,2,101,-3] max',
            return_out=True, ),
            ['-3', '101'])

    def test_conv(self):
        self.assertEqual(self.interface.run(
            '10 asString;type(10 asString);"10" asNum',
            return_out=True, ),
            ['"10"', '"String"', '10'])

    def test_split(self):
        self.assertEqual(self.interface.run(
            '"h a" split',
            return_out=True, ),
            ['["h", "a"]'])

    def test_difference(self):
        self.assertEqual(self.interface.run(
            'difference([0,1,2,3], [0,1,2])',
            return_out=True, ),
            ['[3]'])

    def test_count(self):
        self.assertEqual(self.interface.run(
            '[0,0,1,2] count(0);"hallo" count("l", "h")',
            return_out=True, ),
            ['2', '3'])

    def test_nummap(self):
        self.assertEqual(self.interface.run(
            '"hallo" numMap',
            return_out=True, ),
            ['[8, 1, 12, 12, 15]'])

    def test_upper_lower_capitalize(self):
        self.assertEqual(self.interface.run(
            '"hAlLo" lower;"halLo" upper;"hALLO" capitalize',
            return_out=True, ),
            ['"hallo"', '"HALLO"', '"Hallo"'])

    def test_strip(self):
        self.assertEqual(self.interface.run(
            '"h f    " strip;"jk" strip("k")',
            return_out=True, ),
            ['"h f"', '"j"'])

    def test_replace(self):
        self.assertEqual(self.interface.run(
            '[0,1] replace(0,2)',
            return_out=True, ),
            ['[2, 1]'])

    def test_isupper_islower_iscapitalized(self):
        self.assertEqual(self.interface.run(
            '"hallo" isLower;"Hallo" isUpper;"Hallo" isCapitalized',
            return_out=True, ),
            ['True', 'False', 'True'])

    def test_sort(self):
        self.assertEqual(self.interface.run(
            '[1,0,-1] sort',
            return_out=True, ),
            ['[-1, 0, 1]'])

    def test_posof(self):
        self.assertEqual(self.interface.run(
            '"hallo" find("o")',
            return_out=True, ),
            ['4'])

    def test_combinations_allcombinations_multicombinations_permutations_mostcommon(self):
        self.assertEqual(self.interface.run(
            'x="ha";"hal" combinations(2);x allCombinations;x multiCombinations;x permutations;x mostCommon(1)',
            return_out=True, ),
            ['"ha"', '[["h", "a"], ["h", "l"], ["a", "l"]]', '[[], ["h"], ["a"], ["h", "a"]]',
             '[["h", "h"], ["h", "a"], ["a", "a"]]', '[["h", "a"], ["a", "h"]]', '[["h", 1]]'])

    def test_removeduplicates(self):
        self.assertEqual(self.interface.run(
            '[0,0,1] removeDuplicates',
            return_out=True, ),
            ['[0, 1]'])

    def test_range(self):
        self.assertEqual(self.interface.run(
            '1..10..3',
            return_out=True, ),
            ['[1, 4, 7]'])

    def test_slices(self):
        self.assertEqual(self.interface.run(
            '[0,1,2,3,4,5][1..-1..2]',
            return_out=True, ),
            ['[1, 3]'])

    def test_iter(self):
        self.assertEqual(self.interface.run(
            'iterate 1..6..3 => iterelem',
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

    def test_dicts(self):
        self.assertEqual(self.interface.run(
            'x= {0 > "0", True > "1"};x[0];x[True];x hasKey: 0;x hasValue: "1"',
            return_out=True, ),
            ['{0 > "0", True > "1"}','"0"', '"1"', 'True', 'True'])

    def test_kwargs(self):
        input = """fn x a b c => a/b + c
        x(1, c=2, b=4)
        x(c=0, b=2, a=4)
        """
        self.assertEqual(self.interface.run(
            input,
            return_out=True, ),
            ['2.25', '2'])

    def test_hashstrings(self):
        input = """x = ["t", "s", "t"]
        "#x join#1"
        """
        self.assertEqual(self.interface.run(
            input,
            return_out=True, ),
            ['["t", "s", "t"]', '"tst1"'])

    #def test_change(self):
    #    self.assertEqual(self.interface.run(
    #        """
    #        change("let", "\#")
    #        #x 9
    #        x
    #        """,
    #        return_out=True, ),
    #        ['9', '9'])

    def test_repr(self):
        self.assertEqual(self.interface.run(
            '"hallo" repr out',
            return_out=True, ),
            ['"hallo"'])
    
    def test_all_some_none_every(self):
        input = """
        [True, True] all
        [False, False] some
        [True, True, False] none
        [2,8,6,2,10] every: afn a => a%2==0
        """
        self.assertEqual(self.interface.run(
            input,
            return_out=True, ),
            ['True', 'False', 'False', 'True'])

    def test_fill(self):
        self.assertEqual(self.interface.run(
            '0 fill: 3',
            return_out=True, ),
            ['[0, 0, 0]'])
    
    def test_arrof(self):
        self.assertEqual(self.interface.run(
            'arrOf: 0,0,1',
            return_out=True, ),
            ['[0, 0, 1]'])
            
    def test_foreach(self):
        self.assertEqual(self.interface.run(
            '[-1,1,2] foreach: abs',
            return_out=True, ),
            ['1', '1', '2'])

    def test_select_detect(self):
        self.assertEqual(self.interface.run(
            """[0,1,2,3,4] select: afn a => a%2==0
                    [0,-1, -2, 0] detect: afn a => a<0""",
            return_out=True),
            ['[0, 2, 4]', '-1'])
    
    def test_intelligent_iteration(self):
        self.assertEqual(self.interface.run(
            """dictionaries = [0,1,2]
            dictionaries -> dictionary
            {0 > 1, 2 > 0} keys -> key
            """,
            return_out=True, ),
            ['[0, 1, 2]', '0', '1', '2', '0', '2'])

    def test_getscope_getfields(self):
        input_getscope_getfields = """fn one => 
                                    x=0
                                    out(getFields(getScope()))
                                    out(getScope())
                                    return x
                                <<

                                fn plus_two =>
                                    out(getScope())
                                    repeat 1 =>
                                        out(getScope())
                                    <<
                                    return one() + 2
                                <<

                                out(getScope())
                                plus_two()"""
        self.assertEqual(self.interface.run(
            input_getscope_getfields,
            return_out=True),
            ['global', 'global >> plus_two', 'global >> plus_two > IterLoop', '{"x" > 0}', 'global >> plus_two >> one', '2'])

    def testOperations(self):
        self.assertEqual(self.interface.run("1 equals (0.5 + 2 / 2**2)", return_out=True), ['True'])

    def testPythagoras(self):
        input = """fn get_c a b => (a**2+b**2) sqrt
                get_c(3,4)
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['5'])

    def testNegateBool(self):
        input = """fn negate boolean_value => not boolean_value
                negate(1==1)
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['False'])

    def testIsInRange(self):
        input = """fn is_in_range a b x => a<x<b
                is_in_range(0, 5, 3)
                is_in_range(-2, 2, -4)
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'False'])

    def testDivideByTwo(self):
        input = """fn divide_by_two x => x/2 if x%2 == 0 else x
                12 divide_by_two
                13 divide_by_two
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['6', '13'])

    def testFizzBuzzOneLine(self):
        input = """fn fizz_buzz i => repeat i as c => "FizzBuzz" if c % 3 == 0 and c % 5 == 0 else "Fizz" if c % 3 == 0 else "Buzz" if c % 5 == 0 else c
                10 fizz_buzz"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"FizzBuzz"', '1', '2', '"Fizz"', '4', '"Buzz"', '"Fizz"', '7', '8', '"Fizz"'])

    def testBinCof(self):
        input = """fn bin_cof n k => n factorial / (k factorial * (n-k) factorial)
                fn P p n x => bin_cof(n,x) * p**x * (1-p)**(n-x)
                P(0.3, 20, 6)
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['0.19163898275344238'])

    def testGlobalVarScope(self):
        input = """let x 10
                fn n a =>
                <- a == (x /2)<<
                5 n
                10 n
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['10', 'True', 'False'])

    def testFuncPrint(self):
        input = """fn x a =>
                out(a+1)
                out(a+2)
                <- a-1<<
                0 x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['1', '2', '-1'])

    def testIfScope(self):
        input = """x=-1
                if False =>
                x=0 <<
                else =>
                x=1 <<
                x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['-1', '1', '1'])

    def testFizzBuzz(self):
        input = """fn fizz_buzz i => 
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
        self.assertEqual(self.interface.run(input, return_out=True), ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz'])

    def testOneLineReturn(self):
        input = """fn x a =>
                        <- "Yes" if a else "False"
                    <<
                    True x
                    """
        self.assertEqual(self.interface.run(input, return_out=True), ['"Yes"'])

    def testNegativeNumFunc(self):
        input = """fn x a =>
                    if a > 10 => <- "Greater than 10"
                    or a >= 0 => <- "Positive number"
                    else => <- "Negative number"
                <<
                -1 x
                2 x
                11 x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"Negative number"', '"Positive number"', '"Greater than 10"'])

    def testOneLineIfExtreme(self):
        input = "6 if False else 5 if False else 4 if False else 3"
        self.assertEqual(self.interface.run(input, return_out=True), ['3'])

    def testStatementSeperators(self):
        input = "x=4; x+2; x sqrt"
        self.assertEqual(self.interface.run(input, return_out=True), ['4', '6', '2'])

    def testRep(self):
        input = """repeat 2 as i =>
                    i+1
                    i/2
                <<  
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['1', '0', '2', '0.5'])

    def testMultipleIf(self):
        input = """if False =>
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
        self.assertEqual(self.interface.run(input, return_out=True), ['4', '7'])

    def testAutoMult(self):
        input = """
                x = 2
                y = 2x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['2', '4'])

    def testRecursionFib(self):
        input = """fn fib n =>
            if n == 1 => <- 0
            or n == 2 => <- 1
            else => <- fib(n-1) + fib(n-2)
        <<
        for i=1, i<=15, i++ =>
            out(i, i fib)
        <<
        """
        self.assertEqual(self.interface.run(input, return_out=True), ['1 0', '2 1', '3 1', '4 2', '5 3', '6 5', '7 8', '8 13', '9 21', '10 34', '11 55', '12 89', '13 144', '14 233', '15 377'])

    def testRecursiveFunc(self):
        input = """fn x a =>
                    if a == 1 =>
                        <- 2
                    <<
                    <- x(a-1)
                <<
                10 x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['2'])

    def testArrOperations(self):
        input = """x = [0,1,2,3,4,5,6]
                [1,2,3,4,10,102] union(x)
                [3,4,5,7] intersection(x)
                fn y a => a**2
                x apply(y)
                x >> x+1
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['[0, 1, 2, 3, 4, 5, 6]', '[1, 2, 3, 4, 10, 102, 0, 5, 6]', '[3, 4, 5]', '[0, 1, 4, 9, 16, 25, 36]','[1, 2, 5, 10, 17, 26, 37]'])

    def testEmptyCall(self):
        input = """fn x =>
                return 0 <<
                x()
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['0'])

    def testRevString(self):
        input = "\"hallo\" reverse"
        self.assertEqual(self.interface.run(input, return_out=True), ['"ollah"'])

    def testLinEqSolving(self):
        input = """2*x ? 10
                10*x - 20/19 ? 100
                2*y ?= 4
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['5', '10.105263157894736', '2'])

    def testComments(self):
        input = """
                ~test comment
                1+0.2 ~this comment is a comment
                0.8/2
                ~~~ hi
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['1.2', '0.4'])

    def testArrBracketcalls(self):
        input = """
                x = [[0,1], [2,[3,4]]]
                x[0]
                x[1][0]
                x[1][1][0]
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['[[0, 1], [2, [3, 4]]]', '[0, 1]', '2', '3'])

    def testStringApply(self):
        input = """
                "hallo" >> " " if char in "aeiou" else char
                "lol" >> 1
                "abcdefg" >> i
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"h ll "', '"111"', '"0123456"'])

    def testAddSpaces(self):
        input = """fn add_spaces string => (string asArr >> char+" ") join
                "hallo" add_spaces
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"h a l l o "'])

    def testNarc(self):
        input = """fn narc int => 
                    spl = int asString asArr >> x asNum
                    range = ([0]*10) >> i+1
                    iterate range as i=>
                        sum = 0
                        iterate spl as x=>
                            sum += x**i
                        <<
                        if sum == int => return True
                    <<
                    <- False
                <<
                153 narc out
                371 narc out
                4887 narc out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'True', 'False'])

    def testPrintOrder(self):
        input = """y=0
                fn x a =>
                    y+=1
                    "h" out
                    <- "s"
                <<
                1 x
                y
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['0', 'h', '"s"', '1'])

    def testDictMatcher(self):
        input = """fn func_calc str =>
                    matcher = {"one" > 1, "two" > 2, "three" > 3, "four" > 4, "five" > 5, "six" > 6, "seven" > 7, "eight" > 8, "nine" > 9}
                    operands = str strip: ")" slice: 0,-1 split: "(" 
                    operator = operands middle
                    a = matcher[operands first]; b = matcher[operands last]
                    if operator equals "plus" => <- a+b
                    or operator equals "minus" => <- a-b
                    or operator equals "times" => <- a*b
                    else => <- a/b
                <<
                "seven(times(five()))" func_calc out
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['35'])

    def test_cw8_sum_of_positive(self):
        #https://www.codewars.com/kata/5715eaedb436cf5606000381
        input = """fn sum_of_positive arr => (arr >> 0 if x<0 else x) sum
                    [0,1,2,3,4,5,-2] sum_of_positive
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['15'])

    def test_cw8_opposite_number(self):
        #https://www.codewars.com/kata/56dec885c54a926dcd001095
        input = """fn get_neg num => -abs(num)
                1 get_neg
                -5 get_neg
                0 get_neg
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['-1', '-5', '0'])

    def test_cw8_remove_first_and_last_letter(self):
        #https://www.codewars.com/kata/56bc28ad5bdaeb48760009b0
        input = """fn rem_chars str =>
                let res ""
                for i = 1, i<(str size -1), i++ => res+=str at: i
                <- res<<
                "remove these chars" rem_chars
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"emove these char"'])

    def test_cw7_vowel_count(self):
        #https://www.codewars.com/kata/54ff3102c1bad923760001f3
        input = """fn vowel_ct str =>
                let ct 0
                for c in str => if c in "aeiou" => ct++
                return ct
                <<
                "hallo test" vowel_ct
                "haaaloooo" vowel_ct
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['3', '7'])

    def test_cw7_disemvowel_trolls(self):
        #https://www.codewars.com/kata/52fba66badcd10859f00097e
        input = """
                "Remove all vowels" >> "" if char in "aeiou" else char
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"Rmv ll vwls"'])

    def test_cw6_find_the_parity_outlier(self):
        #https://www.codewars.com/kata/5526fc09a1bbd946250002dc
        input = """fn x nums =>
                    odd_nums = nums >> delete if num%2 equals 0
                    nums difference: odd_nums
                    return odd_nums at: 0 if odd_nums size equals 1 else nums at: 0
                <<
                [160, 3, 1719, 19, 11, 13, -21] x
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['160'])

    def test_cw6_replace_with_alphabet_position(self):
        #https://www.codewars.com/kata/546f922b54af40e1e90001da
        input = """fn repl str =>
                    str >>> delete unless char in ALPHABET
                    <- str numMap join: " "
                <<
                "The sunset sets at twelve o' clock." repl
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"'])

    def test_cw6_your_order_please(self):
        #https://www.codewars.com/kata/55c45be3b2079eccff00010f
        input = """fn order str =>
                    let words str split
                    let new [""] * words size
                    words ->
                        let num 0
                        for char in word => if char in NUMBERS => num = char asNum
                        new[num-1] = word
                    <<
                    return new join: " "
                <<
                "4of Fo1r pe6ople g3ood th5e the2" order out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['Fo1r the2 g3ood 4of th5e pe6ople'])

    def test_cw6_unique_in_order(self):
        #https://www.codewars.com/kata/54e6533c92449cc251001667
        input = """fn uni str =>
                    let new [str at: 0]
                    str -> if iterelem != new[-1] and itercounter >0 => new+=iterelem
                    <- new
                <<
                "AAAABBBCCDAABBB" uni out
                [1,2,2,3,3] uni out
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['["A", "B", "C", "D", "A", "B"]', '[1, 2, 3]'])

    def test_cw6_highest_scoring_word(self):
        #https://www.codewars.com/kata/57eb8fcdf670e99d9b000272/
        input = """fn score string => (string capitalize numMap >> char asNum) sum
                fn highest str => 
                    let h ""
                    let hs 0
                    str split ->
                        let sc word score
                        if sc greater hs =>
                            hs = sc
                            h = word
                        <<
                    <<
                    return h
                <<
                'what time are we climbing up the volcano' highest"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"volcano"'])

    def test_cw5_moving_zeroes_to_the_end(self):
        #https://www.codewars.com/kata/52597aa56021e91c93000cb0
        input = """fn countzeroes nums =>
                zeroes = nums count: 0
                nums >>> delete if num equals 0
                repeat zeroes => nums += 0
                return nums
            <<
            [9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9] countzeroes out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'])

    def test_cw5_valid_perntheses(self):
        #https://www.codewars.com/kata/52774a314c2333f0a7000688
        input = """fn val str =>
                    let open 0
                    iterate str as i, char =>
                        if char == "(" => open +=1
                        or char == ")" =>
                            if open <= 0 => return False
                            else => open -= 1
                        <<
                    <<
                    return open == 0
                <<
                "(())((()())())" val
                "(" val
                ")(()))" val
                ")))(((" val
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'False', 'False', 'False'])

    def test_cw4_sudoku_solution_validator(self):
        #https://www.codewars.com/kata/529bf0e9bdf7657179000008
        input = """fn uniquecheck arr =>
                    arr sort
                    for i=1, i<arr size, i++ =>
                        if not i equals arr[i-1] => return False
                    <<
                    return True
                <<
                fn check sudoku =>
                    column = [0]*9
                    grid = [0]*9
                    count = 0

                    for row in sudoku =>
                        unless row clone uniquecheck => return False
                    <<
                    for i=0, i<9, i++ =>
                        for x=0, x<9, x++ =>
                            column[x] = sudoku[x][i]
                        <<
                        unless column clone uniquecheck => return False
                    <<
                    for i=0, i<9, i+=3 =>
                        for x=0, x<9, x+=3 =>
                            for o=0, o<3, o++ =>
                                for k=0, k<3, k++ =>
                                    grid[count] = sudoku[i+k][x+o]
                                    count++
                                <<
                            <<
                            unless grid clone uniquecheck => return Falseprint
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
                [3, 4, 5, 2, 8, 6, 1, 7, 9]] check
                [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 0, 3, 4, 8],
                [1, 0, 0, 3, 4, 2, 5, 6, 0],
                [8, 5, 9, 7, 6, 1, 0, 2, 0],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 0, 1, 5, 3, 7, 2, 1, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 0, 0, 4, 8, 1, 1, 7, 9]] check
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'False'])

    def test_cw8_remove_string_spaces(self):
        #https://www.codewars.com/kata/57eae20f5500ad98e50002c5
        input = """fn remspace str => str >> delete if char == " "
                "8 j 8   mBliB8g  imjB8B8  jl  B" remspace
                "8 8 Bi fk8h B 8 BB8B B B  B888 c hl8 BhB fd" remspace
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"8j8mBliB8gimjB8B8jlB"', '"88Bifk8hB8BB8BBBB888chl8BhBfd"'])

    def test_cw4_strip_comments(self):
        #https://www.codewars.com/kata/51c8e37cee245da6b40000bd
        input = """
                fn stripcomments str delimiters =>
                    lines = str split: "\\n"
                    newlines = []
                    lines ->
                        newline = ""
                        iterate line as char =>
                            if char in delimiters => break
                            else => newline += char
                        <<
                        newlines += newline strip
                    <<
                    return newlines join: "\\n"
                <<
                stripcomments("apples, pears \# and bananas\\ngrapes\\nbananas !apples", ["\#", "!"])
                stripcomments("a \#b\\nc\\nd $e f g", ["\#", "$"])"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"apples, pears\\ngrapes\\nbananas"', '"a\\nc\\nd"'])

    def test_cw4_next_bigger_number_with_same_digits(self):
        #https://www.codewars.com/kata/55983863da40caa2c900004e
        input = """
                fn nextbigger num =>
                    allnums = (num asString permutations >> permutation join asNum) sort
                    return -1 if allnums find: num equals (allnums size-1) else allnums[allnums find: num +1]
                <<
                12 nextbigger
                518 nextbigger
                2017 nextbigger
                9 nextbigger"""
        self.assertEqual(self.interface.run(input, return_out=True), ['21', '581', '2071', '-1'])

    def test_cw4_most_frequently_used_words_in_text(self):
        #https://www.codewars.com/kata/51e056fe544cf36c410000fb
        input17 = """fn wordcount text =>
                    arr = split(lower(text >> " " unless char in ALPHABET)) 
                    return arr mostCommon >> x at: 0
                <<
                "DDD e e e e ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e" wordcount out
                """
        self.assertEqual(self.interface.run(input17, return_out=True), ['["e", "ddd", "aa"]'])

    def test_cw4_multiply_to_n(self):
        #https://www.codewars.com/kata/5f1891d30970800010626843
        input = """fn multpossibilities n k =>
                    let results []
                    arr = [0]*n >> i+1
                    combs = arr multiCombinations: k
                    combs ->
                        res = 1
                        iterate comb as num => res *= num
                        if res equals n =>
                            iterate comb permutations as perm =>
                                unless perm in results =>
                                    results += perm
                                <<
                            <<
                        <<
                    <<
                    return results size
                <<
                multpossibilities(24,2) out
                multpossibilities(100,1) out
                multpossibilities(20,3) out
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['8', '1', '18'])

    def test_cw4_nesting_structure_comparison(self):
        #https://www.codewars.com/kata/520446778469526ec0000001
        input = """
                fn same_structure_as original other =>
                    if original type != other type != "Array" or original size != other size=>
                        return False<<
                    repeat original size as i =>
                        if type(original[i]) == "Array" and not same_structure_as(original[i], other[i])=>
                            return False<<
                    <<
                    return True
                <<
                same_structure_as([ 1, 1, 1 ], [ 2, 2, 2 ]) out
                same_structure_as([ 1, [ 1, 1 ] ], [ 2, [ 2, 2 ] ] ) out
                same_structure_as([ 1, [ 1, 1 ] ], [ [ 2, 2 ], 2 ] ) out
                same_structure_as([ 1, [ 1, 1 ] ], [ [ 2 ], 2 ] ) out
                same_structure_as([ [ [ ], [ ] ] ], [ [ [ ], [ ] ] ] ) out
                same_structure_as([ [ [ ], [ ] ] ], [ [ 1, 1 ] ] ) out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'True', 'False', 'False', 'True', 'False'])

    def test_cw6_stop_spinning_my_words(self):
        #https://www.codewars.com/kata/5264d2b162488dc400000001
        input = """fn rev_5 str =>
                    return (str split >> word reverse if word size >= 5) join: " "
                <<
                "Hey fellow warriors" rev_5
                "This is a test" rev_5
                "This is another test" rev_5
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"Hey wollef sroirraw"', '"This is a test"','"This is rehtona test"'])

    def test_cw6_digital_root(self):
        #https://www.codewars.com/kata/541c8630095125aba6000c00
        input = """fn sum_of_digits num => sum(num asString asArr >> x asNum)
                16 sum_of_digits out
                493193 sum_of_digits out
                fn root_sum num => 
                    let res num sum_of_digits
                    return res if res asString size == 1 else res root_sum
                <<
                493193 root_sum
                132189 root_sum
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['7', '29', '2', '6'])

    def test_cw6_counting_duplicates(self):
        #https://www.codewars.com/kata/54bf1c2cd5b56cc47f0007a1
        input = """fn duplicates string =>
                    let dup_sum 0
                    string ->
                        if string count: char > 1 =>
                            string removeAll: char
                            dup_sum++
                        <<
                    <<
                    return dup_sum
                <<
                "Indivisibilities" duplicates
                "abcde" duplicates
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['2', '0'])

    def test_cw6_persistent_bugger(self):
        #https://www.codewars.com/kata/55bf01e5a717a0d57e0000ec
        input = """fn persistent_bugger num =>
                    let ct 0
                    while num asString size > 1 =>
                        new = 1
                        iterate num asString asArr as x => new *= x asNum
                        num = new
                        ct++
                    <<
                    return ct
                <<
                39 persistent_bugger
                999 persistent_bugger
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['3', '4'])

    def test_cw6_convert_string_to_camel_case(self):
        #https://www.codewars.com/kata/517abf86da9663f1d2000003
        input = """fn camel_case str => 
                    let a str split("_", "-")
                    let res a[0]
                    iterate a[1..a size] as x =>
                        res += x capitalize<<
                    return res
                <<
                "the-stealth-warrior" camel_case
                "The_Stealth_Warrior" camel_case
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"theStealthWarrior"', '"TheStealthWarrior"'])

    def test_cw6_find_unique_number(self):
        #https://www.codewars.com/kata/585d7d5adb20cf33cb000235
        input = """fn unique_number array =>
                    array ->
                        if array count: iterelem == 1 => <- iterelem
                    <<
                <<
                [ 1, 1, 1, 2, 1, 1 ] unique_number out
                [ 0, 0, 0.55, 0, 0 ] unique_number out
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['2', '0.55'])

    def test_cw3_battleship_field_validator(self):
        #https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7
        input = """fn xy array x y =>
                    return 0 if (x<0 or x>=array[0] size or y<0 or y>=array size) else array[y][x]
                <<

                fn field_validator f =>
                    for y=0,y<f size,y++ =>
                        for x=0,x<f[y] size,x++ =>
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
                    for y=0, y<f size, y++ =>
                        for x=0, x<f[y] size, x++ =>
                            if (xy(f, x, y) == 1) =>
                                len = 1
                                while (xy(f, ++x, y) == 1) => len++
                                if len > 4 => return False
                                ship_counts[len]--
                            <<
                        <<
                    <<
                    for x=0, x<f[0] size, x++ =>
                        for y=0, y<f size, y++ =>
                            if (xy(f, x, y) == -1) =>
                                len = 1
                                while (xy(f, x, ++y) == -1) => len++
                                if len > 4 => return False
                                ship_counts[len]--
                            <<
                        <<
                    <<
                    ship_counts -> if ship_count != 0 => return False
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
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] field_validator out
                [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] field_validator out
                [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]] field_validator out
                """
        self.assertEqual(self.interface.run(input, return_out=True), ["True", "False", "True"])

    def test_cw3_make_a_spiral(self):
        #https://www.codewars.com/kata/534e01fbbb17187c7e0000c6
        input = """fn spiralize size =>
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
                7 spiralize
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['[[1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]'])

    def test_cw5_pick_peaks(self):
        #https://www.codewars.com/kata/5279f6fe5ab7f447890006a7
        input = """fn pick_peaks array =>
                    result = {"pos" > [], "peaks" > []}
                    pos = 0
                    iterate 1..(array size -1) as i =>
                        if array[i] != array[pos] => pos = i
                        if pos and array[pos-1] < array[pos] > array[i+1] =>
                            result["pos"] += pos
                            result["peaks"] += array[pos]
                        <<
                    <<
                    <- result
                <<
                [3, 2, 3, 6, 4, 1, 2, 3, 2, 1, 2, 3] pick_peaks
                [1, 2, 2, 2, 1] pick_peaks
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['{"pos" > [3, 7], "peaks" > [6, 3]}','{"pos" > [1], "peaks" > [2]}'])

    def test_cw4_range_extraction(self):
        #https://www.codewars.com/kata/51ba717bb08c1cd60f00002f
        input = """fn range_extraction a =>
                    let result ""
                    let tmp []
                    iterate a as e =>
                        unless tmp and not abs(e-tmp[-1]) equals 1 => tmp += e
                        else =>
                            if tmp size >= 3 =>
                                result += tmp[0] asString + "-" + tmp[-1] asString + ","
                            <<
                            else =>
                                iterate tmp as t =>
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
                        iterate tmp as t =>
                            result += t asString + ","
                        <<
                    <<
                    return result [0..-1]
                <<

                [-10, -9, -8, -6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20] range_extraction
                """
        self.assertEqual(self.interface.run(input, return_out=True), ['"-10--8,-6,-3-1,3-5,7-11,14,15,17-20"'])

    def test_cw4_human_readable_duration_format(self):
        #https://www.codewars.com/kata/52742f58faf5485cae000b9a
        input = """fn filledvalues values =>
                    filled = 0
                    values ->
                        if value => filled++
                    <<
                    return filled
                <<

                fn format_duration seconds =>
                    if seconds == 0 => return "now"
                    timeNames = ["year", "day", "hour", "minute", "second"]
                    timeValues = [0]*5
                    timeValues[0] = seconds//31536000
                    seconds-=timeValues[0]* 31536000
                    timeValues[1] = seconds//86400
                    seconds-= timeValues[1]*86400
                    timeValues[2] = seconds//3600
                    seconds-= timeValues[2]*3600
                    timeValues[3] = seconds//60
                    seconds-= timeValues[3]*60
                    timeValues[4] = seconds

                    filled = filledvalues: timeValues
                    res = ""
                    for i=0,i<5,i++ =>
                        if timeValues[i] != 0 =>
                            res += timeValues[i] asString + " " + timeNames[i]
                            if timeValues[i] > 1 => res += "s"
                            filled--
                            if filled > 1 => res += ", "
                            if filled == 1 => res += " and "
                        <<
                    <<
                    return res
                <<
                62 format_duration
                3662 format_duration
                33243586 format_duration"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"1 minute and 2 seconds"', '"1 hour, 1 minute and 2 seconds"', '"1 year, 19 days, 18 hours, 19 minutes and 46 seconds"'])

    def test_cw3_sudoku_solver(self):
        self.interface.printall = False
        #https://www.codewars.com/kata/5296bc77afba8baa690002d7
        input="""REF = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                SIZE = 9
                SIZE_SQUARE = 3

                sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                            [6, 0, 0, 1, 9, 5, 0, 0, 0],
                            [0, 9, 8, 0, 0, 0, 0, 6, 0],
                            [8, 0, 0, 0, 6, 0, 0, 0, 3],
                            [4, 0, 0, 8, 0, 3, 0, 0, 1],
                            [7, 0, 0, 0, 2, 0, 0, 0, 6],
                            [0, 6, 0, 0, 0, 0, 2, 8, 0],
                            [0, 0, 0, 4, 1, 9, 0, 0, 5],
                            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
                tsudoku = []
                iterate 0..sudoku size as i, _=>
                    new = []
                    iterate sudoku as x =>
                        new += x[i]
                    <<
                    tsudoku += new
                <<
                fn is_valid => sudoku flatten count:0 == 0

                fn set_val i j val =>
                    sudoku[i][j] = val
                    tsudoku[j][i] = val
                <<
                fn get_val i j => sudoku[i][j]

                fn get_square i j =>
                    lc = i//3
                    cc = j//3
                    res=[]
                    repeat SIZE_SQUARE as l =>
                        repeat SIZE_SQUARE as k =>
                            res += sudoku[SIZE_SQUARE*lc+k][SIZE_SQUARE*cc+l]
                        <<
                    <<
                    return res
                <<
                fn get_row i => sudoku[i]
                fn get_col j =>
                    col = []
                    iterate sudoku => col+=iterelem[j]
                    return col
                <<
                fn simplify =>
                    if not is_valid() =>
                        changed = True
                        while changed =>
                            changed = False
                            for ll in (0..SIZE) =>
                                for lc in (0..SIZE) =>
                                    if get_val(ll, lc) == 0 =>
                                        values = REF clone removeDuplicates difference(get_row(ll) clone removeDuplicates, get_col(lc) clone removeDuplicates, get_square(ll, lc) clone removeDuplicates)
                                        if values size equals 1 =>
                                                set_val(ll, lc, values at(0))
                                                changed = True
                                        <<
                                    <<
                                <<
                            <<
                        <<
                    <<
                <<

                simplify()
                sudoku out
                """
        output = ['[[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6], [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]]']
        self.assertEqual(self.interface.run(input, return_out=True), output)

    def test_cw5_first_non_repeating_character(self):
        #https://www.codewars.com/kata/52bc74d4ac05d0945d00054e
        input = """fn first_non_repeating_character string =>
                    string -> if string lower count: (char lower) smaller 2 => <-char 
                <<
                "sTreSS" first_non_repeating_character out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['T'])

    def test_cw5_pete_the_baker(self):
        #https://www.codewars.com/kata/525c65e51bf619685c000059
        input = """fn cakes cake_recipe ingredients =>
                    ratios = []
                    iterate cake_recipe keys as ingredient=>
                        if ingredient not in ingredients keys => return 0
                        ratios append(ingredients[ingredient] // cake_recipe[ingredient])
                    <<
                    <- ratios min
                <<
                cakes: {"flour" > 500, "sugar" > 200, "eggs" > 1},  {"flour" > 1200, "sugar" > 1200, "eggs" > 5, "milk" > 200}
                cakes: {"apples" > 3, "flour" > 300, "sugar" > 150, "milk" > 100, "oil" > 100}, {"sugar" > 500, "flour" > 2000, "milk" > 2000}"""
        self.assertEqual(self.interface.run(input, return_out=True), ['2', '0'])

    def test_cw5_string_incrementer(self):
        #https://www.codewars.com/kata/54a91a4883a7de5d7800009c
        input = """fn string_inc str =>
                    if str last not in NUMBERS => <- str+"1"
                    let number ""
                    let word ""
                    iterate reverse(0..str size) =>
                        if str[iterelem] in NUMBERS => number insert(0,str[iterelem])
                        else => 
                            let word str[0..(iterelem+1)]
                            break
                        <<
                    <<
                    number_len = number size
                    actual_len = (number asNum +1) asString size
                    zeroes = "0" * (number_len - actual_len)
                    return "#word##zeroes##number asNum +1#"
                <<
                "foo" string_inc out
                "foobar23" string_inc out
                "foo0042" string_inc out
                "foo099" string_inc out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['foo1', 'foobar24', 'foo0043', 'foo100'])

    def test_cw5_scramblies(self):
        #https://www.codewars.com/kata/55c04b4cc56a697bb0000048
        input = """fn scramble str1 str2 =>
                    scramblable = True
                    iterate str2 as char =>
                        if str1 count: char < str2 count: char => scramblable = False
                    <<
                    return scramblable 
                <<

                scramble('rkqodlw', 'world') out
                scramble('cedewaraaossoqqyt', 'codewars') out
                scramble('katas', 'steak')  out"""
        self.assertEqual(self.interface.run(input, return_out=True), ['True', 'True', 'False'])    

    def test_cw5_extract_domain_name_from_url(self):
        #https://www.codewars.com/kata/514a024011ea4fb54200004b/python
        input = """fn domainName url => url replace: "http://", "" replace: "https://", "" replace: "www.", "" split: "." at: 0
                "http://github.com/carbonfive/raygun"  domainName 
                "http://www.zombie-bites.com" domainName 
                "https://www.cnet.com" domainName 
                "hyphen-url.com" domainName"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"github"', '"zombie-bites"', '"cnet"', '"hyphen-url"']) 
    
    def test_cw4_roman_numerals_helper(self):
        #https://www.codewars.com/kata/51b66044bce5799a7f000003
        self.interface.printall = False
        input = """sym = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
                num = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

                fn toRoman number =>
                    let result ""
                    let pointer 0
                    while number =>
                        div = number // num at: pointer
                        number %= num at: pointer
                        while div =>
                            result += sym at: pointer
                            div -= 1
                        <<
                        pointer += 1
                    <<
                    return result
                <<

                fn fromRoman roman_numeral =>
                    let result 0
                    roman_numeral ->
                        let first_num num at(sym find: iterelem)
                        let second_num num at(sym find(roman_numeral at(itercounter + 1))) if itercounter +1 != roman_numeral size else -1
                        if first_num >= second_num => result += first_num
                        else => result -= first_num
                    <<
                    return result
                <<

                toRoman(2541) out
                fromRoman("MCCCXI") out"""
        self.assertEqual(self.interface.run(input, return_out=True), ["MMDXLI", "1311"])
        
    def test_cw8_object_oriented_piracy(self):
        #https://www.codewars.com/kata/54fe05c4762e2e3047000add
        input = """class Ship =>
                    fn setup draft crew=>
                        own draft = draft
                        own crew = crew
                    <<
                    fn worth =>
                        return own draft - 1.5*own crew > 20
                    <<
                <<
                titanic =  Ship new(15, 10)
                other_ship = Ship new(142, 36)
                titanic worth out
                other_ship worth out"""
        self.assertEqual(self.interface.run(input, return_out=True), ["False", "True"])
        
    def test_cw7_object_drills_quarks(self):
        #https://www.codewars.com/kata/5882b052bdeafec15e0000e6
        input = """class Quark =>
                fn setup color flavor =>
                    own color = color
                    own flavor = flavor
                    own baryon_number = 1/3
                <<
                fn interact other =>
                    temp_c = other color
                    other color = own color
                    own color = temp_c
                <<
            <<
            q1 = Quark new("red", "up")
            color(q1)
            flavor: q1
            q2 = Quark new ("blue", "strange")
            q2 color
            q1 interact: q2
            q1 color
            q2 color"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"red"', '"up"', '"blue"', '"blue"', '"red"'])
        
    def test_cw6_version_manager(self):
        #https://www.codewars.com/kata/5bc7bb444be9774f100000c3
        input = """class VersionManager =>
                fn setup version =>
                    own MAJOR = 0
                    own MINOR = 0
                    own PATCH = 1
                    if version size equals 0 =>
                        return
                    <<
                    elems = version split(".") >> x asNum
                    own MAJOR = elems at: 0
                    if elems size greater 0 => own MINOR = elems at: 1
                    if elems size greater 1 => own PATCH = elems at: 2
                <<
                fn major =>
                    own prev = [own MAJOR, own MINOR, own PATCH]
                    own MAJOR += 1
                    own MINOR = 0
                    own PATCH = 0
                <<
                fn minor =>
                    own prev = [own MAJOR, own MINOR, own PATCH]
                    own MINOR += 1
                    own PATCH = 0
                <<
                fn patch => 
                    own prev = [own MAJOR, own MINOR, own PATCH]
                    own PATCH += 1
                <<
                fn rollback =>
                    own MAJOR = own prev at: 0
                    own MINOR = own prev at: 1
                    own PATCH = own prev at: 2
                <<
                fn release =>
                    return "#own MAJOR#.#own MINOR#.#own PATCH#"
                <<
            <<
            game = VersionManager new ("1.1.1")
            game minor
            game patch
            game patch
            game major
            game rollback
            game release"""
        self.assertEqual(self.interface.run(input, return_out=True), ['"1.2.2"'])
        
    def test_cw6_high_score_table(self):
        #https://www.codewars.com/kata/5962bbea6878a381ed000036
        input = """class ScoreTable =>
                fn setup tableSize =>
                    own tableSize = tableSize
                    own scores = []
                <<
                fn update val =>
                    own scores append: val
                    own scores sort reverse
                    if own scores size > own tableSize => own scores = own scores [0..3]
                <<
                fn reset => 
                    own scores = []
                <<
            <<

            table = ScoreTable new: 3
            table scores
            table update: 10
            table scores
            table update: 8
            table update: 12
            table update: 5
            table update: 10
            table scores
            table reset
            table scores"""
        self.assertEqual(self.interface.run(input, return_out=True), ['[]', '[10]', '[12, 10, 10]', '[]'])

    def test_cw4_codewars_style_ranking_system(self):
        #https://www.codewars.com/kata/51fda2d95d6efda45e00004e
        input = """class User =>
                ranks = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]
                fn setup =>
                    own curRank = 0
                    own progress = 0
                    own rank = -8
                <<
                fn incProgress kRank =>
                    kRank = ranks find: kRank
                    if ranks[own curRank] == 8 => return
                    if kRank == own curRank => own progress += 3
                    or kRank == own curRank -1 => own progress += 1
                    or kRank > own curRank =>
                        diff = kRank - own curRank
                        own progress += 10*diff*diff
                    <<
                    while own progress >= 100 =>
                        own curRank += 1
                        own update
                        own progress -= 100
                        if ranks[own curRank] == 8 =>
                            own progress = 0
                            return
                        <<
                    <<
                <<
                fn update => 
                    own rank = ranks at(own curRank)
                <<
            <<

            user = User new
            user rank
            user progress
            user incProgress: -7
            user progress
            user incProgress: -5
            user progress
            user rank"""
        self.assertEqual(self.interface.run(input, return_out=True), ['-8', '0', '10', '0', '-7'])
        
    def test_cw5_the_fruit_juice(self):
        #https://www.codewars.com/kata/5264603df227072e6500006d/train/python
        input = """class Jar =>
                fn setup =>
                    own apple = 0
                    own banana = 0
                <<
                fn add amount kind =>
                    if kind=="apple" => own apple += amount
                    else => own banana += amount
                <<
                fn pour_out amount =>
                    total = own apple + own banana
                    appleConc = own apple / total
                    bananaConc = own banana / total
                    own apple -= amount*appleConc
                    own banana -= amount*bananaConc
                <<
                fn get_total_amount => own apple + own banana 
                fn get_concentration kind =>
                    total = own apple + own banana
                    if total == 0 => return 0
                    or kind=="apple" => return own apple / total
                    else => return own banana / total
                <<
            <<

            jar = Jar new
            jar get_total_amount
            jar add: 100, "apple"
            jar get_total_amount
            jar get_concentration: "apple"
            jar add: 100, "apple"
            jar get_total_amount
            jar get_concentration: "apple"
            jar add: 200, "banana"
            jar get_concentration: "apple"
            jar get_concentration: "banana"
            jar pour_out: 200
            jar get_concentration: "apple"
            jar get_total_amount
            jar add: 200, "apple"
            jar get_total_amount
            jar get_concentration: "banana"
            jar get_concentration: "apple" 
        """
        self.assertEqual(self.interface.run(input, return_out=True), ['0', '100', '1', '200', '1', '0.5', '0.5', '0.5', '200', '400', '0.25', '0.75'])

def main():
    times= []
    for i in range(20):
        start_time = timeit.default_timer()
        unittest.main(exit=False)
        end_time = timeit.default_timer()
        times.append(end_time-start_time)
    print("avg", sum(times)/len(times))


if __name__ == "__main__":
    main()