import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional


DB_PATH = Path(__file__).with_name("finance.db")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                address TEXT,
                date_of_birth TEXT
            );

            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL UNIQUE,
                account_type TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                status TEXT NOT NULL,
                account_id INTEGER NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS currencies (
                currency_code TEXT PRIMARY KEY,
                currency_name TEXT NOT NULL,
                symbol TEXT,
                country TEXT,
                exchange_rate REAL
            );

            CREATE TABLE IF NOT EXISTS exchanges (
                exchange_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange_date TEXT NOT NULL,
                amount_from REAL NOT NULL,
                amount_to REAL NOT NULL,
                rate_used REAL NOT NULL,
                from_currency_code TEXT NOT NULL,
                to_currency_code TEXT NOT NULL,
                transaction_id INTEGER UNIQUE,
                FOREIGN KEY (from_currency_code) REFERENCES currencies(currency_code) ON DELETE RESTRICT,
                FOREIGN KEY (to_currency_code) REFERENCES currencies(currency_code) ON DELETE RESTRICT,
                FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
            );
            """
        )


def prompt(text: str) -> str:
    return input(text).strip()


def prompt_optional(text: str) -> Optional[str]:
    value = input(text).strip()
    return value if value else None


def prompt_int(text: str) -> int:
    while True:
        value = input(text).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter an integer.")


def prompt_float(text: str) -> float:
    while True:
        value = input(text).strip()
        try:
            return float(value)
        except ValueError:
            print("Please enter a number.")


def prompt_update(current: Optional[str], field_name: str) -> Optional[str]:
    value = input(f"{field_name} (Current: {current if current is not None else ''}),Enter to skip: ").strip()
    return value if value != "" else None


def print_rows(rows: Iterable[sqlite3.Row]) -> None:
    rows = list(rows)
    if not rows:
        print("No data.")
        return
    columns = rows[0].keys()
    widths = {col: max(len(col), *(len(str(r[col])) for r in rows)) for col in columns}
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    print(header)
    print("-" * len(header))
    for r in rows:
        print(" | ".join(str(r[col]).ljust(widths[col]) for col in columns))


def create_customer() -> None:
    first_name = prompt("FirstName: ")
    last_name = prompt("LastName: ")
    email = prompt("Email: ")
    phone = prompt_optional("Phone (optional): ")
    address = prompt_optional("Address (optional): ")
    dob = prompt_optional("DateOfBirth (YYYY-MM-DD,optional): ")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO customers (first_name, last_name, email, phone, address, date_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (first_name, last_name, email, phone, address, dob),
        )
    print("Customer created.")


def list_customers() -> None:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM customers ORDER BY customer_id").fetchall()
    print_rows(rows)


def update_customer() -> None:
    customer_id = prompt_int("CustomerID: ")
    with connect() as conn:
        row = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
        if not row:
            print("Customer not found.")
            return
        first_name = prompt_update(row["first_name"], "FirstName")
        last_name = prompt_update(row["last_name"], "LastName")
        email = prompt_update(row["email"], "Email")
        phone = prompt_update(row["phone"], "Phone")
        address = prompt_update(row["address"], "Address")
        dob = prompt_update(row["date_of_birth"], "DateOfBirth")

        updates: dict[str, Any] = {}
        if first_name is not None:
            updates["first_name"] = first_name
        if last_name is not None:
            updates["last_name"] = last_name
        if email is not None:
            updates["email"] = email
        if phone is not None:
            updates["phone"] = phone
        if address is not None:
            updates["address"] = address
        if dob is not None:
            updates["date_of_birth"] = dob

        if not updates:
            print("No changes.")
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        conn.execute(
            f"UPDATE customers SET {set_clause} WHERE customer_id = ?",
            (*updates.values(), customer_id),
        )
    print("Customer updated.")


def delete_customer() -> None:
    customer_id = prompt_int("CustomerID: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
    print("Customer deleted." if cur.rowcount else "Customer not found.")


def create_account() -> None:
    customer_id = prompt_int("CustomerID: ")
    account_number = prompt("AccountNumber: ")
    account_type = prompt("AccountType: ")
    balance = prompt_float("Balance: ")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO accounts (account_number, account_type, balance, customer_id)
            VALUES (?, ?, ?, ?)
            """,
            (account_number, account_type, balance, customer_id),
        )
    print("Account created.")


