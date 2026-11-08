"""How booking works, as a clean 6-slide photo carousel (replaces the zoom-slideshow Reel; Kamel 8 Nov 2026). Real listing photos only.
Steps from weekendna.com/en/how-it-works (checked 30 Oct 2026). Run `source tools/setup.sh` first."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); O = f"{ROOT}/posts/2026-11-how-booking-works"
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("acampar/42-02"), f"{O}/slide-1.jpg", "Found a place you love?", "Here is how to request it", "Four simple steps, nothing to pay Weekendna", "", "Weekendna")
steps = [("acampar/42-04", "Pick your dates", ["Open the stay on weekendna.com", "Choose your dates on the calendar"], "Free to request"),
         ("legrey/48-05", "Send a request", ["WhatsApp opens with your dates,", "guests and request number written"], "One tap"),
         ("fvc/26-01", "The owner replies", ["You talk to the owner directly", "No reply in 48 hours? It expires"], "No middleman"),
         ("gray/55-07", "You never pay Weekendna", ["No online payment, no booking fee", "Agree the deposit with the owner"], "Bank transfer, OMT/Whish or cash")]
for i, (ph, t, facts, line) in enumerate(steps, 1):
    place_slide(P(ph), f"{O}/slide-{i+1}.jpg", i, 4, t, f"Step {i} of 4", facts, line, "")
last(f"{O}/slide-6.jpg", None, "Plan your next weekend", "", main="save", head=("Your next weekend", "starts with a request"))
story(P("acampar/42-02"), f"{O}/story.jpg", "How to request", "your stay", "Four steps, nothing to pay Weekendna", "", main="save")
print("ok")
