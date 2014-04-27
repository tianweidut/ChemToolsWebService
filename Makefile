dev_env:
	sh ./tools/build_env.sh dev

production_env:
	sh ./tools/build_env.sh production

unittest:
	sh ./tools/unittest.sh

web:
	python manage.py runserver
