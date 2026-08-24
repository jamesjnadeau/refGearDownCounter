OPENSCAD ?= openscad
VENV     := .venv

.PHONY: test stl clean

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r requirements.txt
	touch $(VENV)

test: $(VENV)
	$(VENV)/bin/pytest -q

stl: build/down_indicator.stl

build/down_indicator.stl: down_indicator.scad $(wildcard lib/*.scad)
	@mkdir -p build
	$(OPENSCAD) -o $@ $<

clean:
	rm -rf build
