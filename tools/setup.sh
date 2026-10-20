#!/bin/bash
# Prepares a work folder with the brand fonts. Usage: source tools/setup.sh
export WK_WORK=${WK_WORK:-$HOME/wk-work}
mkdir -p $WK_WORK/fonts && cd $WK_WORK/fonts
if [ ! -d fontsource-outfit-5.3.0 ]; then
  npm pack @fontsource/plus-jakarta-sans@5.3.0 @fontsource/outfit@5.3.0 @fontsource/ibm-plex-sans-arabic@5.3.0 --silent >/dev/null 2>&1
  for f in *.tgz; do tar xzf $f --wildcards '*/files/*'; mv package ${f%.tgz}; done
fi
python3 -c "from PIL import features; assert features.check('raqm'), 'Pillow needs raqm for Arabic'" && echo "fonts ready in $WK_WORK/fonts"
cd - >/dev/null
