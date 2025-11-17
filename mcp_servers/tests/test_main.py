import main


def test_main_prints(capsys):
    # main.main prints a greeting
    main.main()
    captured = capsys.readouterr()
    assert "Hello from finalproject!" in captured.out


def test_main_run_as_module(capsys):
    # Running the module as __main__ should also print the greeting
    import runpy

    runpy.run_module("main", run_name="__main__")
    captured = capsys.readouterr()
    assert "Hello from finalproject!" in captured.out
