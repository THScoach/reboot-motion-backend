# 🎨 Catching Barrels - Design System

**Version:** 1.0  
**Last Updated:** December 26, 2025  
**Designer:** Builder 2

---

## 🎯 Design Philosophy

**"Clean Athletic Professional"**

Inspired by Apple Health, Whoop, and Strava, our design prioritizes:
- **Clarity:** Data-first, no visual clutter
- **Performance:** Feels fast and responsive
- **Professional:** Tool for athletes and coaches, not a game
- **Accessible:** WCAG AA compliant

---

## 🎨 Color Palette

### **Background Colors**
```css
--bg-primary: #FAFAFA;      /* Light gray background */
--bg-secondary: #FFFFFF;    /* White cards */
--bg-tertiary: #F5F5F7;     /* Subtle sections */
```

### **Primary Accent (KRS Brand Color)**
```css
--accent-primary: #06B6D4;  /* Electric cyan */
--accent-hover: #0891B2;    /* Darker cyan */
--accent-light: #CFFAFE;    /* Light cyan tint */
```

### **4B Framework Colors (Subtle Tints)**
```css
/* Brain - Purple */
--brain-bg: #EDE9FE;        /* Light purple background */
--brain-text: #7C3AED;      /* Dark purple text */
--brain-icon: #A78BFA;      /* Medium purple icon */

/* Body - Blue */
--body-bg: #DBEAFE;         /* Light blue background */
--body-text: #2563EB;       /* Dark blue text */
--body-icon: #60A5FA;       /* Medium blue icon */

/* Bat - Green */
--bat-bg: #D1FAE5;          /* Light green background */
--bat-text: #059669;        /* Dark green text */
--bat-icon: #34D399;        /* Medium green icon */

/* Ball - Red */
--ball-bg: #FEE2E2;         /* Light red background */
--ball-text: #DC2626;       /* Dark red text */
--ball-icon: #F87171;       /* Medium red icon */
```

### **Semantic Colors**
```css
--success: #10B981;         /* Green */
--warning: #F59E0B;         /* Amber */
--error: #EF4444;           /* Red */
--info: #3B82F6;            /* Blue */
```

### **Text Colors**
```css
--text-primary: #1F2937;    /* Almost black */
--text-secondary: #6B7280;  /* Gray */
--text-tertiary: #9CA3AF;   /* Light gray */
--text-inverse: #FFFFFF;    /* White (on dark backgrounds) */
```

### **Border Colors**
```css
--border-light: #E5E7EB;    /* Light gray */
--border-medium: #D1D5DB;   /* Medium gray */
--border-dark: #9CA3AF;     /* Dark gray */
```

---

## ✍️ Typography

### **Font Family**
```css
--font-primary: 'Inter', system-ui, -apple-system, sans-serif;
```

**Why Inter?**
- Excellent readability at all sizes
- Tabular figures for numbers
- Open-source and free
- Designed for screens

### **Type Scale (1.25 ratio)**
```css
--text-xs: 0.75rem;    /* 12px - Captions, labels */
--text-sm: 0.875rem;   /* 14px - Secondary text */
--text-base: 1rem;     /* 16px - Body text */
--text-lg: 1.125rem;   /* 18px - Large body */
--text-xl: 1.25rem;    /* 20px - Small headings */
--text-2xl: 1.5rem;    /* 24px - Section headings */
--text-3xl: 1.875rem;  /* 30px - Page headings */
--text-4xl: 2.25rem;   /* 36px - Hero text */
--text-5xl: 3rem;      /* 48px - Display text (KRS score) */
```

### **Font Weights**
```css
--font-regular: 400;    /* Body text */
--font-medium: 500;     /* Emphasis */
--font-semibold: 600;   /* Headings, buttons */
--font-bold: 700;       /* Strong emphasis */
```

### **Line Heights**
```css
--leading-tight: 1.25;  /* Headings */
--leading-snug: 1.375;  /* Large body text */
--leading-normal: 1.5;  /* Body text */
--leading-relaxed: 1.625; /* Long-form content */
```

