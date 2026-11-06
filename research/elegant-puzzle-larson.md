# An Elegant Puzzle: Systems of Engineering Management
## Will Larson -- Deep Framework Extraction

Research date: 2026-03-03
Sources: lethain.com (Larson's blog), First Round Review interviews, Pragmatic Engineer review, multiple detailed book summaries and chapter notes.

---

## 1. Core Systems Thinking Models

Larson's central thesis: engineering management IS systems engineering. Every management challenge can be modeled as a system with inputs, outputs, stocks, and flows. The book explicitly draws from Donella Meadows' "Thinking in Systems."

### The Fundamental Insight

> "Once you start thinking about systems, you'll find it's hard to stop. Pretty much any difficult problem is worth trying to represent as a system, and even without numbers plugged in I find them powerful thinking aids."

### Key Systems Larson Models

1. **Team performance as a system**: Teams exist on a continuum of states. Inputs (people, time, slack) cause state transitions. Entropy constantly drags teams backward.
2. **Hiring as a system**: Each new hire consumes ~10 hours/week from a trained engineer. An untrained engineer produces ~1/3 the output of a trained one. Therefore 2 untrained + 1 trainer yields only 1.16x trained-equivalent output. Rapid hiring SLOWS teams before it helps them.
3. **Technical debt as a system**: Debt accumulates faster than it's paid down. Individual refactors don't scale. Only migrations (systematic, organization-wide changes) create leverage.
4. **Organizational design as a system**: `teams = size / 8; groups = teams / 5; orgs = groups / 5`. Simple arithmetic produces the structure.
5. **Metrics as a feedback loop**: Goals decouple the "what" from the "how." Metrics create self-managing systems by nudging teams toward action. Benchmarking across teams is the most general self-managing tool.

### Systems Thinking Anti-Patterns

- Reaching for tactical support before initiating the correct system fix (exhausts the manager with no promise of salvation)
- Optimizing locally instead of globally
- Treating symptoms rather than stocks and flows
- "Working harder" as a solution (breeds hero programmers whose heroic ways make it difficult for non-heroes to contribute)

---

## 2. Team Health: The Four States Framework

This is Larson's most cited and most actionable framework. Teams exist on a continuum of four states, and each state requires a specific, different system fix.

### The Four States

| State | Signals | Morale | User Happiness | System Fix |
|-------|---------|--------|----------------|------------|
| **Falling Behind** | Backlog grows each week. People work hard but can't make progress. | Low | Low | **Add people** |
| **Treading Water** | Critical work gets done but no debt paydown or major projects. | Variable | Low-Medium | **Reduce WIP** |
| **Repaying Debt** | Each debt repaid creates time to repay more. Snowball effect. | Increasing | Medium (may dip temporarily) | **Add time** |
| **Innovating** | Tech debt sustainably low. Majority of work is new user value. | High | High | **Add slack** |

### State Transitions -- Tactical Details

**Falling Behind -> Treading Water (add people):**
- Hiring and onboarding are disruptive. Focus on one team at a time.
- Set expectations with users that output will temporarily decrease.
- Avoid pulling resources from other internal teams -- it inevitably becomes political.
- The productivity math is harsh: doubling a team every 6 months means ~10 interviews per existing engineer per period, at ~2 hours each.

**Treading Water -> Repaying Debt (reduce WIP):**
- Consolidate team efforts to finish more things.
- Limit work in progress until the team can begin addressing tech debt.
- Help people shift from a personal view of productivity to a team view.
- This is the hardest psychological shift -- individuals want to feel productive, but the system needs fewer concurrent efforts.

**Repaying Debt -> Innovating (add time):**
- Everything is already working. Just find space for compounding value.
- Find ways to support users while also repaying debt (avoid disappearing into pure tech debt mode).
- Your stakeholders will be antsy -- your job is to prevent their impatience from causing backslide.
- This is where you most need organizational patience.

**Innovating -> Sustained Innovation (add slack):**
- Maintain enough slack in schedules for quality work.
- Ensure the team's work is valued by the organization -- "the quickest path out of innovation is to be viewed as a team that builds science projects, which inevitably leads to defunding."
- This is the only stable state, but entropy always threatens.

### Critical Properties

- **Fixes are slow.** Systems accumulate months or years of state that must be drained. Conversely, this durability means fixes that work are extremely lasting.
- **Morale and user happiness don't move in tandem.** When you start technical work, the team gets motivated but users may get upset because you're doing even less visible work for them.
- **You cannot skip states.** Adding people to a team that's treading water won't help -- you'll just have more people treading water.

### Proxy Metrics for State Assessment

- Time to root cause for incidents (getting shorter = draining latent incidents = moving toward innovation)
- Backlog growth rate week-over-week (growing = falling behind)
- Ratio of new feature work to maintenance work
- Team throughput measured via lightweight task sizing

---

## 3. Managing Technical Quality

### The Quality Escalation Ladder

Larson presents an escalating series of interventions for managing technical quality, ordered from least to most organizational overhead:

1. **Hot spots**: Find the specific files where 98% of problems occur. Fix those first. "The unreasonable effectiveness of prioritizing hot spots."
2. **Best practices**: Codify what works. Use "model, document, share" rather than top-down mandates.
3. **Leverage points**: Apply Software Design X-Rays techniques to find specific high-impact files. Optimize test runtimes. Move Docker compile steps to RAM disk.
4. **Technical vectors**: Establish architectural guidelines that align work across teams.
5. **Measures of technical quality**: Define and track quality metrics (test coverage, build times, deployment frequency).
6. **Technical quality team**: A dedicated team (Developer Productivity, Developer Tools, Product Infrastructure) with a broader remit than QA -- from workflow to build to test to interface design.
7. **Quality programs**: Organization-wide programs that are essentially "endless migrations." Require a sponsor, golden examples, auto-generated conversion commits.

### Migrations: "The Only Scalable Fix to Tech Debt"

This is one of Larson's strongest opinions. Individual refactoring does not scale. Only systematic migrations work at organizational scale.

**The Migration Playbook: De-risk, Enable, Finish**

**Phase 1 -- De-risk:**
- Write a design document.
- Shop it with teams that will have the hardest time migrating. Iterate.
- Shop it with teams that have atypical patterns and edge cases. Iterate.
- Test it against the next 6-12 months of roadmap. Iterate.
- Goal: validate as quickly and cheaply as possible.

**Phase 2 -- Enable:**
- Build tooling to programmatically migrate the easy 90%.
- This radically reduces migration cost to the broader organization.
- Provide "golden examples" of the target state.
- Provide test scripts to verify migration success.
- Auto-generate conversion commits when possible.
- Do as much as possible to avoid every team having to deeply understand the problem space.

**Phase 3 -- Finish:**
- Generate tracking tickets.
- Push migration status to teams and management (managers are the people who need to prioritize).
- The long tail: finish it yourself. The migration-leading team must dig into nooks and crannies.
- Reserve the majority of celebration and recognition for successful COMPLETION, not initiation.
- Starting but not finishing migrations incurs significant additional technical debt.

**Migration Anti-Patterns:**
- Starting too many concurrent migrations
- Celebrating starts rather than completions (creates perverse incentives)
- Under-investing in tooling (making every team do manual migration work)
- Not having management buy-in (teams won't prioritize without leadership pressure)

### Design Reviews and Consistency

- As organizations grow, there is a subtle slide into inconsistency.
- Centralized decision-making groups help, but must be designed carefully (see Section 7).
- Strategy documents should be grounded in diagnosis (from Rumelt's Good Strategy/Bad Strategy): diagnosis, policies, and actions.

---

## 4. Career Growth and Development

### Career Narratives (Not Career Ladders)

Larson reframes career development around narratives rather than ladders:

**Career Progression Framework:**
1. Identify your 3-5 year goal.
2. Identify gaps in your skills to achieve that goal.
3. Pick a few gaps to focus on for the next 3-6 months.
4. Agree on an action plan with your manager.

> "Chasing the next promotion is at best a marker on a mass-produced treasure map, with every shovel and metal detector re-covering the same patch. Don't go there. Go somewhere that's disproportionately valuable to you because of who you are and what you want."

### Career Ladders

- Foundation of an effective performance management system.
- A good ladder allows folks to accurately self-assess, is self-contained and short.
- A bad ladder is ambiguous and requires deep knowledge of precedent.
- Significant overhead to each ladder you write and maintain.
- Significant downside to grouping different roles onto a shared ladder.
- Crisp level boundaries define role models; role model behaviors propagate 1-2 years later.
- **If you only invest in one component of performance management, make it the ladders.**

### Performance Management System Design

**Three-layer system:**

1. **Career ladders** -- expected behaviors and responsibilities per level.
2. **Performance designations** -- two-axis grid: performance (current impact) and trajectory (growth trend). Creates 9 cells.
3. **Performance cycles** -- periodic calculation of designations in a consistent, fair fashion. Typically Q2 and Q4 (not every quarter -- too much overhead).

### Evaluating Director Candidates (Internal)

Six dimensions:
1. **Partnership**: effective partners to peers and managed teams?
2. **Execution**: support team on operational excellence?
3. **Vision**: compelling, energizing vision for team and scope?
4. **Strategy**: identify steps to transform present into vision?
5. **Spoken and written communication**: convey complex topics engagingly, tuned to audience?
6. **Stakeholder management**: make executives and key stakeholders feel heard?

### Community and Opportunity

Two core dimensions of organizational health for people:
- **Community**: Do people feel involved, comfortable, safe? What is their anxiety level day-to-day?
- **Opportunity**: Who gets important projects? Who gets promoted? Who are the senior staff engineers? These are outcome metrics that are not debatable -- they are the actual state of play.

---

## 5. Organizational Design

### Team Sizing Rules

**Hard numbers:**
- Teams of **6-8 engineers** in steady state.
- Managers of managers support **4-6 managers**.
- **Never** create teams smaller than 4 -- "a leaky abstraction that functions indiscernibly from individuals." Larson regrets every time he sponsored sub-4 teams.
- It takes **8 engineers** to support a 2-tier on-call rotation.
- Most teams work best at ~8 engineers. Beyond that, spin off a new team.
- Grow a team to ~10, then split it.
- Never create empty teams.
- Keep innovation and maintenance together in the same team (don't create a two-tiered class system).

**Manager spans:**
- Hands-on TLMs: no more than 4 direct reports.
- Non-coding managers: 5-8 engineers depending on experience.
- Directors (mid-level management): 4-6 managers, ~20 dotted reports in a 100-person org.
- VP/CTO: ~40 dotted reports in a 100-person org.

**Hiring math:**
- An untrained engineer is 1/3 as productive as a trained one.
- Training consumes ~10 hours/week from each trained engineer.
- Each interview takes ~2 hours (prep, conduct, debrief).
- If an engineer is taking >3 interviews/week, give them a month off every 3-4 months.
- Cold sourcing: 1 hour/week per engineering manager on LinkedIn.

### The Sizing Playbook

```
teams = size / 8
groups = teams / 5
orgs = groups / 5
```

For 60 engineers: 1 org, 2 groups (e.g., product + infrastructure), 4 teams per group.

### Organizational Change (Reorgs)

**Planning algorithm:**
1. Validate that organizational change is the right tool.
2. Project headcount a year out (avoids yearly reorgs).
3. Set target ratio of management to individual contributors.
4. Identify logical teams and groups of teams.
5. Plan staffing for the teams and groups.
6. Commit to moving forward.
7. Roll out the change.

**Rollout tactics:**
1. Discuss with heavily impacted individuals in private first.
2. Ensure managers and key individuals can explain the reasoning.
3. Send a documenting email.
4. Be available for discussion.
5. Hold org all-hands only if necessary (people process poorly in large groups).
6. Double down on skip-level 1:1s.

**Rules of thumb:**
- Company needs before individual wants (fitting to individual asks causes frequent reorgs, accumulates organizational debt, creates appearance of politics).
- Gelled teams are magic -- focus growth to allow some teams to gel even during rapid hiring.
- Balance internal and external managers (all internal = reinvent every best practice from scratch).
- Put teams that work together (especially poorly) as close together as possible to minimize escalation distance.
- Most poor working relationships are the by-product of information gaps.

---

## 6. Managing Up and Stakeholder Management

### Presenting to Senior Leadership

Larson's template for executive presentations:

1. **Start with the conclusion** -- especially in written communication, to prevent skim reading and incorrect assumptions.
2. **Frame why the topic matters** -- tie it to business value. Obvious to you, less so to others.
3. **Everyone loves a narrative** -- create a narrative of where things are, how you got there, and where you're going.
4. **Prepare for detours** -- be prepared to lead the presentation yourself while also being ready for unexpected questions from senior leadership.
5. **Make a clear ask** -- go into the meeting with a clear goal. Start the meeting by framing that goal.

**Additional tactics:**
- **Answer directly**: senior leaders are keenly aware of evasive answers. Instead of hiding problems, explain your plans to address them.
- **Deep dive into the data**: know your data well enough to answer unexpected questions with it.
- **Discuss the details**: some executives test presenters by diving into details, trying to find an area of discomfort. Be familiar with the details but also able to reframe using data or principles.
- **Derive actions from principles**: provide a mental model of how you view a topic, allowing others to understand how you make decisions.
- **Communication is company specific**: watch how others present to leadership and study their approach.

### How Managers Get Stuck

**New managers:**
- Only manage down
- Only manage up
- Never manage up
- Optimize locally
- Assume hiring never solves a problem
- Don't spend time building relationships
- Define their role too narrowly
- Forget that their manager is a human being

**Experienced managers:**
- Do what worked in their previous companies
- Spend too much time building relationships
- Assume more hiring can solve every problem
- Abscond rather than delegate
- Become disconnected from ground truth

### Saying No Effectively

> "When folks want you to commit to more work than you believe you can deliver, your goal is to provide a compelling explanation of how your team finishes work. FINISHES is particularly important, as opposed to DOES, because partial work has no value."

---

## 7. Process and Rituals

### Model, Document, Share

Larson's approach to introducing process change without authority:

**Step 1 -- Model:**
- Start measuring your team's health (short monthly surveys) and throughput (lightweight task sizing).
- Establish baselines before your change.
- Run the new process as a short experiment. Don't publicize it.
- Have courage to keep going for a while, and courage to stop if it doesn't work after a month or two.
- Use health and throughput metrics to ground your decision.

**Step 2 -- Document:**
- Document the problem you set out to solve.
- Document the learning process you went through.
- Document the details of how another team would adopt the practice.
- Be as detailed as possible. Create a canonical document.
- Get folks on other teams to check readability.

**Step 3 -- Share:**
- Share your documented approach along with your experience, in a short email.
- **Don't ask everyone to adopt the practice. Don't lobby for change.**
- Just present the approach and your experience following it.

**When to use Model/Document/Share vs. Top-Down Mandates:**
- **Top-down mandates** when: teams have bandwidth, organization has coordination resources, consistency matters, speed matters, centralized decision-making is needed.
- **Model/Document/Share** when: you have time to iterate, you want the best possible approach, you want buy-in rather than compliance, you lack authority.

### Sprint Health Criteria

Sprints are running well if:
1. Team knows what they should be working on.
2. Team knows why their work is valuable.
3. Team can determine if their work is complete.
4. Team knows how to figure out what to work on next.
5. Stakeholders can learn what the team is working on.
6. Stakeholders can learn what the team plans to work on next.
7. Stakeholders know how to influence the team's plans.

### Team Snippets (Sprint Snapshots)

Each sprint should produce a snapshot containing:
1. What the team is doing.
2. Why they are doing it.
3. What they are planning to do next.

### Centralized Decision-Making Groups

When designing groups for cross-cutting concerns (architecture review, design review, etc.):

| Dimension | Design Choice |
|-----------|--------------|
| Influence | Advisory <-> Authoritarian |
| Interface | Ticket, email, weekly review sessions |
| Size | ~6 people (10+ makes constructive discussion difficult) |
| Time commitment | Top priority or side responsibility? |
| Identity | High commitment required if you want identity to shift to this group |
| Selection process | Transparent requirements + self-nomination |
| Length of term | Permanent or rotating? |
| Representativeness | How representative of the wider org? |

**Failure modes:**
- **Domineering** -- making decisions without sufficient input
- **Bottlenecked** -- too slow to respond, blocks everyone
- **Status-oriented** -- membership becomes a prestige marker rather than work
- **Inert** -- group stops being active or relevant

### Communities of Learning

- Brief presentations, long discussions (1:2 ratio).
- Discuss in groups of 4-5, then regroup and share.
- Be a facilitator, not a lecturer.
- Bias for topics core to daily work.
- Provide pre-read material.
- Include whitepapers in reading rotations (not just books/blog posts).

### Time Management

- **Quarterly time retro**: look back at how you invested your time, shuffle allocation for the incoming quarter.
- **Prioritize long-term success over short-term quality.**
- **Finish small, leveraged things**: each completion should create more bandwidth.
- **Stop doing things with structure**: identify critical work you don't do, recategorize as organizational risk.
- **Delegation**: design a path for someone else to take on the work, even if it takes a year.
- **Size backward, not forward**: allocate X hours to skip-levels and meet as many people as possible, rather than trying to meet everybody.
- **Trust the system you build**: at some point, hand off responsibilities to handle exceptions.

---

## 8. Metrics and Measurement

### Goal Structure

Good goals are a composition of four numbers:

| Component | Definition | Example |
|-----------|-----------|---------|
| **Target** | Where you want to reach | 300ms (p95) |
| **Baseline** | Where you are today | 600ms (p95) |
| **Trend** | Current velocity | Increased from 500ms to 600ms in Q2 |
| **Time frame** | Bounds for the change | End of Q3 |

**Well-structured goal example:** "In Q3, we will reduce time to render our frontpage from 600ms (p95) to 300ms (p95). In Q2, render time increased from 500ms to 600ms."

### Investment Goals and Baselines

- **Investments** describe a future state you want to reach.
- **Baselines** describe aspects of the present you want to preserve.
- **Always pair investment goals with baseline (countervailing) metrics.**

Example: Goal is to speed up data pipeline. Investment: "Core batch jobs finish within 3 hours (p95) by end of Q3." Without baselines, you could just double cluster size. Baselines: "Efficiency should not exceed 0.05 USD/GB" and "Alert load should not increase beyond twice/week."

### Developer Velocity (from Accelerate/DORA)

Four measures Larson recommends tracking:
1. Deployment frequency
2. Lead time for changes
3. Mean time to recovery (MTTR)
4. Change failure rate

### Metrics Anti-Patterns

From Larson's First Round Review interview:

- **Holding out for the perfect metric while measuring nothing.** "You can be ideologically pure and say we shouldn't measure something, but all that does is slow down the learning of the organization around you."
- **Using optimization metrics to judge performance.** If a team generates fewer PRs than others, that might not mean they're less productive.
- **Measuring individuals rather than teams.** Software is a team activity. Individual metrics are diagnostic, not performance tools.
- **Measuring flawed things is still better than measuring nothing.** Start imperfect, iterate toward better metrics.

### What Every Team Needs

- A clear set of directional metrics.
- An easily discoverable dashboard.

### Controls

Controls are mechanisms to align with other leaders. They range from defining metrics (good) to sprint planning (not recommended). The right level of control depends on context, but the key insight is to identify WHERE to engage and where to hang back.

---

## 9. Automatable and LLM-Assistable Practices

Based on the frameworks above, here are the specific practices from Larson's system that are candidates for automation or LLM augmentation:

### High Automation Potential

| Practice | Larson's Description | Automation Approach |
|----------|---------------------|-------------------|
| **Team state assessment** | Classify teams as falling behind/treading water/repaying debt/innovating based on signals | Monitor backlog growth rate, WIP counts, ratio of feature vs maintenance work, incident MTTR trends. Auto-classify team state. |
| **Migration tracking** | Generate tracking tickets, push status to teams and management | Track migration completion percentage across teams, auto-generate status reports, flag stalled migrations. |
| **Sprint health check** | 7 criteria for healthy sprints (see Section 7) | Survey or automated check against the 7 criteria. Score each sprint. |
| **Team snippet generation** | What/why/what-next per sprint | Auto-generate from ticket system data. LLM summarizes into narrative. |
| **Goal structure validation** | 4-number goals (target, baseline, trend, timeframe) | Parse goal statements, flag missing components, validate countervailing metrics exist. |
| **Hiring math** | Impact modeling of new hires on team productivity | Calculate training load, interview burden, net productivity impact based on team size and hire rate. |
| **Org sizing arithmetic** | teams = size/8, groups = teams/5 | Given current headcount + projected growth, auto-recommend team splits and group structure. |
| **Dashboard existence check** | Every team needs directional metrics + discoverable dashboard | Verify dashboard existence per team, flag teams without one. |

### Medium Automation Potential (LLM-Assisted)

| Practice | Larson's Description | LLM Approach |
|----------|---------------------|-------------|
| **Career narrative coaching** | 3-5 year goal, gap analysis, 3-6 month focus areas | LLM can help structure the narrative, identify gaps against a career ladder, suggest focus areas. |
| **Reorg planning** | 7-step planning algorithm | LLM can model headcount projections, suggest team groupings, identify at-risk individuals. |
| **Design document review** | De-risk phase of migrations requires iterating on design docs | LLM can review design docs against migration playbook, flag missing edge cases. |
| **Executive presentation prep** | Start with conclusion, frame business value, prepare for detours | LLM can restructure a draft presentation into Larson's template, generate anticipated questions. |
| **Strategy document generation** | Rumelt framework: diagnosis, policies, actions | LLM can draft strategy documents from inputs, ensure all three sections are present and grounded. |
| **Vision document structure** | Vision statement, value prop, capabilities, constraints, narrative | LLM can validate vision doc completeness, flag missing sections. |
| **Meeting prep** | Know data, prepare for detail-dives, frame clear asks | LLM generates briefing documents, anticipates questions, prepares data summaries. |
| **Communities of learning facilitation** | Pre-read material, discussion questions, group synthesis | LLM can suggest discussion questions, summarize pre-reads, synthesize group outputs. |

### Low Automation / Human-Essential

| Practice | Why Human-Essential |
|----------|-------------------|
| **State transition decisions** | Requires judgment about team morale, organizational patience, stakeholder management |
| **Skip-level 1:1s** | Relationship and trust building |
| **Reorg communication** | Empathy, reading the room, private conversations |
| **"Finish it yourself" (migration long tail)** | Deep technical knowledge of edge cases |
| **Maintaining slack** | Political skill to prevent defunding of innovation |
| **Saying no** | Requires organizational authority and relationship capital |

### Specific Integration Points for Your System

Given your existing management_prep agent, cockpit nudges, and profiler infrastructure:

1. **Team state classifier**: Add to `cockpit/data/` as a collector. Input: JIRA/ticket data (backlog growth, WIP, feature vs maintenance ratio). Output: team state classification per Larson's four states + recommended system fix.

2. **Migration tracker**: Could be a nudge source. Track active migrations, flag stalled ones (no progress in 2 weeks), surface migration completion percentage.

3. **Goal validator**: Parse goals from vault notes or OKR documents. Flag goals missing any of the 4 components. Flag investment goals without countervailing baselines.

4. **Quarterly time retro**: Aggregate calendar data + activity logs. LLM generates time allocation analysis and recommendations for next quarter.

5. **1:1 prep enrichment**: Your existing management_prep agent could incorporate Larson's career narrative framework -- check if direct reports have documented 3-5 year goals, gap analysis, current focus areas.

6. **Sprint health scoring**: Automated scoring against Larson's 7 criteria. Could feed into team health nudges.

---

## Appendix: Book Structure

The book is organized into five sections, each a collection of essays:

1. **Organizations** -- team sizing, four states, org design, hiring
2. **Tools** -- systems thinking, product management, visions/strategies, metrics, migrations, reorgs, controls, career narratives, presenting to leadership
3. **Approaches** -- model/document/share, decision-making groups, time management, communities of learning
4. **Culture** -- opportunity, community, inclusion, kill your heroes, policies
5. **Careers** -- career ladders, performance management, hiring process

## Key References Larson Draws From

- **Thinking in Systems** by Donella Meadows (systems thinking foundation)
- **Good Strategy/Bad Strategy** by Richard Rumelt (strategy framework: diagnosis, policies, actions)
- **Accelerate** by Forsgren/Humble/Kim (DORA metrics)
- **The Goal** by Goldratt (theory of constraints, bottleneck identification)
- **Software Design X-Rays** by Adam Tornhill (behavioral code analysis for hot spots)
- **Work Rules** by Laszlo Bock (performance management systems)
- **The Five Dysfunctions of a Team** by Lencioni (team health)
