import sys
import re

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire les @require de l'ancien header (0, 1 ou N)
requires = re.findall(r'^// @require\s+.+$', content, flags=re.MULTILINE)
requires_block = "\n" + "\n".join(requires) if requires else ""

# Extraire les valeurs à réutiliser depuis le fichier source
version = re.search(r'// @version\s+(\S+)', content).group(1)

# Définir le nouveau header
new_header = f"""// ==UserScript==
// @name           VPN_JV_Chat
// @description    Outil de discussion instantanée (Fork et debug pour iOS et GreasyMonkey) (VPN Build {version})
// @author         Blaff, Rand0max, Atlantis
// @namespace      VPN_JV_Chat
// @license        MIT
// @version        {version}
// @icon           https://images.emojiterra.com/google/noto-emoji/unicode-17.0/color/128px/1f7e6.png
// @match          http://*.jeuxvideo.com/forums/42-*
// @match          https://*.jeuxvideo.com/forums/42-*
// @match          http://*.jeuxvideo.com/forums/1-*
// @match          https://*.jeuxvideo.com/forums/1-*
// @grant          none{requires_block}
// ==/UserScript=="""

# Stripper l'ancien header et recoller
body = re.sub(r'// ==UserScript==.*?// ==/UserScript==\n?', '', content, flags=re.DOTALL)

# Filtrage ligne par ligne — #OFFALTX / #ALTX
lines = body.lstrip().splitlines(keepends=True)
result = []
in_remove_block = False
for line in lines:
    stripped = line.strip()
    if "#OFFALTX:REMOVE-START" in stripped:
        in_remove_block = True
        continue
    if "#OFFALTX:REMOVE-END" in stripped:
        in_remove_block = False
        continue
    if in_remove_block:
        continue
    if "#ALTX:UNCOMMENT" in stripped:
        continue
    result.append(line)


# Filtrage ligne par ligne — #OFFFORVPN / #FORVPN (VPN)
lines = result
result = []
in_vpn_remove_block = False
for line in lines:
    stripped = line.strip()
    if "#OFFFORVPN:REMOVE-START" in stripped:
        in_vpn_remove_block = True
        continue
    if "#OFFFORVPN:REMOVE-END" in stripped:
        in_vpn_remove_block = False
        continue
    if in_vpn_remove_block:
        continue
    if "#FORVPN:UNCOMMENT" in stripped:
        continue
    result.append(line)

result_text = "".join(result)

# ============================================================
# Patches hardcodés
# ============================================================

# 1) updateIntervals
result_text = result_text.replace(
    "let updateIntervals = [2, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 30, 30, 30, 30, 30, 30, 30, 30, 60];",
    "let updateIntervals = [10, 12, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35, 35, 60];",
)

# 2) Titre info-fofo
result_text = result_text.replace(
    "                    <h4 class='titre-info-fofo'>Profil</h4>",
    "                    <h4 class='titre-info-fofo'>Low Requetes</h4>",
)

# 3) Insertion du bloc skip-hidden — ancré sur `let timestamp` + `function scheduleNextUpdate`
result_text = result_text.replace(
    """    let timestamp = getTimestamp();

    function scheduleNextUpdate(interval, p, goLast) {""",
    """    // ##   VPN429 NO REQUET BACKGROUND
    if (document.hidden) {
        currentTimeoutId = setTimeout(tryCatch(function () {
            updateMessages(page, goToLast);
        }), 5000);
        return;
    }
    // ## VPN429 NO REQUET BACKGROUND

    let timestamp = getTimestamp();

    function scheduleNextUpdate(interval, p, goLast) {""",
)


# 4) Re-planifier au lieu d'appeler updateMessages directement
result_text = result_text.replace(
    "            updateMessages(page + 1, true);",
    "            scheduleNextUpdate(2000, page + 1, true);",
)

output = new_header + "\n\n" + result_text

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output)
