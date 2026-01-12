# ============================================================
# ROM-GRADE PYTHON KERNEL MODIFIER
# Repo-agnostic | Zero-touch | Commercial-grade
# ============================================================

import sys
import time
import hashlib
import importlib
import importlib.abc
import importlib.util
from types import ModuleType
from pathlib import Path

# ----------------------------
# GLOBAL REGISTRY
# ----------------------------
COMMODITY_LEDGER = {}
SESSION_ID = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

# ----------------------------
# CONFIG (override via env)
# ----------------------------
DEFAULT_PRICE = 0.001        # cost per execution
HASH_ALGO = "sha256"

# ----------------------------
# UTILITIES
# ----------------------------
def hash_bytes(data: bytes) -> str:
    h = hashlib.new(HASH_ALGO)
    h.update(data)
    return h.hexdigest()

def fingerprint_module(spec):
    try:
        if spec.origin and Path(spec.origin).exists():
            data = Path(spec.origin).read_bytes()
            return hash_bytes(data)
    except Exception:
        pass
    return None

def register_module(name, fingerprint):
    COMMODITY_LEDGER[name] = {
        "fingerprint": fingerprint,
        "price": DEFAULT_PRICE,
        "executions": 0,
        "first_seen": time.time(),
        "session": SESSION_ID,
    }

def charge(name):
    COMMODITY_LEDGER[name]["executions"] += 1

# ----------------------------
# LOADER WRAPPER
# ----------------------------
class CommodityLoader(importlib.abc.Loader):
    def __init__(self, loader, fullname, spec):
        self.loader = loader
        self.fullname = fullname
        self.spec = spec

    def create_module(self, spec):
        if hasattr(self.loader, "create_module"):
            return self.loader.create_module(spec)
        return None

    def exec_module(self, module):
        fingerprint = fingerprint_module(self.spec)

        if self.fullname not in COMMODITY_LEDGER:
            register_module(self.fullname, fingerprint)

        charge(self.fullname)

        start = time.perf_counter()
        self.loader.exec_module(module)
        duration = time.perf_counter() - start

        # Attach commodity metadata directly to module
        module.__commodity__ = {
            "name": self.fullname,
            "fingerprint": fingerprint,
            "price": COMMODITY_LEDGER[self.fullname]["price"],
            "exec_time": duration,
            "session": SESSION_ID,
        }

# ----------------------------
# META PATH FINDER
# ----------------------------
class CommodityFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        try:
            spec = importlib.util.find_spec(fullname)
            if not spec or not spec.loader:
                return None

            # Avoid double-wrapping
            if isinstance(spec.loader, CommodityLoader):
                return spec

            spec.loader = CommodityLoader(spec.loader, fullname, spec)
            return spec
        except Exception:
            return None

# ----------------------------
# INSTALL KERNEL HOOK
# ----------------------------
if not any(isinstance(f, CommodityFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, CommodityFinder())

# ----------------------------
# OPTIONAL EXPORT API
# ----------------------------
def export_ledger():
    return {
        "session": SESSION_ID,
        "modules": COMMODITY_LEDGER,
    }

sys.__commodity_export__ = export_ledger
