def describe_test(name : str):
    print("\n\033[92m-------------------------------\033[0m")
    print(f"\033[92m|TEST : \033[94m{name}\033[0m")
    print("\033[92m-------------------------------\033[0m\n")

def separator(length: int = 30):
    print('-' * length)