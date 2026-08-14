import datetime
import json
import platform
import re
import subprocess
import sys
import urllib.parse
import urllib.request

NOTES = []


def speak(text, silent=False):
    print("assistant:", text)
    if silent:
        return
    try:
        if platform.system() == "Darwin":
            subprocess.run(["say", text], check=False, timeout=30)
        else:
            import pyttsx3
            eng = pyttsx3.init()
            eng.say(text)
            eng.runAndWait()
    except Exception:  # noqa: BLE001 - TTS is best-effort
        pass


# ---------------- skills ----------------
def skill_time(q):
    if re.search(r"\btime\b", q):
        return datetime.datetime.now().strftime("It's %I:%M %p.")
    if re.search(r"\b(date|day|today)\b", q):
        return datetime.datetime.now().strftime("Today is %A, %B %d, %Y.")


def skill_math(q):
    m = re.search(r"(-?\d+\.?\d*)\s*(plus|\+|minus|-|times|x|\*|divided by|/)"
                  r"\s*(-?\d+\.?\d*)", q)
    if not m:
        return None
    a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
    ops = {"plus": a + b, "+": a + b, "minus": a - b, "-": a - b,
           "times": a * b, "x": a * b, "*": a * b}
    if op in ("divided by", "/"):
        return "Cannot divide by zero." if b == 0 else f"That's {a / b:g}."
    return f"That's {ops[op]:g}."


def skill_convert(q):
    m = re.search(r"(-?\d+\.?\d*)\s*(km|kilometers?|miles?|kg|kilograms?|"
                  r"pounds?|lbs?|celsius|c\b|fahrenheit|f\b)\s*"
                  r"(?:to|in|into)\s*(km|kilometers?|miles?|kg|kilograms?|"
                  r"pounds?|lbs?|celsius|c\b|fahrenheit|f\b)", q)
    if not m:
        return None
    v, src, dst = float(m.group(1)), m.group(2)[0], m.group(3)[0]
    table = {("k", "m"): v * 0.621371, ("m", "k"): v / 0.621371,
             ("p", "k"): v * 0.453592, ("l", "k"): v * 0.453592,
             ("c", "f"): v * 9 / 5 + 32, ("f", "c"): (v - 32) * 5 / 9}
    if src in "kK" and dst in "pl":
        return f"That's {v / 0.453592:.2f} pounds."
    r = table.get((src, dst))
    return f"That's {r:.2f}." if r is not None else None


def skill_wikipedia(q):
    m = re.search(r"(?:who is|what is|tell me about|search for)\s+(.+)", q)
    if not m:
        return None
    topic = m.group(1).strip("?. ")
    url = ("https://en.wikipedia.org/api/rest_v1/page/summary/"
           + urllib.parse.quote(topic))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "va/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            summary = json.load(r).get("extract", "")
        if summary:
            return summary.split(". ")[0] + "."
    except Exception:  # noqa: BLE001 - offline or page missing
        return f"I couldn't reach Wikipedia to look up {topic}."


def skill_notes(q):
    m = re.search(r"(?:remember|note)(?: that)?\s+(.+)", q)
    if m:
        NOTES.append(m.group(1))
        return "Noted."
    if "my notes" in q or "what did i" in q:
        return ("Your notes: " + "; ".join(NOTES)) if NOTES \
            else "You have no notes yet."


def skill_joke(q):
    if "joke" in q:
        return ("I told my computer I needed a break, "
                "and it said: no problem, I'll go to sleep.")


SKILLS = [skill_time, skill_math, skill_convert, skill_notes, skill_joke,
          skill_wikipedia]


def answer(q):
    q = q.lower().strip()
    if re.fullmatch(r"(hi|hello|hey)[!. ]*", q):
        return "Hello! Ask me the time, math, conversions, or anything else."
    for skill in SKILLS:
        r = skill(q)
        if r:
            return r
    return "I don't have a skill for that yet — try 'what is <topic>'."


def listen():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        print("listening...")
        audio = r.listen(mic, timeout=6)
    return r.recognize_google(audio)


def main():
    silent = "--silent" in sys.argv
    if "--demo" in sys.argv:
        for q in ["hello", "what time is it", "25 times 4",
                  "100 km to miles", "remember buy milk", "what are my notes",
                  "who is Alan Turing"]:
            print("you:", q)
            speak(answer(q), silent=True)
        return
    voice = "--voice" in sys.argv
    print("Assistant ready (Ctrl-C to quit).")
    while True:
        try:
            q = listen() if voice else input("you: ")
        except KeyboardInterrupt:
            break
        except Exception as e:  # noqa: BLE001 - mic/recognition errors
            print("(voice error:", e, "— falling back to typing)")
            voice = False
            continue
        if q.lower() in ("quit", "exit", "bye"):
            speak("Goodbye!", silent)
            break
        speak(answer(q), silent)


if __name__ == "__main__":
    main()
