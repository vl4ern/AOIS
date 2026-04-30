import unittest
from contextlib import redirect_stdout
from io import StringIO

from hash_table import Hash_Table


class TestHashTable(unittest.TestCase):
    def setUp(self) -> None:
        self.hash_table = Hash_Table(size=20)

    def test_create_hash_table_with_invalid_size_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            Hash_Table(size=0)

    def test_add_record(self) -> None:
        with redirect_stdout(StringIO()):
            result = self.hash_table.add("ab", "first")

        self.assertTrue(result)
        self.assertEqual(self.hash_table.get("ab"), "first")
        self.assertEqual(self.hash_table.count, 1)

    def test_add_duplicate_key_returns_false(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            result = self.hash_table.add("ab", "second")

        self.assertFalse(result)
        self.assertEqual(self.hash_table.get("ab"), "first")
        self.assertEqual(self.hash_table.count, 1)

    def test_collision_creates_chain(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            self.hash_table.add("ba", "second")

        index = 15
        first_node = self.hash_table.table[index]
        second_node = first_node.next if first_node is not None else None

        self.assertIsNotNone(first_node)
        self.assertIsNotNone(second_node)
        self.assertEqual(first_node.key, "ab")
        self.assertEqual(second_node.key, "ba")
        self.assertEqual(self.hash_table.count, 2)

    def test_get_returns_none_if_key_not_found(self) -> None:
        result = self.hash_table.get("unknown")

        self.assertIsNone(result)

    def test_update_existing_record(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            result = self.hash_table.update("ab", "updated")

        self.assertTrue(result)
        self.assertEqual(self.hash_table.get("ab"), "updated")

    def test_update_missing_record_returns_false(self) -> None:
        with redirect_stdout(StringIO()):
            result = self.hash_table.update("unknown", "value")

        self.assertFalse(result)

    def test_delete_existing_record(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            result = self.hash_table.delete("ab")

        self.assertTrue(result)
        self.assertIsNone(self.hash_table.get("ab"))
        self.assertEqual(self.hash_table.count, 0)

    def test_delete_missing_record_returns_false(self) -> None:
        with redirect_stdout(StringIO()):
            result = self.hash_table.delete("unknown")

        self.assertFalse(result)

    def test_delete_first_node_in_collision_chain(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            self.hash_table.add("ba", "second")
            result = self.hash_table.delete("ab")

        self.assertTrue(result)
        self.assertIsNone(self.hash_table.get("ab"))
        self.assertEqual(self.hash_table.get("ba"), "second")
        self.assertEqual(self.hash_table.count, 1)

    def test_delete_second_node_in_collision_chain(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            self.hash_table.add("ba", "second")
            result = self.hash_table.delete("ba")

        self.assertTrue(result)
        self.assertEqual(self.hash_table.get("ab"), "first")
        self.assertIsNone(self.hash_table.get("ba"))
        self.assertEqual(self.hash_table.count, 1)

    def test_load_factor(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            self.hash_table.add("cd", "second")

        self.assertEqual(self.hash_table.load_factor(), 0.1)

    def test_show_outputs_hash_table(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")

        output = StringIO()

        with redirect_stdout(output):
            self.hash_table.show()

        self.assertIn("Хеш-таблица", output.getvalue())
        self.assertIn("ab", output.getvalue())

    def test_show_collisions_outputs_collision_chain(self) -> None:
        with redirect_stdout(StringIO()):
            self.hash_table.add("ab", "first")
            self.hash_table.add("ba", "second")

        output = StringIO()

        with redirect_stdout(output):
            self.hash_table.show_collisions()

        self.assertIn("Коллизии", output.getvalue())
        self.assertIn("ab", output.getvalue())
        self.assertIn("ba", output.getvalue())

    def test_show_collisions_without_collisions(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            self.hash_table.show_collisions()

        self.assertIn("Коллизий нет", output.getvalue())


if __name__ == "__main__":
    unittest.main()