from parser import parseIRC
import json
import pprint
pp = pprint.PrettyPrinter(indent=4, compact=False, depth=100000)

with open("src/parseTests.json", "r") as f:
    tests = json.load(f)

# yes i know its scuffed idc :)

for test in tests:
    # get expected values & print them before calculating real values
    # to make sure that you know what test failed, assuming it fails
    expected = tests[test]
    expected["raw"] = test
    print(f"test: `{test}`")
    print("expected: ")
    pp.pprint(expected)
    actual = parseIRC(test)
    print("actual: ")
    print("{")
    print(f'    "command": ', end="")
    pp.pprint(actual.command)
    print(f'    "param": ', end="")
    pp.pprint(actual.param)
    print(f'    "params": ', end="")
    pp.pprint(actual.params)
    print(f'    "prefix": ', end="")
    pp.pprint(actual.prefix)
    print(f'    "raw": ', end="")
    pp.pprint(actual.raw)
    print(f'    "tags": ', end="")
    pp.pprint(actual.tags)
    print(f'    "trailing": ', end="")
    pp.pprint(actual.trailing)
    print('}')
    assert actual.command == expected["command"]
    assert actual.prefix == expected["prefix"]
    assert actual.tags == expected["tags"]
    assert actual.params == expected["params"]
    assert actual.raw == expected["raw"]
    assert actual.param == expected["param"]
    assert actual.trailing == expected["trailing"]
print("Ur all good!")
