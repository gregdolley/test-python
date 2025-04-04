# Testing GitHub Copilot using the same requset ("give me one line of Python code that enumerates
# primes between x and y") but on two different IDE's - one from Visual Studio Pro 2022 and the
# the other from VS Code v1.72.2.
#
# Both snippets turned out looking pretty similar, but only the one from Visual Studio ended up
# actually fully working.
#
# VS Code snippet:       "[n for n in range(x, y+1) if all(n % i != 0 for i in range(2, int(n**0.5)+1))] if x > 1 else []"
# Visual Studio snippet: "[n for n in range(x, y+1) if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))]"

# Result summary:
#
# print_primes1(1, 100) - VS Code snippet - doesn't work, prints nothing.
# print_primes2(1, 100) - Visual Studio 2022 snippet - seems to work OK. Passing in a range of 1 to 100 printed out all the primes between that range.
#
# print_primes1(0, 100) - VS Code snippet - doesn't work, prints nothing.
# print_primes2(0, 100) - Visual Studio 2022 snippet - OK. Prints out same prime number list as the 1 to 100 range, which is expected
#
# print_primes1(2, 100) - VS Code snippet - OK. Prints all primes from 2 to 100.
# print_primes2(2, 100) - Visual Studio 2022 snippet - OK. Same output prime list as print_primes1() function.

def print_primes1(x, y):
    # from VS Code (v1.72.2) - GitHub Copilot chat window:
    primes = [n for n in range(x, y+1) if all(n % i != 0 for i in range(2, int(n**0.5)+1))] if x > 1 else []

    # The part that VS Code's GitHub Copilot got wrong was the "if x > 1" clause near the end of the line.
    # It's checking the "x" variable (which is the starting number for the prime search passed in from the
    # calling function) when it probably meant to check the "n" variable from the outer "for" loop
    # ("[n for n in range(...)"). Checking the x variable just doesn't make sense.
    #
    # Here's what I think is a correct version of the line:
    #
    # primes = [n for n in range(x, y+1) if all(n % i != 0 for i in range(2, int(n**0.5)+1)) and n > 1]
    #
    # I haven't extensively tested it, but using the above line instead of the original (incorrect) one
    # from Copilot, results in this function returning the same prime list as print_primes2().

    print("Primes from function #1:")
    print(primes)

    return primes


def print_primes2(x, y):
    # from Visual Studio 2022 Professional - GitHub Copilot chat window:
    primes = [n for n in range(x, y+1) if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))]

    print("Primes from function #2:")
    print(primes)

    return primes


def main():
    start = 1
    end = 100

    print_primes1(start, end)
    primes_array = print_primes2(start, end)

    #  double-check
    for num in primes_array:
        if isPrime(num):
            print(f"{num} is prime.")
        else:
            print(f"{num} is NOT prime.")


def isPrime(n):
    # even numbers and numbers < 2 aren't prime by definition (except the number 2 - it's prime, but also even)
    if n % 2 == 0 or n < 2:
        return n == 2

    for i in range(3, int(n**0.5)+1, 2):  # only odd numbers
        if n % i == 0:
            return False

    return True


if __name__ == "__main__":
    main()
