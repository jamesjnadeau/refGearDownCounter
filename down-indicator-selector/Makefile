OPENSCAD ?= openscad
VENV     := .venv
PARTS    := down_indicator_selector \
            down_indicator_selector_bottom \
            down_indicator_selector_button
STLS     := $(addprefix build/,$(addsuffix .stl,$(PARTS)))

.PHONY: test stl clean

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r requirements.txt
	touch $(VENV)

test: $(VENV)
	$(VENV)/bin/pytest -q

stl: $(STLS)
	@ls -lh $^ | awk '{print "ready: " $$9 " (" $$5 ")"}'

build/%.stl: %.scad $(wildcard lib/*.scad)
	@mkdir -p build
	$(OPENSCAD) -o $@ $<

clean:
	rm -rf build
