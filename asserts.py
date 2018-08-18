import run
def test_are_equal(actual, expected):
    assert expected == actual, "Expected {0}, got {1}".format(expected, actual)


def test_not_equal(a, b):
    assert a != b, "Did not expect {0}, but got {1}".format(a, b)


def test_is_in(collection, item):
    assert item in collection, "{0} does not contain {1}".format(collection, item)
    
def test_not_in(collection, item):
    assert item not in collection, "{0} does contain {1}".format(collection, item)    

def test_between(range, number):
    assert number in range, "{1} is not in range {0}".format(range, number)
    
    
    
#print(test_not_equal(3, 3))
#print(test_is_in([player_info], "{}"))
#print(test_not_in(player_info, {'username':'zed'}))
#print(test_not_in(["dog", "cat", "fish"], "bob"))
#print(test_between(range(0,10), 16))


#print("All tests pass!")