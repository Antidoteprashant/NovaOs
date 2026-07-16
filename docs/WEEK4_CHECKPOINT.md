# Week 4 Checkpoint \u2014 Scope Decision Tree

Run this check every week from Week 2 onward, not just Week 4. First-time
live-build teams commonly lose Week 1\u20132 to environment setup, so catching
a slip early matters more than the Week 4 date itself.

## Checkpoint question

**Does a clean, bootable, merged ISO exist right now?**

### If YES
Proceed as planned. Person 3 can attempt the RAG stretch goal in Week 5,
Person 2 can polish branding, Person 1 runs full RAM-tier testing.

### If NO \u2014 build is unstable or dependency conflicts unresolved
- Drop RAG immediately (already marked stretch goal in the PRD).
- Freeze the package list \u2014 no new packages until the build is clean.
- Redirect Person 3's Week 5 to helping Person 1 stabilize the build
  instead of curriculum/docs polish.

### If STILL not booting reliably by mid-Week 5
- Drop the 4GB+ AI tier entirely \u2014 ship 2GB tier (TinyLlama) only.
- Drop the Student Toolkit app (already Nice-to-have).
- Focus 100% of remaining time on the non-negotiable demo floor below.

## Non-negotiable demo floor

No matter how much scope gets cut, the following must work for demo day:

- [ ] ISO boots and installs on a 2GB RAM VM
- [ ] Curriculum tools launch without extra setup
- [ ] `novaai` responds to a basic offline query via TinyLlama

Everything else in the MVP scope table (see [`PRD_TRD.md`](PRD_TRD.md)) is
negotiable if time runs out. These three are not.
