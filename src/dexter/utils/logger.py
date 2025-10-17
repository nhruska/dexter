import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

# Get a logger
log = structlog.get_logger()

class Logger:
    """A logger that uses structlog for structured logging."""

    def info(self, event: str, **kwargs):
        log.info(event, **kwargs)

    def warn(self, event: str, **kwargs):
        log.warning(event, **kwargs)

    def error(self, event: str, **kwargs):
        log.error(event, **kwargs)

    def debug(self, event: str, **kwargs):
        log.debug(event, **kwargs)