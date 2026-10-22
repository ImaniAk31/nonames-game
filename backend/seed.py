from database import SessionLocal, engine, Base
from models import Card

Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    if db.query(Card).count() > 0:
        print("Database already contains cards. Skipping seed.")
        db.close()
        return

    # --- DECK 1: FOR THE CULTURE (50 Cards) ---
    for_the_culture = [
        {"title": "Madea", "category": "Comedy Legend", "words": "Tyler Perry, Halleluyer, Gun", "hint": "Tough, gun-toting grandma played by a famous director."},
        {"title": "Uncle Phil", "category": "TV Classics", "words": "Will, Jazz, Throw", "hint": "The wealthy, strict judge who took in his nephew from Philly."},
        {"title": "Bernie Mac", "category": "Comedy Legend", "words": "Scared, America, Kick", "hint": "King of Comedy who wasn't afraid of anybody's kids."},
        {"title": "Dragon Fly Jones", "category": "TV Classics", "words": "Martin, Martial Arts, Kenji", "hint": "Clumsy martial arts master who always gets beat up."},
        {"title": "Steve Urkel", "category": "TV Classics", "words": "Laura, Cheese, Suspenders", "hint": "Nerdy neighbor who always asked 'Did I do that?'"},
        {"title": "Smokey", "category": "Movie Legends", "words": "Craig, Deebo, Friday", "hint": "He got fired on his day off and loves a certain green plant."},
        {"title": "Randy Watson", "category": "Movie Legends", "words": "Eddie Murphy, Singing, Chocolate", "hint": "Lead singer of Sexual Chocolate in Coming to America."},
        {"title": "Alonzo Harris", "category": "Movie Legends", "words": "Denzel, Cop, King Kong", "hint": "Corrupt detective who claimed King Kong had nothing on him."},
        {"title": "Back It Up, Terry!", "category": "Viral Moment", "words": "Terry, Firework, Reverse", "hint": "Man in a wheelchair who wouldn't move away from the fireworks."},
        {"title": "Sweet Brown", "category": "Viral Legend", "words": "Fire, Bronchitis, Cold Pop", "hint": "She didn't have time for the fire because she had bronchitis."},
        {"title": "Birdman", "category": "Hip-Hop Moment", "words": "Respeck, Name, Finished", "hint": "Demanded the Breakfast Club put respect on his name."},
        {"title": "Kanye West", "category": "Award Show Chaos", "words": "Taylor Swift, Beyoncé, Award", "hint": "Imma let you finish, but Beyoncé had one of the best videos..."},
        {"title": "James Brown", "category": "Soul Legend", "words": "Godfather, Cape, Tired", "hint": "The Godfather of Soul who always fell to his knees in a cape."},
        {"title": "Thriller", "category": "Iconic Music Video", "words": "Michael, Zombie, Red Jacket", "hint": "The greatest zombie dance routine of all time."},
        {"title": "Single Ladies", "category": "Iconic Music Video", "words": "Ring, Beyoncé, Leotard", "hint": "If you liked it, you should have put a piece of jewelry on it."},
        {"title": "The Rain", "category": "Iconic Music Video", "words": "Missy, Trash Bag, Suit", "hint": "She wore a giant inflated garbage bag suit."},
        {"title": "Will Smith", "category": "Movie Legends", "words": "Slap, Fresh, Aliens", "hint": "The Prince of Bel-Air who slaps aliens and comedians."},
        {"title": "Halle Berry", "category": "Movie Legends", "words": "Cat, Monster, Oscar", "hint": "First Black woman to win Best Actress. Played Storm."},
        {"title": "Morgan Freeman", "category": "Movie Legends", "words": "God, Voice, Shawshank", "hint": "The actor with the most soothing voice on earth. Played God."},
        {"title": "Whoopi Goldberg", "category": "Movie Legends", "words": "Sister, Ghost, View", "hint": "She has no eyebrows, played a singing nun, and argues on The View."},
        {"title": "Martin Lawrence", "category": "Comedy Legend", "words": "Bad, Sheneneh, Big", "hint": "Played a Miami detective and dressed as a woman for Big Momma."},
        {"title": "Felicia", "category": "Movie Characters", "words": "Bye, Borrow, Microwave", "hint": "The neighborhood beggar you always tell 'Bye' to."},
        {"title": "Nino Brown", "category": "Movie Characters", "words": "City, Brother, Cancel", "hint": "Ruthless kingpin who asked 'Am I my brother's keeper?'"},
        {"title": "Ricky", "category": "Movie Characters", "words": "Football, Shot, Alley", "hint": "Star athlete in Boyz n the Hood who ran zig-zag in the alley."},
        {"title": "Cleo", "category": "Movie Characters", "words": "Bank, Rob, Queen", "hint": "The tough mechanic bank robber in Set It Off."},
        {"title": "Sho'nuff", "category": "Movie Characters", "words": "Harlem, Shogun, Glow", "hint": "The Shogun of Harlem who demanded people kiss his Converse."},
        {"title": "Why You Always Lying", "category": "Viral Moment", "words": "Lie, Toilet, Yard", "hint": "Guy singing in the yard and leaning over a toilet about a liar."},
        {"title": "The Popeyes Kid", "category": "Viral Legend", "words": "Chicken, Look, Cup", "hint": "Little boy holding a cup giving the most awkward side-eye ever."},
        {"title": "Conceited Reaction", "category": "Viral Moment", "words": "Purse, Lip, Battle", "hint": "Battle rapper pursing his lips and looking away skeptically."},
        {"title": "You About To Lose Yo Job", "category": "Viral Legend", "words": "Dance, Security, Job", "hint": "Woman dancing and singing at a security guard who detained her."},
        {"title": "NeNe Leakes", "category": "Viral Moment", "words": "Said, Housewives, Atlanta", "hint": "Reality star who aggressively pointed and yelled 'I said what I said!'"},
        {"title": "Crank That", "category": "Viral Dance", "words": "Superman, Dance, You", "hint": "The 2007 dance where you 'Superman' that..."},
        {"title": "The Wobble", "category": "Viral Dance", "words": "Line, Wedding, Back", "hint": "The ultimate family reunion line dance where you shake your hips."},
        {"title": "Teach Me How to Dougie", "category": "Viral Dance", "words": "Teach, Hand, Hair", "hint": "Dance where you lean side to side and smooth your hair back."},
        {"title": "Lean Back", "category": "Viral Dance", "words": "Dance, Pull, Pants", "hint": "Terror Squad dance where you just pull up your pants and jerk your shoulder."},
        {"title": "Tootsee Roll", "category": "Viral Dance", "words": "Left, Dip, Butterfly", "hint": "Let me see that... cotton candy, sweet to go!"},
        {"title": "Angela Bassett", "category": "Movie Legends", "words": "Car, Burn, Exhale", "hint": "She burned her husband's clothes and car in Waiting to Exhale."},
        {"title": "Viola Davis", "category": "TV Classics", "words": "Murder, Wig, Purse", "hint": "Law professor who dramatically took her wig and makeup off."},
        {"title": "Samuel L. Jackson", "category": "Movie Legends", "words": "Snakes, Wallet, Mother", "hint": "Actor who yells a specific curse word and fought snakes on a plane."},
        {"title": "Craig Jones", "category": "Movie Characters", "words": "Fired, Boxes, Friday", "hint": "Ice Cube's character who got fired on his day off."},
        {"title": "Carlton Banks", "category": "TV Classics", "words": "Dance, Tom, Will", "hint": "The preppy cousin who loved Tom Jones music."},
        {"title": "Gina Waters", "category": "TV Classics", "words": "Pam, Damn, Radio", "hint": "Martin's girlfriend/wife who had a big head."},
        {"title": "Wesley Snipes", "category": "Movie Legends", "words": "Vampire, Sword, Taxes", "hint": "He played Blade the vampire hunter and famously didn't pay taxes."},
        {"title": "Mama Klump", "category": "Movie Characters", "words": "Eddie, Hercules, Table", "hint": "The mother who always yelled 'Hercules! Hercules!' at the dinner table."},
        {"title": "Keke Palmer", "category": "Viral Moment", "words": "Sorry, Man, Recognize", "hint": "She looked at a photo of Dick Cheney and said 'Sorry to this man'."},
        {"title": "Antoine Dodson", "category": "Viral Legend", "words": "Hide, Wife, Window", "hint": "He told everyone to hide their kids and their wife."},
        {"title": "Shirley Caesar", "category": "Viral Moment", "words": "Beans, Greens, Thanksgiving", "hint": "Gospel singer who listed off beans, greens, potatoes, tomatoes..."},
        {"title": "Ray J (Glasses)", "category": "Viral Moment", "words": "Unbreakable, Hat, Glasses", "hint": "He gave an interview while his glasses kept sliding around his face."},
        {"title": "Cardi B (Coronavirus)", "category": "Viral Moment", "words": "Virus, Panic, Bronx", "hint": "She yelled that the virus is getting real in a panicked video."},
        {"title": "Supa Hot Fire", "category": "Viral Legend", "words": "Rapper, Glasses, Trees", "hint": "The parody battle rapper who said 'I'm not a rapper'."}
    ]

    # --- DECK 2: POP CULTURE (50 Cards) ---
    pop_culture_cards = [
        {"title": "Ross Geller", "category": "TV Classics", "words": "Pivot, Couch, Break", "hint": "He yelled PIVOT while moving a couch and said 'We were on a break!'"},
        {"title": "Michael Scott", "category": "TV Classics", "words": "Office, Boss, Paper", "hint": "The manager of Dunder Mifflin who has a World's Best Boss mug."},
        {"title": "Walter White", "category": "TV Classics", "words": "Meth, Chemistry, Heisenberg", "hint": "Chemistry teacher who said 'I am the one who knocks'."},
        {"title": "Homer Simpson", "category": "TV Classics", "words": "Donut, Yellow, Doh", "hint": "Yellow cartoon dad who loves donuts and chokes his son."},
        {"title": "Sheldon Cooper", "category": "TV Classics", "words": "Bazinga, Bang, Spot", "hint": "Nerdy physicist who always says 'Bazinga' and needs his spot on the couch."},
        {"title": "Tony Stark", "category": "Movie Characters", "words": "Avengers, Suit, Billionaire", "hint": "Genius, billionaire, playboy, philanthropist. He is Iron Man."},
        {"title": "Darth Vader", "category": "Movie Characters", "words": "Luke, Force, Breathe", "hint": "Sith Lord who said 'I am your father'."},
        {"title": "Jack Sparrow", "category": "Movie Characters", "words": "Pirate, Rum, Johnny", "hint": "Drunk captain of the Black Pearl."},
        {"title": "Harry Potter", "category": "Movie Characters", "words": "Wizard, Scar, Hogwarts", "hint": "The boy who lived. Has a lightning bolt on his forehead."},
        {"title": "Regina George", "category": "Movie Characters", "words": "Mean, Plastic, Burn", "hint": "Leader of the Plastics who says 'On Wednesdays we wear pink.'"},
        {"title": "Tom Cruise", "category": "Movie Legends", "words": "Mission, Impossible, Couch", "hint": "Action star who does his own stunts and jumped on Oprah's couch."},
        {"title": "Leonardo DiCaprio", "category": "Movie Legends", "words": "Boat, Oscar, Bear", "hint": "He was King of the World on the Titanic."},
        {"title": "Dwayne Johnson", "category": "Movie Legends", "words": "Rock, Wrestling, Jungle", "hint": "Can you smell what he is cooking?"},
        {"title": "Meryl Streep", "category": "Movie Legends", "words": "Devil, Oscar, Prada", "hint": "Legendary actress who played the mean boss in Devil Wears Prada."},
        {"title": "Tom Hanks", "category": "Movie Legends", "words": "Run, Toy, Volleyball", "hint": "He played Forrest Gump and Woody the Cowboy."},
        {"title": "Keanu Reeves", "category": "Movie Legends", "words": "Pill, Wick, Dog", "hint": "He knows Kung Fu in the Matrix and avenged his puppy."},
        {"title": "Angelina Jolie", "category": "Movie Legends", "words": "Brad, Tomb, Lips", "hint": "Played Lara Croft and Maleficent."},
        {"title": "Jennifer Lawrence", "category": "Movie Legends", "words": "Hunger, Katniss, Fall", "hint": "She volunteered as tribute and tripped at the Oscars."},
        {"title": "Ryan Reynolds", "category": "Movie Legends", "words": "Deadpool, Blake, Suit", "hint": "The hilarious actor who plays the Merc with a Mouth."},
        {"title": "Betty White", "category": "TV Classics", "words": "Golden, Old, Rose", "hint": "The most beloved, long-living Golden Girl."},
        {"title": "Taylor Swift", "category": "Music Legends", "words": "Ex, Shake, Eras", "hint": "Billionaire pop star famous for writing songs about her breakups."},
        {"title": "Lady Gaga", "category": "Music Legends", "words": "Meat, Born, Poker", "hint": "Pop star who wore a dress made entirely of raw meat."},
        {"title": "Eminem", "category": "Music Legends", "words": "Rap, Mom, Spaghetti", "hint": "Will the real Slim Shady please stand up?"},
        {"title": "Britney Spears", "category": "Music Legends", "words": "Snake, Shave, Toxic", "hint": "Pop princess who said 'Oops I did it again'."},
        {"title": "Justin Bieber", "category": "Music Legends", "words": "Baby, Canada, Hair", "hint": "Canadian pop star discovered on YouTube who sang 'Baby'."},
        {"title": "Adele", "category": "Music Legends", "words": "British, Cry, Hello", "hint": "She said 'Hello from the other side'."},
        {"title": "Snoop Dogg", "category": "Music Legends", "words": "Weed, Martha, Dog", "hint": "He told everyone to drop it like it's hot."},
        {"title": "Ariana Grande", "category": "Music Legends", "words": "Ponytail, Next, Wicked", "hint": "Pop star known for her massive high ponytail and whistle notes."},
        {"title": "Bruno Mars", "category": "Music Legends", "words": "Funk, Uptown, Hat", "hint": "He sang 24K Magic and Uptown Funk."},
        {"title": "Billie Eilish", "category": "Music Legends", "words": "Green, Whisper, Bad", "hint": "Whisper-singer who said 'I'm the bad guy, duh'."},
        {"title": "Rickroll", "category": "Viral Moment", "words": "Give, Video, Astley", "hint": "Tricking someone into watching 'Never Gonna Give You Up'."},
        {"title": "Distracted Boyfriend", "category": "Viral Moment", "words": "Look, Girl, Meme", "hint": "Stock photo of a guy looking back at another girl while holding hands."},
        {"title": "Grumpy Cat", "category": "Viral Legend", "words": "Frown, Cat, No", "hint": "The internet's favorite angry-looking feline."},
        {"title": "Doge", "category": "Viral Legend", "words": "Coin, Shiba, Wow", "hint": "The Shiba Inu dog meme that says 'Much wow'."},
        {"title": "This is Fine", "category": "Viral Moment", "words": "Dog, Fire, Coffee", "hint": "Cartoon dog sipping coffee in a burning room."},
        {"title": "Salt Bae", "category": "Viral Moment", "words": "Sprinkle, Meat, Chef", "hint": "The guy who dramatically drops salt off his elbow onto steak."},
        {"title": "Success Kid", "category": "Viral Moment", "words": "Fist, Sand, Baby", "hint": "Little baby pumping his fist on the beach."},
        {"title": "Woman Yelling at Cat", "category": "Viral Moment", "words": "Yell, Cat, Table", "hint": "Real Housewife screaming at a confused white cat at a dinner table."},
        {"title": "Kermit Sipping Tea", "category": "Viral Moment", "words": "Frog, Tea, Business", "hint": "The meme that ends with 'But that's none of my business'."},
        {"title": "Disaster Girl", "category": "Viral Moment", "words": "Fire, House, Smile", "hint": "Little girl smiling devilishly while a house burns down behind her."},
        {"title": "Gangnam Style", "category": "Viral Dance", "words": "Horse, Korea, Psy", "hint": "The invisible horse-riding dance from South Korea."},
        {"title": "Macarena", "category": "Viral Dance", "words": "Arms, Hey, 90s", "hint": "The 90s dance where you put your hands on your head and hips."},
        {"title": "YMCA", "category": "Viral Dance", "words": "Letters, Village, Arms", "hint": "Spelling out four letters with your arms above your head."},
        {"title": "WAP", "category": "Iconic Music Video", "words": "Water, Mansion, Cardi", "hint": "Cardi B and Megan Thee Stallion dancing in a crazy mansion."},
        {"title": "Hotline Bling", "category": "Iconic Music Video", "words": "Cellphone, Box, Dance", "hint": "Drake doing goofy dad-dancing in a glowing box."},
        {"title": "Wrecking Ball", "category": "Iconic Music Video", "words": "Swing, Lick, Hammer", "hint": "Miley Cyrus swinging on a giant demolition ball."},
        {"title": "Chandelier", "category": "Iconic Music Video", "words": "Wig, Swing, Sia", "hint": "Little girl in a blonde wig dancing wildly in an empty apartment."},
        {"title": "Take On Me", "category": "Iconic Music Video", "words": "Sketch, 80s, Comic", "hint": "80s music video drawn like a pencil sketch comic book."},
        {"title": "Baby Shark", "category": "Viral Dance", "words": "Chomp, Kids, Doo", "hint": "Chomping your hands for the mommy, daddy, and grandpa fish."},
        {"title": "Harlem Shake", "category": "Viral Dance", "words": "Helmet, Drop, Crazy", "hint": "One person dances alone, the bass drops, and everyone goes crazy."}
    ]

    print("Adding 100 cards to the database...")
    
    for card_data in for_the_culture:
        db.add(Card(
            title=card_data["title"], category=card_data["category"],
            forbidden_words_str=card_data["words"], hint=card_data["hint"], deck="For The Culture"
        ))
        
    for card_data in pop_culture_cards:
        db.add(Card(
            title=card_data["title"], category=card_data["category"],
            forbidden_words_str=card_data["words"], hint=card_data["hint"], deck="Pop Culture"
        ))

    db.commit()
    db.close()
    print("Success! 100 cards added.")

if __name__ == "__main__":
    seed_database()