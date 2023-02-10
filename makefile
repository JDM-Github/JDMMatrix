all: compile


compile:
	@cls
	@python -m main

icon:
	@cls
	@python create/createIcon.py

splash:
	@cls
	@python create/makePresplash.py
