---
title: Using recall
version: 9
status: current
updated: 2026-08-30T05:28:48Z
updated-by: implement
updated-for: BUG-0001
---

# Using `recall`

This is the whole of what you need to build up a deck and read it back. Everything on this page
works from a checkout with nothing installed but Python 3 [src: ADR-0003].

## The one setup step

Add the checkout's `bin` directory to your `PATH` [src: ADR-0005]:

```
export PATH="$PWD/bin:$PATH"
```

There is no install step, no virtual environment and no package to fetch [src: ADR-0005]. Put
that line in your shell's startup file if you would rather not type it each time. If you would
rather not touch `PATH` at all, `python3 -m recall` from the checkout takes the same subcommands
[src: ADR-0005].

## Adding a card

A card has two sides — the question you will be shown, and the answer you are trying to recall:

```
recall add --question "capital of France" --answer "Paris"
```

Both sides are required, and neither may be blank or only spaces and tabs. If one is missing the
command says which one, changes nothing, and exits non-zero [src: WI-0001 AC2].

The same question may be added twice. Two cards with the same prompt and different senses is a
normal thing to want in a vocabulary deck, so `recall` does not deduplicate and does not refuse
[src: WI-0001 AC9].

## Reading the deck back

```
recall list
```

One line per card [src: tracker/items/WI-0001/artifacts/plan.md], in the order they were added
[src: ADR-0004], each side shown exactly as you typed it [src: WI-0001 AC3]. With no cards yet, it
says the deck is empty and exits successfully — that is not an error [src: WI-0001 AC6].

## Doing a review

```
recall review
```

A sitting shows you the cards you are due to see today, one at a time. For each one it prints
the question side and waits; press return and it shows you the answer; then it asks whether you
got it right. **The two answers it recognises are `y` for right and `n` for wrong**
[src: tracker/items/WI-0002/artifacts/plan.md] — two of them, and no scale in between
[src: ADR-0002]. Capital letters and surrounding spaces are fine.
Type anything else and it tells you what it expected and asks you about the same card again
[src: WI-0002 AC3].

Due means the card's next-review date is today **or earlier**, so a day you miss does not drop
a card out of the schedule — it is simply waiting for you next time [src: WI-0002 AC13]. A card
you add today is due today, so you can try recalling it straight away [src: WI-0002 AC12].

The sitting shows you **everything** that is due, however big the pile, with no cap on it and
no timer [src: WI-0002 AC11]. If it is more than you want in one go, stop
part-way: the answers you have already given are written down as you give them, so nothing you
have done is lost [src: WI-0002 AC9]. Press `Ctrl-D` at either prompt to stop.

When nothing is due, the sitting says so and stops:

```
Nothing is due today. Come back tomorrow.
```

That is not an error — it exits successfully [src: WI-0002 AC5]. You will see the same line if
you have no deck yet, because a deck you have not started is a deck with nothing due in it
[src: ADR-0004; WI-0002 AC6]. A sitting never creates the deck file.

If the deck file exists but cannot be read, `review` refuses in exactly the way `add` and `list`
do — see below. It will not start you a fresh sitting on an empty deck [src: WI-0002 AC7].

As soon as you answer a card, the sitting tells you when you will next see it
[src: ADR-0007; WI-0003 AC4]:

```
capital of France
  [press return to see the answer]
  Paris
  did you get it right? [y/n] y
  next review: 2026-09-06 (in 7 days)
```

That line appears for every card you grade, for a wrong answer as well as a right one
[src: ADR-0007]. The date it names is the one written into the deck file for that card
[src: WI-0003 AC4]. There is no tally or summary at the end of a sitting [src: ADR-0007].

## When each card comes back

Getting a card right pushes it further away; getting it wrong brings it straight back. The gaps
are **1 day, then 3 days, then a week, then 30 days**, and a card that keeps being recalled
correctly stays at 30 days — the gap never grows past a month, and there is no rung above it
[src: ADR-0002; WI-0003 AC1].

Get a card wrong and it goes back to the start of the ladder: it is due again the day after the
sitting, and the *next* time you get it right it moves one day out again rather than a month
[src: ADR-0002; WI-0003 AC2]. Nothing about how well you did on it before is kept — going back to
the start is the whole of what a wrong answer does [src: ADR-0002].

Both gaps are counted **from the day of the sitting**, never from the day the card was due. If
you miss a fortnight, the cards waiting for you are scheduled from the day you actually sit down
with them, so nothing ends up stranded behind today's date [src: ADR-0002; WI-0003 AC3].

