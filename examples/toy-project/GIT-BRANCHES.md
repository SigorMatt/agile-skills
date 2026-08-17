# Git branches, and each item's code history

`git log --grep <ITEM-ID>` is what Definition of Done D8 requires to reconstruct an
item's code history. This file is that command's output, per item, from the real run
repository.

## Branches

```text
main  f16aa0f  tracker: close EP-001 with all seven success measures re-run (refs EP-001)
wi/BUG-0001  15a0216  tracker: the review, the closed item, and the merge (refs BUG-0001)
wi/BUG-0002  c9f3498  tracker: the review, the closed item, and the merge (refs BUG-0002)
wi/BUG-0003  6f7917e  tracker: the review, the closed item, and the merge (refs BUG-0003)
wi/WI-0001  461e37f  tracker: the review, the closed item, and the merge (refs WI-0001)
wi/WI-0002  6201e33  tracker: the review, the closed item, and the merge (refs WI-0002)
wi/WI-0003  035b169  tracker: the review, the closed item, and the merge (refs WI-0003)
```

## BUG-0001

```text
$ git log --grep BUG-0001 --oneline --all
15a0216 tracker: the review, the closed item, and the merge (refs BUG-0001)
5743c3e tracker: the verification report and the ticked criteria (refs BUG-0001)
4bf2cba tracker: Q-002 answered, AC6 scoped to the tests that assert new behaviour (refs BUG-0001)
cbd6768 tracker: the implementation report, Q-002, and this item's record (refs BUG-0001)
06fc185 linecount: ignore an entry that cannot be resolved instead of aborting (refs BUG-0001)
f520c2d tracker: restamp the pre-clamp history row and record the correction (refs BUG-0001)
9030bb3 tracker: Q-001 answered; skewed timestamps corrected where correction is legitimate (refs BUG-0001)
5e7cb98 tracker: correct this execution's journal entry order (refs BUG-0001)
915cc78 tracker: Q-001 on the clock disagreement that invalidates the history (refs BUG-0001)
301bc72 tracker: the plan, ADR-0006, and overview v3 (refs BUG-0001)
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
```

## BUG-0002

```text
$ git log --grep BUG-0002 --oneline --all
c9f3498 tracker: the review, the closed item, and the merge (refs BUG-0002)
ee29341 tracker: the verification report and the ticked criteria (refs BUG-0002)
e1e2985 tracker: the implementation report and this item's record (refs BUG-0002)
277c89c linecount: say when a folder's files were all skipped instead of no files (refs BUG-0002)
558eaaa tracker: the plan and ADR-0007 (refs BUG-0002)
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
```

## BUG-0003

```text
$ git log --grep BUG-0003 --oneline --all
6f7917e tracker: the review, the closed item, and the merge (refs BUG-0003)
9be6142 tracker: Q-001 answered; ADR-0008 corrected to v2 (refs BUG-0003)
e11341e tracker: the verification report, Q-001, and the ticked criteria (refs BUG-0003)
21d583d tracker: the implementation report and this item's record (refs BUG-0003)
8634781 linecount: write the report as bytes so an undecodable name prints (refs BUG-0003)
f1b7524 tracker: the plan, ADR-0008, and overview v4 (refs BUG-0003)
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
```

## EP-001

```text
$ git log --grep EP-001 --oneline --all
f16aa0f tracker: close EP-001 with all seven success measures re-run (refs EP-001)
7073bca tracker: reopen EP-001 and create WI-0003 for --sort (refs EP-001)
0fc856b tracker: the epic closed a second time against its success measures (refs EP-001)
df475d5 tracker: Q-001 answered and EP-001 reopened for the three bugs (refs EP-001)
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
6d1e437 tracker: the epic closed against its success measures (refs EP-001)
3b41d56 tracker: the refined item and its Q&A record (refs WI-0001)
```

## WI-0001

```text
$ git log --grep WI-0001 --oneline --all
035b169 tracker: the review, the closed item, and the merge (refs WI-0003)
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
461e37f tracker: the review, the closed item, and the merge (refs WI-0001)
d41a046 tracker: the review and the record of a gate that refuses every exit (refs WI-0001)
4635eb9 tracker: the verification report and the ticked criteria (refs WI-0001)
7d86345 tracker: the implementation report and this item's record (refs WI-0001)
86f4384 tests: end-to-end coverage of every acceptance criterion (refs WI-0001)
5adc619 linecount: count lines per file and print them largest first (refs WI-0001)
f09a938 tracker: the plan, three ADRs, and the architecture overview (refs WI-0001)
711039e tracker: the refined item and its Q&A record (refs WI-0002)
3b41d56 tracker: the refined item and its Q&A record (refs WI-0001)
```

## WI-0002

```text
$ git log --grep WI-0002 --oneline --all
a95b1be tracker: the independent regression report, three bug items, and Q-001 (refs EP-001)
6201e33 tracker: the review, the closed item, and the merge (refs WI-0002)
37a9324 tracker: the verification report and the ticked criteria (refs WI-0002)
b2d851c tracker: Q-001 answered, AC10's example corrected, plan updated (refs WI-0002)
3687ebb tracker: the implementation report, Q-001, and this item's record (refs WI-0002)
abc7c66 linecount: add --top N, limiting the rows but not the total (refs WI-0002)
4825e16 tracker: the plan, ADR-0004, ADR-0005, and overview v2 (refs WI-0002)
711039e tracker: the refined item and its Q&A record (refs WI-0002)
3b41d56 tracker: the refined item and its Q&A record (refs WI-0001)
```

## WI-0003

```text
$ git log --grep WI-0003 --oneline --all
035b169 tracker: the review, the closed item, and the merge (refs WI-0003)
383e35d tracker: Q-001 answered; vision v3 records --sort as delivered (refs WI-0003)
821eaef tracker: Q-001 filed, D7 blocks closing until the vision is updated (refs WI-0003)
b6c7414 tracker: the verification report and the ticked criteria (refs WI-0003)
8792e41 tracker: the implementation report and this item's record (refs WI-0003)
214dc3d linecount: add --sort to order the rows by name or by count (refs WI-0003)
4b02d9b tracker: the plan, ADR-0009, and overview v5 (refs WI-0003)
2cf8fa1 tracker: the refined item and its Q&A record (refs WI-0003)
7073bca tracker: reopen EP-001 and create WI-0003 for --sort (refs EP-001)
```

