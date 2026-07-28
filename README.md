# thevfxsupervisor.github.io

Source for **thevfxsupervisor**, the personal site of Geoffrey Hancock, VFX supervisor and
producer. Live at **https://thevfxsupervisor.github.io/**.

A deliberately small static site: markdown content compiled to HTML by a single hand-written
Python script. No framework, no dependencies, no build toolchain, no runtime.

## Layout

| Path | What it is |
|------|------------|
| `content/` | The site content, as markdown (pages, project pages, notes) |
| `templates/` | The HTML shell |
| `static/` | The stylesheet |
| `build.py` | A standard-library-only generator that renders `content/` into `docs/` |
| `docs/` | The built site; GitHub Pages serves this folder from `main` |

## Build

```
python build.py
```

Edit markdown under `content/`, run the build, and the site regenerates into `docs/`.
Python 3, standard library only, nothing to install.

---

Build, deploy, content conventions, and domain notes for maintainers live in
[`dev/MAINTAINING.md`](dev/MAINTAINING.md).
