# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MuseMatch 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

It takes a single user profile (favorite genre, favorite mood, target energy 0-1) and ranks a fixed song catalog to return the top 5 closest matches. It assumes the user already knows and can name their favorite genre and mood exactly as they appear in the catalog, and can state a target energy as a number rather than a vague feeling. This is a classroom simulation for exploring how scoring weights shape recommendations, not a production system so there's no login, no listening history, and no real users behind the profiles.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Every song gets scored against the user's profile out of a possible 4 points. If the song's genre matches (ignoring case and extra spaces), it earns 1 point; if the mood matches the same way, it earns 1 more point; and however close the song's energy is to the user's target energy earns up to 2 points, the biggest single piece of the score. If someone types an energy above 1 or below 0, it's treated as exactly 1 or exactly 0 rather than being taken literally. Those three pieces get added together into one score, and the 5 songs with the highest scores win, with closer energy used to break ties. Energy now carries the most individual weight, so a song with a near-perfect energy fit can beat a song that only matches genre or only matches mood so genre and mood still tend to win overall when they're both present, since 1+1 starts ahead of what energy alone can add. Note that although the catalog also tracks tempo, valence, danceability, and acousticness for each song, none of those are actually used in the scoring right now so only genre, mood, and energy factor in.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

    The catalog is 18 songs total, spread across about 15 different genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip hop, country, reggae, metal, folk, r&b, electronic) and a matching variety of moods (happy, chill, intense, peaceful, angry, melancholy, etc.), with each song also carrying tempo, valence, danceability, and acousticness values even though those aren't used in scoring yet. 
    
    Most genres have only a single representative song, so there's very little internal variety once a genre is chosen. Missing from the dataset: genres people commonly ask for in the edge cases, like k-pop, opera, and musical theatre, don't exist in the catalog at all, and there's no way to express blended or in-between tastes (e.g., someone who likes both pop and lofi) since each song only carries one genre and one mood label.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

    It works best when the catalog actually has a song matching the user's genre and mood, like the Starter profile (pop/happy/0.8), which correctly puts Sunrise City first with all three traits agreeing. 
    
    It also handles contradictory requests reasonably, for a "melancholy folk" listener who asks for energy 0.9, it still ranks the one real folk/melancholy song (Wilted Fields) first instead of chasing the energy number into an unrelated genre, which feels closer to what the person would actually want.
    
    Typos in casing or stray spaces ("Pop" vs "pop", " happy" vs "happy") no longer throw off matching, and out-of-range energy inputs (1.5, -0.5) use the same as their nearest valid value instead of tanking every score. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

    A full genre+mood match (1.0+1.0=2.0) still tends to beat a song that only has great energy, since energy alone maxes out at 2.0 and would need to be a near-perfect fit to catch up so genre and mood still matter more in practice, just not by as lopsided a margin as before. Genre/mood matching also still requires the words themselves to line up (just not the casing/spacing anymore), so a synonym or near-miss like "hip-hop" vs "hip hop" would still fail to match. 
    
    With only 18 songs and almost one per genre, a genre match doesn't narrow down real choices, and once that single match is used up, the rest of the top 5 is just whichever songs have the closest raw energy, which is why the same handful of high/low-energy songs (Gym Hero, Iron Fury, Storm Runner, Neon Euphoria, Sunrise City) keeps reappearing for unrelated profiles like Zen and Seven. The scoring also still only considers genre, mood, and energy while tempo, valence, danceability, and acousticness are tracked per song but never used.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

    I tested the 4 main profiles (Starter, Jumin, Zen, Seven) plus the 7 edge cases in section 10. The main surprise: clamping fixed extreme/negative energy silently tanking scores, and the Zen profile still gets zero real matches since its genre/mood don't exist in the catalog, that one needs more data, not a weight fix.

    Profile comparisons:

    - Starter vs. Jumin: high energy vs. low energy flips the whole list from upbeat pop to slow ambient/classical.
    - Starter vs. Seven: both want high energy, so lists overlap, but the genre swap changes who wins #1 (Sunrise City vs. Neon Euphoria).
    - Jumin vs. Zen: Jumin gets a real genre match at #1; Zen's genre doesn't exist, so it just gets "whatever's loudest."
    - Zen vs. Seven: near-identical filler songs since both want near-max energy, Seven's genre is real so it gets a true #1 match, Zen doesn't.
    - Case/whitespace vs. Starter: now identical output, proving formatting no longer matter.
    - Extreme vs. Negative energy: both have a valid boundary and have a clean genre+mood match at #1.

    Why does Gym Hero keep showing up for "Happy Pop" fans? It's genuinely pop (genre) and its energy (0.93) is close enough to 0.8 (energy), it just misses on mood ("intense," not "happy"). 2 out of 3 is enough to outrank songs with no genre match at all.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

    - Actually use valence, danceability, and acousticness as secondary scoring signals instead of just storing them.
    - Add a diversity rule so the top 5 aren't dominated by the same high-energy filler songs when there's no real genre/mood match.
    - Flag "no real match found" when genre and mood both miss, instead of showing an energy-only fallback with the same confidence as a real match.
    - Let users list more than one genre/mood, so blended tastes aren't forced into a single label.
    - Grow the dataset so most genres have more than one song, which would make ranks 2-5 meaningfully different instead of collapsing to raw energy order.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

    - I realized that reweighting genre/mood/energy didn't fix the "same songs keep reappearing" bug. That came from the dataset having  only about 1 song per genre, not from the math. It taught me to trace a bad result back to its actual cause instead of just tweaking the nearest number and showed me how important testing data is.

    - AI was useful for quickly explaining why a specific song scored the way it did and for rerunning all 11 profiles after every code change so I could compare before/after. I double-checked by rerunning main.py myself and reading the raw scores rather than trusting a described outcome, since claims to fix the logic turned out to sometimes be wrong until I saw the actual output.

    - What surprised me was how much a system built from three additions and an if statement can still feel like a real opinion, genre + mood + energy is barely any logic at all, but seeing it correctly separate "Happy Pop" from "calm classical" made it feel more than just arithmetic.

    - If I had more time, I would try growing the dataset so genres aren't 1-song silos, and adding a real diversity rule so no-match profiles don't just return the same 5 loudest songs every time.

