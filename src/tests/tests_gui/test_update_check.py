import pytest

from normcap.gui import update_check


@pytest.mark.skip_on_gh
@pytest.mark.parametrize("packaged", [True, False])
def test_update_checker_new_version(monkeypatch, qtbot, packaged):
    monkeypatch.setattr(update_check, "__version__", "0.0.0")
    checker = update_check.UpdateChecker(None, packaged=packaged)
    with qtbot.waitSignal(checker.com.on_version_retrieved, timeout=4000) as result:
        checker.check()
    version = result.args[0]

    assert isinstance(version, str)
    assert len(version) >= 5
    assert version[0].isdigit()
    assert version.count(".") == 2


@pytest.mark.skip_on_gh
@pytest.mark.parametrize("packaged", [True, False])
def test_update_checker_no_new_version(monkeypatch, qtbot, packaged):
    monkeypatch.setattr(update_check, "__version__", "9.9.9")
    checker = update_check.UpdateChecker(None, packaged=packaged)
    with qtbot.waitSignal(
        checker.com.on_version_retrieved, raising=False, timeout=4000
    ) as result:
        checker.check()
    assert not result.signal_triggered


@pytest.mark.skip_on_gh
@pytest.mark.parametrize(
    "packaged,text",
    [(True, "abc"), (False, '{"no relevant":"info"}'), (False, '{"invalid":"json"')],
)
def test_update_checker_cant_parse(caplog, packaged, text):
    checker = update_check.UpdateChecker(None, packaged=packaged)

    # pylint: disable=protected-access
    version = checker._parse_response_to_version(text)

    assert version is None
    assert "ERROR" in caplog.text
