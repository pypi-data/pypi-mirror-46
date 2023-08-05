from hyperparams.hyperparams import import_params


def test_pyparams():
    params = import_params("test/data/params.py")
    params.immutable = True
    print("Windows Style Path Syntax")
    print(params.win_home)
    print("Linux Style Path Syntax")
    print(params.linux_home)
    # They should not match since one is with % and one with $ if they are not replaced
    assert params.win_home == params.linux_home
    assert params.specific

    # Test for immutability
    try:
        params.specific = False
        assert False
    except RuntimeError:
        print("Changing params failed with runtime error as expected.")

if __name__ == "__main__":
    test_pyparams()
