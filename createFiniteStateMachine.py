def createFiniteStateMachine(input, endStates, currentState, customData = {}, defaultLastElement = '\u0000'):
    inputIter = iter(input)
    currentState = currentState
    curInput = next(inputIter)
    customData["returnValue"] = None
    try:
        while True:
            currentState = currentState(curInput, customData)
            #print(currentState.__name__, currentState in endStates, customData["returnValue"].__repr__())
            if currentState in endStates:
                yield customData["returnValue"]
                customData["returnValue"] = None
            else:
                curInput = next(inputIter)
    except StopIteration:
        currentState = currentState(defaultLastElement, customData)
        if currentState not in endStates:
            raise ValueError("The state {} is not one of the end stats: {}",
                    currentState.__name__,
                    join(',', map(lambda x: x.__name__, endStates))
            )
        elif customData["returnValue"] is not None:
            yield customData["returnValue"]




