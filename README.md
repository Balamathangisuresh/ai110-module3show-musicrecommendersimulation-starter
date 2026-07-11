# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

 **Replace this paragraph with your own summary of what your version does.**

---

## How The System Works

Explain your design in plain language.

  - Real-world recommendation systems use a hybrid approach combining collaborative filtering (tracking what similar users listen to) and content-based filtering (analyzing the specific features of a track). Because the simulation works with a localized dataset without a network of live user history, it prioritizes a pure content-based approach. My system calculates an explicit compatibility score between a user's defined taste profile and a track's metadata attributes. It prioritizes fixed, broad taste signals like genre above all else, using fine-grained granular attributes to filter and break ties among closely matching tracks.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

  In the simulation, each Song uses four traits: genre, mood, energy (scaled 0.0 to 1.0), and tempo_bpm. The UserProfile stores what the user wants to hear: favorite_genre, favorite_mood, and target_energy.

  The Recommender scores each individual song by adding flat points: +2.0 points for a matching genre, +1.0 point for a matching mood, and up to 1.0 point based on how close the song's energy is to the user's target. To choose which songs to suggest, the system collects all the scores, sorts them from highest to lowest, and breaks any point ties by looking for the closest energy match before falling back alphabetically by title to return the final top number of recommendations.

  Some biases:
    Genre-dominance bias: Genre is worth 2 points vs. mood's 1 and energy's max 1, so an exact genre match will almost always outrank a song with a near-perfect mood + energy fit but the "wrong" genre tag.

    Exact-match brittleness: "indie pop" and "pop" score as total strangers (0 credit each), same as "indie pop" vs. "metal." The system can't reward genre-adjacent songs, so musically similar tracks get penalized as harshly as totally unrelated ones.

    Arbitrary tie-break advantage: The id-ascending tie-breaker systematically favors earlier-added songs (the original 10 vs. the 8 you added later) whenever totals tie exactly, an ordering effect that has nothing to do with taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
  Loaded songs: 18

  Top Recommendations
  ===================

  1. Sunrise City by Neon Echo - Score: 3.98/4.00
    Reasons: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)

  2. Gym Hero by Max Pulse - Score: 2.87/4.00
    Reasons: genre match (+2.0), energy closeness (+0.87)

  3. Rooftop Lights by Indigo Parade - Score: 1.96/4.00
    Reasons: mood match (+1.0), energy closeness (+0.96)

  4. Corner Hustle by Tre Nine - Score: 0.98/4.00
    Reasons: energy closeness (+0.98)

  5. Night Drive Loop by Neon Echo - Score: 0.95/4.00
    Reasons: energy closeness (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

  - First, I tried rebalancing the weights from genre=2.0/mood=1.0/energy≤1.0 to genre=1.0/mood=1.0/energy≤2.0. Full genre+mood matches still win overall, but a strong energy fit can now beat a weaker categorical match, e.g. for the Starter profile, Rooftop Lights (mood match only, close energy) now outranks Gym Hero (genre match only, farther energy), which didn't happen under the old weights.

  - I next fixed case/whitespace matching by normalizing genre and mood (.strip().lower()) before comparing. The "Case/whitespace mismatch" test profile ("Pop", " happy") used to lose its genre/mood match and fall back to an energy-only ranking; it now scores identically to the Starter profile.

  - Then finally I clamped energy to [0, 1] before scoring. Before this, requesting energy 1.5 or -0.5 didn't crash, but it quietly tanked every song's score by measuring distance from an out-of-range target; clamping makes those inputs behave the same as requesting exactly 1.0 or 0.0.

  - Didn't add tempo, valence, danceability, or acousticness to the score, the catalog tracks them per song, but the current scoring logic still only uses genre, mood, and energy.

  - Across different "types" of users (high energy vs. low energy, genre that exists vs. genre that doesn't), the system behaves sensibly when there's a real match to find, but collapses to "just the loudest/quietest songs" whenever a user's genre and mood are both missing from the catalog (see the Zen profile).

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

  - The catalog is only 18 songs, and almost every genre has just one representative track, so a genre match doesn't offer real choice so it just crowns whichever single song happens to exist.

  - Energy now carries the single biggest weight, so it can unintentionally favor whichever songs sit at the extreme ends (highest/lowest energy) of the catalog whenever a user's genre or mood isn't represented at all.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

  Building this made it clear that a recommender doesn't need anything close to "understanding" music to feel like it has taste and that it's just a handful of numeric bonuses added together and sorted. Genre and mood matching are literally string equality checks, and energy is just one minus a distance; there's no sense of what a genre or mood actually means. Whatever "personality" the system seems to have comes entirely from how those few weights are tuned relative to each other, not from any real insight into the songs.

  Bias shows up in two places that aren't obvious just from reading the scoring formula: whichever feature has the highest weight (originally genre, now energy) quietly decides the personality of the whole system, and the dataset itself can bias results just as much as the weights do, with only one song per genre, a match doesn't mean the best song for that taste, it means the only song, and when a user's taste isn't represented at all, the system falls back to recommending whatever's loudest or quietest in the whole catalog, regardless of how unrelated it is to what was actually asked for.