def list_accounts() -> None:
    customer_filter = prompt_optional("CustomerID filter(Enter to skip): ")
    with connect() as conn:
        if customer_filter:
            rows = conn.execute(
                "SELECT * FROM accounts WHERE customer_id = ? ORDER BY account_id",
                (int(customer_filter),),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM accounts ORDER BY account_id").fetchall()
    print_rows(rows)


def update_account() -> None:
    account_id = prompt_int("AccountID: ")
    with connect() as conn:
        row = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,)).fetchone()
        if not row:
            print("Account not found.")
            return
        account_number = prompt_update(row["account_number"], "AccountNumber")
        account_type = prompt_update(row["account_type"], "AccountType")
        balance_str = input(f"Balance (Current: {row['balance']}),Enter to skip: ").strip()
        customer_id_str = input(f"CustomerID (Current: {row['customer_id']}),Enter to skip: ").strip()

        updates: dict[str, Any] = {}
        if account_number is not None:
            updates["account_number"] = account_number
        if account_type is not None:
            updates["account_type"] = account_type
        if balance_str != "":
            updates["balance"] = float(balance_str)
        if customer_id_str != "":
            updates["customer_id"] = int(customer_id_str)

        if not updates:
            print("No changes.")
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        conn.execute(
            f"UPDATE accounts SET {set_clause} WHERE account_id = ?",
            (*updates.values(), account_id),
        )
    print("Account updated.")


