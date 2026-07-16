# NovaOS

Lightweight, curriculum-aware Debian-based Linux distribution for B.Tech CS/IT students.

3-person team, beginner-level with Linux/Debian internals, 5\u20136 week timeline.
Full project docs (PRD/TRD, task division, AI prompt pack) live in [`docs/`](docs/).

## Quick links

| Doc | What it's for |
|---|---|
| [`docs/PRD_TRD.md`](docs/PRD_TRD.md) | Full product + technical requirements, MVP scope |
| [`docs/TASK_DIVISION.md`](docs/TASK_DIVISION.md) | Who owns what, week by week, with commands |
| [`docs/AI_PROMPTS.md`](docs/AI_PROMPTS.md) | Ready-to-paste Claude/Claude Code prompts per task |
| [`docs/WEEK4_CHECKPOINT.md`](docs/WEEK4_CHECKPOINT.md) | Scope-cut decision tree if we're behind |

## Team & ownership

| Person | Owns | Primary folder(s) |
|---|---|---|
| Person 1 | Base build, package lists, ISO builds, RAM testing | `config/package-lists/`, `config/` root, `scripts/build.sh` |
| Person 2 | Desktop, branding, Calamares installer | `config/includes.chroot/`, `config/hooks/live/*calamares*` |
| Person 3 | AI assistant, curriculum tools | `config/hooks/live/*ollama*`, `scripts/novaai` |

Everyone can clone this same repo and work from home \u2014 you don't need
each other's machines. You only need a Debian/Ubuntu machine (or VM) to
actually *build* the ISO; branding/AI work can be developed and tested
independently before it's merged into the build tree.

## Getting started (all 3 people, do this first)

```bash
# 1. Clone the repo
git clone <your-repo-url> novaos
cd novaos

# 2. Create your own branch \u2014 don't work directly on main
git checkout -b person1-build      # Person 1
git checkout -b person2-desktop    # Person 2
git checkout -b person3-ai         # Person 3

# 3. Push your branch so others can see your work
git push -u origin <your-branch-name>
```

## Branch strategy

- `main` \u2014 always kept buildable. Only merge into `main` at the weekly sync, after testing.
- `person1-build`, `person2-desktop`, `person3-ai` \u2014 each person's working branch.
- Merge order at weekly sync: Person 1's branch merges first (it's the foundation), then Person 2, then Person 3, resolving conflicts as they come up together on a call.
- **Never force-push to `main`.** If you mess up your own branch, force-push your own branch only.

## Weekly sync checklist

Run through [`docs/WEEK4_CHECKPOINT.md`](docs/WEEK4_CHECKPOINT.md) logic every week, not just Week 4:

1. Each person pulls latest `main`, merges into their own branch, resolves conflicts locally.
2. Each person runs a build test (Person 1 does the actual `lb build`; Person 2/3 verify their files apply without errors).
3. If build is clean, merge to `main`.
4. If build is broken, do **not** merge to `main` \u2014 fix on the branch first.

## Local environment note

Only Person 1 strictly needs a full live-build environment running at all
times. Person 2 can develop LXQt/Calamares config on any Debian-based VM.
Person 3 can develop and test Ollama/model work on literally any machine
with enough RAM \u2014 none of this requires live-build until it's time to
bake it into `config/`.

See [`docs/TASK_DIVISION.md`](docs/TASK_DIVISION.md) for exact commands per person per week.
