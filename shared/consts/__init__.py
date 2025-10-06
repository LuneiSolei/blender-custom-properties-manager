import importlib
from pathlib import Path

# Get all Python files in the current directory (excluding __init__.py and any "private" files)
current_dir = Path(__file__).parent
const_files = [
    file.stem for file in current_dir.glob("*.py")
    if file.stem != "__init__" and not file.stem.startswith("_")
]

# Import all consts from each file
imported_names = []
name_sources = {}
for file_name in const_files:
    try:
        module = importlib.import_module(f".{file_name}", package = __name__)

        # Import all uppercase constants
        for const_name in dir(module):
            const_value = getattr(module, const_name)
            is_class = isinstance(const_value, type)

            # Skip if the constant either is not uppercase, is private, or is callable, and is neither an Enum class nor
            # instance
            if ((not const_name.isupper()
                or const_name.startswith("_")
                or callable(const_value))
                and not is_class):

                continue

            # Check for naming conflicts
            if const_name in name_sources:
                raise ImportError(f"Duplicate constant name: {const_name} (from {name_sources[const_name]} and {file_name})")

            globals()[const_name] = getattr(module, const_name)
            imported_names.append(const_name)
            name_sources[const_name] = file_name

    except ImportError as e:
        print(f"Warning: Could not import constants from {file_name}: {e}")

__all__ = imported_names