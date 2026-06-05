# Makefile — Tarifit-cursus: regenereer _ai/ uit de canonieke bronnen en bewaak drift + NL/EN-pariteit.
#
#   make build   regenereert alle _ai/*.md uit CSV + HTML (elk met "niet met de hand bewerken"-banner)
#   make parity  vergelijkt de Tarifit-tokens NL ↔ EN (gekalibreerd: waarschuwt, zie check_parity.py)
#   make check   build + parity + faalt als _ai/ achterloopt op de bron (handmatige bewerking gevonden)
#
# PYTHON is overschrijfbaar:  make build PYTHON=python   (op systemen zonder `python3`-binary)

PYTHON ?= python3
SCRIPTS := _project/scripts

.PHONY: build check parity

build:
	$(PYTHON) $(SCRIPTS)/gen_woordenlijst_md.py
	$(PYTHON) $(SCRIPTS)/gen_cursus_md.py
	$(PYTHON) $(SCRIPTS)/gen_grammatica_md.py
	$(PYTHON) $(SCRIPTS)/gen_index_md.py

check: build parity
	@git diff --exit-code _ai/ || (echo "FOUT: _ai/ liep achter op de bron. Commit de regeneratie mee." && exit 1)

parity:
	$(PYTHON) $(SCRIPTS)/check_parity.py
