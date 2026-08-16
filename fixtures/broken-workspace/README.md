# Deliberately broken workspace

Every file here is wrong on purpose. `scripts/check` runs `scripts/validate-workspace` against
this tree and asserts that the set of finding codes it produces equals `EXPECTED-CODES.txt`
exactly — so a rule that silently stops firing fails the build, which is the failure mode a
validator is most prone to and least likely to notice.

Do not "fix" anything here. To change what is covered, change the fixture *and*
`EXPECTED-CODES.txt` in the same commit, and say why in the commit message.
