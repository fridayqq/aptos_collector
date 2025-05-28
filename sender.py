import requests
import json
import time
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
import nacl.signing
import nacl.encoding

NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"
EXPLORER_URL = "https://explorer.aptoslabs.com/txn/{}?network=mainnet"

def get_account_from_mnemonic(mnemonic_phrase):
    seed_bytes = Bip39SeedGenerator(mnemonic_phrase).Generate()
    bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.APTOS).DeriveDefaultPath()
    privkey_bytes = bip44_ctx.PrivateKey().Raw().ToBytes()
    signing_key = nacl.signing.SigningKey(privkey_bytes)
    address = bip44_ctx.PublicKey().ToAddress()
    pubkey_bytes = bip44_ctx.PublicKey().RawCompressed().ToBytes()
    return signing_key, pubkey_bytes, address

def get_sequence_number(address):
    url = f"{NODE_URL}/accounts/{address}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Ошибка получения sequence_number")
    return int(r.json()["sequence_number"])

def get_apt_balance(address):
    url = f"{NODE_URL}/accounts/{address}/resource/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    r = requests.get(url)
    if r.status_code != 200:
        return 0
    data = r.json()
    return int(data["data"]["coin"]["value"]) / 1e8

def check_coinstore_exists(address):
    """Check if the account has APT CoinStore registered"""
    url = f"{NODE_URL}/accounts/{address}/resource/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    r = requests.get(url)
    return r.status_code == 200

def register_coinstore(signing_key, sender_address, seq_num):
    """Register APT CoinStore for the account"""
    payload = {
        "type": "entry_function_payload",
        "function": "0x1::managed_coin::register",
        "type_arguments": ["0x1::aptos_coin::AptosCoin"],
        "arguments": []
    }
    
    txn = {
        "sender": sender_address,
        "sequence_number": str(seq_num),
        "max_gas_amount": "2000",
        "gas_unit_price": "100",
        "expiration_timestamp_secs": str(int(time.time()) + 600),
        "payload": payload
    }
    
    headers = {'Content-Type': 'application/json'}
    sim_url = f"{NODE_URL}/transactions/encode_submission"
    resp = requests.post(sim_url, data=json.dumps(txn), headers=headers)
    if resp.status_code != 200:
        print(f"Ошибка encode_submission для регистрации: {resp.text}")
        return None
    
    to_sign_hex = resp.json()
    to_sign = bytes.fromhex(to_sign_hex[2:] if to_sign_hex.startswith('0x') else to_sign_hex)
    signature = signing_key.sign(to_sign).signature.hex()
    pubkey = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
    
    submit_tx = {
        "sender": sender_address,
        "sequence_number": str(seq_num),
        "max_gas_amount": "2000",
        "gas_unit_price": "100",
        "expiration_timestamp_secs": txn["expiration_timestamp_secs"],
        "payload": payload,
        "signature": {
            "type": "ed25519_signature",
            "public_key": f"0x{pubkey}",
            "signature": f"0x{signature}"
        }
    }
    
    submit_url = f"{NODE_URL}/transactions"
    resp = requests.post(submit_url, data=json.dumps(submit_tx), headers=headers)
    if resp.status_code == 202:
        tx_hash = resp.json()['hash']
        print(f"Регистрация CoinStore: {tx_hash}")
        return tx_hash
    else:
        print(f"Ошибка регистрации CoinStore: {resp.text}")
        return None

