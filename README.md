# A simple JSON parser in Python
This project is a part of a lab I do in the university. 

## Requirements
Nothing, just Python 3

## Running
- To run the unit test:
```
python3 test.py
```

- To convert `sample.json` file into `sample.yaml` file in the root folder:
```
python3 main.py
```

## Using the parser
Just include the package JSONParser in your project. This package has 2 main functions:

- `generateJSON_AST(input)` - this function will return the `abstract syntax tree (AST)` for the given input. Some errors will be raised when the parser has some trouble parsing the input. The return value has 2 medthods: 
	+ `toPythonValue()`: convert the AST to Python with the helps of Python's dict and list.
	+ `toYAML(indentLevel = 0, indentPart = '  ')`: convert the AST into YAML string, with *acceptable* format. 

> TODO: specify which error will be raised.

- `parseJSON(input)` - just a shorthand for `generateJSON_AST(input).toPythonValue()`. 
- In addition in the package, there are also classes with name ends with `Token`. The AST is described using these classes.

## About the algorithm
My task in university ask me to write a parser without using any parsing library, except for `re` module, which helps parsing string. But for me, I don't really like how `re` work, so I decided to challenge myself writing my own parser without `re`. After reading [this post](https://hackernoon.com/lexical-analysis-861b8bfe4cb0), I decided to write it with `finite state machine`, but instead of `switch case` hell describe in the post, I use functional-programming style. In short, I describe a state with a function, the changing state condition is the input, and the output is another state, which is also a function.
