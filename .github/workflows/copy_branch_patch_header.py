import sys
import re

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire les valeurs à réutiliser depuis le fichier source
version = re.search(r'// @version\s+(\S+)', content).group(1)

# Définir le nouveau header
new_header = f"""// ==UserScript==
// @name           JV_Chat_Custsom_Fork
// @description    Outil de discussion instantanée (Fork et debug pour iOS et GreasyMonkey)
// @author         Blaff, Rand0max, Atlantis/Lantea-Git
// @namespace      JV_Chat_Custsom_Fork
// @license        MIT
// @version        {version}
// @icon           https://images.emojiterra.com/google/noto-emoji/unicode-17.0/color/128px/2b1b.png
// @match          http://*.jeuxvideo.com/forums/42-*
// @match          https://*.jeuxvideo.com/forums/42-*
// @match          http://*.jeuxvideo.com/forums/1-*
// @match          https://*.jeuxvideo.com/forums/1-*
// @downloadURL https://update.greasyfork.org/scripts/576263/JV_Chat_Custsom_Fork.user.js
// @updateURL https://update.greasyfork.org/scripts/576263/JV_Chat_Custsom_Fork.meta.js
// ==/UserScript=="""

# Stripper l'ancien header et recoller
body = re.sub(r'// ==UserScript==.*?// ==/UserScript==\n?', '', content, flags=re.DOTALL)

# Filtrage ligne par ligne
lines = body.lstrip().splitlines(keepends=True)
result = []
in_remove_block = False

for line in lines:
    stripped = line.strip()

    # REMOVE
    if "#OFFALTX:REMOVE-START" in stripped:
        in_remove_block = True
        continue
    if "#OFFALTX:REMOVE-END" in stripped:
        in_remove_block = False
        continue
    if in_remove_block:
        continue

    # UNCOMMENT
    if "#ALTX:UNCOMMENT" in stripped:
        continue

    result.append(line)

output = new_header + "\n\n" + "".join(result)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output)
