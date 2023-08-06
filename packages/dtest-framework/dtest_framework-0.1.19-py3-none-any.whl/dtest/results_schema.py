
class TestSuiteResultSchema:

    description = None
    ruleSet = None
    dataSet = None
    passed = None
    startTime = None
    duration = None
    topic = None
    testResultsList = []
    testResults = None

    def __init__(self):
        pass


class TestResultSchema:

    description = None
    passed = None
    expectedResult = None
    actualResult = None
    startTime = None
    duration = None
    severity = None

    def __init__(self):
        pass
