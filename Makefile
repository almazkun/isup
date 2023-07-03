k = ./tests/test_*.py

lint:
	pipenv run isort --force-single-line-imports --line-width 999 .
	pipenv run autoflake --ignore-init-module-imports --in-place --remove-all-unused-imports .
	pipenv run isort --use-parentheses --trailing-comma --multi-line 3 --force-grid-wrap 0 --line-width 140 .
	pipenv run black .
	
test:
	pipenv run python -m unittest ${k}