## 10. Edge Case Outputs
```
    Loaded songs: 18

    Top Recommendations - Conflicted energy vs. mood
    ================================================

    1. Wilted Fields by Hollow Pine - Score: 3.40/4.00
    Reasons: genre match (+2.0), mood match (+1.0), energy closeness (+0.40)

    2. Storm Runner by Voltline - Score: 0.99/4.00
    Reasons: energy closeness (+0.99)

    3. Neon Euphoria by Pulse Horizon - Score: 0.98/4.00
    Reasons: energy closeness (+0.98)

    4. Gym Hero by Max Pulse - Score: 0.97/4.00
    Reasons: energy closeness (+0.97)

    5. Iron Fury by Ashen Throne - Score: 0.93/4.00
    Reasons: energy closeness (+0.93)


    Top Recommendations - Nonexistent genre
    =======================================

    1. Rooftop Lights by Indigo Parade - Score: 1.84/4.00
    Reasons: mood match (+1.0), energy closeness (+0.84)

    2. Sunrise City by Neon Echo - Score: 1.78/4.00
    Reasons: mood match (+1.0), energy closeness (+0.78)

    3. Sunset Skank by Coral Tide - Score: 1.00/4.00
    Reasons: energy closeness (+1.00)

    4. Dust Road Memories by Wilder Pines - Score: 0.90/4.00
    Reasons: energy closeness (+0.90)

    5. Velvet Whisper by Nadia Rose - Score: 0.85/4.00
    Reasons: energy closeness (+0.85)


    Top Recommendations - Extreme energy (>1.0)
    ===========================================

    1. Iron Fury by Ashen Throne - Score: 3.47/4.00
    Reasons: genre match (+2.0), mood match (+1.0), energy closeness (+0.47)

    2. Gym Hero by Max Pulse - Score: 0.43/4.00
    Reasons: energy closeness (+0.43)

    3. Storm Runner by Voltline - Score: 0.41/4.00
    Reasons: energy closeness (+0.41)

    4. Neon Euphoria by Pulse Horizon - Score: 0.38/4.00
    Reasons: energy closeness (+0.38)

    5. Sunrise City by Neon Echo - Score: 0.32/4.00
    Reasons: energy closeness (+0.32)


    Top Recommendations - Negative energy (<0.0)
    ============================================

    1. Moonlight Sonata Dreams by Aria Solstice - Score: 3.35/4.00
    Reasons: genre match (+2.0), mood match (+1.0), energy closeness (+0.35)

    2. Spacewalk Thoughts by Orbit Bloom - Score: 0.22/4.00
    Reasons: energy closeness (+0.22)

    3. Wilted Fields by Hollow Pine - Score: 0.20/4.00
    Reasons: energy closeness (+0.20)

    4. Library Rain by Paper Lanterns - Score: 0.15/4.00
    Reasons: energy closeness (+0.15)

    5. Coffee Shop Stories by Slow Stereo - Score: 0.13/4.00
    Reasons: energy closeness (+0.13)


    Top Recommendations - Case/whitespace mismatch
    ==============================================

    1. Sunrise City by Neon Echo - Score: 0.98/4.00
    Reasons: energy closeness (+0.98)

    2. Corner Hustle by Tre Nine - Score: 0.98/4.00
    Reasons: energy closeness (+0.98)

    3. Rooftop Lights by Indigo Parade - Score: 0.96/4.00
    Reasons: energy closeness (+0.96)

    4. Night Drive Loop by Neon Echo - Score: 0.95/4.00
    Reasons: energy closeness (+0.95)

    5. Neon Euphoria by Pulse Horizon - Score: 0.92/4.00
    Reasons: energy closeness (+0.92)


    Top Recommendations - Frankenstein (split genre/mood match)
    ===========================================================

    1. Sunset Skank by Coral Tide - Score: 2.90/4.00
    Reasons: genre match (+2.0), energy closeness (+0.90)

    2. Iron Fury by Ashen Throne - Score: 1.53/4.00
    Reasons: mood match (+1.0), energy closeness (+0.53)

    3. Dust Road Memories by Wilder Pines - Score: 1.00/4.00
    Reasons: energy closeness (+1.00)

    4. Velvet Whisper by Nadia Rose - Score: 0.95/4.00
    Reasons: energy closeness (+0.95)

    5. Midnight Coding by LoRoom - Score: 0.92/4.00
    Reasons: energy closeness (+0.92)


    Top Recommendations - No signal (unknown genre + mood)
    ======================================================

    1. Dust Road Memories by Wilder Pines - Score: 1.00/4.00
    Reasons: energy closeness (+1.00)

    2. Velvet Whisper by Nadia Rose - Score: 0.95/4.00
    Reasons: energy closeness (+0.95)

    3. Midnight Coding by LoRoom - Score: 0.92/4.00
    Reasons: energy closeness (+0.92)

    4. Focus Flow by LoRoom - Score: 0.90/4.00
    Reasons: energy closeness (+0.90)

    5. Sunset Skank by Coral Tide - Score: 0.90/4.00
    Reasons: energy closeness (+0.90)
```
