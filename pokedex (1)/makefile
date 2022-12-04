SOUTPUTS = $(sort $(wildcard outputs/*.txt))
QUESTIONS = $(patsubst outputs/%.txt,%,$(OUTPUTS))
MAKEFILE_PATH = /home/isaac/pokedex
ROOT = $(MAKEFILE_PATH)


all: path $(QUESTIONS)
	rm -rf tmp


%: queries/%.sql
	@echo "checking $@; correct if nothing below ----"
	@psql -A -t -d $(USER) -q -f $< 1> tmp/$@.txt
	@diff outputs/$@.txt tmp/$@.txt || echo "$@ is wrong"; exit 0
	@echo ""


path:
	@mkdir -p tmp


setup_postgres:
	@echo "creating tables"
	psql -d $(USER) -q -f setup_postgres/create_tables.sql

	@echo "importing data"
	psql -d $(USER) -q -c "copy move_damage_class from '$(ROOT)/pokedex_data/move_damage_class.csv' CSV header;"

	psql -d $(USER) -q -c "copy type from '$(ROOT)/pokedex_data/type.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy evolution_trigger from '$(ROOT)/pokedex_data/evolution_trigger.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy move from '$(ROOT)/pokedex_data/move.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy item from '$(ROOT)/pokedex_data/item.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy move_effect_prose from '$(ROOT)/pokedex_data/move_effect_prose.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy move_method from '$(ROOT)/pokedex_data/move_method.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon from '$(ROOT)/pokedex_data/pokemon.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon_move from '$(ROOT)/pokedex_data/pokemon_move.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon_species from '$(ROOT)/pokedex_data/pokemon_species.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy stat from '$(ROOT)/pokedex_data/stat.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon_stat from '$(ROOT)/pokedex_data/pokemon_stat.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon_type from '$(ROOT)/pokedex_data/pokemon_type.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy type_effective from '$(ROOT)/pokedex_data/type_effective.csv' CSV HEADER;"

	psql -d $(USER) -q -c "copy pokemon_evolution from '$(ROOT)/pokedex_data/pokemon_evolution.csv' CSV HEADER;"

	@echo "adding relationships"
	psql -d $(USER) -q -f setup_postgres/add_relationships.sql

clean_postgres:
	psql -d $(USER) -q -f setup_postgres/drop_tables.sql




.PHONY: setup_postgres
