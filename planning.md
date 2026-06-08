# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

The GMU Student Survival Guide is a RAG system that helps students search and access unofficial knowledge about George Mason University. The system focuses on student-generated experiences and advice that are often difficult to find through official university resources. Topics include choosing majors, course selection, professor recommendations, campus life, study locations, freshman advice, housing, social life, and academic success.

This knowledge is valuable because university websites and course catalogs provide official information, but they rarely capture the practical advice, experiences, and recommendations that students share with one another. By collecting and organizing these discussions, the system allows users to ask natural-language questions and receive grounded answers based on real student experiences.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |GMU Reddit: "idk what to do with my life :/| Student discussion about choosing majors, career uncertainty, IT, criminology, forensics, and career planning |https://www.reddit.com/r/gmu/comments/1i24nqp/idk_what_to_do_with_my_life/ |
| 2 |GMU Reddit: "Fall Class Registration begins on the fourth, please use this thread to ask about class recommendations" | Student recommendations regarding professors, course difficulty, scheduling, and registration advice | https://www.reddit.com/r/gmu/comments/89hfti/fall_class_registration_begins_on_the_fourth/ |
| 3 |GMU Reddit: "Hidden Spots around campus" | Student recommendations for quiet, hidden, and interesting locations around campus. | https://www.reddit.com/r/gmu/comments/q6vua9/hidden_spots_around_campus/ |
| 4 |GMU Reddit: "Please stop complaining about GMU" | Discussion about campus culture, social life, commuting, internships, opportunities, and student experiences | https://www.reddit.com/r/gmu/comments/1gvqw12/please_stop_complaining_about_gmu/ |
| 5 |GMU Reddit: "Freshman looking for advice on everything" | Comprehensive freshman advice covering academics, housing, dining, campus resources, social life, and study habits. | https://www.reddit.com/r/gmu/comments/15s8o3f/freshman_looking_for_advice_on_everything/ |
| 6 | Fourth Estate: "Off-Campus Housing Issues" |Student-focused article discussing housing safety, landlord issues, tenant rights, and off-campus housing risks.| https://gmufourthestate.com/2019/02/04/off-campus-housing-issues/ |
| 7 | Fourth Estate: "Expanding Fenwick Library hours: a necessary step for student success" | Student perspective on study spaces, commuter challenges, library access, and academic success at GMU | https://gmufourthestate.com/2025/03/04/expanding-fenwick-library-hours-a-necessary-step-for-student-success/ |
| 8 | Fourth Estate: "Mason's Parking Crisis" | Student-focused reporting on parking shortages, permit costs, commuter challenges, lot capacity, and proposed solutions | https://gmufourthestate.com/2024/09/24/masons-parking-crisis/ |
| 9 | Fourth Estate: "Retail Dining: Monetary Mosquito or Satitating Savior? | Analysis of on-campus dining options, food affordability, student discounts, meal costs, and dining convenience. | https://gmufourthestate.com/2026/04/16/retail-dining-monetary-mosquito-or-satiating-savior/ |
| 10 | Fourth Estate: "Getting Involved on Campus" | Student guidance on clubs, organizations, research opportunities, campus jobs, networking, leadership roles, and building community at GMU. | https://gmufourthestate.com/2015/09/03/getting-involved-on-campus/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 800 Characters**

**Overlap: 150 Characters**

**Reasoning: The corpus consists primarily of Reddit discussions and student-written news articles. These documents are relatively short and often contain multiple independent topics within a single thread or article. A chunk size of approximately 800 characters is large enough to preserve context while remaining focused on a specific idea. An overlap of 150 characters helps prevent important information from being split across chunk boundaries and improves retrieval quality when relevant information spans adjacent chunks. **

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:all-MiniLM-L6-v2 (Sentence Transformers)**

**Top-k:5**

**Production tradeoff reflection: The all-MiniLM-L6-v2 model was selected because it is lightweight, fast, free to run locally, and performs well on semantic similarity tasks. For a production deployment, larger embedding models could potentially improve retrieval quality, especially for nuanced student discussions and longer documents. However, larger models require more computation, storage, and latency. A production system would balance retrieval accuracy against response speed, infrastructure costs, and scalability. Additional considerations would include multilingual support and the ability to handle domain-specific terminology.**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What advice do GMU students give incoming freshmen? | Students recommend time management, attending class, getting involved on campus, using campus resources, and avoiding procrastination. |
| 2 | What do students say about choosing a major when you are undecided? | Students encourage exploring interests, speaking with advisors, considering career goals, and avoiding choosing a major solely for money. |
| 3 | What concerns do students have about parking at GMU? | Students report limited parking availability, high permit costs, lot congestion, and frustration finding spaces before class. |
| 4 | What challenges do students face when searching for off-campus housing? | Students may encounter unreliable landlords, limited university oversight, and should carefully vet housing options before signing leases. |
| 5 | What resources are available for students who want to get involved on campus? | Students can use Get Connected, join clubs and organizations, participate in research opportunities, attend campus events, and explore leadership roles. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some Reddit discussions contain multiple topics within the same thread. Important information may be spread across several comments, making it possible for retrieval to return only part of the relevant context.

2. Student opinions may conflict with one another. For example, one student may recommend a professor while another strongly discourages taking the same professor. The retrieval system may return conflicting viewpoints, requiring the language model to summarize multiple perspectives accurately.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Sentence Transformers (all-MiniLM-L6-v2)
|
v
ChromaDB (Vector Database)
|
v
User question
|
v
query embedding
|
v
Retreive Top-5 Chunks
|
v
Groq API (Llama 3)
|
v
Grounded Response
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use ChatGPT to help implement document ingestion and chunking functions. I will provide my Chunking Strategy section from this planning document, including the 800-character chunk size and 150-character overlap requirements. I expect ChatGPT to generate Python functions that read documents, clean text, and split content into chunks according to the specification. I will verify the output by checking that chunks are generated with the correct size and overlap and that no document content is lost.
**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT to help implement the embedding and retrieval pipeline. I will provide the Retrieval Approach section of this planning document, including the all-MiniLM-L6-v2 embedding model and Top-k value of 5. I expect ChatGPT to generate code that creates embeddings, stores them in ChromaDB, and retrieves relevant chunks for a user query. I will verify the output by testing retrieval against the evaluation questions and checking whether relevant chunks are returned.
**Milestone 5 — Generation and interface:**
I will use ChatGPT to help implement grounded response generation using Groq and Llama 3. I will provide the Architecture section and explain how retrieved chunks should be passed to the language model. I expect ChatGPT to generate code for prompt construction, source attribution, and response generation. I will verify the output by ensuring that responses are based on retrieved documents and do not introduce unsupported information.