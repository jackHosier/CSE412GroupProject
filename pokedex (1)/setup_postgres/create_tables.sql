CREATE TABLE evolution_trigger (ET_evolution_trigger INTEGER NOT NULL,
ET_identifier VARCHAR(25));


CREATE TABLE item (I_item_id INTEGER NOT NULL,
I_name VARCHAR(50),
I_category_id INTEGER,
I_cost INTEGER,
I_fling_power INTEGER,
I_fling_effect_id INTEGER);


CREATE TABLE move (M_move_id INTEGER NOT NULL,
M_name VARCHAR(50),
M_generation_id INTEGER,
M_type_id INTEGER,
M_power INTEGER,
M_pp INTEGER,
M_accuracy INTEGER,
M_priority INTEGER,
M_target_id INTEGER,
M_damage_class_id INTEGER,
M_effect_id INTEGER,
M_effect_chance INTEGER);


CREATE TABLE move_damage_class (MDC_damage_class_id INTEGER NOT NULL,
MDC_name VARCHAR(8));


CREATE TABLE move_effect_prose (ME_effect_id INTEGER NOT NULL,
ME_short_effect VARCHAR(200));


CREATE TABLE move_method (MM_move_method_id INTEGER NOT NULL,
MM_name VARCHAR(30));


CREATE TABLE pokemon (P_poke_id INTEGER NOT NULL, 
P_Name CHAR (50),
P_Dex INTEGER,
P_height INTEGER,
P_weight INTEGER,
P_base_experience INTEGER,
P_order INTEGER,
P_is_default INTEGER);         


CREATE TABLE pokemon_evolution (PE_id INTEGER NOT NULL, 
PE_evolved_species_id INTEGER NOT NULL, 
PE_evolution_trigger_id INTEGER, 
PE_trigger_item_id INTEGER, 
PE_minimum_level INTEGER,
PE_gender_id INTEGER,
PE_location_id INTEGER,
PE_held_item_id INTEGER,
PE_time_of_day VARCHAR(5),
PE_known_move_id INTEGER,
PE_known_move_type_id INTEGER,
PE_minimum_happiness INTEGER,
PE_minimum_beauty INTEGER,
PE_minimum_affection INTEGER,
PE_relative_physical_stats INTEGER,
PE_party_species_id INTEGER,
PE_party_type_id INTEGER,
PE_trade_species_id INTEGER,
PE_needs_overworld_rain INTEGER,
PE_turn_upside_down INTEGER);


CREATE TABLE pokemon_move (PM_poke_id INTEGER NOT NULL, 
PM_version_group_id INTEGER NOT NULL,
PM_move_id INTEGER NOT NULL,
PM_move_method_id INTEGER NOT NULL,
PM_level INTEGER NOT NULL,
PM_order INTEGER);


CREATE TABLE pokemon_species (PS_poke_id INTEGER  NOT NULL, 
PS_name VARCHAR(50), 
PS_generation_id INTEGER, 
PS_evolves_from_species_id INTEGER,
PS_evolution_chain_id INTEGER,
PS_color_id INTEGER,
PS_shape_id INTEGER,
PS_habitat_id INTEGER,
PS_gender_rate INTEGER,
PS_capture_rate INTEGER,
PS_base_happiness INTEGER,
PS_is_baby INTEGER,
PS_hatch_counter INTEGER,
PS_has_gender_differences INTEGER,
PS_growth_rate_id INTEGER,
PS_forms_switchable INTEGER,
PS_is_legendary INTEGER,
PS_is_mythical INTEGER,
PS_order INTEGER);


CREATE TABLE pokemon_stat (PST_poke_id INTEGER NOT NULL,
PST_stat_id INTEGER NOT NULL,
PST_base_stat INTEGER,
PST_effort INTEGER);


CREATE TABLE pokemon_type (PT_poke_id INTEGER NOT NULL,
PT_type_id INTEGER NOT NULL,
PT_slot INTEGER);


CREATE TABLE stat (S_stat_id  INTEGER NOT NULL, 
S_damage_class_id  INTEGER, 
S_name VARCHAR(20), 
S_is_battle_only INTEGER, 
S_game_index INTEGER);


CREATE TABLE type (T_type_id INTEGER NOT NULL, 
T_name VARCHAR(10), 
T_generation_id INTEGER, 
T_damage_class_id INTEGER); 


CREATE TABLE type_effective (TE_damage_type_id INTEGER NOT NULL,
TE_target_type_id INTEGER NOT NULL,
TE_damage_factor INTEGER);
