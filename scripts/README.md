# Banner generator pipeline

Regenerates `assets/dark.svg` and `assets/light.svg` from source. Run in
this order (each stage depends on the previous one's output in
`scripts/_build/`):

```bash
python rasterize_logos.py         # TypeScript/Python/C++ -> point clouds
python build_animation.py         # portrait dot groupings, verified metrics
python build_animated_portrait.py # intro shimmer + loop drift SVG layers
python build_travelers.py         # optimal-transport logo-to-logo matching
python build_traveler_svg.py      # traveler dot SVG layer
python build_banner.py            # assembles everything into the final SVGs
```

Requires `numpy`, `scipy`, `opencv-python-headless`, `svgelements`, `Pillow`.

The actual source-of-truth data is `assets/dot_pattern.npy` and
`assets/foreground_mask.npy` (the approved portrait, dithered and
segmented) — not the SVGs themselves. If you want to change the portrait,
edit the pipeline that produced those two files (crop, dither, mask), not
the generated SVG directly.

`assets/logos/*.svg` are the official simple-icons vector files (unmodified,
MIT licensed) that `rasterize_logos.py` traces — not hand-drawn.
