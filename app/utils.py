"""Password hashing utilities using Argon2 (argon2-cffi).

This module intentionally requires `argon2-cffi`. Install with:
`pip install argon2-cffi`.
"""

try:
    from argon2 import PasswordHasher
except ImportError as e:
    raise ImportError(
        "argon2-cffi is required for password hashing. Install with: pip install argon2-cffi"
    ) from e

# Tune these parameters for your environment.
_ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)


def hash(password: str) -> str:
    return _ph.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    try:
        return _ph.verify(hashed_password, plain_password)
    except Exception:
        return False