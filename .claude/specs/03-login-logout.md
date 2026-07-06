# Spec: Login and Logout

## Overview
This feature implements session-based authentication for Spendly. `GET /login`
already renders a form, but `POST /login` doesn't exist yet, and `/logout` is a
placeholder string. This step wires up real sign-in: verify submitted
credentials against the `users` table, start a Flask session on success, reflect
logged-in state in the shared nav (`base.html`), and let `/logout` clear the
session. It does not implement the `/profile` page or protect any expense
routes — those remain explicit placeholders for later steps.

## Depends on
- Step 1 — Database setup (`users` table with `email`, `password_hash`)
- Step 2 — Registration (there must be a way to create a user with a real
  password hash to log in with)

## Routes
- `GET /login` — renders the login form — public (already exists, unchanged)
- `POST /login` — validates submitted email/password against `users`, starts a
  session on success, otherwise re-renders the form with an error — public
- `GET /logout` — clears the session and redirects to `/login` — public
  (harmless no-op if no one is logged in)

## Database changes
No database changes. The existing `users` table (`email`, `password_hash`) is
sufficient to verify credentials with
`werkzeug.security.check_password_hash`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — repopulate the `email` input's `value` from the
    submitted form data when re-rendering after a validation error (password
    field stays blank, same convention as registration)
  - `templates/base.html` — nav links become conditional on session state: show
    the logged-in user's name + a "Logout" link when `session` has a user,
    otherwise show the existing "Sign in" / "Get started" links

## Files to change
- `app.py`:
  - Set `app.secret_key` (required for Flask sessions to work at all)
  - Change `login` view to accept `GET` and `POST`:
    - `GET` → unchanged, renders `login.html`
    - `POST` → read `email`/`password`, look up the user by email, verify the
      password with `check_password_hash`, and:
      - on success: store `session["user_id"]` and `session["user_name"]`,
        redirect to `/`
      - on failure (no such email, or wrong password): re-render
        `login.html` with one generic error (don't reveal whether the email
        or the password was wrong) and the submitted `email`
      - on missing email/password: re-render with an error, same as above
  - Change `logout` view: clear the session (`session.clear()`) and redirect
    to `/login` instead of returning a placeholder string
- `templates/login.html` — sticky `value` attribute on the email input
- `templates/base.html` — conditional nav block based on `session`
- `static/css/style.css` — small addition for a `.nav-user` style (reuse
  existing CSS variables, e.g. `color: var(--ink-muted)`) to display the
  logged-in user's name next to the Logout link

## Files to create
None

## New dependencies
No new dependencies — Flask's built-in session support and
`werkzeug.security.check_password_hash` are already available.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash` — never
  compare plaintext passwords
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use one generic error message for any login failure (wrong email or wrong
  password) — do not reveal which one was incorrect
- Do not implement `/profile` or add login-required protection to any other
  route in this step — those are later steps
- Session is the only auth mechanism needed here — no "remember me", no
  separate auth tokens

## Definition of done
- [ ] `GET /login` still renders the form with no errors
- [ ] Logging in with a correct email/password (e.g. the seeded demo user)
      redirects to `/` and the nav shows the logged-in state
- [ ] Logging in with a wrong password re-renders `login.html` with a generic
      error and does not start a session
- [ ] Logging in with an email that doesn't exist re-renders with the same
      generic error (no hint that the account doesn't exist)
- [ ] Submitting with a missing email or password re-renders the form with an
      error
- [ ] After a login error, the previously entered email is still shown in the
      form
- [ ] Visiting `/logout` while logged in clears the session, redirects to
      `/login`, and the nav reverts to the logged-out state
- [ ] Session persists across requests (e.g. reload the landing page while
      logged in and the nav still shows the logged-in state)
- [ ] The app starts and runs without errors (`python app.py`)
