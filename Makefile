k = ./tests/test_*.py

test:
	pipenv run python -m unittest ${k}
