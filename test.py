import unittest
from itertools import zip_longest
from lib.JSONParser.JSONLexer import createJSONLexer as JSONLexer
from lib.JSONParser import parseJSON
from lib.JSONParser.JSONLexer import *
import json # ironically, using json to test json

helper = lambda exp: list(map(str, JSONLexer(exp)))

class HelperAssert:
    def assertEqualJSONString(self, a, b):
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

class TestJSONLexer(unittest.TestCase, HelperAssert):
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

    def test_parse_string(self):
        def first(inp):
            return next(JSONLexer(inp))

        self.assertEqual(first('""').content, [])
        self.assertEqual(first('"abc"').content, ['a', 'b', 'c'])
        self.assertEqual(first('" as  \tdsg  ;  s"').content, [' ', 'a', 's', ' ', ' ', '\t', 'd', 's', 'g', ' ', ' ', ';', ' ', ' ', 's'])
        self.assertEqual(first('"\\t\\n\\r \t \\u270A\\u0101"').content, ['\\t', '\\n', '\\r', ' ', '\t', ' ', '\\u270a', '\\u0101'])
        self.assertEqual(first('"[](){}\\"\\\\"').content, ['[', ']', '(', ')', '{', '}', '\\"', '\\\\'])
        with self.assertRaises(ValueError): next(JSONLexer('"'))
        with self.assertRaises(ValueError): next(JSONLexer('     " sagfjsklh hgkdsgh  shuelighkshg'))
        with self.assertRaises(LexingError): next(JSONLexer(' "\\somevalue"  '))
        with self.assertRaises(LexingError): next(JSONLexer('   "\\ux"'))

    def test_parse_signs(self):
        def first(inp):
            return next(JSONLexer(inp))

        def assertIsInstanceList(ins, cls):
            nonlocal self
            for i, (u, v) in enumerate(zip_longest(ins, cls), 1):
                self.assertIsInstance(u, v, "Case {}".format(i))

        self.assertIsInstance(first("  [   "), OpenSquareBracketToken)
        self.assertIsInstance(first("  \n  ] \t  "), CloseSquareBracketToken)
        self.assertIsInstance(first("  { "), OpenCurlyBracketToken)
        self.assertIsInstance(first("  }  "), CloseCurlyBracketToken)
        self.assertIsInstance(first(" , "), CommaToken)
        self.assertIsInstance(first("  :  "), ColonToken)

        assertIsInstanceList(
            JSONLexer(" [][]][]  \t {} {{}{} \n ,,,:::  \t[,]],[\t\t {:}}}{{{:,  \n\n\n"),
            [
                OpenSquareBracketToken,
                CloseSquareBracketToken,
                OpenSquareBracketToken,
                CloseSquareBracketToken,
                CloseSquareBracketToken,
                OpenSquareBracketToken,
                CloseSquareBracketToken,

                OpenCurlyBracketToken, 
                CloseCurlyBracketToken,

                OpenCurlyBracketToken, 
                OpenCurlyBracketToken, 
                CloseCurlyBracketToken,
                OpenCurlyBracketToken, 
                CloseCurlyBracketToken,

                CommaToken,
                CommaToken,
                CommaToken,
                ColonToken,
                ColonToken,
                ColonToken,

                OpenSquareBracketToken,
                CommaToken,
                CloseSquareBracketToken,
                CloseSquareBracketToken,
                CommaToken,
                OpenSquareBracketToken,

                
                OpenCurlyBracketToken, 
                ColonToken,
                CloseCurlyBracketToken,
                CloseCurlyBracketToken,
                CloseCurlyBracketToken,
                OpenCurlyBracketToken, 
                OpenCurlyBracketToken, 
                OpenCurlyBracketToken, 
                ColonToken,
                CommaToken,
            ]
        )

    def test_parse_literals(self):
        def first(inp):
            return next(JSONLexer(inp))
        self.assertIsInstance(first("null"), NullToken)
        self.assertIsInstance(first("false"), FalseToken)
        self.assertIsInstance(first("true"), TrueToken)

        def assertIsInstanceList(ins, cls):
            nonlocal self
            for i, (u, v) in enumerate(zip_longest(ins, cls), 1):
                self.assertIsInstance(u, v, "Case {}".format(i))

        assertIsInstanceList(
            JSONLexer("\n\ntrue\tfalse\ntrue\ntrue null null false\t true"),
            [
                TrueToken,
                FalseToken,
                TrueToken,
                TrueToken,
                NullToken,
                NullToken,
                FalseToken,
                TrueToken,
            ]
        )

    def test_parse_array(self):
        self.assertEqualJSONString(parseJSON("[]"), [])
        self.assertEqualJSONString(parseJSON("[1]"), [1.0])
        self.assertEqualJSONString(parseJSON("[1,2,3,false, true\n,null]"), [1.0, 2.0, 3.0, False, True, None])
        self.assertEqualJSONString(parseJSON("[[]]"), [[]])
        self.assertEqualJSONString(parseJSON("[[], [], []]"), [[], [], []])
        self.assertEqualJSONString(parseJSON("[1e9]"), [1e9])
        self.assertEqualJSONString(parseJSON("[-123545.56457, [\n\n3\n\n\n\n], \nnull, \nfalse]"), [-123545.56457, [3.0], None, False])
        self.assertEqualJSONString(parseJSON('["asbsseesg\\u000a", "   -2345"]'), ["asbsseesg\u000a", "   -2345"])
        self.assertEqualJSONString(parseJSON('["ewrog3u58", 3656.23563,    null,false\t, false]'), ["ewrog3u58", 3656.23563, None, False, False])

    def test_parse_object(self):
        self.assertEqualJSONString(parseJSON("{}"), {})
        self.assertEqualJSONString(parseJSON('{"a": 0.1}'), {"a": 0.1})
        self.assertEqualJSONString(parseJSON('{"b": null,\n"c": false, "d": true, "f": -6.9e-9}'), {"b": None, "c": False, "d": True, "f": -6.9e-9})
        self.assertEqualJSONString(parseJSON('{"a":{"b":{"c":{}}}}'), {"a":{"b":{"c":{}}}})

    def test_complex(self):
        self.assertEqualJSONString(parseJSON('{"command": [   ],"within": \t\t["universe", false\n ] }'), {
            "command": [],
            "within": ["universe", False]
        })
        self.assertEqualJSONString(parseJSON('''
            [
              {
                "program": {
                  "adjective": -108551751,
                  "sense": false
                }
              },
              916748759.1955104
            ]
            '''),
            [ { "program": { "adjective": -108551751.0, "sense": False } }, 916748759.1955104 ]
        )

        self.assertEqualJSONString(parseJSON('''
            {
              "-m5WT/": [ "^koG", "aQ", "%",
                {
                  "gCD@": "7",
              "^;Bbjg": [ 102200932.16621447, -1103826775,
                    [
                    {     "": false,"n=H6":-1959301866, "RJ\\\\": false },
                      true, false, "",
                   -457508445
                ], "fK",
                    [55391913.57936764
                    ]
                  ],
                  "^'#": "", "qtI": "YiKG\\\""
                },
                "|"
              ],
              "w,:V": ".",
              "y_F":false, "zN2AJ!": true, "5t,wGU": { "+IP7L": true, ",V%=_": true,
                "<,$": "_IqqU6",
                "$+_T": {
              "zA>":[ 1455897291.1386685, { ",\\\\fn": [ 1928704017,
               -1913490965.7375894,
                 true, false, -319104944, 1504012558 ],
            \t        ":nN": 814615960.550847, "": false
                    },
                    "d#"
                  ]
                },
                "5[": true, "-pT": false } } 
            '''),{
                  "-m5WT/": [
                    "^koG", "aQ", "%",
                    {
                      "gCD@": "7",
                      "^;Bbjg": [
                        102200932.16621447,
                        -1103826775.0,
                        [ { "": False, "n=H6": -1959301866.0, "RJ\\": False }, True, False, "", -457508445.0 ],
                        "fK",
                        [ 55391913.57936764 ]
                      ],
                      "^'#": "", "qtI": "YiKG\""
                    }, "|"
                  ],
                  "w,:V": ".", "y_F": False, "zN2AJ!": True,
                  "5t,wGU": {
                    "+IP7L": True, ",V%=_": True, "<,$": "_IqqU6",
                    "$+_T": {
                      "zA>": [
                        1455897291.1386685,
                        {
                          ",\\fn": [ 1928704017.0, -1913490965.7375894, True, False, -319104944.0, 1504012558.0 ],
                          ":nN": 814615960.550847, "": False
                        },
                        "d#"
                      ]
                    },
                    "5[": True, "-pT": False
                  }
            } 
        )

if __name__ == "__main__":
    unittest.main()

