from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent


class Setting:
    db_url = f"sqlite+aiosqlite:///{BASE_DIR}/todotasks.db"
