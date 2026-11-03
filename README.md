# KOEX GAMING

A dark browser arcade with five Pygame games, packaged for the web with Pygbag.

## Games included
1. Neon Racer — dodge traffic with left/right arrows or A/D.
2. Snake — use arrow keys or WASD.
3. Pong — move with W/S or up/down arrows.
4. Breakout — move with left/right arrows or A/D.
5. Block Dodger — avoid falling blocks with left/right arrows or A/D.

## Run locally

Use Python 3.11 or 3.12.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m pygbag --build main.py
```

For a quick browser test, Pygbag's build output is in `build/web/`. Serve that folder with a local web server rather than opening the HTML file directly.

## Deploy to Render

1. Create a GitHub repository named `koex-gaming`.
2. Put the contents of this project folder in the repository root.
3. Push the repository to GitHub.
4. In Render, choose **New + → Static Site** and connect the repository.
5. Set:
   - Build Command: `pip install -r requirements.txt && python -m pygbag --build main.py && mkdir -p public/games/arcade && cp -R build/web/. public/games/arcade/`
   - Publish Directory: `public`
6. Deploy.

The included `render.yaml` contains the same static-site configuration and can be used if you choose Render Blueprint deployment.

## Project layout

```text
koex-gaming/
├── main.py                  # Pygame arcade: all five games
├── requirements.txt         # pygame-ce and pygbag
├── render.yaml              # Render static-site configuration
├── README.md
└── public/
    ├── index.html            # Website homepage
    ├── styles.css            # Dark arcade design
    ├── app.js                # Opens/closes the game player
    └── games/
        └── arcade/           # Pygbag build output is copied here during deploy
```

## Notes

- Pygame desktop programs do not run natively in a browser. Pygbag packages compatible Pygame code for browser execution using WebAssembly.
- The website's five game cards open the shared arcade player. Choose the desired game from the in-game menu using keys 1–5.
- This starter does not yet save scores online or provide accounts/leaderboards. Those require a backend and persistent database.
