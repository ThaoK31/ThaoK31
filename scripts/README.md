# Scripts

They draw the images of this profile, in `../assets`. Fonts and icons are embedded in the images: nothing calls a third party.

| Script | Draws | Run from `scripts/` |
| --- | --- | --- |
| `header.py` | `header-dark.svg`, `header-light.svg` | `python header.py <fonts> ../assets` |
| `stack.py` | `stack-dark.svg`, `stack-light.svg` | `python stack.py <react-icons>/si/index.js icons <fonts>/barlow-400.woff2 <TypeSafe icon> ../assets` |
| `visuals.mjs` | `sport-extract.png`, `moss-and-mayhem.png` | `node visuals.mjs <frontend> <phone shots> <game shots> ../assets` |
| `preview.mjs` | Previews of the profile: dark, light and mobile | `node preview.mjs <frontend> .. <out dir>` |

- `<fonts>`: Barlow and Barlow Semi Condensed (OFL), in `frontend/src/fonts` of Sport Extract.
- `<react-icons>`: react-icons 4.12.0, for most icons, from Simple Icons (CC0), and for the cup of Java, from Font Awesome Free 6.4.2 (CC BY 4.0). `icons/` holds the icons of Simple Icons 16.35.0 that react-icons lacks.
- `<TypeSafe icon>`: the icon of the TypeSafe site, from which `stack.py` cuts the mark of Jev. It is not in this repository.
- `<frontend>`: the frontend of Sport Extract, for `playwright-core`. The scripts drive the installed Chrome.
