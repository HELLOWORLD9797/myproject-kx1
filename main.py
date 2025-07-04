import threading
import time
from eth_account import Account
from mnemonic import Mnemonic
import os

# 启用助记词钱包功能
Account.enable_unaudited_hdwallet_features()

# 配置参数
TARGET_SUFFIX = "888888"
NUM_THREADS = 20  # 根据你的系统核心数自动设置线程数
FOUND = False
LOCK = threading.Lock()
mnemo = Mnemonic("english")
START_TIME = time.time()

def generate_wallet(thread_id):
    global FOUND
    attempts = 0

    while not FOUND:
        # 生成助记词和地址
        words = mnemo.generate(strength=128)
        acct = Account.from_mnemonic(words, account_path="m/44'/60'/0'/0/0")
        address = acct.address.lower()
        attempts += 1

        # 匹配尾号
        if address.endswith(TARGET_SUFFIX):
            with LOCK:
                if not FOUND:
                    FOUND = True
                    print(f"\n✅ [线程 {thread_id}] 找到匹配地址！")
                    print(f"地址：{acct.address}")
                    print(f"私钥：{acct.key.hex()}")
                    print(f"助记词：{words}")
            break
        else:
            print(f"地址：{acct.address} 不满足!")

        if attempts % 500 == 0:
            print(f"[线程 {thread_id}] 已尝试 {attempts} 次...")

# 启动线程
threads = []
print(f"🚀 启动 {NUM_THREADS} 个线程查找以 {TARGET_SUFFIX} 结尾的钱包地址...")
for i in range(NUM_THREADS):
    t = threading.Thread(target=generate_wallet, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("🎯 搜索结束。")
