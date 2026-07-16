# NovaOS \u2014 PRD & TRD (Beginner-Team MVP Edition)

## 1. Problem Statement

- Old/hand-me-down laptops struggle to run modern OSes and IDEs smoothly.
- Setting up a dev environment (Python, Java, Git, compilers) from scratch wastes hours every semester.
- No existing Linux distro is curated around actual college syllabus needs (COA, TOC, Compiler Design, NN/DL, Cyber Security).

## 2. Product Vision

NovaOS is a Debian-based Linux distribution built to boot fast on old hardware, arrive pre-loaded with tools mapped to a CS/IT syllabus, and include an offline AI assistant \u2014 fully usable on day one, no setup, no internet dependency.

## 3. Target User

- B.Tech CS/IT students (2nd\u20134th year)
- 2GB\u20138GB RAM machines, including 5+ year old laptops
- Limited/unreliable internet (hostel WiFi, data constraints)

## 4. MVP Scope (team confirmed beginner-level with Linux/Debian)

| Included in MVP | Cut \u2014 add back only if ahead of schedule |
|---|---|
| Plain bootable Debian ISO (LXQt) | GRUB custom theme |
| Calamares installer (default look, minor branding) | Custom login screen |
| Boot splash + wallpaper + icons (basic) | "Welcome to NovaOS" first-login app |
| Core dev tools (Python, Java, Git, gcc) | Student Toolkit app |
| 3\u20134 curriculum tools | Offline docs/cheatsheet bundle |
| NovaAI as a terminal command only (`novaai`) | NovaAI GUI |
| TinyLlama on Ollama, 2GB tier only | Phi-3/Qwen 4GB tier |
| \u2014 | RAG "ask your notes" feature |

## 5. Success Metrics (by RAM tier)

| Metric | 2GB tier | 4GB+ tier |
|---|---|---|
| ISO boots + installs on test VM | Required | Required |
| Idle RAM usage post-login | Under ~450MB (LXQt) | Under ~600MB |
| Curriculum tools launch without setup | Required | Required |
| AI assistant responds offline | TinyLlama only | Phi-3 Mini / Qwen2.5 (stretch) |

## 6. Architecture

```
Debian (base OS)
\u2514\u2500\u2500 live-build (build system)
      \u251c\u2500\u2500 Desktop Environment (LXQt default)
      \u251c\u2500\u2500 Curated Package List (dev tools + student tools)
      \u251c\u2500\u2500 Branding Layer (theme, splash, wallpaper, GRUB)
      \u251c\u2500\u2500 Calamares (installer)
      \u2514\u2500\u2500 NovaAI (Ollama + local model)
            \u2514\u2500\u2500 Output: NovaOS-v1.iso
```

## 7. Tech Stack

| Layer | Tool/Tech |
|---|---|
| Base OS | Debian (stable branch \u2014 bookworm) |
| Build system | live-build |
| Desktop Environment | LXQt (default), XFCE fallback |
| Installer | Calamares |
| AI runtime | Ollama (or llama.cpp for lower overhead) |
| AI model \u2014 2GB tier | TinyLlama 1.1B (Q4_K_M) |
| AI model \u2014 4GB+ tier (stretch) | Phi-3 Mini 3.8B or Qwen2.5 1.5B\u20133B |
| Testing | VirtualBox/QEMU, constrained RAM profiles |

## 8. ISO Size & Distribution

Bundling Ollama + a model typically pushes the ISO to 3\u20135GB+. GitHub Releases caps individual files at 2GB. Decide by Week 2:

- **(a)** Split AI models into a separate downloadable pack fetched post-install (base ISO stays under 2GB), or
- **(b)** Host the full ISO elsewhere (SourceForge, torrent+magnet, cloud bucket), or
- **(c)** Ship two variants: "base" (no AI, ~1.5GB) and "full" (with AI, ~4GB) \u2014 **recommended**, since it naturally demos the 2GB/4GB tier split.

## 9. Non-Goals

- Building a kernel from scratch
- Supporting 32-bit hardware
- Full GPT-4-level AI reasoning
- Multi-language localization (English/Hinglish docs only, for now)

---
This is a living document. Update it as key decisions are finalized \u2014 the LXQt vs XFCE call, the AI model per tier, the ISO distribution approach, and the final package list.
