#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Begotten Wargame — редактор армии (фракции/юниты) + публикация в NewRecruit-репозиторий.
Запуск: двойной клик по start.bat или: python app.py
Открыть: http://localhost:8765
"""
import json, os, subprocess, sys, threading, webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
RULES = os.path.normpath(os.path.join(ROOT, "..", "rules"))
REPO = os.path.normpath(os.path.join(ROOT, "..", "..", "rules-repo"))
PORT = 8765

def jload(p, default):
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default

def jsave(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_all():
    system = jload(os.path.join(RULES, "system.json"), {})
    factions = []
    fdir = os.path.join(RULES, "factions")
    if os.path.isdir(fdir):
        for fn in sorted(os.listdir(fdir)):
            if fn.endswith(".json"):
                factions.append(jload(os.path.join(fdir, fn), {}))
    return {"system": system, "factions": factions}

def faction_path(fid):
    return os.path.join(RULES, "factions", f"{fid}.json")

def publish():
    log = []
    try:
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        r = subprocess.run([sys.executable, os.path.join(RULES, "export_bsdata.py"), RULES, REPO],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, env=env)
        log.append(r.stdout + r.stderr)
        if r.returncode != 0:
            return False, "".join(log)
        def git(*args):
            return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=120, env=env)
        git("add", "-A")
        st = git("status", "--porcelain")
        if not st.stdout.strip():
            log.append("Изменений нет — пуш не нужен.")
            return True, "".join(log)
        c = git("-c", "user.name=AlexRearm", "-c", "user.email=alexrearm@users.noreply.github.com",
                "commit", "-m", "Update army rules (army_tool)")
        log.append(c.stdout + c.stderr)
        p = git("push", "origin", "HEAD:main")
        log.append(p.stdout + p.stderr)
        return p.returncode == 0, "".join(log)
    except Exception as e:
        return False, "".join(log) + f"\nERROR: {e}"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.join(ROOT, "static"), **kw)

    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/data":
            return self._json(load_all())
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/faction/save":
                data = self._body()
                fid = data.get("id", "").strip()
                if not fid:
                    return self._json({"ok": False, "error": "нет id фракции"}, 400)
                jsave(faction_path(fid), data)
                return self._json({"ok": True})
            if path == "/api/faction/delete":
                fid = self._body().get("id", "")
                p = faction_path(fid)
                if os.path.exists(p):
                    os.remove(p)
                return self._json({"ok": True})
            if path == "/api/publish":
                ok, log = publish()
                return self._json({"ok": ok, "log": log})
            return self._json({"ok": False, "error": "unknown"}, 404)
        except Exception as e:
            return self._json({"ok": False, "error": str(e)}, 500)

if __name__ == "__main__":
    url = f"http://localhost:{PORT}"
    print(f"Редактор армии: {url}")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
