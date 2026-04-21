with open("Main/app.py", encoding="utf-8") as f:
    code = compile(f.read(), "Main/app.py", 'exec')
    exec(code, globals())
