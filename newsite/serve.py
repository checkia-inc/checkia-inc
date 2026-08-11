import os, http.server

os.chdir("/Users/chloealpert/Documents/GitHub/checkia-inc")

http.server.test(
    HandlerClass=http.server.SimpleHTTPRequestHandler,
    port=8765,
    bind="127.0.0.1",
)
