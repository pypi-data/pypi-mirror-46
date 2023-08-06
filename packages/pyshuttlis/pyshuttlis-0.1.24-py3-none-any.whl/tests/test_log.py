from shuttlis.log import configure_logging


def test_prints_without_errors():
    _LOG = configure_logging("pyshuttlis", "DEBUG")
    _LOG.debug("hey.there", extra={"one": "one"})


def test_prints_out_exc():
    try:
        raise ValueError
    except ValueError:
        _LOG.error("an.error", exc_info=True)
