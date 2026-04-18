Запуск unit-тестов:
python -m unittest discover -s tests -v

Запуск с покрытием:
coverage run --source=. -m unittest discover -s tests -v
coverage report -m