def delete_account() -> None:
    account_id = prompt_int("AccountID: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
    print("Account deleted." if cur.rowcount else "Account not found.")


def create_transaction() -> None:
    account_id = prompt_int("AccountID: ")
    transaction_date = prompt("TransactionDate (YYYY-MM-DD): ")
    amount = prompt_float("Amount: ")
    transaction_type = prompt("TransactionType: ")
    status = prompt("Status: ")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO transactions (transaction_date, amount, transaction_type, status, account_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (transaction_date, amount, transaction_type, status, account_id),
        )
    print("Transaction created.")


def list_transactions() -> None:
    account_filter = prompt_optional("AccountID filter(Enter to skip): ")
    with connect() as conn:
        if account_filter:
            rows = conn.execute(
                "SELECT * FROM transactions WHERE account_id = ? ORDER BY transaction_id",
                (int(account_filter),),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM transactions ORDER BY transaction_id").fetchall()
    print_rows(rows)


def update_transaction() -> None:
    transaction_id = prompt_int("TransactionID: ")
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM transactions WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()
        if not row:
            print("Transaction not found.")
            return
        transaction_date = prompt_update(row["transaction_date"], "TransactionDate")
        amount_str = input(f"Amount (Current: {row['amount']}),Enter to skip: ").strip()
        transaction_type = prompt_update(row["transaction_type"], "TransactionType")
        status = prompt_update(row["status"], "Status")
        account_id_str = input(f"AccountID (Current: {row['account_id']}),Enter to skip: ").strip()

        updates: dict[str, Any] = {}
        if transaction_date is not None:
            updates["transaction_date"] = transaction_date
        if amount_str != "":
            updates["amount"] = float(amount_str)
        if transaction_type is not None:
            updates["transaction_type"] = transaction_type
        if status is not None:
            updates["status"] = status
        if account_id_str != "":
            updates["account_id"] = int(account_id_str)

        if not updates:
            print("No changes.")
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        conn.execute(
            f"UPDATE transactions SET {set_clause} WHERE transaction_id = ?",
            (*updates.values(), transaction_id),
        )
    print("Transaction updated.")


def delete_transaction() -> None:
    transaction_id = prompt_int("TransactionID: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
    print("Transaction deleted." if cur.rowcount else "Transaction not found.")


def create_currency() -> None:
    currency_code = prompt("CurrencyCode: ")
    currency_name = prompt("CurrencyName: ")
    symbol = prompt_optional("Symbol (optional): ")
    country = prompt_optional("Country (optional): ")
    exchange_rate_str = prompt_optional("ExchangeRate (optional): ")
    exchange_rate = float(exchange_rate_str) if exchange_rate_str else None
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO currencies (currency_code, currency_name, symbol, country, exchange_rate)
            VALUES (?, ?, ?, ?, ?)
            """,
            (currency_code, currency_name, symbol, country, exchange_rate),
        )
    print("Currency created.")


def list_currencies() -> None:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM currencies ORDER BY currency_code").fetchall()
    print_rows(rows)


def update_currency() -> None:
    currency_code = prompt("CurrencyCode: ")
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM currencies WHERE currency_code = ?",
            (currency_code,),
        ).fetchone()
        if not row:
            print("Currency not found.")
            return
        currency_name = prompt_update(row["currency_name"], "CurrencyName")
        symbol = prompt_update(row["symbol"], "Symbol")
        country = prompt_update(row["country"], "Country")
        exchange_rate_str = input(f"ExchangeRate (Current: {row['exchange_rate']}),Enter to skip: ").strip()

        updates: dict[str, Any] = {}
        if currency_name is not None:
            updates["currency_name"] = currency_name
        if symbol is not None:
            updates["symbol"] = symbol
        if country is not None:
            updates["country"] = country
        if exchange_rate_str != "":
            updates["exchange_rate"] = float(exchange_rate_str)

        if not updates:
            print("No changes.")
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        conn.execute(
            f"UPDATE currencies SET {set_clause} WHERE currency_code = ?",
            (*updates.values(), currency_code),
        )
    print("Currency updated.")


def delete_currency() -> None:
    currency_code = prompt("CurrencyCode: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM currencies WHERE currency_code = ?", (currency_code,))
    print("Currency deleted." if cur.rowcount else "Currency not found.")


def create_exchange() -> None:
    exchange_date = prompt("ExchangeDate (YYYY-MM-DD): ")
    amount_from = prompt_float("AmountFrom: ")
    amount_to = prompt_float("AmountTo: ")
    rate_used = prompt_float("RateUsed: ")
    from_currency_code = prompt("FromCurrencyCode: ")
    to_currency_code = prompt("ToCurrencyCode: ")
    transaction_id_str = prompt_optional("TransactionID (optional,1:1): ")
    transaction_id = int(transaction_id_str) if transaction_id_str else None
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO exchanges (
                exchange_date, amount_from, amount_to, rate_used,
                from_currency_code, to_currency_code, transaction_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                exchange_date,
                amount_from,
                amount_to,
                rate_used,
                from_currency_code,
                to_currency_code,
                transaction_id,
            ),
        )
    print("Exchange created.")


def list_exchanges() -> None:
    transaction_filter = prompt_optional("TransactionID filter(Enter to skip): ")
    with connect() as conn:
        if transaction_filter:
            rows = conn.execute(
                "SELECT * FROM exchanges WHERE transaction_id = ? ORDER BY exchange_id",
                (int(transaction_filter),),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM exchanges ORDER BY exchange_id").fetchall()
    print_rows(rows)


def update_exchange() -> None:
    exchange_id = prompt_int("ExchangeID: ")
    with connect() as conn:
        row = conn.execute("SELECT * FROM exchanges WHERE exchange_id = ?", (exchange_id,)).fetchone()
        if not row:
            print("Exchange not found.")
            return
        exchange_date = prompt_update(row["exchange_date"], "ExchangeDate")
        amount_from_str = input(f"AmountFrom (Current: {row['amount_from']}), Enter to skip: ").strip()
        amount_to_str = input(f"AmountTo (Current: {row['amount_to']}), Enter to skip: ").strip()
        rate_used_str = input(f"RateUsed (Current: {row['rate_used']}), Enter to skip: ").strip()
        from_currency_code = prompt_update(row["from_currency_code"], "FromCurrencyCode")
        to_currency_code = prompt_update(row["to_currency_code"], "ToCurrencyCode")
        transaction_id_str = input(
            f"TransactionID (Current: {row['transaction_id']}), Enter to skip: "
        ).strip()

        updates: dict[str, Any] = {}
        if exchange_date is not None:
            updates["exchange_date"] = exchange_date
        if amount_from_str != "":
            updates["amount_from"] = float(amount_from_str)
        if amount_to_str != "":
            updates["amount_to"] = float(amount_to_str)
        if rate_used_str != "":
            updates["rate_used"] = float(rate_used_str)
        if from_currency_code is not None:
            updates["from_currency_code"] = from_currency_code
        if to_currency_code is not None:
            updates["to_currency_code"] = to_currency_code
        if transaction_id_str != "":
            updates["transaction_id"] = int(transaction_id_str) if transaction_id_str else None

        if not updates:
            print("No changes.")
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        conn.execute(
            f"UPDATE exchanges SET {set_clause} WHERE exchange_id = ?",
            (*updates.values(), exchange_id),
        )
    print("Exchange updated.")


def delete_exchange() -> None:
    exchange_id = prompt_int("ExchangeID: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM exchanges WHERE exchange_id = ?", (exchange_id,))
    print("Exchange deleted." if cur.rowcount else "Exchange not found.")


@dataclass(frozen=True)
class MenuItem:
    key: str
    label: str
    action: Optional[callable]


def run_menu(title: str, items: list[MenuItem]) -> None:
    while True:
        print(f"\n==== {title} ====")
        for item in items:
            print(f"{item.key}. {item.label}")
        choice = input("Select: ").strip()
        match = next((i for i in items if i.key == choice), None)
        if not match:
            print("Invalid option.")
            continue
        if match.action is None:
            return
        try:
            match.action()
        except sqlite3.IntegrityError as e:
            print(f"Database constraint error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")
        except ValueError as e:
            print(f"Input error: {e}")


def customers_menu() -> None:
    run_menu(
        "Customers",
        [
            MenuItem("1", "Create", create_customer),
            MenuItem("2", "List", list_customers),
            MenuItem("3", "Update", update_customer),
            MenuItem("4", "Delete", delete_customer),
            MenuItem("0", "Back", None),
        ],
    )


def accounts_menu() -> None:
    run_menu(
        "Accounts",
        [
            MenuItem("1", "Create", create_account),
            MenuItem("2", "List", list_accounts),
            MenuItem("3", "Update", update_account),
            MenuItem("4", "Delete", delete_account),
            MenuItem("0", "Back", None),
        ],
    )


def transactions_menu() -> None:
    run_menu(
        "Transactions",
        [
            MenuItem("1", "Create", create_transaction),
            MenuItem("2", "List", list_transactions),
            MenuItem("3", "Update", update_transaction),
            MenuItem("4", "Delete", delete_transaction),
            MenuItem("0", "Back", None),
        ],
    )


def currencies_menu() -> None:
    run_menu(
        "Currencies",
        [
            MenuItem("1", "Create", create_currency),
            MenuItem("2", "List", list_currencies),
            MenuItem("3", "Update", update_currency),
            MenuItem("4", "Delete", delete_currency),
            MenuItem("0", "Back", None),
        ],
    )


def exchanges_menu() -> None:
    run_menu(
        "Exchanges",
        [
            MenuItem("1", "Create", create_exchange),
            MenuItem("2", "List", list_exchanges),
            MenuItem("3", "Update", update_exchange),
            MenuItem("4", "Delete", delete_exchange),
            MenuItem("0", "Back", None),
        ],
    )


def main() -> None:
    init_db()
    run_menu(
        "Finance DB",
        [
            MenuItem("1", "Customers", customers_menu),
            MenuItem("2", "Accounts", accounts_menu),
            MenuItem("3", "Transactions", transactions_menu),
            MenuItem("4", "Currencies", currencies_menu),
            MenuItem("5", "Exchanges", exchanges_menu),
            MenuItem("0", "Exit", None),
        ],
    )


if __name__ == "__main__":
    main()
