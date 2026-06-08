# The Unofficial Guide — Project 1

## Domain

This system covers student-generated knowledge about George Mason University. The knowledge includes advice for incoming freshmen, major and career selection guidance, professor and course recommendations, parking concerns, off-campus housing experiences, campus involvement opportunities, dining experiences, study spaces, and overall student perspectives about life at GMU.

This knowledge is valuable because it reflects the experiences and recommendations of actual students rather than official university publications. While university websites provide official policies and resources, they often do not capture practical advice, common frustrations, hidden opportunities, or informal knowledge that students share with one another. The goal of this project is to make this unofficial student knowledge searchable through a retrieval-augmented generation (RAG) system.
---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |GMU Reddit: "idk what to do with my life"| Reddit Discussion| https://www.reddit.com/r/gmu/comments/1i24nqp/idk_what_to_do_with_my_life/ |
| 2 |GMU Reddit: "Fall Class Registration begins on the fourth, please use this thread to ask about class recommendations" | Reddit Discussion | https://www.reddit.com/r/gmu/comments/89hfti/fall_class_registration_begins_on_the_fourth/ |
| 3 |GMU Reddit: "Hidden Spots around campus" | Reddit Discussion | https://www.reddit.com/r/gmu/comments/q6vua9/hidden_spots_around_campus/ |
| 4 |GMU Reddit: "Please stop complaining about GMU" | Reddit Discussion | https://www.reddit.com/r/gmu/comments/1gvqw12/please_stop_complaining_about_gmu/ |
| 5 |GMU Reddit: "Freshman looking for advice on everything" | Reddit Discussion | https://www.reddit.com/r/gmu/comments/15s8o3f/freshman_looking_for_advice_on_everything/ |
| 6 | Fourth Estate: "Off-Campus Housing Issues" |News Article| https://gmufourthestate.com/2019/02/04/off-campus-housing-issues/ |
| 7 | Fourth Estate: "Expanding Fenwick Library hours: a necessary step for student success" | News Article| https://gmufourthestate.com/2025/03/04/expanding-fenwick-library-hours-a-necessary-step-for-student-success/ |
| 8 | Fourth Estate: "Mason's Parking Crisis" | News Article | https://gmufourthestate.com/2024/09/24/masons-parking-crisis/ |
| 9 | Fourth Estate: "Retail Dining: Monetary Mosquito or Satiating Savior?" | News Article | https://gmufourthestate.com/2026/04/16/retail-dining-monetary-mosquito-or-satiating-savior/ |
| 10 | Fourth Estate: "Getting Involved on Campus" |News Article | https://gmufourthestate.com/2015/09/03/getting-involved-on-campus/ |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Why these choices fit your documents:** Before chunking, I cleaned the source documents by removing usernames, advertisements, Reddit interface elements, voting information, and other irrelevant text. I also reorganized the content into consistent text documents to improve retrieval quality. The corpus consists primarily of student discussions, advice posts, and campus news articles. An 800-character chunk size preserves enough context for meaningful retrieval while remaining small enough for precise semantic search. A 150-character overlap helps prevent important information from being split across chunk boundaries and improves retrieval quality when related information spans multiple chunks.

**Final chunk count:** 78 chunks

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:** I selected all-MiniLM-L6-v2 because it is lightweight, fast, and widely used for semantic search applications. It provides strong retrieval performance while running locally without requiring additional API costs. If cost were not a constraint, I would evaluate larger embedding models with stronger semantic understanding, longer context support, and better performance on domain-specific educational content. Larger models could improve retrieval accuracy but would increase latency, storage requirements, and computational costs.

---

## Grounded Generation


**System prompt grounding instruction:** The system prompt instructs the language model to answer using only the retrieved context. It explicitly states:

"Answer the user's question using ONLY the provided context. If the context does not contain enough information, say that the documents do not provide enough information. Do not make up facts. Cite the source file names you used."

This instruction reduces hallucinations and encourages the model to remain grounded in retrieved documents.

