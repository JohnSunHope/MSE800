import urllib.request
import zlib
from pathlib import Path
from typing import Final


PLANTUML_SERVER: Final[str] = "https://www.plantuml.com/plantuml/png/"
USER_AGENT: Final[str] = "Mozilla/5.0"


USE_CASE_1_CUSTOMER_EXCHANGE: Final[str] = """@startuml
left to right direction

actor Customer
actor "Teller/Staff" as Teller
actor "FX Rate Service" as Rates

rectangle "Money Exchange System" {
  usecase "Register / Update Profile" as UC_Profile
  usecase "Open Account" as UC_OpenAcct
  usecase "View Balance" as UC_Balance
  usecase "Deposit Funds" as UC_Deposit
  usecase "Withdraw Funds" as UC_Withdraw
  usecase "Get Exchange Quote" as UC_Quote
  usecase "Execute Currency Exchange" as UC_Exchange
  usecase "Record Transaction" as UC_Txn
  usecase "Record Exchange Details" as UC_ExRec
  usecase "Update Account Balance" as UC_UpdateBal
  usecase "Generate Receipt" as UC_Receipt
  usecase "View Transaction History" as UC_History
  usecase "Fetch Current Rates" as UC_FetchRates
  usecase "Calculate Converted Amount" as UC_Calc
}

Customer --> UC_Profile
Customer --> UC_OpenAcct
Customer --> UC_Balance
Customer --> UC_Quote
Customer --> UC_Exchange
Customer --> UC_History

Teller --> UC_Deposit
Teller --> UC_Withdraw
Teller --> UC_Exchange
Teller --> UC_Receipt

UC_Quote ..> UC_FetchRates : <<include>>
UC_Quote ..> UC_Calc : <<include>>
UC_Exchange ..> UC_FetchRates : <<include>>
UC_Exchange ..> UC_Calc : <<include>>
UC_Exchange ..> UC_Txn : <<include>>
UC_Exchange ..> UC_ExRec : <<include>>
UC_Exchange ..> UC_UpdateBal : <<include>>
UC_Exchange ..> UC_Receipt : <<include>>

Rates --> UC_FetchRates
@enduml
"""


USE_CASE_2_ADMIN_OPERATIONS: Final[str] = """@startuml
left to right direction

actor Admin
actor "Compliance Officer" as Compliance
actor "FX Rate Provider" as Provider

rectangle "Money Exchange System" {
  usecase "Manage Customers (CRUD)" as UC_CustCRUD
  usecase "Manage Accounts (CRUD)" as UC_AcctCRUD
  usecase "Manage Currencies (CRUD)" as UC_CcyCRUD
  usecase "Update Exchange Rates" as UC_RatesUpdate
  usecase "Import Rates Automatically" as UC_RatesAuto
  usecase "Set Rates Manually" as UC_RatesManual
  usecase "Review Transactions" as UC_ReviewTxn
  usecase "Flag / Investigate Transaction" as UC_Flag
  usecase "Generate Reports" as UC_Reports
  usecase "Audit Trail Review" as UC_Audit
  usecase "Backup / Restore Database" as UC_Backup
}

Admin --> UC_CustCRUD
Admin --> UC_AcctCRUD
Admin --> UC_CcyCRUD
Admin --> UC_RatesUpdate
Admin --> UC_ReviewTxn
Admin --> UC_Reports
Admin --> UC_Backup

Compliance --> UC_ReviewTxn
Compliance --> UC_Flag
Compliance --> UC_Audit
Compliance --> UC_Reports

UC_RatesUpdate ..> UC_RatesAuto : <<extend>>
UC_RatesUpdate ..> UC_RatesManual : <<extend>>
Provider --> UC_RatesAuto
UC_ReviewTxn ..> UC_Flag : <<extend>>
@enduml
"""


ALPHABET: Final[str] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def _encode6bit(b: int) -> str:
    return ALPHABET[b]


def _append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return "".join(
        (
            _encode6bit(c1 & 0x3F),
            _encode6bit(c2 & 0x3F),
            _encode6bit(c3 & 0x3F),
            _encode6bit(c4 & 0x3F),
        )
    )


def plantuml_encode(text: str) -> str:
    data = text.encode("utf-8")
    compressed = zlib.compress(data)[2:-4]
    out: list[str] = []
    for i in range(0, len(compressed), 3):
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < len(compressed) else 0
        b3 = compressed[i + 2] if i + 2 < len(compressed) else 0
        out.append(_append3bytes(b1, b2, b3))
    return "".join(out)


def fetch_png(puml_text: str) -> bytes:
    encoded = plantuml_encode(puml_text)
    url = f"{PLANTUML_SERVER}{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    (out_dir / "use_case_diagram_1_customer_exchange.png").write_bytes(
        fetch_png(USE_CASE_1_CUSTOMER_EXCHANGE)
    )
    (out_dir / "use_case_diagram_2_admin_operations.png").write_bytes(
        fetch_png(USE_CASE_2_ADMIN_OPERATIONS)
    )


if __name__ == "__main__":
    main()
