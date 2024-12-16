import sqlite3

class DatabaseManager:
    def __init__(self, db_name="secure_chat.db"):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Create the users table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    public_key TEXT NOT NULL,
                    private_key TEXT NOT NULL
                );
            """)
            conn.commit()

    def register_user(self, username, password, public_key, private_key):
        """Register a new user in the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, password, public_key, private_key)
                    VALUES (?, ?, ?, ?);
                """, (username, password, public_key, private_key))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        """Check if the provided username and password are valid."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = ? AND password = ?;
            """, (username, password))
            user = cursor.fetchone()
        return user is not None

    def fetch_contacts(self, current_user):
        """Get a list of all registered users except the current user."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username FROM users WHERE username != ?;
            """, (current_user,))
            users = [row[0] for row in cursor.fetchall()]
        return users

    def get_public_key(self, username):
        """Retrieve the public key of a specific user."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT public_key FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
        return result[0] if result else None

    def get_private_key(self, username):
        """Retrieve the private key of a specific user."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT private_key FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
        return result[0] if result else None
