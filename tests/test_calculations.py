from app.calculations import add, substract, multiply, divide
import pytest


@pytest.mark.parametrize("num1, num2, result", [(3,2,5),(5,5,10)])
def test_add(num1, num2, result):
    print("testing add")
    assert add(num1,num2) == result

