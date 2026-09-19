# Work Card 05 — Submit Complaint Form

## Goal

Build complaint submission page with category dropdown, location input, description textarea, image upload with preview, and server-side file handling.

## Inputs

- `build-blueprint.md` (Student Routes, Implementation Rules)
- `architecture.md` (File Uploads, Student Routes)
- `design.md` (Component Style - Forms, Inputs, File Upload, Mobile Rules)

## Files likely touched

- `app.py` — `/submit` GET/POST route, file upload helper
- `templates/student/submit.html` — new
- `static/js/main.js` — image preview functionality
- `static/css/style.css` — form styles, upload zone, preview

## Instructions for the coding agent

1. Add helper function in `app.py` (before routes):
   ```python
   import os
   import uuid
   from werkzeug.utils import secure_filename
   from PIL import Image

   def allowed_file(filename):
       return '.' in filename and \
              filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

   def save_complaint_image(file):
       if not file or not allowed_file(file.filename):
           return None
       # Verify MIME type
       file.seek(0)
       try:
           img = Image.open(file)
           img.verify()
           file.seek(0)
       except Exception:
           return None
       # Generate secure filename
       ext = file.filename.rsplit('.', 1)[1].lower()
       filename = f"{uuid.uuid4().hex}.{ext}"
       filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
       file.save(filepath)
       return f"uploads/complaints/{filename}"
   ```

2. Add `/submit` route in `app.py`:
   - `@app.route('/submit', methods=['GET', 'POST'])` with `@login_required` + `@student_required`
   - GET: render form with categories list
   - POST: validate all fields
     - category required, must be in CATEGORIES
     - location required, ≤ 200 chars
     - description required, ≥ 20 chars
     - image optional, if provided: validate via `save_complaint_image()`, flash error if invalid
   - On success: create Complaint, flash success, redirect to `/complaints`
   - On error: re-render form with submitted values + error messages

3. Create `templates/student/submit.html` extending `student/base.html`:
   - Page title: "Submit Complaint"
   - Form in centered card (max-width 720px)
   - Fields:
     - Category: `<select>` with all CATEGORIES, required
     - Location: `<input type="text">` placeholder "e.g., Building A, Room 101", required
     - Description: `<textarea rows="5">` placeholder "Describe the issue in detail...", required, minlength 20
     - Image Upload: drag-drop zone with `<input type="file" accept="image/png,image/jpeg,image/webp">`, preview area (hidden until file selected)
   - Submit button: Primary, full-width on mobile
   - Cancel button: Secondary, links to `/dashboard`
   - Client-side: show image preview on file select (JS)

4. Add JS in `static/js/main.js`:
   ```javascript
   // Image preview for complaint submit
   document.addEventListener('DOMContentLoaded', () => {
       const fileInput = document.getElementById('complaint-image');
       const preview = document.getElementById('image-preview');
       const previewImg = document.getElementById('preview-img');
       const removeBtn = document.getElementById('remove-image');

       if (fileInput) {
           fileInput.addEventListener('change', (e) => {
               const file = e.target.files[0];
               if (file) {
                   const reader = new FileReader();
                   reader.onload = (e) => {
                       previewImg.src = e.target.result;
                       preview.classList.remove('d-none');
                   };
                   reader.readAsDataURL(file);
               }
           });
       }
       if (removeBtn) {
           removeBtn.addEventListener('click', () => {
               fileInput.value = '';
               preview.classList.add('d-none');
               previewImg.src = '';
           });
       }
   });
   ```

5. Add CSS in `static/css/style.css`:
   - `.upload-zone` — dashed border, padding, center text, hover state, drag-over state
   - `.upload-zone.drag-over` — primary background, border color
   - `#image-preview` — max-width 200px, border-radius, margin-top
   - Form validation styles (invalid feedback)
   - Mobile: form fields stack, buttons full-width

## What not to do

- Do not implement my complaints list yet
- Do not implement complaint detail yet
- Do not add multiple image upload (single only for V1)
- Do not add client-side validation beyond preview (server-side is source of truth)

## Done when

- Student navigates to `/submit` → sees form with all fields
- Category dropdown populated with 11 categories
- Image upload shows preview on file select
- Submit with valid data → complaint created, image saved to `static/uploads/complaints/`, redirect to `/complaints` with flash success
- Submit with missing/invalid data → form re-renders with values preserved, error messages shown
- Invalid file type/size → error flash, form re-renders
- Mobile: form usable, upload zone works, preview visible

## Verification steps

- [ ] `/submit` GET renders form with category dropdown (11 options), location, description, image upload
- [ ] Image preview appears on file select, remove button clears it
- [ ] POST with valid data creates Complaint in DB, image saved to `static/uploads/complaints/{uuid}.ext`
- [ ] POST redirects to `/complaints` with flash success
- [ ] POST with empty category → error "Category is required"
- [ ] POST with empty location → error "Location is required"
- [ ] POST with description < 20 chars → error "Description must be at least 20 characters"
- [ ] POST with invalid file type (e.g., .pdf) → error "Invalid file type. Allowed: PNG, JPG, JPEG, WebP"
- [ ] POST with file > 5MB → error "File size exceeds 5MB limit" (Flask MAX_CONTENT_LENGTH)
- [ ] Form preserves entered values on validation error
- [ ] Mobile: form fields full-width, upload zone tappable, preview visible
- [ ] Navbar "Submit Complaint" highlighted active

**Design check:** Form follows design.md — single column, 20px gap, labels above inputs (14px, 500 weight), required asterisk red, primary button full-width mobile, upload zone dashed border with hover/drag states, preview thumbnail 200px max, focus rings on all inputs.

## Localhost test before continuing

After this card, the learner should test:

- Start `python app.py`
- Login as student → go to `/submit`
- Fill form: select category, enter location, write description (>20 chars), select image (PNG/JPG/WebP <5MB)
- Submit → verify redirect to `/complaints` (404 expected) with green flash message
- Check `static/uploads/complaints/` — file exists with UUID name
- Try submit with empty fields → verify errors show, values preserved
- Try upload .txt file → verify error
- Mobile view: form stacks, upload zone works, preview shows

If all tests pass, reply `continue`.
If anything fails, reply `fix` and paste the error or describe what you see.

## Stop condition

If file upload fails (permission, path, MIME validation), stop and fix `save_complaint_image()` and upload folder permissions before continuing.

## Status

Not started