**How source attribution is surfaced in the response:** The retrieval system provides the source filename for every retrieved chunk. During generation, the model receives both the chunk text and its source identifier. Responses include references to the source documents used to construct the answer, allowing users to identify where information originated.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What advice do GMU students give incoming freshmen? |Students recommend time management, attending class, getting involved on campus, using campus resources, and avoiding procrastination |The system recommended time management, reviewing syllabi, avoiding procrastination, tracking deadlines, and attending office hours |Relevant |Accurate |
| 2 |What do students say about choosing a major when you are undecided? |Students encourage exploring interests, speaking with advisors, considering career goals, and avoiding choosing a major solely for money. |The system explained that students recommend exploring interests, using Career Services, considering long-term fulfillment, and not selecting a major based only on salary. |Relevant |Accurate |
| 3 |What concerns do students have about parking at GMU? |Students report limited parking availability, high permit costs, lot congestion, and frustration finding spaces before class. |The system identified parking shortages, expensive permits, congestion, long searches for parking, and student frustration |Relevant |Accurate |
| 4 |What challenges do students face when searching for off-campus housing? |Students may encounter unreliable landlords, limited university oversight, and should carefully vet housing options before signing leases |The system identified predatory landlords, unreliable listings, limited oversight, tenant-landlord disputes, and safety concerns. |Relevant |Accurate |
| 5 |What resources are available for students who want to get involved on campus? |Students can use Get Connected, join clubs and organizations, participate in research opportunities, attend campus events, and explore leadership roles. |The system described Get Connected, student organizations, research opportunities, campus jobs, leadership positions, and networking opportunities. |Relevant |Accurate |

**Retrieval quality:** Relevant
**Response accuracy:** Accurate 
Overall, the system successfully retrieved relevant chunks for all five evaluation questions and generated grounded answers that matched the expected outcomes. This suggests that the retrieval and generation pipeline performed reliably on the selected test cases.
---

## Failure Case Analysis


**Question that failed:** What are the best professors at GMU?

**What the system returned:** The system returned information about course registration advice and a limited set of professor recommendations from the registration discussion.

**Root cause (tied to a specific pipeline stage):** The corpus contains only one source focused on professor recommendations. Because the document collection did not include enough professor-review data, retrieval could only return a small amount of relevant information. The issue was caused primarily by limitations in the document collection stage rather than the retrieval algorithm.

**What you would change to fix it:** I would add additional sources such as more professor recommendation discussions, course review threads, and student feedback documents. Expanding the corpus would provide broader coverage and improve retrieval quality for professor-related questions.

---

## Spec Reflection

**One way the spec helped you during implementation:** The planning document helped organize the project before any coding began. Defining the domain, document sources, chunking strategy, evaluation questions, and retrieval approach made it easier to implement each stage of the RAG pipeline systematically. Having a clear specification reduced confusion and provided a roadmap for building ingestion, retrieval, and generation components. 

**One way your implementation diverged from the spec, and why:** My implementation evolved as I collected documents and tested retrieval. Initially, I expected to use raw Reddit discussions and articles directly, but I decided to clean and restructure the documents into consistent formats before ingestion. This improved retrieval quality by removing usernames, advertisements, and irrelevant content while preserving the most useful student-generated knowledge.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I provided my project requirements, planning document, and the desired chunking strategy.
- *What it produced:* The AI generated the document ingestion and chunking code used to load text files and split them into overlapping chunks.
- *What I changed or overrode:* I adjusted the chunk size and overlap values to better fit the structure of my student discussion documents and verified that the implementation produced meaningful chunks.

**Instance 2**

- *What I gave the AI:* I provided the retrieval requirements and project architecture, including the use of ChromaDB, sentence-transformers, and Groq.
- *What it produced:* The AI generated code for vector embeddings, semantic retrieval, and grounded response generation using Llama 3.1 through the Groq API.
- *What I changed or overrode:* I modified the prompts to enforce grounding, added source attribution, tested multiple retrieval queries, and verified that the system answered using only retrieved documents.
