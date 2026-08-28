<!--
  DRAFT — not live yet. See status notes at the bottom of this file for
  what's finished, what's a placeholder, and what's still blocked.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/assets/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/assets/light.svg">
  <img alt="Rajshekhar Das" src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/main/assets/light.svg">
</picture>

<!-- ============================================================
     PHASE 2 — stats cards (self-hosted). YOUR-INSTANCE below must be
     replaced with your own Vercel deployment URL once you've done the
     one-time setup (see the Setup Guide, Phase 2). Do not point this at
     the public github-readme-stats.vercel.app — that's the shared
     instance that returns "API rate limit exceeded".
     ============================================================ -->

<div align="center">
<img width="100%" src="https://streak-stats.demolab.com/?user=Rajshekhar25&hide_border=true&background=0A101F&stroke=22D3EE&ring=A78BFA&fire=10B981&currStreakLabel=22D3EE&sideLabels=94A3B8&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=64748B&titleColor=22D3EE&card_width=1180" alt="streak" />
<br/>
<img width="49%" src="https://YOUR-INSTANCE.vercel.app/api?username=Rajshekhar25&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=22D3EE&icon_color=A78BFA&text_color=94A3B8&bg_color=0A101F&card_width=500" alt="stats" />
<img width="49%" src="https://YOUR-INSTANCE.vercel.app/api/top-langs/?username=Rajshekhar25&layout=compact&langs_count=8&hide_border=true&title_color=22D3EE&text_color=94A3B8&bg_color=0A101F&card_width=500" alt="top langs" />
</div>

<!-- ============================================================
     PHASE 3 — contribution snake. Only add this once the Action has
     run green at least once (Actions tab -> Generate Snake Animation)
     -- the output branch doesn't exist before that, and both <source>
     URLs below will show as broken images until then.
     ============================================================ -->

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)"
    srcset="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)"
    srcset="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/output/github-snake.svg" />
  <img alt="Snake eating my contributions"
    src="https://raw.githubusercontent.com/Rajshekhar25/Rajshekhar25/output/github-snake.svg" />
</picture>
</div>

<!-- ============================================================
     PHASE 4 — social badges. LinkedIn is locked to brand blue (#0A66C2)
     deliberately -- shields.io's LinkedIn glyph only renders on that
     exact colour; any custom colour silently drops the icon and leaves
     bare text. GitHub badge omitted (circular on your own profile).
     ============================================================ -->

<div align="center">

<a href="https://www.linkedin.com/in/rajshekhar25/">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
&nbsp;&nbsp;
<a href="https://leetcode.com/u/0xRajshekhar/">
  <img src="https://img.shields.io/badge/LeetCode-0A101F?style=for-the-badge&logo=leetcode&logoColor=FFA116&labelColor=0A101F" alt="LeetCode" />
</a>
&nbsp;&nbsp;
<a href="https://codeforces.com/profile/0xRajshekhar">
  <img src="https://img.shields.io/badge/Codeforces-0A101F?style=for-the-badge&logo=codeforces&logoColor=22D3EE&labelColor=0A101F" alt="Codeforces" />
</a>
&nbsp;&nbsp;
<a href="mailto:rajshekhardas85@gmail.com">
  <img src="https://img.shields.io/badge/Email-0A101F?style=for-the-badge&logo=gmail&logoColor=10B981&labelColor=0A101F" alt="Email" />
</a>

</div>

---

## Status — what's real, what's placeholder, what's blocked

**Finished and verified:**
- Banner layout: terminal chrome, dot-path portrait (crispEdges paths built
  from your approved dot pattern — not a raster image), SYSTEM.INFO panel
  with programmatically-computed dotted leaders, pulsing LIVE badge.
- Intro shimmer: 60 dot groups fade in over ~2s, scattered across the whole
  portrait by construction (random group assignment). Verified with an
  evenness metric (0.056 — matches the doc's own "good" target of ~0.05).
- Loop drift/return: 94 dot bands, grouped with noise-perturbed clustering
  (not a naive grid) so the dissolve doesn't look like mosaic tiles.
  Verified against a positive control — true grid-quantization of the same
  dots scores 0.645 on the straight-boundary metric; the real bands score
  0.356, a real 45% separation, with an assertion that fails the build if
  that ever stops being true.
- Full 14.2s timeline verified by directly scrubbing the SVG's SMIL clock
  (`setCurrentTime`) and checking computed opacity at five checkpoints —
  hold, exiting, hidden mid-logo-phase, entering, held again next cycle.
  All five now match the intended design exactly. (A first version had a
  real bug here: SMIL measures `keyTimes` as elapsed-since-an-element's-own
  `begin`, not since document t=0 — I'd computed them as absolute-time
  fractions, which silently shifted the whole cycle by +3s. Fixed and
  re-verified.)

**Known placeholder:**
- `LOGO_TARGET` (where the portrait bands drift toward) is currently the
  portrait frame's own center, not a real logo centroid — see below.

**Blocked, not placeholder — genuinely not built yet:**
- The traveler layer (the ~900 dots that morph between the TypeScript,
  Python and C++ logos during the logo-hold phases) does not exist yet.
  It needs real vector path data for those three logos, which needs a
  network fetch. This environment's DNS resolution has been down for this
  entire session (confirmed via curl, WebFetch, and git — all three fail
  with "could not resolve host", while raw IP connectivity works). I will
  not hand-draw the logos as a workaround; the build spec is explicit that
  they must be traced from real reference data, not invented.
- Nothing has been pushed. `git push` needs the same DNS resolution that's
  currently down, so this repo's live README is untouched.

**Needs you regardless of the network:**
- Phase 2 self-hosted stats: create a GitHub PAT, fork
  `anuraghazra/github-readme-stats`, deploy it to your own Vercel account,
  and send me the resulting instance URL — I can't do the account creation
  or deployment for you. `YOUR-INSTANCE` above is the placeholder.
- Once the network recovers (or if you'd rather send me the three logo
  images directly instead of waiting), I'll build the traveler layer, then
  this stops being a draft.
