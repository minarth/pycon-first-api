# This module is a abstract model usually replaced by database
# for sake of simplicity of the example we will keep it in memory
# and focus on API

from dataclasses import dataclass

@dataclass
class Client:
    uid: int
    first_name: str
    last_name: str


@dataclass
class Product:
    uid: int
    name: str


@dataclass
class ProductClient:
    uid: int
    client_id: int
    product_id: int
    params: dict


class Repository:

    def __init__(self, initial_values: dict) -> None:
        self.data = initial_values

    def _generate_uid(self):
        return max(self.data.keys())+1

    def add(self, uid, value):
        if uid is None: uid = self._generate_uid()
        value.uid = uid
        self.data[uid] = value
        
        return self.data[uid]


class ClientRepository(Repository):

    def __init__(self):
        super().__init__({
            0: Client(0, "Clark", "Kent"),
            1: Client(1, "Green", "Goblin")
        })


class ProductRepository(Repository):

    def __init__(self):
        super().__init__({
            10: Product(10, "Account")
        })


class ProductClientRepository(Repository):

    def __init__(self):
        super().__init__({
            100: ProductClient(100, 0, 10, {"balance": 1337., "currency": "CZK"}),
            101: ProductClient(101, 1, 10, {"balance": 50., "currency": "CZK"})
        })

