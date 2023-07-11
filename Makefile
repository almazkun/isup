k = ./tests/test_*.py

lint:
	pipenv run isort --recursive --force-single-line-imports --line-width 999 .
	pipenv run autoflake --recursive --ignore-init-module-imports --in-place --remove-all-unused-imports .
	pipenv run isort --recursive --use-parentheses --trailing-comma --multi-line 3 --force-grid-wrap 0 --line-width 140 .
	pipenv run black .
	
test:
	pipenv run python -m unittest ${k}

check:
	PYTHONDONTWRITEBYTECODE=1 python3 -m isup.check \
	https://akun.dev/ \
	https://jeonse.akun.dev/ \
	https://shipper.akun.dev/ \
