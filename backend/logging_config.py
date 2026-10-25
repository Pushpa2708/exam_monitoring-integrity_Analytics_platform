import logging
from pathlib import Path

# Create a folder for application logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Store logs in a file
LOG_FILE = LOG_DIR / "examguard.log"

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

# Create a logger for ExamGuard
logger = logging.getLogger("examguard")