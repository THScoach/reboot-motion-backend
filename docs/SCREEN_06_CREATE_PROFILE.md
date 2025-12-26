# Screen 06: Create Profile

**Screen Name**: Create Profile  
**Route**: `/profile/create`  
**Complexity**: MEDIUM (Form with validation)  
**Priority**: P0 (Critical Path)

---

## 📐 Layout Overview

```
┌───────────────────────────────┐
│  ⬅️ Back                       │ ← Header
├───────────────────────────────┤
│                               │
│  Create Your Profile          │ ← Heading-01
│                               │
│  Tell us about yourself       │ ← Body-02
│  to personalize your          │
│  training experience.         │
│                               │
│  [Name]                       │ ← Input
│  ┌─────────────────────────┐ │
│  │ John Smith              │ │
│  └─────────────────────────┘ │
│                               │
│  [Age]                        │
│  ┌──────┐                    │
│  │  24  │  years             │
│  └──────┘                    │
│                               │
│  [Height]                     │
│  ┌──────┐  ┌──────┐          │
│  │  6   │' │  2   │"         │
│  └──────┘  └──────┘          │
│                               │
│  [Weight]                     │
│  ┌──────┐                    │
│  │ 185  │  lbs               │
│  └──────┘                    │
│                               │
│  [Wingspan] (Optional)        │
│  ┌──────┐  ┌──────┐          │
│  │  6   │' │  4   │"         │
│  └──────┘  └──────┘          │
│                               │
│  [Continue]                   │ ← Primary button
│                               │
└───────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Header
```css
display: flex;
align-items: center;
padding: 16px 24px;
background: #FFFFFF;
border-bottom: 1px solid #E5E7EB; /* Gray-200 */
```

**Back Button**:
```css
display: flex;
align-items: center;
gap: 8px;
color: #6B7280; /* Gray-500 */
font-size: 16px;
cursor: pointer;
```

### Form Container
```css
max-width: 480px;
margin: 0 auto;
padding: 32px 24px;
background: #FAFAFA; /* Gray-50 */
min-height: calc(100vh - 64px);
```

### Heading
```css
font-family: 'Inter', sans-serif;
font-weight: 600; /* Semibold */
font-size: 32px;
line-height: 40px;
color: #111827; /* Gray-900 */
margin-bottom: 12px;
```

### Subheading
```css
font-family: 'Inter', sans-serif;
font-weight: 400; /* Regular */
font-size: 16px;
line-height: 24px;
color: #6B7280; /* Gray-500 */
margin-bottom: 32px;
```

### Form Group
```css
margin-bottom: 24px;
```

**Label**:
```css
display: block;
font-family: 'Inter', sans-serif;
font-weight: 500; /* Medium */
font-size: 14px;
line-height: 20px;
color: #374151; /* Gray-700 */
margin-bottom: 8px;
```

**Input**:
```css
width: 100%;
height: 48px;
padding: 12px 16px;
background: #FFFFFF;
border: 1px solid #D1D5DB; /* Gray-300 */
border-radius: 8px;
font-family: 'Inter', sans-serif;
font-size: 16px;
color: #111827; /* Gray-900 */
transition: all 200ms ease;
```

**Input Focus**:
```css
border-color: #06B6D4; /* Electric Cyan */
outline: none;
box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
```

**Input Error**:
```css
border-color: #EF4444; /* Error Red */
```

**Error Message**:
```css
display: block;
font-size: 14px;
color: #EF4444; /* Error Red */
margin-top: 6px;
```

### Number Input (Age, Weight)
```css
max-width: 120px;
display: inline-block;
```

**Unit Label** (years, lbs):
```css
display: inline-block;
margin-left: 8px;
color: #6B7280; /* Gray-500 */
font-size: 16px;
```

### Height/Wingspan Input (Feet + Inches)
```css
display: flex;
gap: 12px;
align-items: center;
```

**Feet Input**:
```css
max-width: 80px;
```

**Inches Input**:
```css
max-width: 80px;
```

**Unit Labels** (', "):
```css
display: inline-block;
margin-left: 4px;
color: #6B7280; /* Gray-500 */
font-size: 16px;
```

### Optional Label
```css
font-size: 12px;
color: #9CA3AF; /* Gray-400 */
margin-left: 8px;
font-weight: 400;
```

### Continue Button
```css
width: 100%;
height: 48px;
background: #06B6D4; /* Electric Cyan */
color: #FFFFFF;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
border: none;
cursor: pointer;
margin-top: 32px;
transition: background 200ms ease;
```

**Disabled**:
```css
background: #D1D5DB; /* Gray-300 */
cursor: not-allowed;
```

---

## 📋 Form Fields

### 1. Name (Required)
- **Type**: Text input
- **Placeholder**: "Enter your full name"
- **Validation**: 
  - Min 2 characters
  - Max 50 characters
  - Letters, spaces, hyphens, apostrophes only
- **Error Messages**:
  - "Name is required"
  - "Name must be at least 2 characters"
  - "Name can only contain letters, spaces, and hyphens"

### 2. Age (Required)
- **Type**: Number input
- **Placeholder**: "24"
- **Unit**: "years"
- **Validation**:
  - Min 10 years
  - Max 100 years
  - Integer only
- **Error Messages**:
  - "Age is required"
  - "Age must be between 10 and 100"

### 3. Height (Required)
- **Type**: Two number inputs (feet + inches)
- **Feet**: 3-8 feet
- **Inches**: 0-11 inches
- **Validation**:
  - Both required
  - Valid ranges
- **Error Messages**:
  - "Height is required"
  - "Feet must be between 3 and 8"
  - "Inches must be between 0 and 11"

### 4. Weight (Required)
- **Type**: Number input
- **Placeholder**: "185"
- **Unit**: "lbs"
- **Validation**:
  - Min 50 lbs
  - Max 500 lbs
  - Integer only
- **Error Messages**:
  - "Weight is required"
  - "Weight must be between 50 and 500 lbs"

### 5. Wingspan (Optional)
- **Type**: Two number inputs (feet + inches)
- **Feet**: 3-9 feet
- **Inches**: 0-11 inches
- **Validation**: 
  - If provided, must be valid
  - Can be left empty
- **Error Messages**:
  - "Feet must be between 3 and 9"
  - "Inches must be between 0 and 11"

---

## ✅ Validation Rules

### Real-time Validation
- Validate on blur (when user leaves field)
- Show error messages immediately
- Clear errors when user starts typing

### Submit Validation
- Check all required fields
- Validate all field values
- Show first error field
- Focus on first error

### Form State
```typescript
interface ProfileForm {
  name: string;
  age: number;
  heightFeet: number;
  heightInches: number;
  weightLbs: number;
  wingspanFeet?: number;
  wingspanInches?: number;
}

