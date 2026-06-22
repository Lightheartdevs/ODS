import os
from pathlib import Path

base = Path(r"c:\Users\gaura\Desktop\opensource3\DreamServer\dream-server\extensions\services\dashboard-api")

# File 1: main.py
f1 = base / "main.py"
text1 = f1.read_text(encoding="utf-8")
text1 = text1.replace("""    def set(self, key: str, value: object, ttl: float):
        self._store[key] = (time.monotonic() + ttl, value)


_cache = TTLCache()""", """    def set(self, key: str, value: object, ttl: float):
        self._store[key] = (time.monotonic() + ttl, value)

    def invalidate(self, key: str) -> None:
        \"\"\"Remove a single cache entry.\"\"\"
        self._store.pop(key, None)

    def clear(self) -> None:
        \"\"\"Remove all cache entries.\"\"\"
        self._store.clear()


_cache = TTLCache()""")
text1 = text1.replace("        _cache._store.pop(key, None)", "        _cache.invalidate(key)")
f1.write_text(text1, encoding="utf-8")

# File 2: helpers.py
f2 = base / "helpers.py"
text2 = f2.read_text(encoding="utf-8")
text2 = text2.replace("""    def set(self, path: Path, value: float):
        self._store[str(path.resolve())] = (time.monotonic() + self._ttl, value)


_dir_size_cache = _DirSizeCache()""", """    def set(self, path: Path, value: float):
        self._store[str(path.resolve())] = (time.monotonic() + self._ttl, value)

    def invalidate(self, path: Path) -> None:
        self._store.pop(str(path.resolve()), None)

    def clear(self) -> None:
        self._store.clear()


_dir_size_cache = _DirSizeCache()""")
text2 = text2.replace("    _dir_size_cache._store.pop(str(path.resolve()), None)", "    _dir_size_cache.invalidate(path)")
text2 = text2.replace("    _dir_size_cache._store.clear()", "    _dir_size_cache.clear()")
f2.write_text(text2, encoding="utf-8")

# File 3: routers/resources.py
f3 = base / "routers" / "resources.py"
text3 = f3.read_text(encoding="utf-8")
text3 = text3.replace('    _cache._store.pop("service_resources_containers", None)', '    _cache.invalidate("service_resources_containers")')
f3.write_text(text3, encoding="utf-8")

# File 4: tests/test_resources.py
f4 = base / "tests" / "test_resources.py"
text4 = f4.read_text(encoding="utf-8")
text4 = text4.replace("""        _cache._store.pop("service_resources_containers", None)
        _cache._store.pop("service_resources_disk", None)""", """        _cache.invalidate("service_resources_containers")
        _cache.invalidate("service_resources_disk")""")
f4.write_text(text4, encoding="utf-8")

# File 5: tests/test_settings_env.py
f5 = base / "tests" / "test_settings_env.py"
text5 = f5.read_text(encoding="utf-8")
text5 = text5.replace("    _cache._store.clear()", "    _cache.clear()")
f5.write_text(text5, encoding="utf-8")

# File 6: tests/test_main.py
f6 = base / "tests" / "test_main.py"
text6 = f6.read_text(encoding="utf-8")
text6 = text6.replace('        main._cache._store.pop("gpu_info", None)', '        main._cache.invalidate("gpu_info")')
f6.write_text(text6, encoding="utf-8")

print("Done")