Worked through, a card added on day 0 and answered right every time is due on days
**0, 1, 4, 11, 41, 71 and 101** [src: ADR-0002; WI-0003 AC5] — you can check the tool against that
by hand. A card answered wrong on any sitting is due the day after that sitting, whichever of
those days it was on [src: ADR-0002].

Nothing else shows you the schedule. `recall list` prints `question | answer` and no dates
[src: ADR-0007; WI-0001 AC3]; the sitting's line is the whole of it, and there is no way to tune
the gaps [src: WI-0003].

## Deleting a card

```
recall delete --question "capital of France"
```

You say which card you mean by typing its question side, **exactly** as `recall list` shows it —
same capitals, same spaces, nothing shortened [src: WI-0004/Q-001; WI-0004 AC4]. There is no card
number and no code to quote; the listing is unchanged by this command [src: WI-0004 AC12].

It shows you both sides of the card and asks before it removes anything:

```
capital of France
  Paris
delete this card? [y/n] y
Deleted. The deck now holds 2 card(s).
```

Only `y` goes through with it — capital letters and surrounding spaces are fine, as at a
sitting's prompt. Anything else — `n`, a word it does not recognise, an empty line, or `Ctrl-D` —
leaves the deck exactly as it was, says on standard output that the card was not deleted, and
exits successfully [src: WI-0004 AC6; ADR-0009]. Unlike a sitting, which re-asks until it
understands you, the question is put **once**: here doing nothing is the safe answer, and you can
simply run the command again [src: ADR-0009]. There is no flag that skips the prompt
[src: WI-0004/Q-002].

If what you type matches no card, nothing is removed and the command exits non-zero
[src: WI-0004 AC4]. If it matches **two**, nothing is removed either: `recall` says how many
matched rather than guessing which one you meant [src: WI-0004 AC5; WI-0004/Q-001]. Two cards may
share a question side [src: WI-0001 AC9], and removing one of such a pair means editing the deck
file by hand [src: tracker/items/WI-0004/item.md].

Deleting the last card in the deck leaves an empty deck rather than a broken one: `recall list`
then says the deck is empty, and `recall add` starts it again [src: WI-0004 AC10].

