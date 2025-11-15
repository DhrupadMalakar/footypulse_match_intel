import contextlib
import io
from typing import Tuple


def run_safe_python_snippet(code: str) -> Tuple[bool, str]:
    safe_globals = {'__builtins__': {'print': print, 'len': len, 'range': range}}
    buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, safe_globals, {})
        return True, buffer.getvalue()
    except Exception as exc:
        return False, str(exc)
