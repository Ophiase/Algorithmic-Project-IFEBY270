def describe_test(name : str):
    print("\n\033[92m-------------------------------\033[0m")
    print(f"\033[92m|TEST : \033[94m{name}\033[0m")
    print("\033[92m-------------------------------\033[0m\n")

def separator(length: int = 30, symbol='-'):
    print(symbol * length)

def truth_vs_computed(value_name, truth, computed) :
    if truth != computed:
        print(f"Wrong {value_name} | Truth: {truth}\t Computed : {computed}")
        return False
    return True