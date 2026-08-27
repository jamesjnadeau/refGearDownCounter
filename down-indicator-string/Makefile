OPENSCAD ?= openscad
VENV     := .venv

# OpenSCAD reaches the vendored Archivo faces only through fontconfig; without
# this it silently substitutes another face instead of failing.
export FONTCONFIG_FILE := $(CURDIR)/fonts/fonts.conf

.PHONY: test stl clean

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r requirements.txt
	touch $(VENV)

test: $(VENV)
	$(VENV)/bin/pytest -q

stl: build/down_indicator_string.stl
	@ls -lh $< | awk '{print "ready: $< (" $$5 ")"}'

build/down_indicator_string.stl: down_indicator_string.scad $(wildcard lib/*.scad) $(wildcard fonts/*.ttf)
	@mkdir -p build
	$(OPENSCAD) -o $@ $<

clean:
	rm -rf build
