import json
from dexter.utils.logger import Logger

def test_logger(capsys):
    """
    Tests that the logger logs a message in the correct format.
    """
    logger = Logger()
    logger.info("test.event", key="value")

    captured = capsys.readouterr()
    log_output = json.loads(captured.out)

    assert log_output["event"] == "test.event"
    assert log_output["key"] == "value"
    assert "level" in log_output
    assert "timestamp" in log_output