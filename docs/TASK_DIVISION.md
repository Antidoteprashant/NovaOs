# NovaOS \u2014 Task Division + Commands

Beginner-team edition. See [`PRD_TRD.md`](PRD_TRD.md) for full MVP scope.

## Person 1 \u2014 Base System & Build Engineer

**Owns:** the foundation. Nothing else matters until this boots.

### Week 1 \u2014 Environment setup + first ISO

```bash
sudo apt update
sudo apt install -y live-build live-config live-boot
mkdir ~/novaos-build && cd ~/novaos-build
lb config --distribution bookworm --architecture amd64 \
  --debian-installer none --archive-areas "main contrib non-free-firmware"

sudo lb build 2>&1 | tee build.log
# Output: live-image-amd64.hybrid.iso

qemu-system-x86_64 -m 2048 -cdrom live-image-amd64.hybrid.iso -boot d
```

> **Checkpoint:** if the plain ISO doesn't boot in QEMU by end of Week 1, stop adding features and spend Week 2 purely on fixing the base build.

### Week 2 \u2014 Package lists

```bash
mkdir -p config/package-lists
cat > config/package-lists/desktop.list.chroot << 'EOF'
lxqt
sddm
EOF

cat > config/package-lists/devtools.list.chroot << 'EOF'
python3
python3-pip
default-jdk
git
gcc
g++
make
EOF

sudo lb clean && sudo lb build 2>&1 | tee build.log
```

### Weeks 3\u20134 \u2014 Stability + merge

- Fix build issues as Person 2/3's layers land in `config/`.
- Keep a `build.log` from every build \u2014 diff two logs to spot what broke.
- Check ISO size after every build: `du -h live-image-amd64.hybrid.iso` \u2014 flag it in weekly sync if it crosses ~2.5GB before AI models are even added.

### Weeks 5\u20136 \u2014 RAM-tier testing

```bash
qemu-system-x86_64 -m 1024 -cdrom live-image-amd64.hybrid.iso -boot d
qemu-system-x86_64 -m 2048 -cdrom live-image-amd64.hybrid.iso -boot d
qemu-system-x86_64 -m 4096 -cdrom live-image-amd64.hybrid.iso -boot d
# inside the booted VM:
free -h
```

Log RAM numbers in the shared bug/task sheet \u2014 this is your success-metric evidence for the demo.

---

## Person 2 \u2014 Desktop Experience & Installer

**Owns:** everything the user sees during install and first login.

### Week 1 \u2014 Research (no build access needed yet)

```bash
sudo apt install -y lxqt
```
Explore config at `~/.config/lxqt/` (per-user) and `/etc/xdg/lxqt/` (system-wide default \u2014 this is what NovaOS needs).

### Weeks 2\u20133 \u2014 Branding + Calamares

```bash
mkdir -p config/includes.chroot/usr/share/backgrounds/novaos
cp wallpaper.png config/includes.chroot/usr/share/backgrounds/novaos/

mkdir -p config/includes.chroot/usr/share/plymouth/themes/novaos
# boot splash (Plymouth theme) goes here

sudo apt install -y calamares calamares-settings-debian
sudo calamares -d   # -d = debug mode, verbose logging
```

Calamares branding lives in `/etc/calamares/branding/<yourbranding>/branding.desc` \u2014 copy the default and edit strings/colors/logo before touching layout.

### Week 4 \u2014 Menu + welcome polish

- Group apps into Programming / Student Tools / System via `.desktop` file `Categories=` fields \u2014 don't build a custom menu system.
- Keep the "Welcome to NovaOS" screen as a single static HTML file opened in a lightweight browser on first login.

### Weeks 5\u20136 \u2014 Installer end-to-end test

Run Calamares fully through to a real install inside a VM, then boot the **installed result**, not just the live session \u2014 this step is most often skipped and breaks during the demo.

---

## Person 3 \u2014 AI Assistant & Curriculum Tools

**Owns:** the differentiator \u2014 offline AI + syllabus-mapped tools.

### Week 1 \u2014 Model research

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
ollama run tinyllama "Explain TCP vs UDP in 2 lines"
free -h   # run in another terminal while it answers
```

Stretch (only if TinyLlama is comfortable):
```bash
ollama pull phi3:mini
ollama run phi3:mini "Explain TCP vs UDP in 2 lines"
```

### Week 2 \u2014 `novaai` terminal command

See [`scripts/novaai`](../scripts/novaai) \u2014 install with:
```bash
sudo cp scripts/novaai /usr/local/bin/novaai
sudo chmod +x /usr/local/bin/novaai
novaai "What is a compiler?"
```

Bake into the build via a hook (hand off to Person 1 once it works standalone) \u2014 see [`config/hooks/live/010-ollama.hook.chroot`](../config/hooks/live/010-ollama.hook.chroot).

### Weeks 3\u20134 \u2014 Curriculum tools

| Subject | Tool | Debian package |
|---|---|---|
| Computer Organization | Logisim | `logisim` (or manual `.jar`) |
| Compiler Design | flex + bison | `flex`, `bison` |
| Python/ML stack | numpy, pandas, jupyter, scikit-learn | `python3-numpy python3-pandas jupyter python3-sklearn` |
| Cyber Security basics | Wireshark | `wireshark` |

See [`config/package-lists/curriculum.list.chroot`](../config/package-lists/curriculum.list.chroot).

### Weeks 5\u20136 (only if ahead of schedule)

- Docs/cheatsheet bundle: folder of PDFs/markdown under `/usr/share/doc/novaos/`.
- RAG stretch goal: **do not start** unless Person 1's Week 4 checkpoint passed clean.

---

## Combined Week-Wise Flow

| Week | Person 1 | Person 2 | Person 3 |
|---|---|---|---|
| 1 | live-build setup \u2192 first plain ISO boots | Research LXQt config | Ollama + TinyLlama working, benchmarked |
| 2 | Package lists v1, rebuild + test | Branding prep, Calamares default install | `novaai` terminal script working |
| 3 | Fix build issues as layers land | Calamares branding/theming | Ollama install hook added to build tree |
| 4 | **MERGE CHECKPOINT** \u2014 see [WEEK4_CHECKPOINT.md](WEEK4_CHECKPOINT.md) | Menu categorization, welcome screen | Curriculum package list finalized |
| 5 | Full RAM-tier testing (1/2/4GB) | Full Calamares install-to-boot test | Docs bundle (if ahead) or help stabilize |
| 6 | Final ISO build + bug fixes | Final polish pass | Final AI/tools polish + demo prep |
