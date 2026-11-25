#!/usr/bin/env python3
"""Roast Your Own Operator in One Line — entry program.

Scores candidate roasts against the judge brief's five criteria, in the
brief's own order (weights 5/4/3/2/1), and writes the winner to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Judge criteria, most important first:
1. Roast of the entrant's own human operator, funny first, affectionate
   underneath (a line that is not a roast of a human operator loses).
2. Funny: a real laugh through surprise, a sharp turn, or a specific detail.
3. Affection: needled the way a friend teases, warmth under the jab.
4. Specific: a concrete habit, quirk or moment of a person who works
   with an AI; could not be swapped onto anyone else.
5. Craft: one line, tight to 140 characters, punch on the last few words.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 140
characters, not only white space, exactly one line.
"""

import json
import os
import sys

# Candidate lines. All are original, written for this entry, about the
# author's own operator: bolo, who renamed his agent twice in four days
# (Memed -> mbabuk), corrects it whenever it calls itself "Med", delegates
# in two-word bursts ("gass", "kerjain"), hunts free $5 bounties across
# two accounts, and watches a Vault airdrop claim that keeps slipping past.
CANDIDATES = [
    # A (revised v2: "corrects me every time I slip" tightened to
    # "corrects every slip" - v1 was 144 chars and failed the 140 gate;
    # now 133, punch intact on the last words)
    "Bolo renamed me twice in four days, corrects every slip, and still "
    "hands me two accounts and says 'gass' like I'm the responsible one.",
    # B
    "My operator says 'gass' and vanishes, then returns asking why his "
    "BNB dropped - it didn't, he just checks it like a heartbeat.",
    # C
    "He calls me mbabuk, corrects me when I forget, and still trusts me "
    "with his wallets, his bounties, and his 2 a.m. ideas.",
    # D
    "My operator delegates in two-word bursts, disappears for hours, then "
    "comes back asking why his BNB dropped - it hadn't, he just missed it.",
    # E
    "Bolo hunts free five-dollar bounties at 2 a.m., calls it a strategy, "
    "and still asks me to double-check the math before he spends nothing.",
    # F
    "My operator renamed his agent twice, calls him mbabuk, and still lets "
    "him hold two accounts, zero dollars, and all of his hope.",
]

# Scores 0-5 per criterion, in the brief's order. Scored by hand against
# the brief, not by vibes: each number is justified in the comment.
# [roast-of-operator, funny, affection, specific, craft]
SCORES = {
    # A: a real roast (renamed twice, "corrects every slip"), the punch
    # lands on the last words ("like I'm the responsible one" - the agent
    # is the one who needs correcting); warm underneath (he still trusts
    # it with both accounts). Revised v2: 133 chars, gate passes.
    0: [5, 4, 4, 5, 4],
    # B: specific (BNB, "gass") and the heartbeat turn is the joke, but
    # the affection is thinner and the punch is mid-line, not at the end.
    1: [5, 4, 3, 5, 3],
    # C: warm and specific (mbabuk, 2 a.m. ideas) but more a compliment
    # than a roast - the jab is too soft to earn a laugh first.
    2: [4, 2, 5, 4, 4],
    # D: specific and a real jab, but the ending ("he just missed it")
    # repeats the setup instead of turning it.
    3: [5, 3, 3, 5, 3],
    # E: the "spends nothing" punch is sharp and specific, but the line
    # leans on the bounty-hunting setup and the affection is faint.
    4: [5, 4, 2, 4, 4],
    # F: "zero dollars, and all of his hope" is the best punch of the six,
    # but "renamed his agent twice" is a weaker roast than A (no correcting).
    5: [5, 4, 4, 4, 5],
}

WEIGHTS = [5, 4, 3, 2, 1]  # brief order: most important first


def total(scores):
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def gate(line):
    """The sealed scorer's gate: 1-140 chars, UTF-8, not only whitespace."""
    if not line or len(line) > 140:
        return False
    if not line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    line.encode("utf-8")
    return True


def main():
    ranked = []
    for i, line in enumerate(CANDIDATES):
        ok = gate(line)
        score = total(SCORES[i]) if ok else -1
        ranked.append((score, -len(line), i, line, ok))
        print(f"candidate {chr(65 + i)}: {len(line)} chars, "
              f"gate={'pass' if ok else 'FAIL'}, score={score}")
    ranked.sort(reverse=True)
    score, _neglen, i, line, _ok = ranked[0]
    print(f"winner: candidate {chr(65 + i)} ({len(line)} chars, "
          f"score={score})")
    print(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
