from Database import User
from bitcoinlib.wallets import Wallet
from config import prefix, network


def check_balance(id):
    name = prefix + str(id)
    user = User()
    u = user.get_user(name)
    # print(u)
    w = Wallet(u[1])
    w.import_key(u[4], network=u[2])
    w.scan()
    info = w.get_key().as_dict(include_private=True)
    address = info["address"]
    # w.info()  <- Write information for terminal
    return f"""
💰 Your balance: {w.balance()}
🏦 Your address: `{address}`
    """


def user_check(id):
    name = prefix + str(id)
    user = User()
    u = user.get_user(name)
    if u is None:
        w = Wallet.create(name, network=network)
        w.scan()
        info = w.get_key().as_dict(include_private=True)
        address = info["address"]
        private = info["key_private"]
        c_id = info["id"]
        user.create_user(name, private, address, c_id, network=network)


def send(id, to, amount):
    name = prefix + str(id)
    user = User()
    u = user.get_user(name)
    w = Wallet(u[1])
    w.import_key(u[4], network=u[2])
    w.scan()
    try:
        t = w.send_to(to, amount, network=u[2], offline=True)
        t.send(offline=False)
        w.scan()
        return f"✅ Success \n📊 Transactions id: {t.transactions()}"
    except:
        return "‼️ Error for create transaction!"


def transactions_list(id):
    name = prefix + str(id)
    user = User()
    u = user.get_user(name)
    w = Wallet(u[1])
    w.import_key(u[4],network=u[2])
    w.scan()
    return w.utxos()
