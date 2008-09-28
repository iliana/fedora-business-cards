GENERATE = python generate.py
GENERATE_OPTIONS = 
INKSCAPE = /usr/bin/inkscape
INKSCAPE_OPTIONS = --export-dpi=300 --without-gui
CONVERT = /usr/bin/convert

all: out.png back.png

out.svg out.png out.pdf:
	$(GENERATE) $(GENERATE_OPTIONS)

back.png: back.svg
	$(INKSCAPE) $(INKSCAPE_OPTIONS) --export-area-canvas --export-png=$@ $<

bleed16-under.png:
	$(INKSCAPE) $(INKSCAPE_OPTIONS) --export-area-canvas --export-png=$@ $<

bleed16.png: out.png bleed16-under.png
	$(CONVERT) bleed16-under.png out.png -geometry +19+19 -composite bleed16.png

clean:
	rm -f out.svg out.png out.pdf bleed16-under.png bleed16.png back.png
