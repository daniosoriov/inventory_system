import pathlib
import os

PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent
LOG_PATH = f'{PROJECT_ROOT_PATH}/logs'

os.makedirs(LOG_PATH, exist_ok=True)
if not os.path.isfile(f'{LOG_PATH}/logs.log'):
    with open(f'{LOG_PATH}/logs.log', 'w') as f:
        pass

LOGGING_CONF = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        "advanced": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "advanced",
            "level": "INFO",
            "filename": f'{LOG_PATH}/logs.log',
            "mode": "a",
        }
    },
    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file"
        ]
    }
}
