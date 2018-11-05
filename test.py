import unittest
from Lexer.JSONLexer import JSONLexer

helper = lambda exp: list(map(str, JSONLexer(exp)))

class TestJSONLexer(unittest.TestCase):
    #@unittest.skip("")
    def test_skip_spaces(self):
        self.assertEqual(helper(""), [])
        self.assertEqual(helper(" "), [])
        self.assertEqual(helper("    "), [])
        self.assertEqual(helper("\n"), [])
        self.assertEqual(helper("\n\n"), [])
        self.assertEqual(helper(" \n \n"), [])
        self.assertEqual(helper("\t \t \n \t\n \t\r\t"), [])

    def test_parse_number(self):
        self.assertEqual(helper("0"), ["+0.0e+0"])
        self.assertEqual(helper("1 "), ["+1.0e+0"])
        self.assertEqual(helper("2"), ["+2.0e+0"])
        self.assertEqual(helper(" 9"), ["+9.0e+0"])
        self.assertEqual(helper("\n10 "), ["+10.0e+0"])
        self.assertEqual(helper("\n\n\n45643456"), ["+45643456.0e+0"])

        self.assertEqual(helper("\t-0"), ["-0.0e+0"])
        self.assertEqual(helper("\n-1 "), ["-1.0e+0"])
        self.assertEqual(helper("   -2  "), ["-2.0e+0"])
        self.assertEqual(helper(" -9"), ["-9.0e+0"])
        self.assertEqual(helper("\n-10 "), ["-10.0e+0"])
        self.assertEqual(helper("   \n-546406749  "), ["-546406749.0e+0"])

        self.assertEqual(helper("  0.1453 \t  "), ["+0.1453e+0"]);
        self.assertEqual(helper("4043.24536"), ["+4043.24536e+0"]);
        self.assertEqual(helper("  -3.4\n\t\t"), ["-3.4e+0"])
        self.assertEqual(helper("\t\t\t\t\t-546.578584"), ["-546.578584e+0"])
        self.assertEqual(helper("-0.8453\t\t\t"), ["-0.8453e+0"])

        self.assertEqual(helper("0e0"), ["+0.0e+0"])
        self.assertEqual(helper("0E-0"), ["+0.0e-0"])
        self.assertEqual(helper("-0e-0"), ["-0.0e-0"])
        self.assertEqual(helper("345E54563"), ["+345.0e+54563"]);
        self.assertEqual(helper("5646e-56483"), ["+5646.0e-56483"]);

        self.assertEqual(helper("34654.0765E3467"), ["+34654.0765e+3467"])
        self.assertEqual(helper("-454765.25738e-76543"), ["-454765.25738e-76543"])

        self.assertEqual(helper("007589.969"), ["+0.0e+0", "+0.0e+0", "+7589.969e+0"])
        self.assertEqual(helper("3564\n \n36456e946\n -45.324\t\t  3346.65476E-9456"),
                ["+3564.0e+0", "+36456.0e+946", "-45.324e+0", "+3346.65476e-9456"])

        # TODO: add test for exceptions
