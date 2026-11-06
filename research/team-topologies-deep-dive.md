# Team Topologies: Deep Dive Research

**Source:** "Team Topologies: Organizing Business and Technology Teams for Fast Flow" by Matthew Skelton and Manuel Pais (IT Revolution Press, 2019; 2nd Edition 2025)

**Research date:** 2026-03-03

**Purpose:** Inform management automation system design. Identify which Team Topologies practices can be automated by LLMs, which require human judgment, and which benefit from continuous sensing/monitoring.

---

## Table of Contents

1. [The Four Fundamental Team Types](#1-the-four-fundamental-team-types)
2. [The Three Interaction Modes](#2-the-three-interaction-modes)
3. [Cognitive Load as Primary Design Constraint](#3-cognitive-load-as-primary-design-constraint)
4. [Conway's Law and the Inverse Conway Maneuver](#4-conways-law-and-the-inverse-conway-maneuver)
5. [Team-First Thinking vs Individual-First Thinking](#5-team-first-thinking-vs-individual-first-thinking)
6. [Fracture Planes for Splitting Teams](#6-fracture-planes-for-splitting-teams)
7. [DORA Metrics and Flow](#7-dora-metrics-and-flow)
8. [Evolution Triggers](#8-evolution-triggers)
9. [Sensing and Detecting the Need for Change](#9-sensing-and-detecting-the-need-for-change)
10. [LLM Automation Categories](#10-llm-automation-categories)

---

## 1. The Four Fundamental Team Types

Team Topologies restricts all teams in an organization to exactly four types. This constraint is deliberate — it acts as a powerful template that reduces ambiguity, clarifies responsibilities, and promotes flow. As Martin Fowler notes: "all models are wrong, some are useful. Thus Team Topologies is wrong: complex organizations cannot be simply broken down into just four kinds of teams and three kinds of interactions. But constraints like this are what makes a model useful."

The restriction to four types prevents organizational sprawl where teams have poorly defined or overlapping responsibilities. The majority of teams (6:1 to 9:1 ratio) should be stream-aligned, with the other three types existing to support them.

### 1.1 Stream-Aligned Team

**Definition:** A team aligned to a single, valuable stream of work from (usually) a segment of the business domain. This is the primary team type — the fundamental unit of delivery.

**What constitutes a "stream":**
- A single product or service
- A single set of features
- A single user journey
- A single user persona
- A geographic area
- A compliance stream
- A specific business area

**Responsibilities:**
- Full ownership of the entire flow of work from concept through production
- Full-stack and full-lifecycle: front-end, back-end, database, business analysis, feature prioritization, UX, testing, deployment, monitoring
- "You build it, you run it" — no hand-offs to other teams for any purpose
- Outcome-oriented (focused on business outcomes) rather than activity-oriented (focused on functions like testing or databases)

**Expected behaviors:**
1. Produces a steady flow of feature delivery
2. Proactively reaches out to supporting teams (enabling, platform, complicated-subsystem)
3. Team members achieve "autonomy, mastery, and purpose" (Dan Pink's intrinsic motivation)
4. Constantly learns and adapts
5. Minimal dependencies on other teams; when unavoidable, interacts through well-defined interfaces

**Capabilities within a stream-aligned team (non-exhaustive):**
- Application security
- Commercial and operational viability
- Design and architecture
- Development and coding
- Infrastructure and operability
- Metrics and monitoring
- Product management and ownership
- Testing and QA
- UX

**Key constraint:** Should not be too large — ideally a "Two Pizza Team" (5-9 people). Must remain within cognitive load limits.

### 1.2 Enabling Team

**Definition:** A team of specialists that helps stream-aligned teams overcome obstacles and detects missing capabilities. They grow relevant skills inside other teams so those teams can remain independent and better own and evolve their services.

**Purpose:** Bridge knowledge and capability gaps for stream-aligned teams. Stream-aligned teams are focused on continuous delivery and cannot easily spend time on research and upskilling.

**Responsibilities:**
- Understand problems of stream-aligned teams and provide assistance
- Research new technologies, frameworks, and practices relevant to stream-aligned teams
- Help stream-aligned teams understand constraints rather than dictating choices
- Grow stream-aligned team capabilities rather than providing solutions directly
- Proactively detect missing capabilities across the organization

**Expected behaviors:**
1. Proactively seeks to understand the needs of stream-aligned teams
2. Stays ahead of the curve in its technical domain
3. Acts as a bridge between stream-aligned teams and the broader technology community
4. Successfully upskills other teams so they become self-sufficient (then moves on)
5. Collaboration is temporary and focused — measured by how quickly teams become independent

**Key principle:** Enabling teams do not write and enforce standards. They educate and coach. The facilitating interaction mode is primary. An enabling team engagement should have clear exit criteria.

**Conversion patterns:** DBA teams become enabling teams focused on spreading awareness of database performance, monitoring, etc. Architecture teams become part-time enabling teams emphasizing that many decisions should be taken by implementing teams.

### 1.3 Complicated-Subsystem Team

**Definition:** A team responsible for building and maintaining a part of the system that depends on specific specialist skills and knowledge. Most team members must be specialists in a particular area of knowledge.

**Purpose:** Reduce the cognitive load of stream-aligned teams that work on systems including or using the complicated subsystem. Worthwhile even if there's only one client team.

**Examples:**
- Mathematical/algorithmic components (financial modeling, ML models)
- Specialized billing services
- Video processing codecs
- Real-time trading engines
- Cryptographic subsystems

**Responsibilities:**
- Build and maintain the subsystem with deep specialist expertise
- Provide the subsystem as a service to stream-aligned teams
- Abstract away specialist complexity so consumers don't need domain expertise

**Expected behaviors:**
1. Strong collaboration with stream-aligned teams (especially during initial development)
2. Primarily provides X-as-a-Service once the subsystem matures
3. Uses collaboration mode for short periods when exploring new capabilities
4. Focuses on reliability and clear interfaces

**Key distinction from platform teams:** Complicated-subsystem teams handle a single specific complex domain; platform teams provide a broad set of foundational services.

### 1.4 Platform Team

**Definition:** A grouping of other team types that provide a compelling internal product to accelerate delivery by stream-aligned teams. Enables stream-aligned teams to deliver work with substantial autonomy.

**Purpose:** Reduce cognitive load and extraneous effort for stream-aligned teams by providing self-service internal services (infrastructure, deployment pipelines, observability, etc.).

**Responsibilities:**
- Build and maintain internal platform services
- Treat the platform as a product with stream-aligned teams as customers
- Provide self-service capabilities with minimal friction
- Maintain reliability of platform services
- Actively seek feedback from consuming teams

**Expected behaviors:**
1. Strong collaboration with stream-aligned teams (for understanding needs)
2. Focuses on reliability and developer experience (DX) of platform services
3. Proactively reaches for stream-aligned teams' feedback
4. Uses Net Promoter Score (NPS) or similar measures for developer experience
5. Builds on top of other platform teams (fractal/Russian doll pattern)

**Key concepts:**

**Thinnest Viable Platform (TVP):** "The smallest set of APIs, documentation, and tools needed to accelerate the teams developing modern software services and systems." The platform should always remain as thin as possible — don't build more than teams need. TVP is not a one-time starting point; it's a continuous principle. As Matthew Skelton stated: "TVP is about 'thinness' to try and avoid a massive platform. TVP is something that remains throughout an organizational evolution — it should always be the thinnest viable."

**Platform-as-a-Product:** Apply the same practices used for customer-facing products to internal platforms: user research, roadmaps, versioning, usability testing. Developer experience is paramount.

**Fractal platform structure:** Inside a platform, there may be stream-aligned teams, enabling teams, and even complicated-subsystem teams — the same topology principles apply recursively.

### Team Type Conversion Patterns

| Traditional Team | Converts To |
|-----------------|-------------|
| Infrastructure team | Platform team |
| Component team | Platform or complicated-subsystem team |
| DBA team | Enabling team |
| Architecture team | Part-time enabling team |
| Tooling team | Enabling team or part of platform |
| Support team | Aligned to streams of change |

---

## 2. The Three Interaction Modes

Team Topologies defines exactly three ways teams should interact. This constraint makes collaboration explicit, plannable, and measurable. The interaction modes are not static — they should evolve as systems mature and team capabilities grow.

### 2.1 Collaboration

**Definition:** Two teams working closely together for a defined period of time to discover new things (APIs, practices, technologies, etc.).

**When to use:**
- Teams need to innovate together on a new solution
- Cross-functional expertise is required for a complex challenge
- Rapid discovery and learning is needed
- Defining a new service boundary or API
- Early-stage development of a platform feature

**Characteristics:**
- High bandwidth, high cost
- Temporary by nature — must have explicit exit criteria and timeframes
- Increases cognitive load on both teams during the collaboration period
- Both teams share responsibility for outcomes
- Requires mutual respect and high interaction frequency

**Success metrics:** Measured by what teams learn, decide, and create — not by duration of collaboration.

**Typical evolution:** Collaboration --> X-as-a-Service (once the service/API matures)

**Warning signs of dysfunction:**
- Collaboration that never ends (no exit criteria)
- One team doing all the work while the other "collaborates"
- Collaboration used as a euphemism for unclear ownership
- Too many collaboration relationships simultaneously (signal of missing platform capabilities)

### 2.2 X-as-a-Service

**Definition:** One team provides and one team consumes something "as a Service" with minimal direct interaction.

**When to use:**
- A service/capability is mature and well-understood
- Clear, well-documented interfaces exist
- One team can provide a repeatable service that many teams consume
- The provider team has established reliability and documentation

**Characteristics:**
- Low cost, clear boundaries
- Requires clear, well-documented interface (the "Team API")
- High reliability of the provided service
- Consumer teams can use the service on-demand without elaborate coordination
- One provider can serve many consumers

**Success metrics:** Service adoption rate, user (developer) satisfaction, reliability metrics, self-service completion rate.

**Provider team behaviors:**
- Focus on developer experience (DX) and documentation
- Establish FAQ and troubleshooting guides
- Use feedback loops to improve service quality
- Treat internal consumers as real customers

**Consumer team behaviors:**
- Use the service as documented
- Provide feedback through established channels
- Avoid bypassing the service interface

### 2.3 Facilitating

**Definition:** One team (typically enabling) helps and mentors another team to overcome a specific obstacle or learn a new skill.

**When to use:**
- A stream-aligned team needs to learn a new technology or practice
- A team lacks a specific capability needed for their work
- Temporary coaching is needed to bridge a knowledge gap
- A team is adopting a new tool or framework

**Characteristics:**
- Temporary and focused
- The facilitating team does not take over work — it coaches
- Goal is empowerment: the receiving team becomes self-sufficient
- Involves a coaching role, not a standards-enforcement role

**Success metrics:** How quickly the receiving team becomes self-sufficient on the topic.

**Key principle:** The facilitating team should actively work itself out of a job for each engagement.

### Interaction Mode by Team Type (Typical Patterns)

| | Stream-Aligned | Enabling | Complicated-Subsystem | Platform |
|---|---|---|---|---|
| **Stream-Aligned** | Collaboration (occasional) | Facilitation (typical) | X-as-a-Service (typical) / Collaboration (occasional) | X-as-a-Service (typical) / Collaboration (occasional) |
| **Enabling** | Facilitation (typical) | — | — | — |
| **Complicated-Subsystem** | X-as-a-Service (typical) / Collaboration (occasional) | — | — | — |
| **Platform** | X-as-a-Service (typical) / Collaboration (occasional) | — | — | X-as-a-Service / Collaboration |

### Evolutionary Dynamics

Interaction modes naturally evolve over time:

1. **Collaboration** (high cost, high learning) -- teams jointly discover and define a new service
2. **X-as-a-Service** (low cost, high efficiency) -- the service matures and stabilizes
3. **Facilitating** (temporary support) -- if consuming teams struggle with the service

This evolution is a healthy organizational heartbeat. Static interaction modes are a smell — they suggest either the service hasn't matured (stuck in collaboration) or the service is stagnating (stuck in X-as-a-Service without improvement).

---

## 3. Cognitive Load as Primary Design Constraint

Cognitive load is arguably the most important concept in Team Topologies. It serves as the primary compass for organizational design decisions.

### 3.1 Origin: John Sweller's Cognitive Load Theory

Cognitive Load Theory (CLT) was developed by educational psychologist John Sweller in the 1980s. It argues that instruction must account for the severe limitations of working memory (which can handle approximately 4-5 items simultaneously) while leveraging the vast capacity of long-term memory.

Team Topologies adapts CLT from individual learning to team performance, arguing that teams have finite cognitive capacity just as individuals do.

### 3.2 The Three Types of Cognitive Load

**Intrinsic cognitive load:**
- Related to the fundamental complexity of the problem space
- Examples: the programming language, the domain model, core algorithms
- Cannot be eliminated but can be **managed** through training, good technology choices, clear documentation, and sequencing

**Extraneous cognitive load:**
- Related to the environment in which the task is performed
- Examples: how to deploy, navigating complex CI/CD pipelines, understanding organizational processes, tool sprawl, unclear responsibilities
- Should be **eliminated** or minimized wherever possible
- This is what platform teams primarily address

**Germane cognitive load:**
- Related to aspects of the task requiring special attention for high performance
- The productive mental effort devoted to solving actual business problems
- Examples: how services should interact, business domain modeling, user experience design
- This is where teams should spend most of their mental energy
- Should be **maximized** by freeing capacity from the other two types

### 3.3 The Formula

**Total cognitive load = Intrinsic + Extraneous + Germane**

The three types are additive. Total load cannot exceed working memory capacity without degraded performance. The organizational design imperative:

> **Minimize intrinsic load. Eliminate extraneous load. Maximize room for germane load.**

### 3.4 Consequences of Cognitive Overload

When a team's cognitive load exceeds what it can cope with:
- Delivery bottleneck (delays, missed deadlines)
- Quality issues (bugs, technical debt accumulation)
- Decreased motivation and engagement
- Inability to pursue mastery
- Context-switching costs compound
- Burnout

Research finding: 74% of developers report working on operations tasks instead of product development. The average organization uses 8-12 tools just for CI/CD. Each requires its own mental model.

### 3.5 Measuring Cognitive Load

Skelton and Pais suggest a pragmatic heuristic rather than formal measurement:

> "Ask the team: Do you feel like you are effective and able to respond in a timely fashion to the work you are asked to do?"

Additional measurement approaches:
- Relative domain complexity assessment
- Count the number of distinct domains a team must understand
- Track context-switching frequency
- Monitor work-in-progress (WIP) limits

### 3.6 Domain Complexity Heuristics

1. **Simple domains** are procedural — a single team can handle 2-3 simple domains
2. **Complicated domains** require specialist knowledge — one per team
3. **Complex domains** require experimentation and discovery — one per team maximum, often needs splitting

**Assignment rule:** Each domain should be assigned to exactly one team. If a domain is too large, split the domain into subdomains first, then assign each subdomain to a team. Never split responsibility for a single domain across multiple teams.

### 3.7 Cognitive Load as Organizational Sensor

When a stream-aligned team is overloaded, it is a clear signal that one of these actions is needed:
- Part of its domain should be outsourced to a complicated-subsystem team
- A platform solution is needed to reduce extraneous load
- An enabling team should provide temporary support
- The team's scope should be narrowed

This makes cognitive load a continuous feedback mechanism for organizational design.

---

## 4. Conway's Law and the Inverse Conway Maneuver

### 4.1 Conway's Law (1968)

Melvin Conway published "How Do Committees Invent?" in Datamation magazine. The law:

> "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure."

Ruth Malan's corollary: "If the architecture of the system and the architecture of the organization are at odds, the architecture of the organization wins."

**Implications:**
1. Technical leaders must have a say in organizational design
2. Not all communication between teams is beneficial — unnecessary communication produces unnecessary coupling in the system
3. An organization arranged in functional silos (QA, DBA, security) is unlikely to produce software systems well-architected for end-to-end flow
4. When designing teams, you are implicitly designing systems

**Conway's example:** Eight people split into two teams — five for Fortran, three for COBOL. The Fortran compiler ended up with five phases; the COBOL compiler with three phases.

### 4.2 Three Responses to Conway's Law

| Response | Description |
|----------|-------------|
| **Ignore** | Proceed without considering Conway's Law. Software structures reflect communication gaps. |
| **Accept** | Acknowledge the law; design architecture to align with existing communication patterns. |
| **Inverse Conway Maneuver** | Proactively change team structures to influence and shape the desired software architecture. |

### 4.3 The Inverse Conway Maneuver

First named by Jonny Leroy and Matt Simons (ThoughtWorks) in the December 2010 issue of the Cutter IT Journal. Validated by Nicole Forsgren et al. in "Accelerate" (2018).

**Core idea:** Instead of letting organizational structure dictate system design, deliberately reorganize teams around business capabilities and desired architectural outcomes. Design the organization you want, and the architecture will follow.

> "Organizations should evolve their team and organizational structure to achieve the desired architecture. The goal is for your architecture to support the ability of teams to get their work done — from design through to deployment — without requiring high-bandwidth communication between teams." — Forsgren et al., Accelerate

**Practical application:**
1. Define the desired target architecture
2. Design team communication structures to match that architecture
3. Create small, cross-functional, long-lived teams with end-to-end ownership of specific business capabilities
4. This produces autonomous services that can evolve independently

**Important caveat:** The Inverse Conway Maneuver applies to designing software delivery teams and their communication patterns. It is not a general organizational design tool for the entire enterprise. As one critic noted: "Evolving your software delivery teams and how they communicate to achieve a desired technical architecture is not organisational design. There's much more to the enterprise than just the engine room."

### 4.4 Conway's Law + Team Topologies

Team Topologies is designed explicitly recognizing Conway's Law. The interplay:

1. Stream-aligned teams own bounded contexts -- their software architecture reflects their team boundaries
2. Platform teams provide services -- the service APIs reflect the team interaction boundaries
3. Restricting communication paths to well-defined team interactions produces modular, decoupled systems
4. If two teams that shouldn't need to communicate are communicating, it signals a missing API, service, or platform capability

---

## 5. Team-First Thinking vs Individual-First Thinking

### 5.1 The Paradigm Shift

Traditional organizational design focuses on individuals: their skills, their roles, their career paths, their performance metrics. Team Topologies inverts this:

> "The team is the most effective means of software delivery, not individuals."
> "The team is the smallest entity of delivery within an organization and should be a stable group of 5 to 9 people working towards a shared goal as a unit."

This means:
- Responsibilities are assigned to teams, not individuals
- Performance is measured at the team level, not individual level
- Training budgets are allocated to teams, letting them decide
- The team owns the software, not individual developers

### 5.2 Three Organizational Structures

Every organization has three overlapping structures:

1. **Formal structure** — the org chart (hierarchy, reporting lines)
2. **Informal structure** — the "space of influence" (who actually talks to whom, personal relationships)
3. **Value creation structure** — how work actually gets done (cross-team collaborations, real workflows)

The key to success in knowledge work lies in the interactions between the informal and value creation structures. The formal org chart is always out of sync with reality. Team Topologies focuses on optimizing the value creation structure.

### 5.3 Dunbar's Number and Trust Boundaries

Robin Dunbar's research on primate brain size and social group size established key thresholds:

| Number | Relationship Type |
|--------|------------------|
| ~5 | Close personal friendships |
| ~15 | Deep trust (Dunbar trust boundary) |
| ~50 | Mutual trust |
| ~150 | Stable social relationships (Dunbar's number) |
| ~500 | Acquaintances |

**Team size implications:**
- Individual teams: 5-9 people (within the deep trust boundary of 15)
- A team of teams: must stay within Dunbar's trust boundary of 15 for close coordination
- When a startup grows beyond 15 people, formal team structures become necessary
- When an organization exceeds 150 people, it experiences a huge jump in complexity requiring more restrictive rules

**If you favour pairing:** Select an even number between 4-8 per team. If a team exceeds 9, look for ways to split it.

### 5.4 Team Stability

- **Stable, not static:** Team membership should be relatively constant, but individuals can rotate on longer timescales
- Forming an effective team takes 2 weeks to 3 months
- Constantly reshuffling teams destroys accumulated context and trust — the hidden cost is astronomical
- "Who is on the team matters less than the team dynamics" — invest in dynamics, not just hiring

### 5.5 The Team API

Each team should define a "Team API" — a clear interface describing how other teams should interact with them. Includes:

- **Code:** Runtime endpoints, libraries, clients, UI produced by the team
- **Versioning:** How the team communicates changes to its code and services
- **Wiki and documentation:** Especially how-to guides for software owned by the team
- **Practices and principles:** The team's preferred ways of working
- **Communication:** Preferred channels, response times, availability windows
- **Work information:** What the team is working on, what's coming next, short-to-medium term priorities
- **Other:** Anything else other teams need for interaction

The Team API encourages teams to deliberately consider how they want to be viewed by and interact with people outside the team. It minimizes cognitive load on others by making access to information as clear as possible.

---

## 6. Fracture Planes for Splitting Teams

A **fracture plane** is a natural seam in a software system that allows the system to be split easily into two or more parts. When a monolith needs to be decomposed or a team's cognitive load is too high, look for these natural split points.

**Test for any split:** Does the resulting architecture support more autonomous teams with reduced cognitive load?

### 6.1 Business Domain Bounded Context (Preferred)

From Domain-Driven Design (DDD). A bounded context is a unit for partitioning a larger domain model into smaller parts, each representing an internally consistent business domain area.

- **Preferred fracture plane** — should be the default choice
- Aligns technology with business, reducing terminology mismatches and "lost in translation" issues
- Improves flow of changes and reduces rework
- Expect iteration as you understand the context better
- Requires fair amount of business knowledge and technical expertise to identify

**Example:** A music streaming service split into discovery (search, recommendations), playback (streaming, audio quality), library (user collections, playlists), and licensing (rights management, royalties).

### 6.2 Regulatory Compliance

In highly regulated industries (banking, pharmaceuticals, healthcare), regulatory requirements provide hard boundaries.

- Split subsystems that fall under different scopes of regulation
- Compliance boundaries create natural team boundaries
- Different regulatory regimes may require different change processes, audit trails, and approval workflows

### 6.3 Change Cadence

Different parts of a system need to change at different frequencies.

- With a monolith, every piece moves at the speed of the slowest part
- Splitting off parts that change at different speeds allows each to change at the pace business needs dictate
- The business drives speed of change, rather than the monolith imposing a fixed speed

**Example:** A core billing engine changes quarterly (regulatory), while the customer-facing UI changes weekly (competitive pressure).

### 6.4 Team Location

Physical and temporal separation creates natural boundaries.

- Working across different time zones aggravates communication delays and introduces bottlenecks
- Three models: full collocation, remote-first, or split team
- If teams are geographically separated, design system boundaries to match — don't force tight collaboration across time zones

### 6.5 Risk

Different subsystems have different risk profiles.

- Splitting off subsystems with clearly different risk profiles allows mapping technology changes to business appetite or regulatory constraints
- High-risk subsystems (payments, security, safety-critical) may need different testing, review, and deployment processes
- Depending on appetite for failure: some components can tolerate more experimental approaches

### 6.6 Performance Isolation

Some subsystems have fundamentally different performance requirements.

- Splitting based on performance demands ensures autonomous scaling
- Increases performance and reduces cost
- High-throughput data processing should not be coupled with low-latency user-facing services

### 6.7 Technology

Different technologies create natural boundaries.

- Particularly relevant for old or less automatable tech
- Three very disparate technologies (e.g., mobile, cloud, IoT) may warrant separate teams
- Legacy systems that cannot be easily modernized should be isolated behind clear interfaces
- Consider: can the team realistically master multiple technology stacks without cognitive overload?

### 6.8 User Personas

Different user groups with distinct needs can define team boundaries.

- Internal admin users vs. external customers
- Power users vs. casual users
- B2B vs. B2C
- Different user journeys may warrant separate stream-aligned teams

### 6.9 Organization-Specific

Some fracture planes are unique to specific organizations based on their history, culture, or business model. The eight listed above are common patterns, but not exhaustive.

---

## 7. DORA Metrics and Flow

Team Topologies is explicitly designed to optimize for "fast flow of value." The connection to DORA metrics is direct and foundational.

### 7.1 The Four DORA Metrics

From "Accelerate: The Science of Lean Software and DevOps" by Nicole Forsgren, Jez Humble, and Gene Kim (2018). Validated through six years of research across 32,000+ professionals by the DevOps Research and Assessment (DORA) team (now part of Google Cloud).

**Throughput metrics (speed):**

| Metric | Definition | Elite | High | Medium | Low |
|--------|-----------|-------|------|--------|-----|
| **Deployment Frequency** | How often the organization deploys to production | Multiple/day | Daily-weekly | Weekly-monthly | Monthly-6 months |
| **Lead Time for Changes** | Time from commit to running in production | < 1 hour | 1 day - 1 week | 1 week - 1 month | > 6 months |

**Stability metrics (reliability):**

| Metric | Definition | Elite | High | Medium | Low |
|--------|-----------|-------|------|--------|-----|
| **Change Failure Rate** | % of deployments causing production failure | 0-15% | 16-30% | 31-45% | 46-60% |
| **Mean Time to Recovery (MTTR)** | Time to restore service after failure | < 1 hour | < 1 day | 1 day - 1 week | > 6 months |

A fifth metric, **Reliability**, has been added in recent DORA research as an additional stability measure.

### 7.2 Key Finding: Speed and Stability Are Not Trade-offs

The most important finding from the Accelerate research: elite teams are better at **both** speed and stability simultaneously. Speed does not come at the expense of reliability. This directly validates Team Topologies' approach of optimizing for flow while maintaining quality.

Elite teams are **twice as likely** to meet or exceed organizational performance targets.

### 7.3 How Team Topologies Connects to DORA

| Team Topologies Practice | DORA Metric Impact |
|-------------------------|-------------------|
| Stream-aligned teams with full ownership | Increases deployment frequency, reduces lead time |
| Eliminating hand-offs between teams | Reduces lead time for changes |
| Platform teams providing self-service | Reduces lead time, enables higher deployment frequency |
| Cognitive load management | Reduces change failure rate (fewer errors from overload) |
| Clear team boundaries and APIs | Reduces MTTR (faster isolation and diagnosis) |
| Enabling teams upskilling other teams | Reduces change failure rate through capability building |
| X-as-a-Service interaction mode | Reduces lead time (no blocking dependencies) |

### 7.4 Flow and Hidden Monoliths

Team Topologies identifies several types of monoliths that impede flow:

| Monolith Type | Description |
|--------------|-------------|
| Application monolith | Single large application with many dependencies |
| Joined-at-the-database monolith | Multiple applications sharing a single database |
| Monolithic build | One gigantic CI build for everything |
| Monolithic (coupled) release | Smaller components bundled together for release |
| Monolithic model | Single domain language/representation across all contexts |
| Monolithic thinking | One-size-fits-all approach to team design |
| Monolithic workplace | Single open office layout for all teams |

Each type of monolith creates coupling that reduces flow and increases cognitive load.

---

## 8. Evolution Triggers

Team Topologies are not designed once and left static. They must evolve as the organization, technology, and business needs change. The most important thing is not the shape of the organization but the **decision rules used to adapt and change it**.

### 8.1 Trigger: Software Has Grown Too Large for One Team

**Symptoms:**
- A startup grows beyond 15 people (Dunbar's trust boundary)
- Other teams spend significant time waiting on a single team
- Changes to certain components routinely get assigned to the same people, even when busy or away
- Team members complain about lack of system documentation
- Increasing context-switching within the team

**Response:** Identify fracture planes and split into multiple stream-aligned teams. Consider creating a platform team if common infrastructure needs emerge.

### 8.2 Trigger: Delivery Cadence Is Becoming Slower

**Symptoms:**
- Lead time for changes is increasing
- Deployment frequency is decreasing
- More work-in-progress, less throughput
- Teams feel blocked waiting for other teams
- Sprint commitments are consistently missed

**Response:** Investigate bottlenecks. Look for missing platform capabilities, unclear team boundaries, or excessive collaboration where X-as-a-Service would be more efficient.

### 8.3 Trigger: Multiple Business Services Rely on a Large Set of Underlying Services

**Symptoms:**
- Multiple stream-aligned teams depend on the same infrastructure or services
- Changes to shared services create cascading delays
- No clear ownership of shared capabilities
- "Tragedy of the commons" around shared code or infrastructure

**Response:** Create or strengthen platform teams. Move shared capabilities to X-as-a-Service mode. Establish clear ownership.

### 8.4 Trigger: Teams Spending Too Much Time on Non-Domain Work

**Symptoms:**
- Developers spending more time on operations than product development
- Shadow operations: senior developers informally taking on platform responsibilities
- Tool sprawl creating excessive cognitive overhead
- Teams maintaining their own infrastructure rather than using shared services

**Response:** Create or expand platform teams. Enable self-service capabilities. Reduce extraneous cognitive load.

### 8.5 Trigger: Frequent Cross-Team Coordination Required

**Symptoms:**
- Many meetings needed to coordinate changes across teams
- Release trains or fixed release windows
- Feature development requires touching code in multiple team repositories
- Integration testing bottlenecks

**Response:** Realign team boundaries to reduce coupling. Apply the Inverse Conway Maneuver. Look for missing bounded contexts.

### 8.6 Trigger: New Technology Adoption

**Symptoms:**
- Stream-aligned teams struggling to adopt a new technology
- Inconsistent implementation of new practices across teams
- Knowledge concentrated in a few individuals

**Response:** Create an enabling team to facilitate adoption. Use facilitating interaction mode. Once teams are self-sufficient, the enabling team moves on or pivots to the next technology gap.

### 8.7 Interaction Mode Evolution Patterns

Different phases of work require different topologies:

| Phase | Topology Approach |
|-------|------------------|
| **Explore** | More collaboration, enabling teams active, higher cognitive load tolerance |
| **Exploit** | More X-as-a-Service, clear boundaries, optimize for throughput |
| **Sustain** | Stable platforms, minimal interaction, focus on reliability |
| **Withdraw** | Reduce investment, simplify, potentially merge teams |

---

## 9. Sensing and Detecting the Need for Change

### 9.1 The Sensing Organization

Team Topologies treats the organization as a sensing organism, drawing from cybernetics (specifically Norbert Wiener's 1948 work on organizational sensing mechanisms). The approach provides "a key technology-agnostic mechanism for modern software-intensive enterprises to sense when a change in strategy is required."

> "Well-defined, stable teams taking effective ownership of different parts of the software systems and interacting using well-defined communication patterns allow organizations to activate a powerful strategic capability: organizational sensing."

### 9.2 What to Sense

The organization should continuously monitor:

**Team-level signals:**
- Cognitive load indicators (team self-assessment, context-switching frequency)
- Delivery metrics (deployment frequency, lead time, failure rates)
- Team satisfaction and motivation
- Expertise concentration (bus factor)
- Work queue depth and wait times

**Inter-team signals:**
- Interaction mode mismatches (collaboration that should be X-as-a-Service)
- Unexpected communication patterns (teams communicating that shouldn't need to)
- Blocking dependencies
- Excessive coordination meetings
- Cross-team friction and complaints

**System-level signals:**
- Architecture-organization misalignment
- Growing technical debt in specific areas
- Production incidents concentrated in certain components
- Inconsistent practices across teams
- Customer feedback patterns

**External signals:**
- Technology landscape changes
- Competitive pressure
- Regulatory changes
- Market shifts

### 9.3 Using Team Interactions as Sensors

A key insight: the interaction modes themselves serve as organizational sensors. When interaction modes don't match expectations, it signals problems:

| Observed Pattern | Signal |
|-----------------|--------|
| Collaboration that never transitions to X-as-a-Service | Service isn't maturing; unclear ownership; or scope is too broad |
| X-as-a-Service that teams frequently work around | Service doesn't meet needs; poor DX; missing capabilities |
| Facilitating engagement that never ends | Deeper capability gap than expected; may need team restructuring |
| Teams not using any defined interaction mode | Unclear boundaries; missing Team API; organizational design gap |
| Unexpected ad-hoc communication between teams | Missing API, service, or platform capability |

### 9.4 Operations as High-Fidelity Sensory Input

Operations teams (IT Operations, DevOps, SRE) provide critical feedback. For this sensing to work:
- Operations must be embedded in or closely coupled to development teams, not separated
- Production incidents are signals for organizational improvement, not just technical fixes
- Monitoring data should flow back to the teams responsible for the code
- Self-management capabilities grow when teams own their operational feedback loops

### 9.5 Naomi Stanford's Five Rules for Organizational Design

Team Topologies references Naomi Stanford's principles:

1. Design when there is a compelling reason (not for its own sake)
2. Develop options for deciding on design (don't just copy what others do)
3. Choose the right time for design (timing matters)
4. Look for clues that things are out of alignment (sensing)
5. Stay alert to the future (anticipate, don't just react)

---

## 10. LLM Automation Categories

This section categorizes Team Topologies practices by their suitability for LLM automation, specifically in the context of a management automation system.

### Category A: Directly Automatable

These are monitoring, detection, and data collection tasks that LLMs can perform with minimal or no human intervention. They produce structured outputs that can feed dashboards, alerts, and reports.

| Practice | Automation Approach | Data Sources |
|----------|-------------------|--------------|
| **DORA metric tracking** | Automated collection from CI/CD pipelines, deployment tools, incident management | Git logs, CI/CD APIs, incident trackers |
| **Deployment frequency measurement** | Count deployments per team per time period | CI/CD pipeline logs |
| **Lead time calculation** | Measure commit-to-production timestamps | Git + deployment logs |
| **Change failure rate tracking** | Correlate deployments with production incidents | Deployment + incident data |
| **MTTR measurement** | Track incident open/close timestamps | Incident management system |
| **Work queue depth monitoring** | Track WIP per team, identify bottlenecks | Project management tools (Jira, Linear) |
| **Cross-team dependency tracking** | Identify blocking dependencies between teams | PR reviews, linked tickets, API call graphs |
| **Communication pattern detection** | Analyze which teams communicate and how frequently | Chat tools (Slack/Teams), meeting calendars, PR/review activity |
| **Documentation freshness tracking** | Monitor when team APIs, docs, runbooks were last updated | Wiki/docs platform timestamps |
| **Production incident concentration** | Map incidents to team-owned components | Incident + service ownership data |
| **Team composition tracking** | Monitor team size, tenure, churn against Dunbar thresholds | HR/org data |
| **Platform adoption metrics** | Track which teams use platform services and how frequently | Platform telemetry, API call logs |
| **Monolith detection** | Identify coupled releases, shared databases, monolithic builds | Build system, database schema analysis, release logs |

### Category B: LLM-Assisted (Analysis with Human Decision)

These practices benefit from LLM analysis, pattern recognition, and recommendation, but require human judgment for final decisions. The LLM prepares; the human decides and acts.

| Practice | LLM Contribution | Human Decision Required |
|----------|------------------|------------------------|
| **Cognitive load assessment** | Analyze team scope, domain count, technology diversity, operational burden. Generate cognitive load report per team. | Validate assessment with team. Decide on remediation (scope reduction, platform investment, enabling team). |
| **Fracture plane identification** | Analyze codebase for bounded contexts, change frequency patterns, risk profiles, regulatory boundaries. Recommend split points. | Choose which fracture planes to act on. Sequence the splitting. Manage people impact. |
| **Interaction mode assessment** | Compare current team interactions against TT prescriptions. Flag mismatches (e.g., collaboration that should be X-as-a-Service). | Decide whether to evolve the interaction mode. Negotiate with teams. |
| **Team type classification** | Analyze team responsibilities, outputs, and interactions. Suggest which TT type each team most resembles. Flag hybrid/unclear teams. | Confirm or correct classification. Drive transitions where needed. |
| **Evolution trigger detection** | Correlate multiple signals (slowing cadence + growing queue + incident concentration) into evolution recommendations. | Decide whether trigger warrants action. Design the specific change. |
| **Inverse Conway analysis** | Compare desired architecture with current team structure. Identify misalignments. Generate reorganization proposals. | Evaluate proposals. Consider people impact, timing, political dynamics. Execute. |
| **Platform roadmap recommendations** | Analyze which capabilities stream-aligned teams are building redundantly. Recommend platform investment areas. | Prioritize platform roadmap. Budget allocation. Build vs buy. |
| **TVP assessment** | Analyze platform usage, feature adoption, developer satisfaction data. Flag platform bloat or missing capabilities. | Decide what to add/remove from platform. Balance stability with new capabilities. |
| **Team API review** | Analyze team documentation, communication patterns, and boundary clarity. Identify gaps in team APIs. | Approve and publish Team APIs. Drive cultural change around explicit boundaries. |
| **1:1 and team health preparation** | Aggregate signals (cognitive load, delivery metrics, interaction patterns) into prep documents for manager-team conversations. | Have the actual conversations. Coach. Build trust. Make judgment calls about people. |
| **Organizational sensing report** | Generate periodic "state of the topology" reports synthesizing all signals. Highlight areas needing attention. | Interpret in context. Prioritize. Act on the most important signals. |
| **Hidden monolith detection** | Analyze build pipelines, database schemas, release processes, codebase coupling. Flag each monolith type. | Decide remediation approach and timeline. Staff the work. |
| **New technology adoption planning** | Assess technology landscape. Recommend enabling team engagements. Draft learning plans. | Decide adoption timing. Assign enabling team. Set exit criteria. |
| **Domain complexity classification** | Analyze codebase complexity, change frequency, incident rates per domain. Classify as simple/complicated/complex. | Validate with team expertise. Adjust team scope based on classification. |

### Category C: Continuous Sensing/Monitoring

These are ongoing observation patterns that surface signals over time. LLMs provide the sensing layer — watching, correlating, and alerting — while humans interpret and decide. This differs from Category A (which produces specific metrics) in that Category C involves detecting emergent patterns and anomalies that don't reduce to a single number.

| Sensing Pattern | What the LLM Watches | Signals It Surfaces |
|----------------|---------------------|-------------------|
| **Team cognitive load drift** | Expanding team scope over time. New responsibilities assigned without anything removed. Growing list of owned services. | "Team X has absorbed 3 new services in 6 months without any scope reduction. Cognitive load likely elevated." |
| **Interaction mode staleness** | Duration of current interaction modes. Whether collaboration has defined exit criteria. | "Teams A and B have been in 'collaboration' mode for 8 months with no transition to X-as-a-Service." |
| **Organizational communication anomalies** | Communication patterns that don't match defined interaction modes. Teams that should be independent are frequently coordinating. | "Teams C and D have had 12 ad-hoc coordination meetings this month despite having no defined interaction mode." |
| **Platform adoption resistance** | Teams building their own solutions for problems the platform addresses. Workarounds proliferating. | "3 stream-aligned teams have implemented custom deployment pipelines instead of using the platform service." |
| **Enabling team engagement effectiveness** | Duration of facilitating engagements. Whether receiving teams become self-sufficient. Repeat engagements on the same topic. | "Team E received enabling support on observability 6 months ago but is requesting help on the same topic again." |
| **Architecture-topology drift** | Software architecture evolving to not match team boundaries. Services that span multiple teams' domains. | "Service X is now modified by 4 different teams regularly, suggesting domain boundaries have shifted." |
| **Delivery flow degradation** | Gradual trends in DORA metrics rather than acute drops. Slowly increasing lead times, slowly decreasing deployment frequency. | "Team F's lead time has increased 40% over the past quarter. No single incident explains this — likely systemic." |
| **Team stability erosion** | Team membership changes, increasing churn, key person dependencies. | "Team G has had 60% turnover in 9 months. Team forming dynamics are being continuously reset." |
| **Cross-team friction accumulation** | Escalation frequency, cross-team complaints, blocked PR reviews, delayed cross-team requests. | "Cross-team friction between teams H and I has increased 3x. Consider whether team boundaries need realignment." |
| **Technology landscape shifts** | External technology changes that affect current team capabilities. New tools/frameworks gaining traction that could reduce cognitive load. | "3 stream-aligned teams still maintain custom ML pipelines. Managed ML platforms have matured significantly — enabling team engagement opportunity." |
| **Conway's Law violations** | Team structure drifting away from architecture. Reorgs that don't consider software impact. | "Recent reorg moved developer X from Team J to Team K, but X still owns critical Service Y in Team J's domain." |
| **Flow bottleneck formation** | Queuing patterns. Work items waiting on specific teams or individuals. Increasing cycle time for specific work types. | "All API changes now queue behind Team L's review process. Average wait: 4.3 days. This is a newly formed bottleneck." |

### Integration Model: The Three Categories Working Together

The three categories form a complete management intelligence loop:

```
Category A (Automated Metrics)
    |
    v
Category C (Continuous Sensing) -- detects patterns in Category A data
    |
    v
Category B (LLM-Assisted Analysis) -- synthesizes signals into recommendations
    |
    v
Human Decision & Action
    |
    v
Category A (Automated Metrics) -- measures impact of changes
```

**Example flow:**
1. **Category A** detects: Team X's deployment frequency dropped from daily to weekly
2. **Category C** correlates: Team X absorbed a new service 3 months ago. Their cognitive load survey scores declined. They've had 5 cross-team coordination meetings this month.
3. **Category B** synthesizes: "Team X shows signs of cognitive overload after absorbing Service Y. Recommend: (a) move Service Y to a separate team or (b) engage platform team to absorb operational burden of Service Y."
4. **Human** decides: Engages platform team to provide managed infrastructure for Service Y, reducing Team X's extraneous cognitive load.
5. **Category A** measures: 6 weeks later, Team X's deployment frequency recovers to daily.

---

## Key Sources

- Skelton, M. & Pais, M. (2019). *Team Topologies: Organizing Business and Technology Teams for Fast Flow.* IT Revolution Press.
- Skelton, M. & Pais, M. (2025). *Team Topologies, 2nd Edition.* IT Revolution Press.
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps.* IT Revolution Press.
- Conway, M.E. (1968). "How Do Committees Invent?" *Datamation.*
- Sweller, J. (2011). "Cognitive Load Theory." In *Psychology of Learning and Motivation.*
- Dunbar, R.I.M. (1992). "Neocortex size as a constraint on group size in primates." *Journal of Human Evolution.*
- Fowler, M. (2024). "Team Topologies." *martinfowler.com.*
- teamtopologies.com/key-concepts — Official key concepts page.
- IT Revolution — Team Topologies excerpts, articles, and case studies.
