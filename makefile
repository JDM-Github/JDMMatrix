all: compile


compile:
	@cls
	@python -m main

build:
	@cls
	@python buildozer-create.py

icon:
	@cls
	@python create/createIcon.py

splash:
	@cls
	@python create/makePresplash.py
