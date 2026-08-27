<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=venom&color=0:1B0F3B,100:FF2E88&height=200&section=header&text=RAJSHEKHAR%20DAS&fontSize=52&fontColor=FFE45E&fontAlignY=40&desc=Software%20Engineer%20%C2%B7%20Systems%2C%20Backends%20and%20Applied%20AI&descSize=16&descAlignY=62" />

<img src="https://readme-typing-svg.demolab.com?font=Press+Start+2P&size=15&pause=1000&color=FFE45E&center=true&vCenter=true&width=820&height=80&lines=SOFTWARE+ENGINEER+%2F%2F+SYSTEMS+%26+APPLIED+AI;SWE+INTERN+%40+HSBC+%C2%B7+CSE+%40+NIT+DURGAPUR;REAL-TIME+BACKENDS+%C2%B7+LOW-LEVEL+C+%C2%B7+LLM+SYSTEMS;BUILDING+TOWARD+GENERATIVE+AI+%26+DEEP+LEARNING" alt="Software engineer, systems and applied AI" />

[![LinkedIn](https://img.shields.io/badge/LINKEDIN-6C4CFF?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=1B0F3B)](https://www.linkedin.com/in/rajshekhar25/)
[![LeetCode](https://img.shields.io/badge/LEETCODE-FFE45E?style=for-the-badge&logo=leetcode&logoColor=1B0F3B&labelColor=1B0F3B)](https://leetcode.com/u/0xRajshekhar/)
[![Codeforces](https://img.shields.io/badge/CODEFORCES-FF2E88?style=for-the-badge&logo=codeforces&logoColor=white&labelColor=1B0F3B)](https://codeforces.com/profile/0xRajshekhar)
[![CodeChef](https://img.shields.io/badge/CODECHEF-8DE8FF?style=for-the-badge&logo=codechef&logoColor=1B0F3B&labelColor=1B0F3B)](https://www.codechef.com/users/rajshekhar25)
[![Email](https://img.shields.io/badge/EMAIL-FF2E88?style=for-the-badge&logo=gmail&logoColor=white&labelColor=1B0F3B)](mailto:rajshekhardas85@gmail.com)
[![GitHub](https://img.shields.io/badge/GITHUB-6C4CFF?style=for-the-badge&logo=github&logoColor=white&labelColor=1B0F3B)](https://github.com/Rajshekhar25?tab=repositories)

</div>

```
+==================================================================+
|  SYSTEM PROFILE                                    NIT DURGAPUR  |
+==================================================================+
|  ENGINEER    Rajshekhar Das                                      |
|  EDUCATION   B.Tech CSE, NIT Durgapur                            |
|  EXPERIENCE  Software Engineering Intern, HSBC                   |
|  DOMAIN      Backend systems . compliance tooling . applied AI   |
|  LANGUAGES   JavaScript/TypeScript, Python, C, C++               |
|  EXPLORING   Generative AI, deep learning, distributed systems   |
|  STATUS      Open to SDE internships and new grad roles          |
+==================================================================+
```

## &nbsp;`//`&nbsp; EXPERIENCE

### Software Engineering Intern &nbsp;·&nbsp; HSBC

Change-management compliance tooling, in Python — turning a written governance
catalogue into something a machine can decide on, and defend.

- Built a **compliance engine** that evaluates enterprise Change Requests against a
  data-driven SDLC and deployment governance control catalogue, producing a
  **deterministic, auditable approve / not-approve verdict with per-control reasoning**.
- Built a **live evidence-probing service** over the Jira, GitHub and Confluence REST APIs
  that authenticates and validates the state of every artefact linked as Change Request
  evidence, rather than trusting what the ticket claims.
- Designed a **three-state evaluation model** — passed / failed / manual — that promotes
  controls it cannot verify to an external IT governance system instead of guessing, with
  PAT-based Bearer authentication wired across all three APIs.
- Engineered a **fully offline pytest suite** with mocked HTTP clients and JSON fixtures, so
  the whole engine tests deterministically with no credentials and no network.

### Elsewhere

| Role | Where | What I worked on |
|:--|:--|:--|
| **Contributor** | **Brabble.ai** | Built [Brabble-Bites](https://github.com/Rajshekhar25/Brabble-Bites), the email digest feature — scheduled aggregation, Handlebars templating and delivery. |
| **Backend Developer** | **NITMUN XIII** | Designed and shipped the [registration backend](https://github.com/Rajshekhar25/NITMUN_XIII_Backend) and [conference site](https://github.com/Rajshekhar25/NITMUN-XIII) used by the delegate intake for NIT Durgapur's Model UN. |

<sub>Smart India Hackathon 2025 — built the [GIA beneficiary identification system](https://github.com/Rajshekhar25/SIH2025-25152) (problem statement 25152).</sub>

```
+==================================================================+
|  ENGINEERING FOCUS                                SELF-ASSESSED  |
+==================================================================+
|  BACKEND / APIs           [###################---]  88%          |
|  REAL-TIME / CONCURRENCY  [##################----]  82%          |
|  DATABASES / MODELING     [#################-----]  78%          |
|  SYSTEMS PROGRAMMING      [################------]  72%          |
|  APPLIED GENAI / LLMs     [#################-----]  76%          |
|  DEEP LEARNING            [##############--------]  62%          |
|  DSA / PROBLEM SOLVING    [##################----]  80%          |
+==================================================================+
```

## &nbsp;`//`&nbsp; SELECTED SYSTEMS

| System | What it is | What it demonstrates | Stack |
|:--|:--|:--|:--|
| **[SnackGPT](https://github.com/Rajshekhar25/SnackGPT)** | Nutrition tracker driven by natural language. | **LLMs in production.** Editable model output before any write, rate limiting counted in Postgres so it survives stateless serverless functions, and full graceful degradation — the manual path keeps working when the model is down. | Next.js · Prisma · PostgreSQL · Gemini |
| **[Chess Arena](https://github.com/Rajshekhar25/Chess_App)** | Real-time two-player chess over WebSockets. | **Authoritative server design.** The server is the sole authority on move legality and turn order; clients only render. Per-match Socket.io rooms, cookie-based seat identity that survives reconnects, and every move persisted to SQLite so a restart resumes play. CI on every push. | Node · Socket.io · SQLite · Docker |
| **[MCQ Exam System](https://github.com/Rajshekhar25/MCQ_Exam_System)** | End-to-end online examination platform. | **A complete transactional loop** — authentication, timed sessions, question banks, submission and scoring. Not a demo screen. | MERN |
| **[CodeMate](https://github.com/Rajshekhar25/CodeMate)** | AI-assisted code review pipeline. | Feeding diffs to a model and turning free-form output into structured, reviewable findings. | Node · LLM |
| **[CramBot](https://github.com/Rajshekhar25/CramBot)** | Containerised Python study assistant. | Reproducible builds and deployment — Dockerfile, pinned environment, runs identically anywhere. | Python · Docker |
| **[DiNoSignal](https://github.com/Rajshekhar25/DiNoSignal)** | A fixed-timestep render loop and collision engine in pure C. | **Systems programming without a net** — manual frame buffer, fixed-timestep loop, collision detection and input handling with no engine, no framework and no garbage collector. | C |
| **[Auth101](https://github.com/Rajshekhar25/Auth101)** | Session authentication built from primitives. | Cookie-based sessions, hashing and protected routes implemented directly rather than delegated to a library. | MERN |
| **[Blogster](https://github.com/Rajshekhar25/Blogster)** · **[TrackMate](https://github.com/Rajshekhar25/TrackMate)** · **[Plinkoo](https://github.com/Rajshekhar25/Plinkoo)** | Publishing platform, device tracking service, and a probability simulation. | Typed frontends, geolocation streams, and physics-driven probability simulation. | TypeScript · JavaScript |

## &nbsp;`//`&nbsp; GENERATIVE AI &amp; DEEP LEARNING

Most of my recent work sits where conventional backend engineering meets model output — the
interesting problems are not the prompts, they are everything around them.

- **Shipping with LLMs, not demoing with them.** [SnackGPT](https://github.com/Rajshekhar25/SnackGPT) treats the model as an untrusted
  upstream: structured output is validated, surfaced to the user for confirmation before it
  is written, rate limited per user in the database, and fully bypassable when the API fails.
- **Retrieval and structured generation** — constraining a model to a schema and to a budget
  computed in plain code rather than asking the model to do arithmetic.
- **Currently studying** — transformer internals, PyTorch, training and fine-tuning workflows,
  embeddings and retrieval-augmented generation, and the systems work that makes inference
  affordable at scale.

<div align="center">
<img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,sklearn,fastapi,docker&perline=6" />
</div>

## &nbsp;`//`&nbsp; COMPETITIVE PROGRAMMING

- **Codeforces [@0xRajshekhar](https://codeforces.com/profile/0xRajshekhar)** · **LeetCode [@0xRajshekhar](https://leetcode.com/u/0xRajshekhar/)** · **CodeChef [@rajshekhar25](https://www.codechef.com/users/rajshekhar25)**
- I maintain [**CP-resources**](https://github.com/Rajshekhar25/CP-resources), my own snippet and template library for contests.

<div align="center">

<img height="185" src="https://leetcard.jacoblin.cool/0xRajshekhar?theme=nord&font=JetBrains%20Mono&ext=heatmap" alt="LeetCode statistics" />
<img height="185" src="https://codeforces-readme-stats.vercel.app/api/card?username=0xRajshekhar&theme=nord" alt="Codeforces rating" />

</div>

<sub>Both cards are generated live on every page load — rating and solve counts stay current with no maintenance.</sub>

## &nbsp;`//`&nbsp; STACK

<div align="center">

**Languages and runtime**

<img src="https://skillicons.dev/icons?i=cpp,c,js,ts,python,nodejs,bash&perline=7" />

**Backend, data and infrastructure**

<img src="https://skillicons.dev/icons?i=express,nextjs,react,tailwind,mongodb,postgres,prisma,redis,docker,linux,git,vercel&perline=12" />

</div>

## &nbsp;`//`&nbsp; CONTRIBUTION GRAPH

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/output/snake-dark.svg" />
  <img alt="Contribution graph being consumed by a snake" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/output/snake.svg" />
</picture>

</div>

## &nbsp;`//`&nbsp; METRICS

<div align="center">

<img width="88%" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/profile-summary-card-output/2077/0-profile-details.svg" alt="Profile details" />

<img width="44%" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/profile-summary-card-output/2077/3-stats.svg" alt="Contribution stats" />
<img width="44%" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/profile-summary-card-output/2077/4-productive-time.svg" alt="Productive time" />

<img width="44%" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/profile-summary-card-output/2077/1-repos-per-language.svg" alt="Repositories per language" />
<img width="44%" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/profile-summary-card-output/2077/2-most-commit-language.svg" alt="Most committed language" />

<img src="https://komarev.com/ghpvc/?username=Rajshekhar25&color=FF2E88&style=for-the-badge&label=PROFILE+VIEWS" />

</div>

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=venom&color=0:FF2E88,100:1B0F3B&height=120&section=footer&text=Let%27s%20build%20something%20that%20holds%20up%20under%20load.&fontSize=19&fontColor=FFE45E&fontAlignY=76" />

</div>
