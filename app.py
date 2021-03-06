from hdwallet import BIP44HDWallet
from hdwallet.utils import generate_mnemonic
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import BitcoinMainnet, EthereumMainnet
from bip_utils import Bip84, Bip84Coins, Bip44Changes, Bip39SeedGenerator
import requests
import os
import time
import base64
import telega

def writeto(mnemonic, wallet, balance):
    f = open(os.path.join(os.path.dirname(__file__), 'wallets.txt'), "a")
    f.write(mnemonic + "\n" + wallet + "\n" + balance + "\n" + "|------------------------------------------------------------|")
    f.close()

LanguageInMnemonic = "english"
BalanceUrl = "https://blockchain.info/q/addressbalance/"

def main(start):
    Mnemonic = generate_mnemonic(language = LanguageInMnemonic, strength = 128)
    Seed = Bip39SeedGenerator(Mnemonic).Generate()
    CheckedWalletBTCBip84 = Bip84.FromSeed(Seed, Bip84Coins.BITCOIN)
    CheckedWalletBTCBip84Step1 = (CheckedWalletBTCBip84.Purpose().Coin().Account(0)).Change(Bip44Changes.CHAIN_EXT)
    CheckedWalletBTCBip84Step2 = CheckedWalletBTCBip84Step1.AddressIndex(0)
    CheckedAddressBTCBip84 = CheckedWalletBTCBip84Step2.PublicKey().ToAddress()


    #print(Seed)
    
    r = requests.get(BalanceUrl + CheckedAddressBTCBip84)

    if (r.status_code == 200) :
        Balance = int(r.text)/100000000
        print("Balance: " + str(Balance) + " BTC | " + "Address: " + CheckedAddressBTCBip84 + " | " + "Mnemonic: " + Mnemonic)
        if(Balance != 0.0):
            telega.restart('Balance: {} BTC | Address: {} | Mnemonic: {}'.format(Balance, CheckedAddressBTCBip84, Mnemonic))
            writeto(str(Mnemonic), str(CheckedAddressBTCBip84), str(Balance))
    time.sleep(3)               #if time < 3 server give permanent ban by ip
    return 1
    
if __name__ == "__main__":
    start = 1
    while start:
        start = main(start)
