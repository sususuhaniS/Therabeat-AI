# TheraBeat AI → MeloMatch AI: migration notes

## How to apply this

I don't have push/write access to `sususuhaniS/Therabeat-AI`, and I read the
repo through GitHub's web UI rather than a real git clone (no outbound
network access in this environment, and GitHub blocks automated tree
browsing). The files in this delivery are a faithful *functional*
reconstruction — correct logic, imports, and control flow — but I'd
recommend diffing them against your actual local checkout before committing,
rather than treating them as a byte-exact patch.

```bash
git clone <your repo>
cd Therabeat-AI
git mv README.md README.md.orig  # or just diff manually
# copy in Home.py, database.py, README.md from this delivery
# review the diff, especially indentation, before committing
```

## A. Diff summary

- **`Home.py`** — now the single entry point. Merged in the recommendation
  UI (`show_music_recommendations`) previously duplicated in `app.py`.
  Renamed all TheraBeat/therapy copy to MeloMatch AI + research-prototype
  framing. Fixed a pre-existing CSS bug (`background-color: black` was
  missing a semicolon). Added a non-clinical disclaimer in the hero and
  sidebar. Model loading, Spotify init, and Firestore calls are unchanged.
- **`app.py`** — removed. Its only unique logic (the recommendations UI) now
  lives in `Home.py`.
- **`database.py`** — reworded section headers/help text around the
  self-report sliders ("Initial Mood Settings" → "Self-Reported Listening
  Context (Research Use Only)", added disclaimer captions). **All dict keys
  used by the model's feature vector are unchanged** (`Anxiety`,
  `Depression`, `Insomnia`, `OCD`, `BPM`, `Frequency_*`, etc.) — required by
  constraint #6.
- **`music.py`** — no changes. Already free of clinical/therapy framing;
  genre prediction, feature vector, and output mapping untouched.
- **`login.py`** — no changes needed (no TheraBeat/clinical language found).
- **`README.md`** — full rewrite: MeloMatch AI branding, research-prototype
  description, explicit non-clinical disclaimer, updated project structure,
  updated repo clone URL placeholder.
- **`.devcontainer/devcontainer.json`** — I could not fetch the original
  file's contents (GitHub blocked the tree view, and I didn't have the
  filename to fetch it directly). I've included a reconstructed version
  that launches `streamlit run Home.py` — **please merge this against your
  actual file** rather than overwriting it blind.
- **`pages/`** — not reviewed. I don't know the filenames in this directory
  ; if any of them reference TheraBeat, therapy, or clinical framing, they
  still need the same string replacements. Send me the contents and I'll
  finish this pass.
- **`best_xgb`, `requirements.txt`** — untouched, per constraints #6.

## B. Files removed / renamed

| File | Action |
|---|---|
| `app.py` | Removed (logic merged into `Home.py`) |
| `Home.py` | Kept as canonical entry point, content rewritten |
| `README.md` | Content rewritten, same filename |
| `database.py` | Content rewritten (copy only), same filename |
| `.devcontainer/devcontainer.json` | Needs manual merge — update `postAttachCommand`/`postCreateCommand` (or equivalent) to launch `Home.py` instead of `app.py` |

No files were renamed at the filesystem level in this pass — only content
and the repo name (`Therabeat-AI` → `MeloMatch-AI`, a GitHub rename you'd do
separately in repo settings, which preserves the old URL as a redirect).

## C. Local smoke test

```bash
# 1. Set up a clean environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Make sure secrets exist locally (do NOT commit this file)
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
SPOTIFY_CLIENT_ID = "..."
SPOTIFY_CLIENT_SECRET = "..."
LYRIA_API_KEY = "..."
[firebase]
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
client_x509_cert_url = "..."
[users]
"test@example.com" = "testpassword"
EOF

# 3. Confirm app.py is gone and Home.py is the only entry point
ls *.py                            # should NOT list app.py

# 4. Static sanity checks
python -m py_compile Home.py login.py music.py database.py

# 5. Run it
streamlit run Home.py

# 6. Manually verify in the browser:
#    - Page title reads "MeloMatch AI - Home" (browser tab)
#    - No "TheraBeat" or therapy-framed copy anywhere in the UI
#    - Login works, profile form saves, "Generate AI Music" and
#      "Get Spotify Playlist" both work end-to-end
#    - grep confirms no leftover branding:
grep -ri "therabeat\|music therapy\|mental wellness treatment" *.py README.md
```
