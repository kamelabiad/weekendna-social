"""The Friday Drop builder (weekly from Thu 5 Nov 2026). Builds BOTH Drop items from the places you pass:
  posts/<drop>/        Thursday feed carousel: cover, one slide per place ("Confirmed Thursday"), last slide; story.jpg; caption.txt
  posts/<drop>-reel/   Friday recap Reel config (reel-remotion.json), caption.txt and the 4-image story sequence (story-1..4.jpg)
Only facts from the listings (checked with tools/verify_post.py). Run `source tools/setup.sh` first; photos in reels/public/photos/<dir>.

Usage: python3 tools/make_drop.py <drop-folder> "<dates EN>" "<dates AR>" <place> <place> [<place>]
  e.g. python3 tools/make_drop.py 2026-11-friday-drop-1 "Fri 6 – Sun 8 Nov" "الجمعة ٦ لـ الأحد ٨ تشرين الثاني" royal ghosta aqualand
When Kamel confirms ("Drop confirmed: A, B, C"), rerun with only the confirmed places (swap in the reserve if one is missing), delete
any leftover drop-N.jpg slides from the old run, render the Reel (reels/README.md) and run tools/add_follow_card_v2.py on the -reel folder,
then set drop_confirmed true + status "scheduled" on both log items and update listing_ids/drop_places. A Drop needs at least 2 places.
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..")
PLACES = {
    "royal": dict(name="Royal Chalets and Restaurant", where="Bcharre & the Cedars", photo="royal/54-01", framed=True, scene="mountain", ids=[54],
                  facts=["A fireplace and mountain views", "6 bedrooms, up to 12 guests", "Near the ski slopes"], price="From $80 a night",
                  ar="شومينيه وتلج، ببشري والأرز", cap="fireplace and mountain views, 6 bedrooms for up to 12, near the ski slopes. From $80/night",
                  cap_ar="شومينيه ومنظر عالجبل، ٦ غرف نوم لحد ١٢ شخص، قريب من التلج. من ٨٠$ بالليلة",
                  reel=("Fireplace, up to 12 guests", "شومينيه، لحد ١٢ شخص", "$80 / night"), kw="CEDARS", ar_name="رويال شاليهات ومطعم، بشري والأرز"),
    "ghosta": dict(name="Ghosta Guest House", where="Above Jounieh · 25 min from Beirut", photo="ghosta/37-14", scene="mountain", ids=[37],
                   facts=["A 180° view from Beirut to Byblos", "5 bedrooms, up to 12 guests", "800 m above the sea"], price="From $220 a night",
                   ar="منظر من بيروت لجبيل، فوق جونية", cap="a 180° view from Beirut to Byblos, 5 bedrooms for up to 12, 25 min from Beirut. From $220/night",
                   cap_ar="منظر من بيروت لجبيل، ٥ غرف نوم لحد ١٢ شخص، ٢٥ دقيقة عن بيروت. من ٢٢٠$ بالليلة",
                   reel=("A 180° view, up to 12 guests", "منظر من بيروت لجبيل، لحد ١٢ شخص", "$220 / night"), kw="GHOSTA", ar_name="بيت ضيافة بغوسطا، فوق جونية"),
    "aqualand": dict(name="Aqualand Hotel & Resort", where="Batroun · 35 min from Beirut", photo="aqualand/24-02", scene="sea", ids=[18, 24, 25],
                     facts=["Sea views and beach access", "Rooms for 2", "Garden, heating and valet parking"], price="From $150 a night",
                     ar="منظر عالبحر وبحر عالباب، بالبترون", cap="sea views and beach access, rooms for 2, 35 min from Beirut. From $150/night",
                     cap_ar="منظر عالبحر ونزلة عالبحر، غرف لشخصين، ٣٥ دقيقة عن بيروت. من ١٥٠$ بالليلة",
                     reel=("Sea views and beach access", "منظر عالبحر ونزلة عالبحر", "$150 / night"), kw="BATROUN", ar_name="أكوالاند، البترون"),
    "majestic": dict(name="Majestic Byblos Grand Hotel", where="Byblos · Jbeil", photo="majestic/23-03", scene="sea", ids=[23, 45, 46, 47],
                     facts=["Private balcony, sea or city views", "Rooms for 2, family rooms for 4", "Day use from $65"], price="From $130 a night",
                     ar="بلكون خاص عالبحر، بجبيل", cap="a private balcony with sea or city views, rooms for 2 and family rooms for 4. From $130/night",
                     cap_ar="بلكون خاص بيطلّ عالبحر أو على جبيل، غرف لشخصين وغرف عيلة لـ٤. من ١٣٠$ بالليلة",
                     reel=("Private balcony, sea views", "بلكون خاص عالبحر", "$130 / night"), kw="BYBLOS", ar_name="فندق ماجستيك، جبيل"),
    "baabdat": dict(name="Bayt Baabdat", where="Metn · 15 min from Beirut", photo="baabdat/32-02", unbar=True, scene="mountain", ids=[32],
                    facts=["A fireplace, a garden and a barbecue", "2 bedrooms, up to 5 guests", "15 min from Beirut"], price="$80 a night · $100 Fri & Sat",
                    ar="شومينيه وجنينة، ١٥ دقيقة عن بيروت", cap="a fireplace, a garden and a barbecue, 2 bedrooms for up to 5, 15 min from Beirut. $100 on Fri & Sat",
                    cap_ar="شومينيه وجنينة ومنقل، غرفتين نوم لحد ٥ أشخاص، ١٥ دقيقة عن بيروت. ١٠٠$ الجمعة والسبت",
                    reel=("A fireplace, 15 min from Beirut", "شومينيه، ١٥ دقيقة عن بيروت", "$100 Fri & Sat"), kw="BAABDAT", ar_name="بيت بعبدات، المتن"),
    "acampar": dict(name="Acampar Faraya", where="Faraya · 45 min from Beirut", photo="acampar/42-02", scene="mountain", ids=[39, 40, 41, 42],
                    facts=["Wooden bungalows, most with a fireplace", "From 2 up to 6 guests", "Near the ski slopes"], price="From $80 a night",
                    ar="بنغلوهات خشب مع شومينيه بفاريا", cap="wooden bungalows near the ski slopes, most with a fireplace, for 2 to 6 guests, 45 min from Beirut. From $80/night",
                    cap_ar="بنغلوهات خشب قريبة من التلج، أغلبها فيها شومينيه، من شخصين لـ٦، ٤٥ دقيقة عن بيروت. من ٨٠$ بالليلة",
                    reel=("Fireplace bungalows, 2 to 6 guests", "بنغلوهات مع شومينيه، من ٢ لـ٦ أشخاص", "$80 / night"), kw="FARAYA", ar_name="Acampar، فاريا"),
    "legrey": dict(name="Le Grey Haven", where="Batroun · 45 min from Beirut", photo="legrey/48-05", scene="sea", ids=[48],
                   facts=["2 bedrooms, up to 4 guests", "Sea and mountain views", "Close to the beach, pubs and restaurants"], price="$80 a night",
                   ar="منظر عالبحر والجبل، بالبترون", cap="2 bedrooms for up to 4, sea and mountain views, close to the beach, 45 min from Beirut. $80/night",
                   cap_ar="غرفتين نوم لـ٤ أشخاص، منظر عالبحر والجبل، قريبة عالبحر، ٤٥ دقيقة عن بيروت. ٨٠$ بالليلة",
                   reel=("Sea and mountain views, up to 4", "منظر عالبحر والجبل، لحد ٤ أشخاص", "$80 / night"), kw="BATROUN", ar_name="Le Grey Haven، البترون"),
    "fvc": dict(name="Faraya Village Club", where="Faraya · Mzaar · 45 min from Beirut", photo="fvc/28-07", framed=True, scene="mountain", ids=[26, 27, 28],
                facts=["Chalets with a chimney", "A heated pool on site", "From 2 up to 7 guests"], price="From $150 a night",
                ar="شاليهات مع شومينيه ومسبح مدفّى", cap="chalets with a chimney and a heated pool on site, for 2 to 7 guests, 45 min from Beirut. From $150/night",
                cap_ar="شاليهات مع شومينيه ومسبح مدفّى، من شخصين لـ٧، ٤٥ دقيقة عن بيروت. من ١٥٠$ بالليلة",
                reel=("Chimney and a heated pool", "شومينيه ومسبح مدفّى", "$150 / night"), kw="FARAYA", ar_name="فاريا ڤيلادج كلوب، المزار"),
}
NUM_AR = "١٢٣"
CONF, CONF_AR = "Confirmed Thursday", "تأكّدنا الخميس"

def photo(p):
    im = Image.open(f"{ROOT}/reels/public/photos/{p['photo']}.webp").convert("RGB")
    return unbar(im) if p.get("unbar") else im

def build(folder, dates, dates_ar, keys):
    ps = [PLACES[k] for k in keys]; n = len(ps); OUT = f"{ROOT}/posts/{folder}"; OUTR = f"{OUT}-reel"
    os.makedirs(OUT, exist_ok=True); os.makedirs(OUTR, exist_ok=True)
    for f in glob.glob(f"{OUT}/drop-*.jpg"): os.remove(f)
    word = {2: "2", 3: "3"}[n]
    slide1(photo(ps[0]), f"{OUT}/drop-1.jpg", "The Friday Drop:", f"{word} places free this weekend", f"{CONF} · {dates}",
           f"{NUM_AR[n-1]} محلات فاضيين هالويكند", " · ".join(p["where"].split(" · ")[0] for p in ps), framed=ps[0].get("framed", False))
    for i, p in enumerate(ps, 1):
        place_slide(photo(p), f"{OUT}/drop-{i+1}.jpg", i, n, p["name"], p["where"], p["facts"], p["price"], p["ar"], tag=CONF)
    last(f"{OUT}/drop-{n+2}.jpg", None, f"{word} places confirmed free for {dates}", "ويكندكن بيبلش من هون", "DROP", head=("Your weekend", "starts here"))
    story(photo(ps[0]), f"{OUT}/story.jpg", "The Friday Drop:", f"{word} places free this weekend", f"{CONF} · {dates}",
          f"{NUM_AR[n-1]} محلات فاضيين هالويكند", "DROP", badge="The Friday Drop", box=("Want one of them?", "Reply DROP for the details"))
    en = "\n".join(f"{i}. {p['name']}, {p['where'].replace(' · ', ', ')}: {p['cap']}. {CONF} ✅" for i, p in enumerate(ps, 1))
    arl = "\n".join(f"{NUM_AR[i-1]}. {p['ar_name']}: {p['cap_ar']}. {CONF_AR} ✅" for i, p in enumerate(ps, 1))
    tail_en = ("Request your dates on WhatsApp, nothing to pay yet. Link in bio 📅\n"
               "👉 Follow @weekendna.lb so you don't miss the next one. We find a new place for your weekend every week 🏡")
    tail_ar = ("ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق. اللينك بالبايو 📅\n"
               "👉 تابعونا عـ@weekendna.lb كرمال ما يفوتكن المحل الجاي. كل أسبوع منلاقيلكن محل جديد لويكندكن 🏡")
    tags = "#Weekendna #TheFridayDrop #LebanonWeekend #Lebanon #WeekendInLebanon"
    cap = (f"The Friday Drop 🔥 {word} places free this weekend ({dates}), found for you. We checked with the owners on Thursday.\n"
           f"Found on Weekendna:\n{en}\n\n💬 Want one of them? Comment DROP and we'll check availability for you.\n\n{tail_en}\n\n"
           f"الـFriday Drop 🔥 {NUM_AR[n-1]} محلات فاضيين هالويكند ({dates_ar})، لقيناهن إلكن. تأكّدنا من أصحابهن يوم الخميس.\n"
           f"على Weekendna:\n{arl}\n\n💬 بدكن واحد منهن؟ اكتبوا DROP بالتعليق وبنتأكدلكن من التوفر.\n\n{tail_ar}\n\n{tags}\n")
    open(f"{OUT}/caption.txt", "w", encoding="utf-8").write(cap)
    capr = (f"Still free this weekend? These were 🔥 The Friday Drop recap: {word} places confirmed Thursday for {dates}.\n"
            f"Found on Weekendna:\n{en}\n\n💬 Want one of them? Comment DROP and we'll check availability for you.\n\n{tail_en}\n\n"
            f"ملخّص الـFriday Drop 🔥 {NUM_AR[n-1]} محلات تأكّدنا الخميس إنّن فاضيين ({dates_ar}).\n"
            f"على Weekendna:\n{arl}\n\n💬 بدكن واحد منهن؟ اكتبوا DROP بالتعليق وبنتأكدلكن من التوفر.\n\n{tail_ar}\n\n{tags}\n")
    open(f"{OUTR}/caption.txt", "w", encoding="utf-8").write(capr)
    # Friday Reel (oud, 129 bpm, 6 beats a shot, end 8 beats)
    bpm = 129; sec = lambda b: round(b * 60 / bpm + 0.3, 3)
    shots = [{"photo": f"photos/{ps[0]['photo']}.webp", "seconds": sec(6), "move": "zoom_in", "framed": ps[0].get("framed", False),
              "text": {"type": "hook", "en": f"The Friday Drop: {word} places free this weekend", "ar": f"{NUM_AR[n-1]} محلات فاضيين هالويكند"}}]
    moves = ["pan_right", "zoom_out", "pan_left"]
    for i, p in enumerate(ps):
        shots.append({"photo": f"photos/{p['photo']}.webp", "seconds": sec(6), "move": moves[i % 3], "framed": p.get("framed", False),
                      "text": {"type": "room", "name": f"{CONF} · {p['where'].split(' · ')[0]}", "en": f"{p['name']}: {p['reel'][0]}",
                               "ar": p["reel"][1], "price": p["reel"][2]}})
    shots.append({"photo": f"photos/{ps[-1]['photo']}.webp", "seconds": sec(8), "move": "zoom_out", "framed": ps[-1].get("framed", False),
                  "text": {"type": "end", "name": "The Friday Drop", "price": dates, "ar": "ابعتوا تواريخكن عالواتساب"}})
    json.dump({"music": "music/oud-alexmorgan.mp3", "musicStart": 12, "bpm": bpm, "shots": shots}, open(f"{OUTR}/reel-remotion.json", "w"), ensure_ascii=False, indent=1)
    # Friday story sequence (plain images: the API can't add poll or link stickers)
    sea = next((p for p in ps if p["scene"] == "sea"), ps[0]); mtn = next((p for p in ps if p["scene"] == "mountain"), ps[-1])
    story(photo(sea), f"{OUTR}/story-1.jpg", "Sea or mountain", "this weekend?", "Tell us and we'll send you a place", "بحر أو جبل هالويكند؟",
          badge="The Friday Drop", box=("Sea or mountain?", "Comment or DM SEA or MOUNTAIN"))
    story(photo(mtn), f"{OUTR}/story-2.jpg", f"{mtn['name'].split(' and ')[0]},", "free this weekend", f"{CONF} · {mtn['price']}", mtn["ar"],
          badge=CONF, box=("Want this place?", f"Reply {mtn['kw']} for the details"))
    story(photo(ps[1 % n]), f"{OUTR}/story-3.jpg", "How many", "are you?", "Send your group size, we'll send options", "قدّيش عددكن؟ ابعتولنا",
          badge="The Friday Drop", box=("Send your group size", "and we'll send you options"))
    story(photo(ps[-1]), f"{OUTR}/story-4.jpg", "Request your dates", "on WhatsApp", "Nothing to pay yet · weekendna.com", "ابعتوا تواريخكن عالواتساب",
          badge="Found on Weekendna", box=("Nothing to pay yet", "Link in bio"))
    return [i for p in ps for i in p["ids"]]

if __name__ == "__main__":
    folder, dates, dates_ar, *keys = sys.argv[1:]
    print("listing_ids:", build(folder, dates, dates_ar, keys))
