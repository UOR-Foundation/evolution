import sys
import types

# Provide lightweight stubs for optional heavy dependencies when missing
optional_modules = [
    "numpy",
    "networkx",
    "scipy.constants",
    "scipy.linalg",
    "scipy",
]
for mod_name in optional_modules:
    if mod_name not in sys.modules:
        try:
            __import__(mod_name)
        except Exception:
            base_name = mod_name.split('.')[0]
            if base_name not in sys.modules:
                sys.modules[base_name] = types.ModuleType(base_name)
            if mod_name != base_name:
                sys.modules[mod_name] = types.ModuleType(mod_name)

