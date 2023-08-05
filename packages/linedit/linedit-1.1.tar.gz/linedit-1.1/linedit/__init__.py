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

def medit(file, container):
    with open(file, 'r') as r:
        fetch = r.readlines()
    container = sorted(container, key=lambda x: x[0])
    for line in container:
        assert len(fetch) >= line[0], f"File does not contain {str(line[0])} lines."
        assert len(line) == 2, f"Edit to line {line[0]} contains too many objects."
    with open(file, 'w') as w:
        for i, curline in enumerate(fetch, 1):
            if (len(container) > 0) and (i == container[0][0]):                              
                w.writelines(f"{container[0][1]}\n")
                container.pop(0)
            else:
                w.writelines(curline)

