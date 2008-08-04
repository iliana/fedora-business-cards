GENERATE = python generate.py
GENERATE_OPTIONS = 
INKSCAPE = /usr/bin/inkscape
INKSCAPE_OPTIONS = --export-dpi=300 --without-gui

all: out.png

out.svg:
	$(GENERATE) $(GENERATE_OPTIONS)

out.png: out.svg
	$(INKSCAPE) $(INKSCAPE_OPTIONS) --export-area-canvas --export-png=out.png out.svg
