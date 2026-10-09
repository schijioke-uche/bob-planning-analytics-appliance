# Offline tests

Run `bash tests/run-tests.sh` from the distribution. The suite uses temporary
copies, never the actual customer environment. Source-derived renderer cases,
synthetic ANSI/PTYS, a strict fake Bob executable, financial toy fixtures and
loopback-only TLS exercise the package. The tests do not establish live backend,
MCP selector acceptance, actual TM1 behavior or full native redraw compatibility.

Content hashes used inside tests assert preservation. They are not invoked by
maintenance and are not a runtime baseline mechanism. `audit/` is review evidence.
