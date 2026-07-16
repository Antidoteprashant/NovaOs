# NovaOS \u2014 AI Prompt Pack

Paste these into Claude / Claude Code. Replace anything in `[brackets]` first.
If using Claude Code inside this repo, you can say "look at `config/` in this
folder" instead of pasting file contents.

## Person 1

<details>
<summary>Week 1 \u2014 live-build environment setup</summary>

```
I'm a Linux/Debian beginner setting up live-build for the first time on
a Debian/Ubuntu machine to create a custom Debian-based distro called
NovaOS. Walk me through, step by step, installing live-build and
creating a minimal 'lb config' for Debian bookworm, amd64, with
no debian-installer (we'll add Calamares separately later).

After each command, briefly explain what it does in plain terms
(I don't have prior live-build experience). Then give me the exact
'lb build' command to produce a first plain ISO with zero
customization \u2014 my only goal this week is to see ANY iso boot in
QEMU. Also give me the QEMU command to test-boot the resulting ISO
with 2048MB RAM.

If the build fails, ask me to paste the last 30 lines of the build
log before suggesting a fix \u2014 don't guess blind.
```
</details>

<details>
<summary>Week 2 \u2014 Package lists + dependency errors</summary>

```
I have a working live-build tree at [path] that produces a plain
bootable Debian bookworm ISO. Now I need to add package lists for:
- Desktop environment: lxqt, sddm
- Dev tools: python3, python3-pip, default-jdk, git, gcc, g++, make

Show me the correct file(s) to create under config/package-lists/
and the correct filename suffix convention live-build expects.
Then walk me through rebuilding with 'lb clean' + 'lb build'.

I'm going to run into dependency conflicts I don't understand yet.
When I paste you an error from the build log, diagnose it from the
actual error text only (don't assume) and give me the minimal fix
\u2014 don't rewrite my whole config tree unless the error requires it.
```
</details>

<details>
<summary>Weeks 3\u20134 \u2014 Merging teammates' layers</summary>

```
I'm merging desktop/branding files from a teammate (Calamares
installer config + LXQt branding + Plymouth boot splash) and AI
tooling from another teammate (an Ollama install hook under
config/hooks/live/) into my live-build tree.

Here is my current config/ directory structure: [paste 'find config
-maxdepth 3' output]. Here is the error I get after merging
[paste build log tail]. Diagnose whether this is a file-conflict,
a hook ordering issue, or a missing dependency, and tell me exactly
which file to change. Also tell me if my hook script needs a
specific numeric prefix to run in the right order relative to
other hooks.
```
</details>

<details>
<summary>Weeks 5\u20136 \u2014 RAM-tier testing + reporting</summary>

```
I need to benchmark a Debian-based live ISO called NovaOS across
1GB, 2GB, and 4GB RAM allocations in QEMU. Give me the QEMU
commands for each tier, and a simple way to capture idle RAM usage
(via 'free -h') plus boot time semi-automatically, so I can log
results in a table without doing it all by hand each time.

Also help me write a short markdown report template summarizing:
ISO size, boot success per tier, idle RAM per tier, and any
failures \u2014 something I can drop straight into our project doc
as evidence for the success metrics.
```
</details>

## Person 2

<details>
<summary>Week 1 \u2014 Learning LXQt config</summary>

```
I'm new to Linux desktop customization. I've installed LXQt on a
VM and want to understand, at a beginner level, where its config
lives (panel layout, menu structure, keybindings) so I can later
apply the same customization inside a custom Debian live-build
image (not just my live session).

Explain the difference between per-user config (~/.config/lxqt/)
and system-wide defaults (/etc/xdg/lxqt/), since for NovaOS I need
changes to apply to every new user by default, not just my account.
Then give me a minimal example: change the panel to be at the top
and remove one default widget, and show me exactly which config
file changed as a result.
```
</details>

<details>
<summary>Weeks 2\u20133 \u2014 Branding assets + Calamares default install</summary>

```
I need to add branding assets into a teammate's live-build config
tree using includes.chroot: a wallpaper PNG, and a Plymouth boot
splash theme. Give me the exact directory paths under
config/includes.chroot/ these need to go in for Debian bookworm,
and the minimal Plymouth theme files required (I don't need
animation, just a static branded splash for now).

Separately: I've installed calamares and calamares-settings-debian
and want to run a fully default, unmodified install first to make
sure it works end-to-end before I customize branding. Give me the
debug-mode command to run it and a checklist of what a successful
full install (not just the live session) should look like.
```
</details>

<details>
<summary>Weeks 2\u20133 \u2014 Calamares branding customization</summary>

```
Calamares installed and ran successfully in default form. Now I
want to customize its branding: product name to 'NovaOS', a
custom logo, and a custom accent color \u2014 without touching page
layout or logic yet (too risky for my experience level this early).

Show me the branding.desc file structure, which fields control
name/logo/color, and how to point Calamares at my custom branding
component instead of the Debian default. Keep the diff minimal \u2014
I want to change strings/images, not YAML page logic.
```
</details>

<details>
<summary>Week 4 \u2014 Menu categorization + welcome screen</summary>

