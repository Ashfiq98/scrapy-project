import random


def generate_random_number(length):
    return random.randint(0, length - 1)


# Example usage:
length = 10
random_number = generate_random_number(length)
print(f"Random number for length {length}: {random_number}")

length = 24
random_number = generate_random_number(length)
print(f"Random number for length {length}: {random_number}")
