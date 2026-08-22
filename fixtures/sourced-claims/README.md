# A workspace whose claims are sourced

The counterpart of `../broken-workspace`. Every absolute claim here carries a citation and every
citation resolves, so `scripts/lint-claims --all` must report **zero** findings over it.

It exists because a rule nobody can satisfy is not a rule. The must-fail fixture proves
`lint-claims` can fail; this one proves it can be passed, by prose a person would actually write.
Change either and change `scripts/check` in the same commit.
