# Makefile — Tarifit-cursus: regenereer _ai/ uit de canonieke bronnen en bewaak drift + NL/EN-pariteit.
#
#   make build         regenereert alle _ai/*.md uit CSV + HTML ("niet met de hand bewerken"-banner)
#   make parity        vergelijkt de Tarifit-tokens NL ↔ EN (gekalibreerd: waarschuwt, zie check_parity.py)
#   make zinnen        valideert assets/zinnen/zinnen.csv tegen _ai/grammatica.md (zie check_zinnen.py)
#   make check         build + parity + zinnen + check-cursus + faalt als _ai/ achterloopt op de bron
#   make ankers        zet §-ankers in nl/uitleg.html + en/grammar.html (gen_ankers.py, idempotent)
#   make bouw          rendert nl/blok-N.html + nl/lezen.html uit bron/lessen (bouw_cursus.py)
#   make cursus        ankers + bouw
#   make check-cursus  cursus + check_bronnen + check_register + check_dekking
#
# PYTHON is overschrijfbaar:  make build PYTHON=python   (op systemen zonder `python3`-binary)

PYTHON ?= python3
SCRIPTS := _project/scripts

.PHONY: build check parity zinnen ankers bouw cursus check-cursus

# build hangt af van bouw: gen_cursus_md.py leest nl/blok-1..8.html (gegenereerd door
# bouw_cursus.py), niet meer het hand-geschreven nl/cursus.html — die moeten dus vers zijn
# vóórdat build ze inleest.
build: bouw
	$(PYTHON) $(SCRIPTS)/gen_woordenlijst_md.py
	$(PYTHON) $(SCRIPTS)/gen_cursus_md.py
	$(PYTHON) $(SCRIPTS)/gen_grammatica_md.py
	$(PYTHON) $(SCRIPTS)/gen_zinnen_md.py
	$(PYTHON) $(SCRIPTS)/gen_index_md.py

check: build parity zinnen check-cursus
	@git diff --exit-code _ai/ || (echo "FOUT: _ai/ liep achter op de bron. Commit de regeneratie mee." && exit 1)

parity:
	$(PYTHON) $(SCRIPTS)/check_parity.py

zinnen:
	$(PYTHON) $(SCRIPTS)/check_zinnen.py

ankers:
	$(PYTHON) $(SCRIPTS)/gen_ankers.py

bouw:
	$(PYTHON) $(SCRIPTS)/bouw_cursus.py

cursus: ankers bouw

check-cursus: cursus
	$(PYTHON) $(SCRIPTS)/check_bronnen.py
	$(PYTHON) $(SCRIPTS)/check_register.py
	$(PYTHON) $(SCRIPTS)/check_dekking.py
