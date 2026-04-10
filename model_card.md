# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

TunesTuner 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This system is based on the song recommendation from spotify and youtube music, trying to combine best of both aspects of those systems. It takes the complied information of the user profile (such as favorite genre, mood) and recommends songs based on it. This a test version is for classroom exploration. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The features of each song used is genre, mood, energy along with a few optional fields to used to compare to a user's profile. The top five is chosen based on how well it matched the user's profile with number one, almost perfectly matching the profile. the system hasn't been changed much, just a few tweaks so the code can run more smoothly and the recommender to be less bias towards users. 

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are 18 total songs in songs.csv, I added eight new songs to the data set. There is pop, lofi, rock, ambient, jazz, synthwave, indie pop,  soul, aggressive, classical, reggae, blues, funk, and drum and bass. The moods represented is happy, chill, intense, chill, relaxed, moody, focused, melanocholic, aggressive, serene, uplifting, nostalgic, uplifting. The taste does this data mostly reflect a variety of people, but mainly younger people. 

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system does well with users types with high and low energy along with favorite genres or moods being pop and happy. This is because the songs in the data tend to be happy or pop songs with more extreme ends of the energy scale although it does work with the other types of data, just the results might not be accurate. 

User profiles with favorite genre being pop and favorite mood happy with all of the optional fields tend to get the best results from the system. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system struggles with figuring out middle users, extreme users are rewarded because songs cluster near their ceiling. Optional fields because very split in the system due to the users without the optional fields tend to be at the disadvange. Also acousticness has almost no voice in the system due to the fields along with some genres having more options than others. Overall a messy system. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

The types of user profiles I tested was mostly edge cases such as high energy and sad mood profile, all of the optional fields don't match, tuned to hit every bonus, and conflicting personality. I looked to push the recommendation system hard and it resulted in mainly pop songs being recommeneded since the system deemed them to be the safe option to recommend to the user. It didn't surprise me. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

If I had more time to imporve this recommender, I would go more in depth with the different songs to have a better varity instead of sticking to the user's preferences along with features such as knowing about the lyrics or language to more in line with the user's profile. 

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that recommender systems are less random than I previously thought of, taking account of user's tastes and preferences scores to best present a new favorite to the user. 