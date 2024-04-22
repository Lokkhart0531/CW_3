from datetime import datetime


class Payment:
    """
    Весь этот класс занимается получением данных карты/счета.
    Преобразованием из формата Счет 10848359769870775355 в Счет **5355.
    Также, если это номер карты, то разбитие на блоки и приведение
    к нужному формату: Visa Classic 6831 98** **** 7658
    """
    def __init__(self, name, number):
        self.name = name
        self.number = number
    def __repr__(self):
        return f"Payment(name={self.name}, number={self.number})"


    @classmethod
    def init_from_str(cls, payment):
        *name, number = payment.split(' ')
        return cls(' '.join(name), number)


    def safe(self) -> str:
        if self.name.lower() == "счет":
            safe_number = self._get_safe_account()
        else:
            safe_number = self._get_safe_card_number
            safe_number = self.split_card_number_by_blocks(safe_number)
        return f"{self.name} {safe_number}"

    def _get_safe_account(self) -> str:
        return '*' * 2 + self.number[-4:]

    @property
    def _get_safe_card_number(self) -> str:
        start, middle, end = self.number[:6], self.number[6:-4], self.number[-4:]
        return start + "*" * len(middle) + end

    @staticmethod
    def split_card_number_by_blocks(card_number: str) -> str:
        return f'{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}'



class Amount:
    """
    Данный класс работает с денежной суммой. Разделение на
    name (валюта) и number（сумма)
    """
    def __init__(self, value, currency_name, currency_code):
        self.value = value
        self.currency_name = currency_name
        self.currency_code = currency_code

    def __repr__(self):
        return f"Amount(value={self.value}, currency_name={self.currency_name})"


class Operation:
    """
    В данном классе происходят все операции, те инициализация, работа с данными
    приведение даты к нужному формату из 2018-08-19 в 19.08.2018, возвращение откуда/куда с
    -> и приведение суммы к формату с двумя знаками после запятой из 79931.0 в 79931.03
    """
    def __init__(self, operation_id, state, operation_date, amount, description, payment_to, payment_from=None):
        self.id = operation_id
        self.state = state
        self.date = operation_date
        self.amount = amount
        self.description = description
        self.payment_to = payment_to
        self.payment_from = payment_from

    @classmethod
    def init_from_dict(cls, data: dict):
        return cls(operation_id=int(data["id"]), state=data["state"],
                    operation_date=datetime.fromisoformat(data["date"]),
                    amount=Amount(value=float(data["operationAmount"]["amount"]),
                                 currency_name=data["operationAmount"]["currency"]["name"],
                                 currency_code=data["operationAmount"]["currency"]["code"]),
                    description=data["description"], payment_to=Payment.init_from_str(data["to"]),
                    payment_from=Payment.init_from_str(data["from"]) if "from" in data else None)

    def __repr__(self):
        return (
            f"Operation({self.id}, {self.description}, state={self.state}, date={self.date}, amount={self.amount}, from={self.payment_from}, to={self.payment_to}")

    def save(self) -> str:
        lines = [f"{self.date.strftime('%d.%m.%Y')} {self.description}"]
        if self.payment_from:
            lines.append(f"{self.payment_from.safe()} -> {self.payment_to.safe()}")
        else:
            lines.append(f"{self.payment_to.safe()}")
        lines.append(f"{self.amount.value:.2f} {self.amount.currency_name}")
        return "\n".join(lines)
