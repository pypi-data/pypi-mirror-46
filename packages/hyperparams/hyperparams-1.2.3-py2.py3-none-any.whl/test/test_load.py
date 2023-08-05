from hyperparams import load_params
import os


def test_int():
    params = load_params("test/data/hyperparams.json")
    assert params.TestInt == 42


def test_float():
    params = load_params("test/data/hyperparams.json")
    assert params.TestFloat == 4.2


def test_str():
    params = load_params("test/data/hyperparams.json")
    assert params.TestStr == "Foo"


def test_obj():
    params = load_params("test/data/hyperparams.json")
    assert params.TestObj.TestA == "a" and params.TestObj.TestB == "b"


def test_arr():
    params = load_params("test/data/hyperparams.json")
    assert params.TestArr[0] == "Foo" and params.TestArr[1] == "bar"


def test_env_var():
    params = load_params("test/data/hyperparams.json")
    print("Windows Style Path Syntax")
    print(params.TestWinEnvPythonPath)
    print("Linux Style Path Syntax")
    print(params.TestLinuxEnvPythonPath)
    # They should not match since one is with % and one with $ if they are not replaced
    assert params.TestWinEnvPythonPath == params.TestLinuxEnvPythonPath

    params.foobar = "$HOME"
    params.foobaz = "%HOME%"
    print(params.foobar)
    assert params.foobar == params.foobaz


def test_equal():
    params1 = load_params("test/data/hyperparams.json")
    params2 = load_params("test/data/hyperparams.json")
    assert params1 == params2


if __name__ == "__main__":
    test_int()
    test_float()
    test_str()
    test_obj()
    test_arr()
    test_env_var()
    test_equal()
    print("All tests passed!")
