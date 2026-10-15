#!/bin/sh
# Render the dummy app pages to the screenshots the site uses.
#   python3 app-shots/build.py && sh app-shots/render.sh
# Needs Google Chrome and cwebp (brew install webp). Output: site-assets/app/<view>.webp
set -e
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PORT="${PORT:-8799}"
W="${W:-800}"
H="${H:-540}"
mkdir -p site-assets/app
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER' EXIT
sleep 1
for view in feed board compose conversations thread summary; do
  VW="$W"; VH="$H"
  # The board is shown at a wide window, like the real app's masonry wall.
  [ "$view" = summary ] && VH=660
  # Board: a slightly larger window so four columns fit and the UI stays legible.
  { [ "$view" = board ] || [ "$view" = compose ] || [ "$view" = conversations ] || [ "$view" = feed ]; } && VW=960 && VH=648
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --virtual-time-budget=4000 --window-size="$VW,$VH" \
    --screenshot="site-assets/app/$view.png" "http://localhost:$PORT/app-shots/$view.html" 2>/dev/null
  cwebp -quiet -q 88 "site-assets/app/$view.png" -o "site-assets/app/$view.webp"
  MV="$view"; [ "$view" = compose ] && MV=compose-typed
  # Phone frame: the same page rendered at a narrow window, so the UI reflows
  # and stays legible at 390px.
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --virtual-time-budget=4000 --window-size=600,520 \
    --screenshot="site-assets/app/$view-m.png" "http://localhost:$PORT/app-shots/phone.html#$MV" 2>/dev/null
  cwebp -quiet -q 88 -crop 0 0 780 1040 "site-assets/app/$view-m.png" -o "site-assets/app/$view-m.webp"
  rm "site-assets/app/$view-m.png"
  rm "site-assets/app/$view.png"
  echo "rendered site-assets/app/$view.webp"
done
# Summary dialog close-up (site AI section).
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --virtual-time-budget=4000 --window-size=720,542 \
  --screenshot="site-assets/app/summary-card.png" "http://localhost:$PORT/app-shots/summary-card.html" 2>/dev/null
cwebp -quiet -q 88 "site-assets/app/summary-card.png" -o "site-assets/app/summary-card.webp"
rm "site-assets/app/summary-card.png"
echo "rendered site-assets/app/summary-card.webp"
# Tall timeline strip, scrolled inside a window frame on the site.
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --virtual-time-budget=4000 --window-size=960,3400 \
  --screenshot="site-assets/app/timeline-strip.png" "http://localhost:$PORT/app-shots/timeline-strip.html" 2>/dev/null
cwebp -quiet -q 84 "site-assets/app/timeline-strip.png" -o "site-assets/app/timeline-strip.webp"
rm "site-assets/app/timeline-strip.png"
echo "rendered site-assets/app/timeline-strip.webp"