### **Usage Examples**
```html
<!-- Page Heading -->
<h1 class="text-3xl font-bold text-primary">Your Swing Report</h1>

<!-- Section Heading -->
<h2 class="text-2xl font-semibold text-primary">4B Framework</h2>

<!-- Body Text -->
<p class="text-base text-secondary">Your creation score improved 5 points...</p>

<!-- Caption -->
<span class="text-xs text-tertiary">Updated 2 hours ago</span>

<!-- Display Number (KRS Score) -->
<div class="text-5xl font-bold text-accent">82</div>
```

---

## 📏 Spacing System

### **Base Unit: 4px**
```css
--space-0: 0;           /* 0px */
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
```

### **Usage Guidelines**
- **Card padding:** `space-6` (24px) or `space-8` (32px)
- **Section spacing:** `space-8` (32px) or `space-12` (48px)
- **Component spacing:** `space-4` (16px) minimum
- **Icon margins:** `space-2` (8px) or `space-3` (12px)
- **Page margins:** `space-4` (16px) on mobile, `space-6` (24px) on desktop

---

## 🔲 Border Radius

```css
--radius-sm: 8px;      /* Small elements (badges, pills) */
--radius-md: 12px;     /* Standard cards, buttons */
--radius-lg: 16px;     /* Large cards, modals */
--radius-xl: 24px;     /* Hero sections */
--radius-full: 9999px; /* Circular (avatars, dots) */
```

---

## 🌑 Shadows

**Philosophy:** Subtle shadows for depth, not drama.

```css
/* Subtle shadow for cards at rest */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* Standard card shadow */
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07),
             0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* Elevated elements (modals, floating buttons) */
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
             0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* High elevation (tooltips, dropdowns) */
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
             0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## 🎬 Animation & Motion

### **Timing Functions**
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### **Durations**
```css
--duration-fast: 150ms;     /* Micro-interactions (hover) */
--duration-base: 200ms;     /* Standard transitions */
--duration-slow: 300ms;     /* Complex animations */
--duration-slower: 500ms;   /* Page transitions */
```

### **Principles**
1. **Fast feedback:** Hover states respond in 150ms
2. **Smooth transitions:** Use ease-out for entering, ease-in for exiting
3. **Natural motion:** No bounce or elastic effects
4. **Performance:** Animate transform and opacity only (GPU-accelerated)

### **Examples**
```css
/* Button hover */
.button {
  transition: all 150ms ease-out;
}

/* Card hover */
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}

/* Modal entrance */
.modal {
  animation: fadeIn 300ms ease-out;
}
```

---

## 🧩 Component Library

### **Buttons**

**Primary Button**
```html
<button class="button-primary">
  Upload Swing
</button>
```
- Background: `--accent-primary`
- Text: `--text-inverse`
- Padding: `12px 24px`
- Border radius: `--radius-md`
- Font weight: `--font-semibold`
- Min height: 44px (accessibility)

**Secondary Button**
```html
<button class="button-secondary">
  Cancel
</button>
```
- Background: `--bg-secondary`
- Text: `--text-primary`
- Border: 1px solid `--border-medium`
- Padding: `12px 24px`
- Border radius: `--radius-md`

**Icon Button**
```html
<button class="button-icon">
  <IconClose size={20} />
</button>
```
- Background: transparent
- Padding: `8px`
- Border radius: `--radius-sm`
- Min touch target: 44×44px

---

### **Cards**

**Standard Card**
```html
<div class="card">
  <!-- Content -->
</div>
```
- Background: `--bg-secondary`
- Padding: `--space-6`
- Border radius: `--radius-md`
- Shadow: `--shadow-md`

**4B Card (Example: Brain)**
```html
<div class="card-4b brain">
  <div class="card-header">
    <IconBrain />
    <h3>BRAIN</h3>
    <span>Motor Profile</span>
  </div>
  <div class="card-content">
    <!-- Content -->
  </div>
