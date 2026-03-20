from passlib.context import CryptContext

# 创建密码哈希上下文，使用 bcrypt 算法进行密码哈希，并设置过时算法的处理方式
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# deprecated：处理已弃用哈希算法。
# 简单的说：这实现了“渐进式密码升级”：用户下次登录时，旧哈希会被透明地升级为新哈希，提升安全性而无需强制用户改密码。


# 密码加密
def set_hash_password(password: str):
    return pwd_context.hash(password)

# 密码验证      verify: 返回是 布尔型
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # plain_password：明文密码 hashed_password：密文密码