import sys
from pathlib import Path
from sqlalchemy import text

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from app.database import engine

sql_drop = 'ALTER TABLE "Votes" DROP CONSTRAINT IF EXISTS "Votes_post_id_fkey"'
sql_add = 'ALTER TABLE "Votes" ADD CONSTRAINT "Votes_post_id_fkey" FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE'

with engine.begin() as conn:
    conn.execute(text(sql_drop))
    conn.execute(text(sql_add))

print('Fixed Votes.post_id foreign key to reference posts(id)')