</div>
```
- Background: `--brain-bg`
- Border left: 4px solid `--brain-text`
- Padding: `--space-6`
- Border radius: `--radius-md`

---

### **Navigation**

**Bottom Tab Bar**
```html
<nav class="bottom-nav">
  <button class="tab active">
    <IconHome />
    <span>Home</span>
  </button>
  <button class="tab">
    <IconCamera />
    <span>Live</span>
  </button>
  <!-- ... -->
</nav>
```
- Position: fixed bottom
- Background: `--bg-secondary`
- Height: 64px
- Shadow: `--shadow-lg` (top)
- 5 tabs: Home, Live, Upload, Progress, Settings

---

### **Status Indicators**

**Status Pill**
```html
<div class="status-pill green">
  <div class="dot"></div>
  <span>On Track</span>
</div>
```
- Background: translucent color (e.g., `rgba(16, 185, 129, 0.1)`)
- Border: 1px solid color
- Padding: `4px 12px`
- Border radius: `--radius-full`
- Dot: 8px circle with glow

---

### **KRS Gauge**

**SVG Ring Chart**
```html
<div class="krs-gauge">
  <svg viewBox="0 0 120 120">
    <circle class="track" />
    <circle class="progress" />
  </svg>
  <div class="score">82</div>
</div>
```
- Size: 120×120px
- Ring thickness: 12px
- Track color: `--border-light`
- Progress color: `--accent-primary`
- Animated: stroke-dashoffset transition

---

### **Input Fields**

**Text Input**
```html
<div class="input-group">
  <label>Name</label>
  <input type="text" placeholder="Enter your name" />
</div>
```
- Background: `--bg-secondary`
- Border: 1px solid `--border-medium`
- Padding: `12px 16px`
- Border radius: `--radius-md`
- Focus: 2px ring `--accent-primary`

**Number Input with Unit**
```html
<div class="input-group">
  <label>Weight</label>
  <div class="input-with-unit">
    <input type="number" />
    <span class="unit">lbs</span>
  </div>
</div>
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile first (default) */
--screen-sm: 640px;   /* Small tablets */
--screen-md: 768px;   /* Tablets */
--screen-lg: 1024px;  /* Small laptops */
--screen-xl: 1280px;  /* Desktops */
```

### **Usage**
```css
/* Mobile (default) */
.container {
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
  }
}
```

---

## ♿ Accessibility

### **Color Contrast**
- Text on background: minimum 4.5:1 (WCAG AA)
- Large text (18px+): minimum 3:1
- UI components: minimum 3:1

### **Touch Targets**
- Minimum size: 44×44px
- Spacing between targets: minimum 8px

### **Focus States**
- Visible focus ring: 2px solid `--accent-primary`
- Offset: 2px from element
- Never remove focus styles

### **Keyboard Navigation**
- All interactive elements focusable
- Logical tab order
- Skip links for navigation

---

## 🎨 Brand Assets

### **Logo**
- Primary: CB monogram (gradient)
- Full: "Catching Barrels" wordmark
- KRS Badge: "Powered by KRS™"

### **App Icon**
- Size: 1024×1024px (export at 2x)
- Format: PNG with transparency
- Rounded corners: 22.37% (Apple standard)

### **Favicon**
- Sizes: 16×16, 32×32, 64×64, 180×180 (Apple)
- ICO + PNG formats

---

## 📦 Export & Handoff

### **Design Tokens (JSON)**
```json
{
  "colors": {
    "bg": {
      "primary": "#FAFAFA",
      "secondary": "#FFFFFF"
    },
    "accent": {
      "primary": "#06B6D4"
    }
  },
  "spacing": {
    "4": "16px",
    "6": "24px"
  }
}
```

### **Assets to Export**
- [ ] Logo (SVG + PNG @1x, @2x, @3x)
- [ ] App icon (1024×1024 PNG)
- [ ] Favicon set
- [ ] Icon set (SVG)
- [ ] Design tokens (JSON)

---

**Version:** 1.0  
**Next Review:** Friday, December 27, 2025 @ 4pm
