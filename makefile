all: compile


compile:
	@cls
	@python -m main

build:
	@cls
	@python build-create.py

icon:
	@cls
	@python create/createIcon.py

splash:
	@cls
	@python create/makePresplash.py
