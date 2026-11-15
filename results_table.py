def print_table(title, rows):
    print(f"\n{title}")
    print("-" * 85)
    print(f"{'Parameter':<30} {'Value':>20} {'Converted Value':>25}")
    print("-" * 85)

    for name, value, converted in rows:
        print(f"{name:<30} {value:>20} {converted:>25}")

    print("-" * 85)