from models import HashNode
from hash_function import (calculate_V, calculate_hash)

class Hash_Table:
    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("Размер таблица должен быть больше 0")
        
        self.size = size
        self.table: list[HashNode | None] = [None] * size
        self.count = 0

    def add(self, key: str, value: str) -> bool:
        v = calculate_V(key)
        h = calculate_hash(key, self.size)

        new_node = HashNode(key=key, value=value, v=v, h=h)

        if self.table[h] is None:
            self.table[h] = new_node
            self.count += 1
            print(f"Добавлена запись. V = {v}, h = {h}")
            return True
        
        print(f"Обнаружена коллизия {h}.")
        print("Решаем коллизию")

        current = self.table[h]

        while current is not None:
            if current.key == key:
                print("Ошибка записи, этот ключ уже занят")
                return False
            
            if current.next is None:
                current.next = new_node
                self.count += 1
                print(f"Запись добавлена в цепочку V = {v}, h = {h}")
                return True
            
            current = current.next

        return False
    
    def get(self, key: str) -> str | None:
        h = calculate_hash(key, self.size)
        current = self.table[h]

        while current is not None:
            if current.key == key:
                return current.value
            
            current = current.next

        return None
    
    def update(self, key: str, new_value: str) -> bool:
        h = calculate_hash(key, self.size)
        current = self.table[h]

        while current is not None:
            if current.key == key:
                current.value = new_value
                print("Запись обновлена")
                return True
            
            current = current.next

        print("Запись не найдена")
        return False
    
    def delete(self, key: str) -> bool:
        h = calculate_hash(key, self.size)
        current = self.table[h]
        previous: HashNode | None = None

        while current is not None:
            if current.key == key:
                if previous is None:
                    self.table[h] = current.next
                else:
                    previous.next = current.next

                self.count -= 1
                print("Запись удалена")
                return True

            previous = current
            current = current.next

        print("Запись не найдена")
        return False
    
    def load_factor(self) -> float:
        return self.count / self.size
    
    def show(self) -> None:
        print("\nХеш-таблица:")
        print("-" * 80)

        for index, node in enumerate(self.table):
            if node is None:
                print(f"{index}: пусто")
                continue

            chain_parts = []
            current = node

            while current is not None:
                chain_parts.append(f"[kew={current.key}, value={current.value}, V={current.v}, h={current.h}]")
                current = current.next

            print(f"{index}:" + " -> ".join(chain_parts))

        print("-" * 80)
        print(f"Коэффициент заполнения: {self.load_factor():.2f}")

    def show_collisions(self) -> None:
        print ("\nКоллизии в хеш-таблице:")
        print("-" * 80)

        found_collision = False

        for index, node in enumerate(self.table):
            if node is None or node.next is None:
                continue

            found_collision = True
            chain_parts = []
            current = node

            while current is not None:
                chain_parts.append(
                    f"[key={current.key}, value={current.value}, V={current.v}, h={current.h}]"
                )
                current = current.next

            print(f"Индекс {index}: " + " -> ".join(chain_parts))

        if not found_collision:
            print("Коллизий нет.")

        print("-" * 80)