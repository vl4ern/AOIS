def calculate_V(key: str) -> str:
    if not key:
        raise ValueError("Ключ не может быть пустым")
    
    return sum(ord(char) for char in key)

def calculate_hash(key: str, table_size: int) -> int:
    if table_size <= 0:
        raise ValueError("Размер таблицы должен быть больше 0")
    
    V = calculate_V(key)
    return V % table_size