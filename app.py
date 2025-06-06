from flask import Flask, render_template, request, redirect, flash, session
import psycopg2

app = Flask(__name__)
app.secret_key = "supersecret" 

conn = psycopg2.connect(
    dbname="todo",
    user="mads",           
    host="localhost",
    port="5432"
)


@app.route("/", methods=["GET", "POST"])
def index():
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        weight = request.form["weight"]
        hp = request.form["hp"]
        attack = request.form["attack"]
        defense = request.form["defense"]
        special_attack = request.form["special_attack"]
        special_defense = request.form["special_defense"]
        speed = request.form["speed"]
        totalstats = request.form["totalstats"]
        type = request.form["type(s)"]
        evolution_stg = request.form["evolution_stg"]


    search = request.args.get("search", "")

    cur.execute("""
        SELECT id, name, weight, hp, attack, defense, specialattack, specialdefense, speed, totalstats, type, evolution_stg
        FROM pokemon
        WHERE name ~* %s OR type ~* %s 
        ORDER BY id
    """, (search, search))
    pokemons = cur.fetchall()
    cur.close()

    return render_template("index2.html", pokemons=pokemons)

@app.route("/trainer", methods=["GET"])
def trainer_page():
    cur = conn.cursor()
    cur.execute("SELECT name FROM trainers ORDER BY name")
    trainers = cur.fetchall()
    cur.close()
    return render_template("trainer.html", trainers=trainers)


@app.route("/trainer/login", methods=["POST"])
def trainer_login():
    name = request.form["trainer_name"]
    cur = conn.cursor()
    cur.execute("SELECT id FROM trainers WHERE name = %s", (name,))
    trainer = cur.fetchone()
    cur.close()

    if trainer:
        return redirect(f"/trainer/{trainer[0]}")
    else:
        flash("Trainer not found, please register.")
        return redirect("/trainer")




@app.route("/trainer/create", methods=["POST"])
def trainer_create():
    name = request.form["trainer_name"]
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO trainers (name) VALUES (%s)", (name,))
        conn.commit()
        flash("✅ Trainer registered successfully!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flash("⚠️ Trainer already exists.")
    finally:
        cur.close()
    return redirect("/trainer")


@app.route("/trainer/<int:trainer_id>")
def trainer_home(trainer_id):
    cur = conn.cursor()
    cur.execute("SELECT name FROM trainers WHERE id = %s", (trainer_id,))
    trainer = cur.fetchone()

    cur.execute("""
        SELECT p.id, p.name, p.type
        FROM pokemon p
        JOIN trainer_pokedex tp ON tp.pokemon_id = p.id
        WHERE tp.trainer_id = %s
    """, (trainer_id,))
    pokedex = cur.fetchall()

    cur.execute("""
        SELECT p.id, p.name
        FROM pokemon p
        JOIN favorites f ON f.pokemon_id = p.id
        WHERE f.trainer_id = %s
    """, (trainer_id,))
    favorites = cur.fetchall()

    cur.close()
    return render_template("trainerhome.html", trainer=trainer[0], trainer_id=trainer_id, pokedex=pokedex, favorites=favorites)


@app.route("/trainer/<int:trainer_id>/add", methods=["POST"])
def add_to_pokedex(trainer_id):
    pokemon_name = request.form["pokemon_name"].strip().lower()
    cur = conn.cursor()

    cur.execute("SELECT id FROM pokemon WHERE LOWER(name) = %s", (pokemon_name,))
    result = cur.fetchone()

    if not result:
        cur.close()
        return f"❌ Pokémon '{pokemon_name}' not found."

    pokemon_id = result[0]

    try:
        cur.execute("INSERT INTO trainer_pokedex (trainer_id, pokemon_id) VALUES (%s, %s)", (trainer_id, pokemon_id))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
    cur.close()
    return redirect(f"/trainer/{trainer_id}")



@app.route("/trainer/<int:trainer_id>/favorite", methods=["POST"])
def add_to_favorites(trainer_id):
    pokemon_name = request.form["pokemon_name"].strip().lower()
    cur = conn.cursor()

    # Lookup ID
    cur.execute("SELECT id FROM pokemon WHERE LOWER(name) = %s", (pokemon_name,))
    result = cur.fetchone()

    if not result:
        cur.close()
        return f"❌ Pokémon '{pokemon_name}' not found."

    pokemon_id = result[0]

    # Check favorite count
    cur.execute("SELECT COUNT(*) FROM favorites WHERE trainer_id = %s", (trainer_id,))
    count = cur.fetchone()[0]

    if count >= 6:
        cur.close()
        return f"⚠️ You already have 6 favorites!"

    try:
        cur.execute("INSERT INTO favorites (trainer_id, pokemon_id) VALUES (%s, %s)", (trainer_id, pokemon_id))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
    cur.close()
    return redirect(f"/trainer/{trainer_id}")

@app.route("/trainer/<int:trainer_id>/favorite/<int:pokemon_id>/delete", methods=["POST"])
def delete_favorite(trainer_id, pokemon_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM favorites
        WHERE trainer_id = %s AND pokemon_id = %s
    """, (trainer_id, pokemon_id))
    conn.commit()
    cur.close()
    return redirect(f"/trainer/{trainer_id}")



if __name__ == "__main__":
    app.run(debug=True)



