import time

# Prints Fizz, Buzz, FizzBuzz divisible by 3 and 5 and both
def looprange(count):
    start = time.time()

    # Python program to print Fizz Buzz, loop for 50 times i.e. range
    for fizzbuzz in range(int(count)):

        # number divisible by 15 (divisible by both 3 & 5), print 'FizzBuzz' in place of the number
        if fizzbuzz % 3 == 0 and fizzbuzz % 5 == 0:
            print('FizzBuzz')
            continue

        # number divisible by 3, print 'Fizz' in place of the number
        elif fizzbuzz % 3 == 0:
            print('Fizz')
            continue

        # number divisible by 5, print 'Buzz' in place of the number
        elif fizzbuzz % 5 == 0:
            print('Buzz')
            continue

        # print numbers
        print(fizzbuzz)

    end = time.time()
    print(str("Time taken for execution") + " : " + str(round(end - start)) + " " + str("seconds"))
