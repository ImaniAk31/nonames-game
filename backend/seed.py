from database import SessionLocal, engine, Base
from models import Card

# Create the tables in the database if they don't exist yet
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    if db.query(Card).count() > 0:
        print("Database already contains cards. Skipping seed.")
        db.close()
        return

    # All 50 prototype cards straight from the Digital Card Game file!
    initial_cards = [
        # --- THE ORIGINAL 16 ---
        {"title": "Madea", "category": "Comedy Legend", "words": "Tyler Perry, Halleluyer, Gun"},
        {"title": "Uncle Phil", "category": "TV Classics", "words": "Will, Jazz, Throw"},
        {"title": "Bernie Mac", "category": "Comedy Legend", "words": "Scared, America, Kick"},
        {"title": "Dragon Fly Jones", "category": "TV Classics", "words": "Martin, Martial Arts, Kenji"},
        {"title": "Steve Urkel", "category": "TV Classics", "words": "Laura, Cheese, Suspenders"},
        {"title": "Smokey", "category": "Movie Legends", "words": "Craig, Deebo, Friday"},
        {"title": "Randy Watson", "category": "Movie Legends", "words": "Eddie Murphy, Singing, Chocolate"},
        {"title": "Alonzo Harris", "category": "Movie Legends", "words": "Denzel, Cop, King Kong"},
        {"title": "Back It Up, Terry!", "category": "Viral Moment", "words": "Terry, Firework, Reverse"},
        {"title": "Sweet Brown", "category": "Viral Legend", "words": "Fire, Bronchitis, Cold Pop"},
        {"title": "Birdman", "category": "Hip-Hop Moment", "words": "Respeck, Name, Finished"},
        {"title": "Kanye West", "category": "Award Show Chaos", "words": "Taylor Swift, Beyoncé, Award"},
        {"title": "James Brown", "category": "Soul Legend", "words": "Godfather, Cape, Tired"},
        {"title": "Thriller", "category": "Iconic Music Video", "words": "Michael, Zombie, Red Jacket"},
        {"title": "Single Ladies", "category": "Iconic Music Video", "words": "Ring, Beyoncé, Leotard"},
        {"title": "The Rain", "category": "Iconic Music Video", "words": "Missy, Trash Bag, Suit"},

        # --- THE EXPANSION 20 ---
        {"title": "Will Smith", "category": "Movie Legends", "words": "Slap, Fresh, Aliens"},
        {"title": "Halle Berry", "category": "Movie Legends", "words": "Cat, Monster, Oscar"},
        {"title": "Morgan Freeman", "category": "Movie Legends", "words": "God, Voice, Shawshank"},
        {"title": "Whoopi Goldberg", "category": "Movie Legends", "words": "Sister, Ghost, View"},
        {"title": "Martin Lawrence", "category": "Comedy Legend", "words": "Bad, Sheneneh, Big"},
        {"title": "Felicia", "category": "Movie Characters", "words": "Bye, Borrow, Microwave"},
        {"title": "Nino Brown", "category": "Movie Characters", "words": "City, Brother, Cancel"},
        {"title": "Ricky", "category": "Movie Characters", "words": "Football, Shot, Alley"},
        {"title": "Cleo", "category": "Movie Characters", "words": "Bank, Rob, Queen"},
        {"title": "Sho'nuff", "category": "Movie Characters", "words": "Harlem, Shogun, Glow"},
        {"title": "Why You Always Lying", "category": "Viral Moment", "words": "Lie, Toilet, Yard"},
        {"title": "The Popeyes Kid", "category": "Viral Legend", "words": "Chicken, Look, Cup"},
        {"title": "Conceited Reaction", "category": "Viral Moment", "words": "Purse, Lip, Battle"},
        {"title": "You About To Lose Yo Job", "category": "Viral Legend", "words": "Dance, Security, Job"},
        {"title": "NeNe Leakes", "category": "Viral Moment", "words": "Said, Housewives, Atlanta"},
        {"title": "Crank That", "category": "Viral Dance", "words": "Superman, Dance, You"},
        {"title": "The Wobble", "category": "Viral Dance", "words": "Line, Wedding, Back"},
        {"title": "Teach Me How to Dougie", "category": "Viral Dance", "words": "Teach, Hand, Hair"},
        {"title": "Lean Back", "category": "Viral Dance", "words": "Dance, Pull, Pants"},
        {"title": "Tootsee Roll", "category": "Viral Dance", "words": "Left, Dip, Butterfly"},

        # --- THE FINAL 14 ---
        {"title": "Angela Bassett", "category": "Movie Legends", "words": "Car, Burn, Exhale"},
        {"title": "Viola Davis", "category": "TV Classics", "words": "Murder, Wig, Purse"},
        {"title": "Samuel L. Jackson", "category": "Movie Legends", "words": "Snakes, Wallet, Mother"},
        {"title": "Craig Jones", "category": "Movie Characters", "words": "Fired, Boxes, Friday"},
        {"title": "Carlton Banks", "category": "TV Classics", "words": "Dance, Tom, Will"},
        {"title": "Gina Waters", "category": "TV Classics", "words": "Pam, Damn, Radio"},
        {"title": "Wesley Snipes", "category": "Movie Legends", "words": "Vampire, Sword, Taxes"},
        {"title": "Mama Klump", "category": "Movie Characters", "words": "Eddie, Hercules, Table"},
        {"title": "Keke Palmer", "category": "Viral Moment", "words": "Sorry, Man, Recognize"},
        {"title": "Antoine Dodson", "category": "Viral Legend", "words": "Hide, Wife, Window"},
        {"title": "Shirley Caesar", "category": "Viral Moment", "words": "Beans, Greens, Thanksgiving"},
        {"title": "Ray J (Glasses)", "category": "Viral Moment", "words": "Unbreakable, Hat, Glasses"},
        {"title": "Cardi B (Coronavirus)", "category": "Viral Moment", "words": "Virus, Panic, Bronx"},
        {"title": "Supa Hot Fire", "category": "Viral Legend", "words": "Rapper, Glasses, Trees"}
    ]

    print(f"Adding {len(initial_cards)} cards to the database...")
    
    for card_data in initial_cards:
        new_card = Card(
            title=card_data["title"],
            category=card_data["category"],
            forbidden_words_str=card_data["words"],
            difficulty_level=1,
            is_active=True
        )
        db.add(new_card)

    db.commit()
    db.close()
    
    print(f"Success! {len(initial_cards)} cards have been added to the game.")

if __name__ == "__main__":
    seed_database()