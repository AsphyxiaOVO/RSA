import sympy as sp
import random

# 定义指数判断函数
def is_prime(n):
    """

    :param n:需要判断的数
    :return: 判断结果
    """
    return sp.isprime(n)

# 生成一个1-500内的指数组
primes_under_500 = list(sp.primerange(1, 500))

# 定义isrsac质数生成算法
def isrsac():
    '''

    :return: 生成的强素数
    '''
    attempts_limit = 10  # 现在尝试的次数最多为10次

    for attempt in range(attempts_limit):
        try:
            # Step 1: 随机选择一个1-500的指数
            h1 = random.choice(primes_under_500)

            # Step 2: 随机生成一个1-9的整数x，计算2ah1+1(a从x开始逐渐增加)，直到找到一个质数h2
            x = random.randint(1, 9)
            a = x
            for _ in range(200):  # 限制尝试的次数
                h2 = 2 * a * h1 + 1
                if is_prime(h2):
                    break
                a += 1
            else:
                raise Exception("Failed to find h2")

            # Step 3 and 4: 随机生成一个1-9的整数y，计算2ah2+1(b从y开始逐渐增加)，直到找到一个质数h3
            for _ in range(50):  # 限制h3的尝试次数
                y = random.randint(1, 9)
                b = y
                for _ in range(200):  # x限制h3的尝试次数
                    h3 = 2 * b * h2 + 1
                    if is_prime(h3):
                        P = 2 * h3 - 1
                        if is_prime(P):
                            return P
                        break
                    b += 1

            raise Exception("not find")

        except Exception as e:
            # 打印结果
            print(f"Attempt {attempt + 1}: {str(e)}")

    return "not find a strong prime"

# 测试用例
strong_prime_with_exception_handling = isrsac()
print(strong_prime_with_exception_handling)