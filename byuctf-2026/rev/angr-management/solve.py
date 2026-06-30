import angr


def main():
    project = angr.Project("./angr_management_test", auto_load_libs=False)

    # We want to find the address that prints the flag
    # From objdump, this is around 0xedfe (which is an offset if PIE is enabled)
    # The base address of the main object is usually 0x400000. Let's check angr's base address.

    # The success address in objdump is 0xedfe
    # Since PIE is enabled, angr might load it at 0x400000
    base_addr = project.loader.main_object.min_addr
    print(f"Base address: {hex(base_addr)}")

    success_addr = base_addr + 0xEDFE
    # Failure addresses are everywhere we call exit(1), but specifically we can avoid puts("That's not a valid destination")
    # which is loaded using lea rax, [rip+...] where the string is at 0xf028.

    state = project.factory.entry_state()
    simgr = project.factory.simulation_manager(state)

    simgr.explore(find=success_addr)

    if simgr.found:
        found_state = simgr.found[0]
        # Get the input required
        print("Found path!")
        stdin_content = found_state.posix.dumps(0)
        print("Input needed:", stdin_content)

        # Write to file so we can pipe it
        with open("solve.txt", "wb") as f:
            f.write(stdin_content)
    else:
        print("Could not find a path")


if __name__ == "__main__":
    main()
