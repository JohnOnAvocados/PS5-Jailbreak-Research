from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import time

from scripts import ingest, normalize, extract, linker, graph_builder, obsidian_sync, wiki_sync, report_builder
from scripts.query_engine import execute, QueryError

RUN_LOG = Path("intermediate/run_log.json")

class Controller:
    def __init__(self):
        self.steps = []

    def _log(self, step: str, status: str, detail: str = ""):
        RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
        log = []
        if RUN_LOG.exists():
            try:
                log = json.loads(RUN_LOG.read_text(encoding="utf-8"))
            except Exception:
                log = []
        log.append({"step": step, "status": status, "detail": detail, "ts": time()})
        RUN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")

    def run_step(self, name: str, fn):
        self._log(name, "started")
        result = fn()
        self._log(name, "finished")
        return result

    def ingest(self):
        return self.run_step("ingest", ingest.run)

    def normalize(self):
        return self.run_step("normalize", normalize.run)

    def extract(self):
        return self.run_step("extract", extract.run)

    def link(self):
        return self.run_step("link", linker.run)

    def graph(self):
        return self.run_step("graph", graph_builder.run)

    def obsidian(self):
        return self.run_step("obsidian_sync", obsidian_sync.run)

    def wiki(self):
        return self.run_step("wiki_sync", wiki_sync.run)

    def reports(self):
        return self.run_step("report_builder", report_builder.run)

    def full_run(self):
        self.ingest()
        self.normalize()
        self.extract()
        self.link()
        self.graph()
        self.obsidian()
        self.wiki()
        self.reports()

    def query(self, query: str):
        try:
            return execute(query)
        except QueryError as e:
            return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="PS5 research graph controller")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest")
    sub.add_parser("normalize")
    sub.add_parser("extract")
    sub.add_parser("link")
    sub.add_parser("graph")
    sub.add_parser("obsidian")
    sub.add_parser("wiki")
    sub.add_parser("reports")
    sub.add_parser("full_run")

    q = sub.add_parser("query")
    q.add_argument("query", nargs="+", help="Graph query string")

    args = parser.parse_args()
    ctl = Controller()

    if args.command == "ingest":
        ctl.ingest()
    elif args.command == "normalize":
        ctl.normalize()
    elif args.command == "extract":
        ctl.extract()
    elif args.command == "link":
        ctl.link()
    elif args.command == "graph":
        ctl.graph()
    elif args.command == "obsidian":
        ctl.obsidian()
    elif args.command == "wiki":
        ctl.wiki()
    elif args.command == "reports":
        ctl.reports()
    elif args.command == "full_run":
        ctl.full_run()
    elif args.command == "query":
        out = ctl.query(" ".join(args.query))
        print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
