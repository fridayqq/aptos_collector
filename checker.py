from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
import requests

NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"

APT_RESOURCE = "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
LSD_RESOURCE = "0x1::coin::CoinStore<0x53a30a6e5936c0a4c5140daed34de39d17ca7fcae08f947c02e979cef98a3719::coin::LSD>"

def get_aptos_keys_from_mnemonic(mnemonic_phrase):
    seed_bytes = Bip39SeedGenerator(mnemonic_phrase).Generate()
    bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.APTOS).DeriveDefaultPath()
    privkey = bip44_ctx.PrivateKey().Raw().ToHex()
    pubkey = bip44_ctx.PublicKey().RawCompressed().ToHex()
    address = bip44_ctx.PublicKey().ToAddress()
    return privkey, pubkey, address

def get_token_balance(address, resource_string):
    url = f"{NODE_URL}/accounts/{address}/resource/{resource_string}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    value = int(data["data"]["coin"]["value"])
    return value / 1e8

def get_apt_price_usd():
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=aptos&vs_currencies=usd")
    if r.status_code == 200:
        return r.json().get("aptos", {}).get("usd", None)
    return None

apt_price_usd = get_apt_price_usd()

total_apt = 0.0
total_usd = 0.0

with open("seed.txt", "r", encoding="utf-8") as f:
    for i, mnemonic_phrase in enumerate(f):
        mnemonic_phrase = mnemonic_phrase.strip()
        if not mnemonic_phrase:
            continue
        try:
            privkey, pubkey, address = get_aptos_keys_from_mnemonic(mnemonic_phrase)
            apt_balance = get_token_balance(address, APT_RESOURCE)
            lsd_balance = get_token_balance(address, LSD_RESOURCE)

            apt_balance_str = f"{apt_balance} APT" if apt_balance is not None else "не удалось получить"
            lsd_balance_str = f"{lsd_balance} LSD" if lsd_balance is not None else "не удалось получить"

            if apt_balance is not None and apt_price_usd:
                apt_usd = apt_balance * apt_price_usd
                apt_usd_str = f"~ {apt_usd:.2f} $"
                total_apt += apt_balance
                total_usd += apt_usd
            else:
                apt_usd_str = "?"

            print(f"{i+1}) Сид: {mnemonic_phrase}")
            print(f"    Приватник: {privkey}")
            print(f"    Адрес:     {address}")
            print(f"    Баланс:    {apt_balance_str} ({apt_usd_str})")
            print(f"    LSD:       {lsd_balance_str}")
        except Exception as e:
            print(f"{i+1}) Ошибка с фразой: {mnemonic_phrase} -> {e}")
        print("-" * 40)

print(f"Итого по всем кошелькам:")
print(f"    {total_apt} APT")
if apt_price_usd:
    print(f"    ~ {total_usd:.2f} $")
else:
    print("    Курс APT не удалось получить")
