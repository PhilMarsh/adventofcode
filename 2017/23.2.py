###### annotated input
# set b 65
# set c b
# jnz a 2
# jnz 1 5
# mul b 100
# sub b -100000
# set c b
# sub c -17000
# set f 1       <.
# set d 2        |
# set e 2   <.   |
# set g d <. |   |
# mul g e  | |   |
# sub g b  | |   |
# jnz g 2  | |   |
# set f 0  | |   |
# sub e -1 | |   |
# set g e  | |   |
# sub g b  | |   |
# jnz g -8 / |   |
# sub d -1   |   |
# set g d    |   |
# sub g b    |   |
# jnz g -13  /   |
# jnz f 2        |
# sub h -1       |
# set g b        |
# sub g c        |
# jnz g 2 # exit |
# jnz 1 3        |
# sub b -17      |
# jnz 1 -23      /

###### pythonic
# b = 65
# c = 65
#
# b = (b * 100) + 100000 # 106500
# c = b + 17000 # 123500
#
# while True:
#     f = 1
#     d = 2
#     while d != b:
#         e = 2
#         while e != b:
#             if (d * e) == b:
#                 f = 0
#             e += 1
#         d += 1
#     if f == 0:
#         h += 1
#     if b == c:
#         break
#     b += 17

###### reduced
#
# while True:
#     if b is not prime:
#         h += 1
#     if b == c:
#         break
#     b += 17

###### in words
# count composite numbers in range(b, c+1, 17), where b = 106500, c = 123500

def is_prime(i):
    for j in range(2, int(i**0.5)+1):
        if i % j == 0:
            return False
    return True

composites = [
    i
    for i in range(106500, 123500+1, 17)
    if not is_prime(i)
]

print(len(composites))
print(composites)

primes = [
    i
    for i in range(106500, 123500+1, 17)
    if is_prime(i)
]

print(len(primes))
print(primes)

# should get 1001 numbers total (composites + primes)