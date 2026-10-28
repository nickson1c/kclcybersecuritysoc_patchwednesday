# patch wednesday

last week you broke things. this week you fix them.

this is a small members-portal web app with five **deliberate security bugs**
in it. your job is the blue-team side: find each bug, understand why it's a
problem, and **patch it properly**, not just block the one input you were shown.

a fix counts when the tests pass. each bug has two kinds of test:

- an **exploit test** that fails while the bug is there, and
- **normal-use tests** that check the feature still works.

so deleting the feature doesn't count, and neither does a blocklist of "bad
characters": the exploit tests try several versions of the same trick.

---

## what you need

- a **github account**
- **git** ([git-scm.com/downloads](https://git-scm.com/downloads), on windows
  the default installer options are fine)
- an editor. vs code is good, but anything works.

you **don't** need python to take part: github runs the tests for you every time
you push. if you do have python and want to run things on your laptop, see
[running it locally](#running-it-locally-optional) at the bottom.

## 1. get your own copy

1. click the green **use this template** button at the top of this page, then
   **create a new repository**. give it any name and keep it **public**.
2. on your new repo, click the green **code** button and copy the https link.
3. in a terminal (on windows: **git bash**, which came with git):

```
git clone <the link you copied>
cd <your repo name>
```

open the folder in your editor.

## 2. see what's broken

on your repo's page on github, open the **actions** tab. your first run has a
**red cross**: that's normal, because the bugs are still in there. click the
run, then **pytest**, and you'll see five failing tests, one per bug.

no run there yet? click **tests** on the left, then **run workflow**.

## 3. the loop

1. pick a bug from the table below and open its file in `challenges/`. the top
   of each file explains the bug and points at the function to fix.
2. fix that one function.
3. ship it:

```
git add .
git commit -m "fix the notes ownership check"
git push
```

4. go back to the **actions** tab. a new run starts within a few seconds. one
   less failure means that fix worked. **all green = every bug patched.**

if github asks you to log in when you push, sign in through the browser window
that pops up.

> **before you commit**, run `git diff` to read exactly what you changed.
> **broke something?** `git restore <file>` puts a file back to your last commit.

## the bugs

top is easiest.

| file | what's wrong |
|---|---|
| `challenges/login.py` | the login query is built from what you type (we fix this one together) |
| `challenges/notes.py` | you can read other people's notes by changing the number in the url |
| `challenges/files.py` | the download can be tricked into reading files outside its folder |
| `challenges/tools.py` | *(bonus)* the host box can run extra commands |
| `challenges/redirect_after_login.py` | *(bonus)* the `?next=` redirect can send you to another site |

## running it locally (optional)

needs **python 3.10+** ([python.org](https://www.python.org/downloads/); on
windows, tick **add python to path** in the installer).

**windows (powershell):**

```
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
python app.py
```

if powershell says running scripts is disabled, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

**mac / linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
python app.py
```

`python app.py` serves the app at http://127.0.0.1:5000 (users: `alice` /
`alpaca`, `bob` / `bonobo`). on windows, one bonus test is skipped locally because
`cmd.exe` uses different shell syntax. github actions still grades it, so trust
the tick there.

## what you'll pick up

- the git loop: clone, change, diff, commit, push
- how automated tests decide whether a change is good enough to ship
- why a real fix beats a blocklist, and five kinds of web bug you'll see
  everywhere: sql injection, idor, path traversal, command injection and open
  redirects

made for kcl cyber security society · [kclcybersoc.org.uk](https://kclcybersoc.org.uk)