def send_apt(signing_key, sender_address, to_address, amount_apt, seq_num):
    payload = {
        "type": "entry_function_payload",
        "function": "0x1::aptos_account::transfer",
        "type_arguments": [],
        "arguments": [to_address, str(int(amount_apt * 1e8))]
    }
    txn = {
        "sender": sender_address,
        "sequence_number": str(seq_num),
        "max_gas_amount": "2000",  # Increased for auto-registration
        "gas_unit_price": "100",
        "expiration_timestamp_secs": str(int(time.time()) + 600),
        "payload": payload
    }
    headers = {'Content-Type': 'application/json'}
    sim_url = f"{NODE_URL}/transactions/encode_submission"
    resp = requests.post(sim_url, data=json.dumps(txn), headers=headers)
    if resp.status_code != 200:
        print(f"Ошибка encode_submission: {resp.text}")
        return None
    to_sign_hex = resp.json()
    to_sign = bytes.fromhex(to_sign_hex[2:] if to_sign_hex.startswith('0x') else to_sign_hex)
    signature = signing_key.sign(to_sign).signature.hex()
    pubkey = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
    submit_tx = {
        "sender": sender_address,
        "sequence_number": str(seq_num),
        "max_gas_amount": "2000",
        "gas_unit_price": "100",
        "expiration_timestamp_secs": txn["expiration_timestamp_secs"],
        "payload": payload,
        "signature": {
            "type": "ed25519_signature",
            "public_key": f"0x{pubkey}",
            "signature": f"0x{signature}"
        }
    }
    submit_url = f"{NODE_URL}/transactions"
    resp = requests.post(submit_url, data=json.dumps(submit_tx), headers=headers)
    if resp.status_code == 202:
        tx_hash = resp.json()['hash']
        print(f"TX отправлен: {tx_hash}")
        print(f"Ссылка: {EXPLORER_URL.format(tx_hash)}")
        return tx_hash
    else:
        print(f"Ошибка отправки: {resp.text}")
        return None

def check_tx_status(tx_hash, max_attempts=12, delay=5):
    url = f"{NODE_URL}/transactions/by_hash/{tx_hash}"
    for attempt in range(1, max_attempts + 1):
        r = requests.get(url)
        if r.status_code == 200:
            tx = r.json()
            status = tx.get('success')
            vm_status = tx.get('vm_status', '').lower() if tx.get('vm_status') else ''
            print(f"[{attempt}] TX статус: success={status}, vm_status='{vm_status}'")
            if status is True or 'executed' in vm_status:
                print("✅ Транзакция подтверждена и исполнена!")
                return True
            elif "move abort" in vm_status or "abort" in vm_status or "failure" in vm_status:
                print(f"❌ Транзакция завершилась ошибкой:\n{vm_status}")
                return False
            # Если неуспех и не ошибка - ждём дальше (может быть pending)
        else:
            print(f"[{attempt}] Ожидаем появление транзакции...")

        time.sleep(delay)
    print("‼️ Не удалось подтвердить исполнение транзакции по API Aptos. Проверьте вручную в эксплорере (иногда статус появляется с задержкой).")
    return None

# -------------- ОСНОВНОЙ ЦИКЛ --------------

with open("to_send.txt", "r", encoding="utf-8") as f:
    for line in f:
        if ";" not in line: continue
        mnemonic, to_addr = [x.strip() for x in line.split(";")]
        try:
            signing_key, pubkey_bytes, address = get_account_from_mnemonic(mnemonic)
            balance = get_apt_balance(address)
            print(f"\nКошелёк:    {address}")
            print(f"Получатель: {to_addr}")
            print(f"Баланс:     {balance} APT")
            
            seq = get_sequence_number(address)
            send_amount = max(0, balance - 0.01)
            if send_amount <= 0:
                print("Баланс слишком мал для отправки")
                continue
                
            tx_hash = send_apt(signing_key, address, to_addr, send_amount, seq)
            if not tx_hash:
                continue
            ok = check_tx_status(tx_hash)
            if ok is True:
                print("✅ Отправка подтверждена!\n")
            elif ok is False:
                print("❌ В транзакции ошибка! Проверьте детали выше и ссылку в эксплорере.\n")
            else:
                print("⚠️ Статус не определён (API не ответил однозначно). Проверьте TX в эксплорере вручную.\n")
            print("-" * 40)
        except Exception as e:
            print(f"Ошибка: {e}")