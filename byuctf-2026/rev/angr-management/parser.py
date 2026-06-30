import re
from collections import defaultdict, deque


def solve():
    with open("objdump.txt") as f:
        lines = f.readlines()

    start_idx = 0
    for i, line in enumerate(lines):
        if "<main>:" in line:
            start_idx = i
            break

    instructions = {}
    addrs_in_order = []
    for line in lines[start_idx:]:
        if "<_fini>:" in line:
            break
        m = re.match(r"\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*(.*)", line)
        if m:
            addr = int(m.group(1), 16)
            instr = m.group(2).strip()
            instructions[addr] = instr
            addrs_in_order.append(addr)

    # Now we build a graph.
    # Nodes are addresses.
    # Edges are (target_address, condition_value_if_any)

    graph = defaultdict(list)

    i = 0
    while i < len(addrs_in_order):
        addr = addrs_in_order[i]
        instr = instructions[addr]

        if instr.startswith("jmp"):
            target = int(re.search(r"([0-9a-f]+) <", instr).group(1), 16)
            graph[addr].append((target, None))

        elif instr.startswith("cmp") and "DWORD PTR [rbp-0x4]" in instr:
            # e.g., cmp    DWORD PTR [rbp-0x4],0x100
            m = re.search(r"\[rbp-0x4\],(0x[0-9a-f]+)", instr)
            if not m:
                # maybe it's a decimal value?
                m = re.search(r"\[rbp-0x4\],(\d+)", instr)
                if not m:
                    i += 1
                    continue
                val = int(m.group(1))
            else:
                val = int(m.group(1), 16)

            # Look at next instruction
            next_addr = addrs_in_order[i + 1]
            next_instr = instructions[next_addr]

            if next_instr.startswith("jne"):
                target = int(re.search(r"([0-9a-f]+) <", next_instr).group(1), 16)
                fallthrough = addrs_in_order[i + 2]

                # If != val, jump to target. So if == val, fallthrough!
                graph[next_addr].append((fallthrough, val))
                graph[next_addr].append((target, f"!={val}"))

                graph[addr].append((next_addr, None))

            elif next_instr.startswith("je"):
                target = int(re.search(r"([0-9a-f]+) <", next_instr).group(1), 16)
                fallthrough = addrs_in_order[i + 2]

                # If == val, jump to target. If != val, fallthrough!
                graph[next_addr].append((target, val))
                graph[next_addr].append((fallthrough, f"!={val}"))

                graph[addr].append((next_addr, None))

        else:
            if i + 1 < len(addrs_in_order) and not instr.startswith("ret") and "exit" not in instr and "jmp" not in instr:
                graph[addr].append((addrs_in_order[i + 1], None))

        i += 1

    # Let's find the success address.
    success_addr = 0xEDFE
    start_addr = addrs_in_order[0]

    print(f"Start: {hex(start_addr)}, Success: {hex(success_addr)}")

    # BFS to find path
    queue = deque([(start_addr, [], [])])
    visited = set()

    while queue:
        curr, path, val_path = queue.popleft()

        if curr == success_addr:
            print("Found success!")
            print("Values:", [p for p in val_path if p is not None and not str(p).startswith("!=")])
            for p, v in zip(path, val_path):
                print(f"Addr: {hex(p)} via {v}")
            return

        if curr in visited:
            continue
        visited.add(curr)

        for neighbor, cond in graph[curr]:
            new_path = list(path)
            new_path.append(neighbor)
            new_val_path = list(val_path)
            new_val_path.append(cond)
            queue.append((neighbor, new_path, new_val_path))

    print("Could not find path to success")


solve()
