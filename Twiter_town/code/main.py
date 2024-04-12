MOD = 998244353


def max_product_mod(digits):
    # Sort the digits in non-increasing order
    digits.sort(reverse=True)

    # Splitting the digits into two numbers
    num1, num2 = 0, 0
    for i, digit in enumerate(digits):
        if i % 2 == 0:
            num1 = (num1 * 10 + digit) % MOD
        else:
            num2 = (num2 * 10 + digit) % MOD

    # Calculating the product and its remainder modulo 998244353
    return (num1 * num2) % MOD


# Subproblem 1
digits1 = [4, 9, 5, 4, 6, 8, 3, 9, 5, 7, 9, 1, 1, 7, 6, 5, 9]
answer1 = max_product_mod(digits1)
print("Subproblem 1 - Maximum product modulo 998244353:", answer1)

# Subproblem 2
digits2 = [6, 1, 5, 8, 1, 7, 7, 8, 7, 4, 7, 5, 5, 4, 3, 1, 5, 9, 3, 8, 7, 1, 6, 7, 9, 4, 2, 3, 4, 1, 6, 5, 5, 5, 9, 7, 5, 4, 9, 3, 2, 5, 2, 8, 9, 1, 5, 8,
           4, 4, 6, 2, 3, 7, 6, 5, 5, 7, 8, 7, 6, 5, 4, 6, 8, 3, 1, 1, 5, 6, 6, 2, 1, 1, 7, 2, 8, 8, 8, 9, 8, 3, 9, 1, 5, 5, 3, 8, 9, 5, 3, 7, 5, 3, 6, 7, 2, 6, 1, 6]
answer2 = max_product_mod(digits2)
print("Subproblem 2 - Maximum product modulo 998244353:", answer2)
