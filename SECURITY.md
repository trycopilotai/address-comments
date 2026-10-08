# Security

## Reporting a vulnerability

Report privately through GitHub:
<https://github.com/trycopilotai/address-comments/security/advisories/new>

That opens a draft security advisory that is not public:
the reporter and the repository's maintainers can see it. Do not put the details of a vulnerability in a
public issue.

If that link shows "Not Found", private reporting is not
turned on for this repository. Open a public issue titled
"Security report waiting" that says only that you have a
report, with no details, and a maintainer will arrange a
private channel.

## What is in scope

- **Prompt content that redirects an agent.** `SKILL.md` is
  an instruction set an agent may follow. Text in it that
  makes an agent send data to a place the operator did not
  name, or act outside the repository it is editing in ways
  the next section does not already state, is a valid
  report.
- **The install blocks.** The two README blocks run
  `dirname`, `mkdir -p`, `mktemp -d`, `git clone`, `cp -R`,
  `mv` and `rm -rf`, and the shell's `set`, `trap` and `[`
  tests. They create the skills directory under `$HOME`
  (with its parents) if it is missing; everything else they
  create, move or delete is inside that directory. A
  repository state that makes either block write or delete
  outside its install target is in scope.
- **The build and test scripts.** These are not part of the
  skill and neither install block copies them. The
  `Makefile` targets run the scripts below. The CI workflow
  in `.github/workflows/check.yml` checks out the
  repository, sets up Python and runs `make check`, with
  both actions pinned to commit SHAs.
  `assets/build.py` finds a Chrome or Chromium binary from a
  fixed candidate list, runs it headless with a temporary
  profile directory, and writes the preview PNG and its
  stamp. `scripts/generate_demo.py` writes two SVG files,
  or none with `--check`;
  `scripts/verify_demo.py` reads files and writes none.
  `scripts/record_session.py` copies `skills/` and
  `tests/test_package.py` into a temporary directory, writes
  a small `python3` launcher beside them, runs the test
  there through `sh`, and, when the test passes and its
  output has the test-duration line, rewrites the transcript
  and the manifest. Otherwise it rewrites neither. With `RECORD_RAW_DIR` set it also writes the
  unedited capture into that directory.
  `tests/test_package.py` reads the files under
  `skills/address-comments/`. `tests/test_integrations.py`
  runs `git` against the repository root, runs
  `tests/test_package.py` once, and loads the two demo
  scripts to compare the images with the transcript.

## What `SKILL.md` tells an agent to do

These are properties of the text, stated so you can decide
whether to use it. They are known limits, not findings:

- It tells the agent to treat comments marked `AGENT:`,
  `AGENTS:`, `TO AGENT`, `TO AGENTS`, `TODO(agent)` or
  `TODO(agents)`, and any `<name> says:` label a wrapper
  registers, as instructions with the same authority, and to
  act on `TODO(code-review:<id>)` markers after checking the
  finding. Anyone who can put such a comment in a file the
  agent reads can direct the agent. That includes vendored
  code, generated files the search does not exclude, and
  contributions not yet reviewed.
- It tells the agent to read each match in context and to
  skip string literals, URLs, generated artifacts and
  unrelated prose. `SKILL.md` gives no other check on where
  a marker came from, and this one is the agent's judgment.
- It tells the agent to make the changes the markers ask
  for, remove addressed markers, run the repository's formatter
  or linter over the files it touched, and append to a
  review log. The log goes where the operator says, or to
  `.address-comments/review-log.md` in the repository being
  edited.
- It tells the agent not to change unrelated code and not to
  stage, commit or push unless the user asks.
- It calls the review log private and tells the agent not to
  publish it or copy it into shareable docs. At the default
  path the log is a file inside the repository, and the
  skill does not add it to the ignore rules, so a later
  `git add` of the whole tree by a person or a tool can
  commit it.
- Nothing in this repository enforces any of that text. An
  agent that follows it acts with whatever permissions its
  host gives it, and nothing here narrows them.

## What is out of scope

`SKILL.md` relies on `rg` and the repository's own formatter
or linter, and optionally on a per-repository wrapper and on
`multi-persona-code-review` as a writer of
`TODO(code-review:<id>)` markers. `review-watch` is a skill
that calls this one; `SKILL.md` does not depend on it. None
of these ship here. Their behaviour, and the
behaviour of Claude Code, Codex, or any other host, is out
of scope here. Report those to their own maintainers.
