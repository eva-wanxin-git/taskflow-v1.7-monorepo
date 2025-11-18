#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份数据库
"""

import shutil
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
BACKUP_DIR = Path(__file__).parent.parent / "database" / "backups"

def backup_database():
    """备份数据库"""
    BACKUP_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"tasks_backup_{timestamp}.db"
    
    shutil.copy2(DB_PATH, backup_file)
    
    print(f"Database backed up to: {backup_file}")
    return backup_file

if __name__ == "__main__":
    backup_database()

