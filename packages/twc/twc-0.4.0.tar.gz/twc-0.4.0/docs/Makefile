OUT_DIR=build
BOOK_DIR=$(OUT_DIR)/book
MAN_DIR=$(OUT_DIR)/man/man1

BOOK_SRC = index.adoc
MAN_SRC = twc.1.adoc

GEN = ../devtools/gen-in
VERSION = $(shell ../devtools/gen-version)

ASCIIDOC = asciidoctor -a "revnumber=$(VERSION)"

.PHONY: all
all: book man

.PHONY: book
book: $(BOOK_SRC)
	mkdir -p $(BOOK_DIR)
	$(ASCIIDOC) $^ -o $(BOOK_DIR)/twc.html

.PHONY: man
man: $(MAN_SRC)
	mkdir -p $(MAN_DIR)
	$(ASCIIDOC) -d manpage -b manpage -o $(MAN_DIR)/twc.1 $<
	$(ASCIIDOC) -d manpage -o $(MAN_DIR)/twc.1.html $<

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)

%.adoc: %.adoc.in
	$(GEN) $< > $@