```
I need installed applications on a custom Debian/LXQt image
grouped into three menu categories: Programming, Student Tools,
System. Explain how LXQt reads .desktop file Categories= fields
and whether I can achieve this by editing/adding .desktop files
rather than building a custom menu system (I want the simplest
approach that still works).

Also help me build a single static HTML 'Welcome to NovaOS' page
(no backend, no build step) that I can set to auto-open in a
lightweight browser on first login. Keep it to one file, simple
inline CSS, no external dependencies since the machine is offline.
```
</details>

<details>
<summary>Weeks 5\u20136 \u2014 Full installer end-to-end test</summary>

```
I need to validate that Calamares, once run inside a live NovaOS
VM, actually produces a working installed system \u2014 not just that
the live session works. Give me a step-by-step VM test plan: how
to boot the ISO, run the full install through Calamares to a
virtual disk, reboot into the installed system (not the live
media), and a checklist of what to verify (bootloader present,
user account created, network/desktop working, branding present).
```
</details>

## Person 3

<details>
<summary>Week 1 \u2014 Ollama + TinyLlama, benchmarked</summary>

```
I want to run a small local LLM fully offline on a machine with
around 2GB RAM available, for a college project (NovaOS \u2014 an
offline AI assistant for students). Walk me through installing
Ollama and pulling TinyLlama, then running a basic test query.

Then help me write a tiny bash one-liner (or short script) that
runs a test query while logging RAM usage (via 'free -h') and
response time to a text file, so I have concrete benchmark
numbers \u2014 not just a vibe of 'it felt slow/fast' \u2014 to report back
to my team by end of this week.
```
</details>

<details>
<summary>Week 1 (stretch) \u2014 Testing a bigger model</summary>

```
TinyLlama is working fine on my 2GB test. I now want to try a
larger model (Phi-3 Mini or Qwen2.5 1.5B\u20133B) on a machine with
4GB RAM available, to serve as a 'better quality tier' for higher-
spec machines in the same project. Give me the pull/run commands
for both, and help me design a simple side-by-side comparison:
same 3 test questions to each model, comparing response quality,
speed, and peak RAM \u2014 so I can recommend one to my team with
actual evidence instead of guessing.
```
</details>

<details>
<summary>Week 2 \u2014 novaai terminal command</summary>

```
I have Ollama + TinyLlama working. I want a simple terminal
command called 'novaai' that a student can type followed by a
question in plain text, e.g. 'novaai what is a compiler', and get
an offline answer back. Write me a minimal bash script for this,
explain how to install it to /usr/local/bin so it's available
system-wide, and how to test it. Keep it as simple as possible \u2014
no GUI, no config file, just a working command for now.
```
</details>

<details>
<summary>Week 2 \u2014 Baking Ollama into the live-build image</summary>

```
I need Ollama and a pulled model to be present automatically when
a Debian live-build ISO boots, not something the user installs
manually. I'm told this is done via a hook script under
config/hooks/live/ in the live-build config tree (owned by a
teammate). Explain what a .hook.chroot script is, how/when it
runs during the build, and write me one that installs Ollama and
pulls tinyllama automatically during the chroot build stage.
Flag anything about this that could make the build fail silently
or blow up the ISO size, since we're offline-first and need this
baked in, not downloaded at runtime.
```
</details>

<details>
<summary>Weeks 3\u20134 \u2014 Curating curriculum tools</summary>

```
I'm choosing 3\u20134 offline tools to bundle into a Debian-based
student Linux distro (NovaOS), mapped to a CS/IT B.Tech syllabus:
Computer Organization, Compiler Design, Python/ML stack, and
Cyber Security basics. I'm considering: Logisim for digital logic,
flex+bison for compiler/parsing exercises, numpy/pandas/jupyter/
scikit-learn for ML, and Wireshark for networking/security.

Check whether all of these are available as standard Debian
bookworm packages (not needing manual .jar/.deb downloads), flag
any that aren't, and suggest a lighter substitute for anything
too heavy for a low-RAM machine. Then give me the package-list
file content ready to drop into config/package-lists/.
```
</details>

<details>
<summary>Weeks 5\u20136 (if ahead) \u2014 Docs bundle</summary>

```
I want to bundle a small set of offline cheatsheets/docs (PDF or
markdown) into a Debian live-build image, viewable without
internet access, no custom viewer app \u2014 just dropped into a
sensible location under /usr/share/doc/ and reachable from the
desktop. Give me the directory convention to use and how to add
them via includes.chroot, plus a one-line way to add a desktop
shortcut pointing at the docs folder.
```
</details>

## Shared \u2014 Weekly Sync Prompt

```
Here is our current state for the NovaOS project (3-person team,
beginner Linux/Debian level, week [N] of 6):
- Person 1 (build): [paste status / errors]
- Person 2 (desktop/installer): [paste status / errors]
- Person 3 (AI/tools): [paste status / errors]

Tell me honestly, based only on what's pasted above: are we on
track for a Week 4 clean merge, or should we be cutting scope now
rather than waiting? If cutting, tell me specifically what to cut
first based on our MVP priority order (RAG > GUI > custom login
screen > welcome app > docs bundle, in that order of what goes
first). Don't be diplomatically vague \u2014 give a direct yes/no on
whether we're behind.
```
