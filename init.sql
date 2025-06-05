DROP TABLE IF EXISTS trainers CASCADE;
DROP TABLE IF EXISTS pokemon CASCADE;
DROP TABLE IF EXISTS trainer_pokedex CASCADE;
DROP TABLE IF EXISTS favorites CASCADE;

CREATE TABLE trainers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE pokemon (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  weight INTEGER,
  hp INTEGER,
  attack INTEGER,
  defense INTEGER,
  specialattack INTEGER,
  specialdefense INTEGER,
  speed INTEGER,
  totalstats INTEGER,
  type VARCHAR(30),
  evolution_stg INTEGER
  -- level INTEGER
);

-- Link table: Which Pokémon a trainer has
CREATE TABLE IF NOT EXISTS trainer_pokedex (
  trainer_id INTEGER REFERENCES trainers(id),
  pokemon_id INTEGER REFERENCES pokemon(id),
  PRIMARY KEY (trainer_id, pokemon_id)
);

-- Favorites (up to 6)
CREATE TABLE IF NOT EXISTS favorites (
  trainer_id INTEGER REFERENCES trainers(id),
  pokemon_id INTEGER REFERENCES pokemon(id),
  PRIMARY KEY (trainer_id, pokemon_id)
);

COPY pokemon(name, weight, hp, attack, defense, specialattack, specialdefense, speed, totalstats, type, evolution_stg) -- , level
FROM '/Users/mads/Desktop/Datalogi/DIS/PokeTest/generation1_pokemon.csv'
DELIMITER ',' CSV HEADER;
