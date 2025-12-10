# Submission Screenshots — Application Functionality (BREAD)

This folder groups the screenshots that demonstrate the front-end performing BREAD operations (Browse, Read, Edit, Add, Delete).

Files recorded during Playwright E2E runs are in `e2e_screenshots/` — below are the recommended images to include with your submission.

- Create (Add):
  - `e2e_screenshots/1765343188_after_create.png`
  - `e2e_screenshots/1765343267_after_create.png`
  - `e2e_screenshots/1765343375_after_create.png`

- Browse (List):
  - `e2e_screenshots/04_dashboard_after_registration.png` (dashboard showing calculations list)
  - `e2e_screenshots/1765343187_dashboard_after_register.png`

- Edit (Update):
  - `e2e_screenshots/1765343189_after_edit.png`
  - `e2e_screenshots/1765343269_after_edit.png`
  - `e2e_screenshots/1765343377_after_edit.png`

- Delete (Remove):
  - `e2e_screenshots/1765343270_after_delete.png`
  - `e2e_screenshots/1765343377_after_delete.png`

How to view locally
-------------------

Open a single image with Preview (macOS):

```bash
open e2e_screenshots/1765343188_after_create.png
```

Or serve the directory and browse the index:

```bash
python -m http.server 8001 --directory e2e_screenshots
# then open http://127.0.0.1:8001 in your browser
```

If you'd like, I can copy the chosen screenshots into `submission_screenshots/` and commit them (or create a ZIP) so they're grouped for upload. Say "copy screenshots" and I'll move the selected files and push the change.
