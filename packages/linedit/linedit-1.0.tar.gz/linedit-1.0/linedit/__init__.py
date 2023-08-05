def edit(file, line, newline):
    with open(file, 'r') as r:
        fetch = r.readlines()
    assert len(fetch) >= line, f"File does not contain {str(line)} lines."
    with open(file, 'w') as w:
        for i, curline in enumerate(fetch, 1):
            if i == line:                              
                w.writelines(f"{newline}\n")
            else:
                w.writelines(curline)
