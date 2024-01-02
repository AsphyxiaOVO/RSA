import sympy as sp
# 扩展欧几里得算法
def extended_gcd(aa, bb):
    """

    :param aa:第一个元素
    :param bb:第二元素
    :return:返回最大公约数和模的逆
    """
    last_remainder, remainder = abs(aa), abs(bb)#初始化余数
    x, last_x, y, last_y = 0, 1, 1, 0#初始化系数
    while remainder:
        last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)#辗转相除法
        x, last_x = last_x - quotient * x, x#更新x的系数
        y, last_y = last_y - quotient * y, y#更新y的系数
    if aa < 0:
        last_x = -last_x  # 如果aa为负数，取last_x的相反数
    if bb < 0:
        last_y = -last_y  # 如果bb为负数，取last_y的相反数
    return last_remainder, last_x, last_y


# 求模逆元素
def mod_inverse(a, m):
    """

    :param a: 被模元素
    :param m: 模
    :return: 输出模逆元
    """
    g, x, y = extended_gcd(a, m)#调用扩展欧几里得算法
    if g != 1:#最大公约数不为1，则不存在模逆元
        return None
    else:#返回模逆元
        return x % m

# 定义rsa密钥生成算法
def generate_rsa_keys(e=65537, keysize=1024):
    """

    :param e:公钥指数
    :param keysize:密钥长度
    :return:返回公私钥对
    """
    p = sp.randprime(2**(keysize//2 - 1), 2**(keysize//2))# 随机生成一个1024//2位的大素数p
    q = sp.randprime(2**(keysize//2 - 1), 2**(keysize//2))# 随机生成一个1024//2位的大素数q
    while q == p:
        q = sp.randprime(2**(keysize//2 - 1), 2**(keysize//2))#如果pq相等重新生成

    n = p * q#计算n值
    culer = (p - 1) * (q - 1)#计算欧拉函数值
    d = mod_inverse(e, culer)#计算私钥指数d

    return ((e, n), (d, n))#返回公钥(e, n)和私钥(d, n)

# RSA加密函数的定义
def encrypt_rsa(public_key, plaintext):
    '''

    :param public_key: 公钥对
    :param plaintext: 明文
    :return: 密文
    '''
    e, n = public_key
    plaintext_bytes = plaintext.encode('utf-8') #将明文转换为字节串
    plaintext_int = int.from_bytes(plaintext_bytes, 'big')# 大端法将字节串转换为整数
    ciphertext_int = pow(plaintext_int, e, n)#计算密文整数，c = m^e mod n
    return ciphertext_int

# RSA解密函数的定义
def decrypt_rsa(private_key, ciphertext):
    '''

    :param private_key: 密钥对
    :param ciphertext: 密文
    :return: 明文
    '''
    d, n = private_key
    plaintext_int = pow(ciphertext, d, n)#计算明文整数，m = c^d mod n
    decrypted_byte_length = (plaintext_int.bit_length() + 7) // 8#计算明文字节长度，向下取整保证不会溢出
    plaintext_bytes = plaintext_int.to_bytes(decrypted_byte_length, 'big')#大端法将明文整数转换为字节串
    try:
        return plaintext_bytes.decode('utf-8')#尝试将字节串解码为明文
    except UnicodeDecodeError:
        return "Decoding error: Data may be corrupted."#否则抛出报错

def main():#主函数界面
    while True:
        a=int(input("请输入要进行的操作：\n1.加密\n2.解密\n"))
        if(a==1):#加密过程
            plaintext=input("请输入加密内容：")
            public_key, private_key = generate_rsa_keys()
            ciphertext = encrypt_rsa(public_key, plaintext)
            print("加密成功，文件已保存！")
            print(f"密文为：{ciphertext}\n公钥为：{public_key}\n私钥为：{private_key}")
            break
        if(a==2):#解密过程
            ciphertext=int(input("请输入解密内容："))
            private=int(input("请输入私钥："))
            n=int(input("请输入n值："))
            private_key=(private,n)
            decrypted_text = decrypt_rsa(private_key, ciphertext)
            print("解密成功，文件已保存！")
            print(f"明文为：{decrypted_text}")
            break
        else:
            print("输入错误，请重新输入！")

if __name__ == "__main__":
    main()
