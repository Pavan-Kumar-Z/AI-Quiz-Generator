# Frontend Testing Checklist

## Pre-Testing Setup
- [ ] Backend server running on http://localhost:5000
- [ ] Frontend opened in browser
- [ ] Browser console open (F12)
- [ ] No console errors on load

## File Upload Tests
- [ ] Browse button opens file selector
- [ ] Can upload TXT file
- [ ] Can upload PDF file (when implemented)
- [ ] Can upload DOCX file (when implemented)
- [ ] Drag and drop works
- [ ] Drag over shows visual feedback
- [ ] Invalid file types rejected
- [ ] Files >10MB rejected
- [ ] File info displays correctly
- [ ] Remove file button works

## Settings Tests
- [ ] Radio buttons switch correctly
- [ ] MCQ mode selected by default
- [ ] Q&A mode selectable
- [ ] Slider moves smoothly
- [ ] Slider value updates in real-time
- [ ] Slider range is 5-20
- [ ] Difficulty dropdown works
- [ ] All three difficulty levels selectable

## Quiz Generation Tests
- [ ] Generate button disabled when no file
- [ ] Generate button enabled after upload
- [ ] Progress bar appears on click
- [ ] Progress messages update
- [ ] Progress bar fills to 100%
- [ ] Quiz appears after generation
- [ ] MCQ format displays correctly
- [ ] Q&A format displays correctly
- [ ] Question numbering correct
- [ ] All questions display

## Quiz Display Tests
- [ ] Questions are readable
- [ ] MCQ options labeled A, B, C, D
- [ ] Q&A answers hidden by default
- [ ] Toggle answers button works
- [ ] Show answers displays correctly
- [ ] Green highlight on correct answers
- [ ] Explanations display (MCQ)
- [ ] Hide answers works
- [ ] Scroll to quiz after generation

## Download Tests
- [ ] Download button appears after generation
- [ ] Click shows placeholder message
- [ ] No errors in console

## UI/UX Tests
- [ ] Instructions toggle works
- [ ] Instructions expand/collapse smoothly
- [ ] Arrow rotates on toggle
- [ ] Status messages appear
- [ ] Success messages auto-hide (5s)
- [ ] Error messages stay visible
- [ ] Close button works on status
- [ ] Hover effects work on buttons
- [ ] Button animations smooth

## Responsive Design Tests
- [ ] Desktop layout correct (>1200px)
- [ ] Tablet layout correct (768-1200px)
- [ ] Mobile layout correct (<768px)
- [ ] No horizontal scroll
- [ ] Touch targets adequate (mobile)
- [ ] Text readable on all sizes

## Browser Compatibility
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile browsers

## Performance Tests
- [ ] Page loads quickly (<2s)
- [ ] File upload responsive
- [ ] Quiz generation smooth
- [ ] No lag on interactions
- [ ] Animations smooth (60fps)

## Error Handling Tests
- [ ] Backend offline shows error
- [ ] Invalid file shows error
- [ ] Large file shows error
- [ ] API errors handled gracefully
- [ ] No uncaught exceptions

## Accessibility Tests
- [ ] Keyboard navigation works
- [ ] Tab order logical
- [ ] Focus indicators visible
- [ ] Color contrast adequate
- [ ] Screen reader friendly (basic)

## Final Checks
- [ ] No console errors
- [ ] No console warnings
- [ ] All features work end-to-end
- [ ] User flow intuitive
- [ ] Design consistent