interface FormErrors {
  name?: string;
  age?: string;
  heightFeet?: string;
  heightInches?: string;
  weightLbs?: string;
  wingspanFeet?: string;
  wingspanInches?: string;
}
```

---

## 🔄 Form Submission

### Submit Flow
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  // Validate
  const errors = validateForm(formData);
  if (Object.keys(errors).length > 0) {
    setFormErrors(errors);
    // Focus first error field
    return;
  }
  
  // Save to Supabase
  setIsSubmitting(true);
  try {
    const profile = await createUserProfile({
      name: formData.name,
      age: formData.age,
      height_inches: formData.heightFeet * 12 + formData.heightInches,
      weight_lbs: formData.weightLbs,
      wingspan_inches: formData.wingspanFeet 
        ? formData.wingspanFeet * 12 + formData.wingspanInches
        : null,
    });
    
    // Navigate to next screen
    router.push('/home');
    
    // Track analytics
    analytics.track('Profile Created', {
      age: formData.age,
      height_inches: profile.height_inches,
      has_wingspan: !!formData.wingspanFeet,
    });
  } catch (error) {
    setFormErrors({ submit: 'Failed to create profile. Please try again.' });
  } finally {
    setIsSubmitting(false);
  }
};
```

---

## 📱 Responsive Behavior

### Mobile (< 768px)
- Full-width inputs
- Stacked form groups
- Padding: 24px

### Tablet (768px - 1023px)
- Max-width: 480px (centered)
- Padding: 32px

### Desktop (1024px+)
- Max-width: 480px (centered)
- Padding: 40px

---

## ♿ Accessibility

### Form Labels
```html
<label htmlFor="name">
  Name <span className="required" aria-label="required">*</span>
</label>
<input 
  id="name"
  name="name"
  type="text"
  aria-required="true"
  aria-invalid={!!errors.name}
  aria-describedby={errors.name ? "name-error" : undefined}
/>
{errors.name && (
  <span id="name-error" role="alert" className="error">
    {errors.name}
  </span>
)}
```

### Keyboard Navigation
- **Tab**: Navigate through inputs
- **Shift+Tab**: Navigate backwards
- **Enter**: Submit form (when valid)

### Screen Reader
- Labels associated with inputs
- Error messages announced
- Required fields indicated
- Invalid fields announced

---

## 🎬 Animations

### Input Focus
```css
transition: border-color 200ms ease, box-shadow 200ms ease;
```

### Error Message
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.error {
  animation: fadeIn 200ms ease;
}
```

---

## 📊 Analytics Events

```typescript
// Form viewed
analytics.track('Create Profile Viewed');

// Field interaction
analytics.track('Profile Field Focused', {
  field: string,
});

// Validation error
analytics.track('Profile Validation Error', {
  field: string,
  error: string,
});

// Form submitted
analytics.track('Profile Created', {
  age: number,
  height_inches: number,
  weight_lbs: number,
  has_wingspan: boolean,
});
```

---

## 🎯 Success Metrics

### Completion Rate
- **Target**: > 90% complete profile
- **Benchmark**: < 10% drop-off

### Time to Complete
- **Target**: 60-120 seconds
- **Median**: ~90 seconds

### Error Rate
- **Target**: < 20% encounter validation errors
- **Most Common**: Age, height validation

---

## 🔍 Testing Checklist

- [ ] All inputs render correctly
- [ ] Real-time validation works
- [ ] Error messages display
- [ ] Required fields enforced
- [ ] Submit validation works
- [ ] Form submits to Supabase
- [ ] Navigation works (back, success)
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Keyboard accessible
- [ ] Screen reader announces
- [ ] Focus indicators visible
- [ ] Analytics events fire

---

## ✅ Definition of Done

- [ ] Form layout implemented
- [ ] All inputs functional
- [ ] Real-time validation works
- [ ] Submit validation works
- [ ] Error handling implemented
- [ ] Supabase integration
- [ ] Navigation logic
- [ ] Responsive design
- [ ] Keyboard accessible
- [ ] Screen reader accessible
- [ ] Analytics integrated
- [ ] No console errors

---

**Priority**: P0 (Critical Path)  
**Complexity**: MEDIUM (Form with validation)  
**Estimated Dev Time**: 6-8 hours (Phase 1)

**Dependencies**:
- Supabase profile table
- Form validation library (React Hook Form)
- Analytics setup

---

*Last Updated: December 27, 2025*  
*Screen Specification v1.0*
