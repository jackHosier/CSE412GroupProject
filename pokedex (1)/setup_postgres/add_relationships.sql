ALTER TABLE move_damage_class
ADD PRIMARY KEY (MDC_damage_class_id);
COMMIT WORK;


ALTER TABLE type
ADD PRIMARY KEY (T_type_id);
ALTER TABLE type
ADD FOREIGN KEY (T_damage_class_id) references move_damage_class;
COMMIT WORK;


ALTER TABLE evolution_trigger
ADD PRIMARY KEY (ET_evolution_trigger);
COMMIT WORK;


ALTER TABLE item
ADD PRIMARY KEY (I_item_id);
COMMIT WORK;


ALTER TABLE move_effect_prose
ADD PRIMARY KEY (ME_effect_id);
COMMIT WORK;


ALTER TABLE move
ADD PRIMARY KEY (M_move_id);
ALTER TABLE move
ADD FOREIGN KEY (M_type_id) references type;
ALTER TABLE move
ADD FOREIGN KEY (M_damage_class_id) references move_damage_class;
ALTER TABLE move
ADD FOREIGN KEY (M_effect_id) references move_effect_prose;
COMMIT WORK;


ALTER TABLE move_method
ADD PRIMARY KEY (MM_move_method_id);
COMMIT WORK;


ALTER TABLE pokemon
ADD PRIMARY KEY (P_poke_id);
COMMIT WORK;


ALTER TABLE pokemon_move
ADD PRIMARY KEY (PM_poke_id, PM_move_id, PM_move_method_id, PM_version_group_id, PM_level);
COMMIT WORK;


ALTER TABLE pokemon_species
ADD PRIMARY KEY (PS_poke_id);
COMMIT WORK;


ALTER TABLE stat
ADD PRIMARY KEY (S_stat_id);
ALTER TABLE stat
ADD FOREIGN KEY (S_damage_class_id) references move_damage_class;
COMMIT WORK;


ALTER TABLE pokemon_stat
ADD PRIMARY KEY (PST_poke_id, PST_stat_id);
COMMIT WORK;


ALTER TABLE pokemon_type
ADD PRIMARY KEY (PT_poke_id, PT_type_id);
COMMIT WORK;


ALTER TABLE type_effective
ADD PRIMARY KEY (TE_damage_type_id, TE_target_type_id);
COMMIT WORK;


ALTER TABLE pokemon_evolution
ADD PRIMARY KEY (PE_id, PE_evolved_species_id);
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_evolution_trigger_id) references evolution_trigger;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_trigger_item_id) references item;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_held_item_id) references item;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_known_move_id) references move;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_known_move_type_id) references type;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_party_species_id) references pokemon;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_party_type_id) references type;
ALTER TABLE pokemon_evolution
ADD FOREIGN KEY (PE_trade_species_id) references pokemon;
COMMIT WORK;
