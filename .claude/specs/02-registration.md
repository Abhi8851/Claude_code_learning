# Spec: Registration

## Overview
This feature implements account creation for Spendly. The `/register` page already
exists as a static template with a form, but the backend does not yet process
submissions. This step wires up `POST /register` so a visitor can create a real
account: validating input, preventing duplicate emails, hashing the password, and
storing a new row in the `users` table. It does not implement login sessions or
authentication state — that is a later step (`/logout` is still explicitly a
placeholder for "Step 3").

## Depends on
- Step 1 — Database setup (`database/db.py`: `get_db()`, `init_db()`, users table
  with `name`, `email`, `password_hash`). Must already be complete.

## Routes
- `GET /register` — renders the registration form — public (already exists, unchanged)
- `POST /register` — validates submitted name/email/password, creates the user
  record if valid, otherwise re-renders the form with an error — public

## Database changes
No database changes. The `users` table created in Step 1
(`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) already supports
this feature. `POST /register` will use parameterised `INSERT` and rely on the
existing `UNIQUE` constraint on `email`.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — repopulate the `name` and `email`
  input `value` attributes from the submitted form data when re-rendering after
  a validation error, so the user doesn't have to retype them. The password
  field is left blank on error.

## Files to change
- `app.py` — change the `register` view to accept `GET` and `POST`:
  - On `POST`, read `name`, `email`, `password` from the form
  - Validate: all fields present, password is at least 8 characters
  - Check for an existing user with the same email via `get_db()`
  - On any validation failure or duplicate email, re-render `register.html`
    with an `error` message and the submitted `name`/`email`
  - On success, hash the password with `werkzeug.security.generate_password_hash`,
    insert the new user, and redirect to `/login`
- `templates/register.html` — add sticky `value` attributes for `name` and `email`

## Files to create
None

## New dependencies
No new dependencies — `werkzeug.security` is already used in `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`), never stored or logged in plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Check for duplicate email before inserting, not by relying only on the `UNIQUE` constraint exception
- Do not implement login/session logic in this step — redirect to `/login` and stop there

## Definition of done
- [ ] `GET /register` still renders the form with no errors
- [ ] Submitting valid name/email/password creates a new row in `users` with a hashed password (verify with a DB query — the stored value is not the plaintext password)
- [ ] Submitting an email that already exists re-renders `register.html` with an error and does not create a duplicate row
- [ ] Submitting with a missing name, email, or password re-renders the form with an error
- [ ] Submitting a password shorter than 8 characters re-renders the form with an error
- [ ] After a validation error, the previously entered name and email are still shown in the form
- [ ] A successful registration redirects to `/login`
- [ ] The app starts and runs without errors (`python app.py`)
