GENERATE = python generate.py
GENERATE_OPTIONS = 
INKSCAPE = /usr/bin/inkscape
INKSCAPE_OPTIONS = --export-dpi=300 --without-gui
CONVERT = /usr/bin/convert

all: out.png

out.svg:
	$(GENERATE) $(GENERATE_OPTIONS)

out.png: out.svg
	$(INKSCAPE) $(INKSCAPE_OPTIONS) --export-area-canvas --export-png=out.png out.svg

bleed16-under.png:
	$(INKSCAPE) $(INKSCAPE_OPTIONS) --export-area-canvas --export-png=bleed16-under.png bleed16-under.svg

bleed16.png: out.png bleed16-under.png
	$(CONVERT) bleed16-under.png out.png -geometry +19+19 -composite bleed16.png

clean:
	rm -f out.svg out.png bleed16-under.png bleed16.png
