def createFiniteStateMachine(input, endStates, initState, customData = {}, lastElement = '\u0000'):
    inputIter = iter(input)
    curInput = next(inputIter)
    customData["returnValue"] = None
    currentState = initState
    try:
        while True:
            currentState = currentState(curInput, customData)
            #print(currentState.__name__, currentState in endStates, customData["returnValue"].__repr__())
            if currentState in endStates:
                yield customData["returnValue"]
                customData["returnValue"] = None
                currentState = initState
            else:
                curInput = next(inputIter)
    except StopIteration:
        currentState = currentState(lastElement, customData)
        if currentState not in endStates:
            raise ValueError("The state {} is not one of the end states: {}".format(
                    currentState.__name__,
                    ', '.join(map(lambda x: x.__name__, endStates))
            ))
        elif customData["returnValue"] is not None:
            yield customData["returnValue"]