With no deck yet, `recall delete` reports that no card has that question and creates nothing — a
deletion never writes a deck file into existence [src: WI-0004 AC9]. If the deck file exists but
cannot be read, `delete` refuses in exactly the way `add`, `list` and `review` do — see [what
happens if that file gets damaged](#what-happens-if-that-file-gets-damaged) — and removes nothing
[src: WI-0004 AC8].

**There is no undo.** Nothing is kept aside, and a deleted card cannot be brought back except
from a copy of the deck file you made yourself [src: tracker/items/WI-0004/item.md]. That is why
it asks.

## Where the deck is kept

```
~/.local/share/recall/deck.json
```

One file, under your home directory, holding the whole deck [src: ADR-0004]. It is not under
`/tmp` or any other directory the system clears at boot, so it is still there after a reboot
[src: WI-0001 AC7]. Its location is fixed: there is no flag, no environment variable and no
configuration file for pointing `recall` at a different deck [src: ADR-0004].

It is ordinary JSON. You can read it, copy it, put it in a backup, or open it in an editor
[src: ADR-0004].

## What happens if that file gets damaged

`recall` will not repair it and will not replace it. If the file exists but cannot be read as a
deck, `add`, `list`, `review` and `delete` all say so, name the file, and stop without writing
anything — the file's bytes are left exactly as they were
[src: ADR-0004; WI-0001 AC8; WI-0002 AC7; WI-0004 AC8]:

```
recall: cannot read the deck file /home/you/.local/share/recall/deck.json -- it is not valid
JSON (Expecting property name enclosed in double quotes, line 1). Nothing has been written and
the file is exactly as it was. Move it aside or repair it by hand, then run recall again.
```

Repairing it is your call, not the tool's, because the alternative is a tool that quietly starts
you a fresh empty deck and loses everything you had. Writes go through a temporary file and an
atomic rename, so an interrupted `add` leaves the previous deck whole rather than a truncated one
[src: ADR-0004].

The same holds when the *file system* is what refuses, rather than the file being damaged — the
folder is not writable, the folder cannot be read at all, or something is sitting where the deck
file or its folder belongs. Every subcommand names the deck file, says whether it could not be
**read** or could not be **written**, writes nothing, and exits non-zero
[src: BUG-0001 AC1; BUG-0001 AC2; ADR-0010]:

```
recall: cannot write the deck file /home/you/.local/share/recall/deck.json -- permission
denied. Nothing has been written and the deck file is exactly as it was before this attempt.
Put that right, then run recall again.
```

When what is in the way is not the deck file itself but a folder on the path to it, the message
names *that* instead, because that is the thing you have to move [src: BUG-0001 AC3]:

```
recall: cannot read the deck file /home/you/.local/share/recall/deck.json --
/home/you/.local/share/recall is not a directory, and the deck's directory has to be one.
```

A deck you have not started yet is still not an error — only a missing file, or a missing folder
on the way to it, counts as "no deck yet" [src: ADR-0004; ADR-0010]. A *file* where
`~/.local/share/recall` should be is a different thing entirely, and `recall list` says so rather
than telling you your deck is empty [src: BUG-0001 AC3].

## What this version does not do yet

The ladder above is fixed. There is no way to change the four gaps, to set an interval for one
card, or to reschedule a pile of cards at once [src: WI-0003].

If you hand-edit the deck file and give a card a `rung` that is not a position on the ladder,
`recall` refuses to read the deck and names the card, in exactly the way it refuses a damaged one
above — it will not guess what you meant and will not quietly reschedule the card
[src: ADR-0008; ADR-0004].

Editing a card is out of scope for this epic [src: tracker/items/WI-0001/item.md], so changing
a card's wording means deleting it and adding it again — which restarts its schedule, because an
added card starts at the bottom of the ladder and is due today [src: recall/deck.py; ADR-0002].
There is no way to delete more than one card at once, and no way to empty the deck in one command
[src: tracker/items/WI-0004/item.md]. There is no summary or tally at the end of a sitting, and no
streaks or statistics anywhere [src: docs/product/vision.md]. Nothing keeps a
record of past sittings: the deck file holds how the *last* one went and no more
[src: ADR-0006].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 9 | 2026-08-30T05:28:48Z | implement | BUG-0001 | Added the folder that cannot be *read* to the list of file-system refusals the page already covered. The sentence claimed every subcommand names the deck file and exits non-zero when the file system refuses; a deck folder at mode `000` produced a traceback instead, so the claim was false for that case until this execution fixed `store._refusal` (`verify-report.md`, D1) |
| 8 | 2026-08-30T05:13:11Z | implement | BUG-0001 | Extended "What happens if that file gets damaged" to the case where the file system refuses the deck rather than the deck being malformed: that every subcommand names the deck file, says whether it could not be read or written, writes nothing and exits non-zero; that a folder in the way is named instead of the deck file; and that a *file* where `~/.local/share/recall` belongs is now reported rather than shown as an empty deck |
| 7 | 2026-08-30T04:56:43Z | review-close | WI-0004 | No claim changed: re-wrapped two lines version 6 left at 160 and 115 characters, back inside the width every other line in the file keeps |
| 6 | 2026-08-30T04:46:40Z | implement | WI-0004 | Added "Deleting a card": naming a card by typing its question side exactly, the confirmation that only `y` answers and that is asked once, the two refusals (no card matches, two cards match), that the last card leaving an empty deck is normal, that a deletion never creates a deck file, and that there is no undo. Corrected two claims this item made false: the damaged-deck paragraph named three subcommands and there are now four, and "What this version does not do yet" listed deleting a card as future work |
| 5 | 2026-08-30T04:12:00Z | implement | WI-0003 | Added "When each card comes back" - the gaps 1, 3, 7 and 30 days, that the gap holds at 30, that a wrong answer returns the card to the start, that a gap counts from the day of the sitting even when the card is overdue, and the worked example (days 0, 1, 4, 11, 41, 71, 101). Added the next-review line a sitting now prints after each answer. Rewrote "What this version does not do yet", which said scheduling was unbuilt and that a reviewed card comes back tomorrow whatever you answered - both false as of this item |
| 4 | 2026-08-30T03:08:20Z | implement | WI-0002 | Corrected the scheduling paragraph in "What this version does not do yet". It said a reviewed card's answer carries forward, cited to `ADR-0006`, which does not say that and which the code does not do: `record_answer` leaves `rung` untouched. Replaced with what is true - the answer is stored, nothing reads it back, and every card is still on the bottom rung (review.md finding F1) |
| 3 | 2026-08-30T02:50:52Z | implement | WI-0002 | Added "Doing a review": the two recognised responses `y` and `n`, the nothing-due message, that a sitting has no cap and may be stopped part-way, and what due means. Rewrote "What this version does not do yet", which said reviewing was unbuilt |
| 2 | 2026-08-30T02:12:00Z | review-close | WI-0001 | Split the `recall list` paragraph's citation: the sentence made four claims and cited the source for one. All four were verified against the code during review; only the citation was wrong |
| 1 | 2026-08-30T02:05:00Z | implement | WI-0001 | First version: the setup step, add, list, where the deck is kept, and what happens when it is damaged |
