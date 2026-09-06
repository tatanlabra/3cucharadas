# Publishing 3cucharadas

## Production model

Production is GitLab Pages on the custom domain:

```text
https://3cucharadas.cl
```

The canonical Jekyll config is `url: "https://3cucharadas.cl"` and
`baseurl: ""`. GitHub remains a public mirror and its Pages surface must publish
only the static redirector from `gh-pages-redirect`; it must not publish a
duplicate copy of the site.

## Push targets

`origin` is the publishing remote for the site. Its fetch URL points to GitLab,
and its push URLs publish the same `main` ref to both mirrors:

```bash
git remote -v
git config --local --get-all remote.origin.pushurl
```

Expected push URLs:

```text
git@gitlab.com:tatanlabra/3cucharadas.git
https://github.com/tatanlabra/3cucharadas.git
```

With that configuration, this command pushes `main` to GitLab and GitHub:

```bash
git push origin main
```

This multi-URL push is not atomic. If one service accepts the push and the other
fails, verify both remote refs before retrying or fixing the failed side.

## Authentication

GitLab uses SSH. GitHub uses HTTPS through the GitHub CLI credential helper:

```bash
git ls-remote --heads git@gitlab.com:tatanlabra/3cucharadas.git main
git ls-remote --heads https://github.com/tatanlabra/3cucharadas.git main
git push --dry-run origin main
```

## Local Telegram notification

Un commit local no acredita publicación: puede no haberse subido, no tener CI verde
o no estar disponible en la página pública. Por eso `post-commit` termina en
silencio y sólo conserva la traza de destinos de difusión.

Install or refresh the local hook with:

```bash
scripts/install_git_hooks.sh
```

El aviso es explícito y local. Úsalo sólo después de que una persona haya
autorizado el push y con la URL pública más un texto distintivo del post:

```bash
python3 scripts/notify_telegram_publication.py \
  --publication-url https://3cucharadas.cl/ruta-del-post/ \
  --expect-text 'Título distintivo del post' \
  --subject 'Título distintivo del post' \
  --dry-run
```

El comando verifica el build del commit aislado, el mismo SHA en GitLab y
GitHub, un pipeline exitoso de GitLab para ese SHA y el texto esperado en la página
pública. Si cualquiera falla, no envía Telegram. Al pasar el `--dry-run`,
repite el comando sin ese flag para enviar un único aviso con URL, commit y gates.
Las credenciales siguen llegando sólo por `EPUB_CURATOR_TG_TOKEN` y
`EPUB_CURATOR_TG_CHAT_ID` del entorno de ejecución; nunca se guardan en el repo.

Before publishing, keep checking:

```bash
bash -n scripts/git-hooks/post-commit scripts/install_git_hooks.sh
python -m py_compile scripts/notify_telegram_commit.py scripts/notify_telegram_publication.py
python -m unittest tests/test_notify_telegram_publication.py
```

Also scan `scripts`, `docs`, and `README.md` for concrete Telegram variable
assignments, bot API tokens, bearer tokens, OpenAI-style API keys, and private
key headers.

## GitHub Pages redirector

Build the real site first, then generate the redirector:

```bash
JEKYLL_ENV=production bundle exec jekyll build
python3 tools/build_github_redirector.py
```

Publish `.redirect_build/` to the `gh-pages-redirect` branch, with no custom
domain. The redirector must keep canonical links on `https://3cucharadas.cl/`
and `robots` as `index, follow` so the historical GitHub Pages URLs point
cleanly to the new canonical site instead of becoming a duplicate site.

Preferred setup is the dedicated workflow
`.github/workflows/github-pages-redirector.yml`; it checks out only
`gh-pages-redirect`, stages it as `_site_redirect`, and deploys exactly one
GitHub Pages artifact. It does not build or publish the full Jekyll site.
