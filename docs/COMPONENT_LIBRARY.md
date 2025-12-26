# 🧩 Catching Barrels - Component Library Specification

**Version:** 1.0  
**Date:** December 26, 2025  
**Status:** Design Specification (Ready for Implementation)

---

## 📋 Component Overview

This document specifies all UI components for the Catching Barrels PWA. Each component includes:
- Visual design
- States (default, hover, active, disabled)
- Variants
- HTML/CSS/Tailwind implementation
- Accessibility requirements

**Total Components:** 25+

---

## 1️⃣ BUTTONS

### **Primary Button**

**Purpose:** Main call-to-action (Upload, Continue, Start)

**Design:**
```
Background: #06B6D4 (Electric Cyan)
Text: #FFFFFF (White)
Font: Inter Semibold (600)
Size: 16px
Padding: 12px 24px
Border Radius: 12px
Height: 48px (minimum for accessibility)
Shadow: 0 2px 4px rgba(6, 182, 212, 0.2)
```

**States:**
```css
/* Default */
.btn-primary {
  background: #06B6D4;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  min-height: 48px;
  transition: all 150ms ease-out;
}

/* Hover */
.btn-primary:hover {
  background: #0891B2;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(6, 182, 212, 0.3);
}

/* Active (Pressed) */
.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(6, 182, 212, 0.2);
}

/* Disabled */
.btn-primary:disabled {
  background: #E5E7EB;
  color: #9CA3AF;
  cursor: not-allowed;
}
```

**Tailwind Classes:**
```html
<button class="bg-cyan-500 hover:bg-cyan-600 text-white font-semibold px-6 py-3 rounded-xl min-h-[48px] transition-all duration-150 hover:-translate-y-0.5 hover:shadow-lg disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed">
  Upload Swing
</button>
```

---

### **Secondary Button**

**Purpose:** Less important actions (Cancel, Back, Skip)

**Design:**
```
Background: #FFFFFF (White)
Border: 1px solid #D1D5DB (Gray)
Text: #1F2937 (Dark Gray)
Font: Inter Semibold (600)
Size: 16px
Padding: 12px 24px
Border Radius: 12px
Height: 48px
```

**Tailwind Classes:**
```html
<button class="bg-white border border-gray-300 text-gray-900 font-semibold px-6 py-3 rounded-xl min-h-[48px] hover:bg-gray-50 transition-all duration-150">
  Cancel
</button>
```

---

### **Icon Button**

**Purpose:** Single icon actions (Close, Back, Settings)

**Design:**
```
Background: Transparent
Size: 44×44px (accessibility minimum)
Icon Size: 20×20px
Border Radius: 8px
Hover Background: #F3F4F6 (Light Gray)
```

**Tailwind Classes:**
```html
<button class="w-11 h-11 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors">
  <IconClose size={20} />
</button>
```

---

### **Pill Button (Toggle)**

**Purpose:** Toggle options (L/R/S for batting stance)

**Design:**
```
Background: #FFFFFF (White) when inactive
Background: #06B6D4 (Cyan) when active
Border: 1px solid #D1D5DB (Gray) when inactive
Border: 1px solid #06B6D4 (Cyan) when active
Text: #6B7280 (Gray) when inactive
Text: #FFFFFF (White) when active
Padding: 8px 20px
Border Radius: 24px (full pill)
```

**Tailwind Classes:**
```html
<!-- Inactive -->
<button class="bg-white border border-gray-300 text-gray-600 px-5 py-2 rounded-full">
  L
</button>

<!-- Active -->
<button class="bg-cyan-500 border border-cyan-500 text-white px-5 py-2 rounded-full">
  R
</button>
```

---

## 2️⃣ CARDS

### **Standard Card**

**Purpose:** Container for content sections

**Design:**
```
Background: #FFFFFF (White)
Border: None
Border Radius: 16px
Padding: 24px
Shadow: 0 4px 6px rgba(0, 0, 0, 0.07)
```

**Tailwind Classes:**
```html
<div class="bg-white rounded-2xl p-6 shadow-md">
  <!-- Content -->
</div>
```

**Hover State (optional):**
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}
```

---

### **4B Card (Brain/Body/Bat/Ball)**

**Purpose:** Display 4B framework breakdown

**Design (Brain Example):**
```
Background: #EDE9FE (Light Purple)
Border Left: 4px solid #7C3AED (Purple)
Border Radius: 16px
Padding: 24px
```

**Structure:**
```html
<div class="bg-purple-50 border-l-4 border-purple-600 rounded-2xl p-6">
  <!-- Header -->
  <div class="flex items-center gap-3 mb-4">
    <IconBrain class="w-10 h-10 text-purple-600" />
    <div>
      <h3 class="text-lg font-semibold text-purple-600">BRAIN</h3>
      <span class="text-sm text-gray-600">Motor Profile</span>
    </div>
  </div>
  
  <!-- Content -->
  <div class="space-y-3">
    <!-- Dynamic content -->
  </div>
</div>
```

**Color Variants:**
- Brain: `bg-purple-50 border-purple-600 text-purple-600`
- Body: `bg-blue-50 border-blue-600 text-blue-600`
- Bat: `bg-green-50 border-green-600 text-green-600`
- Ball: `bg-red-50 border-red-600 text-red-600`

---

### **Glass Card**

**Purpose:** Overlay cards (Live Mode coach cue, tooltips)

**Design:**
```
Background: rgba(255, 255, 255, 0.9)
Backdrop Filter: blur(12px)
Border: 1px solid rgba(255, 255, 255, 0.5)
Border Radius: 16px
Padding: 16px
Shadow: 0 8px 16px rgba(0, 0, 0, 0.1)
```

**Tailwind Classes:**
```html
<div class="bg-white/90 backdrop-blur-md border border-white/50 rounded-2xl p-4 shadow-lg">
  <!-- Content -->
</div>
```

---

## 3️⃣ NAVIGATION

### **Bottom Tab Bar**

**Purpose:** Main navigation (5 tabs)

**Design:**
```
Position: Fixed bottom
Background: #FFFFFF (White)
Height: 64px
Shadow: 0 -4px 12px rgba(0, 0, 0, 0.08)
Padding: 8px 0
```

**Tab Structure:**
```html
<nav class="fixed bottom-0 left-0 right-0 bg-white shadow-2xl h-16 flex items-center justify-around px-4">
  <!-- Home Tab (Active) -->
  <button class="flex flex-col items-center gap-1 text-cyan-500">
    <IconHome size={24} />
    <span class="text-xs font-medium">Home</span>
  </button>
  
  <!-- Live Tab (Inactive) -->
  <button class="flex flex-col items-center gap-1 text-gray-400">
    <IconCamera size={24} />
    <span class="text-xs font-medium">Live</span>
  </button>
  
  <!-- ... (5 tabs total) -->
</nav>
```

**Tab States:**
- Active: `text-cyan-500` (icon and label)
- Inactive: `text-gray-400`
- Hover: `text-gray-600` (transition 150ms)

---

## 4️⃣ INPUTS

### **Text Input**

**Design:**
```
Background: #FFFFFF (White)
Border: 1px solid #D1D5DB (Gray)
Border Radius: 12px
Padding: 12px 16px
Font: Inter Regular (400), 16px
Height: 48px
```

**States:**
```css
/* Default */
.input {
  background: white;
  border: 1px solid #D1D5DB;
  border-radius: 12px;
  padding: 12px 16px;
}

/* Focus */
.input:focus {
  border-color: #06B6D4;
  outline: none;
  ring: 2px solid rgba(6, 182, 212, 0.2);
}

/* Error */
.input.error {
  border-color: #EF4444;
}
```

**Tailwind Classes:**
```html
<input 
  type="text" 
  placeholder="Enter your name"
  class="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all"
/>
```

---

### **Number Input with Unit**

**Design:**
```html
<div class="relative">
  <input 
    type="number" 
    placeholder="185"
    class="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 pr-16 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none"
  />
  <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 font-medium">
    lbs
  </span>
</div>
```

---

### **Toggle Button Group**

**Purpose:** Select one option (Bats: L/R/S)

**Design:**
```html
<div class="flex gap-2">
  <button class="px-5 py-2 rounded-full bg-white border border-gray-300 text-gray-600 hover:border-cyan-500 transition-colors">
    L
  </button>
  <button class="px-5 py-2 rounded-full bg-cyan-500 border border-cyan-500 text-white">
    R
  </button>
  <button class="px-5 py-2 rounded-full bg-white border border-gray-300 text-gray-600 hover:border-cyan-500 transition-colors">
    S
  </button>
</div>
```

---

## 5️⃣ STATUS INDICATORS

### **Status Pill**

**Purpose:** Show status with color coding (Green/Yellow/Red)

**Design:**
```html
<!-- Green (Good) -->
<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-50 border border-green-500 text-green-700">
  <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
  <span class="text-sm font-medium">On Track</span>
</div>

<!-- Yellow (Warning) -->
<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-yellow-50 border border-yellow-500 text-yellow-700">
  <div class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></div>
  <span class="text-sm font-medium">Needs Work</span>
</div>

<!-- Red (Critical) -->
<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 border border-red-500 text-red-700">
  <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
  <span class="text-sm font-medium">Critical</span>
</div>
```

---

### **Level Badge**

**Purpose:** Show KRS level (Foundation → Elite)

**Design:**
```html
<div class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-cyan-600 text-white font-semibold shadow-lg">
  <span class="text-lg">⭐</span>
  <span>ADVANCED</span>
</div>
```

**Color by Level:**
- Foundation: Gray gradient
- Building: Blue gradient
- Developing: Purple gradient
- Advanced: Cyan gradient
- Elite: Gold gradient

---

### **Recording Indicator**

**Purpose:** Show when camera is recording

**Design:**
```html
<div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-500 text-white">
  <div class="w-3 h-3 rounded-full bg-white animate-pulse"></div>
  <span class="text-sm font-semibold">REC</span>
</div>
```

---

## 6️⃣ PROGRESS & SCORES

### **Progress Bar**

**Design:**
```html
<div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
  <div 
    class="h-full bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full transition-all duration-1000"
    style="width: 65%"
  ></div>
</div>
```

**With Label:**
```html
<div class="space-y-2">
  <div class="flex justify-between text-sm">
    <span class="text-gray-600">Processing</span>
    <span class="font-semibold text-gray-900">65%</span>
  </div>
  <div class="w-full bg-gray-200 rounded-full h-2">
    <div class="h-full bg-cyan-500 rounded-full" style="width: 65%"></div>
  </div>
</div>
```

---

### **KRS Gauge (SVG Ring)**

**Design:**
```html
<div class="relative w-32 h-32">
  <svg viewBox="0 0 120 120" class="transform -rotate-90">
    <!-- Background Track -->
    <circle 
      cx="60" 
      cy="60" 
      r="54" 
      fill="none" 
      stroke="#E5E7EB" 
      stroke-width="12"
    />
    
    <!-- Progress Ring -->
    <circle 
      cx="60" 
      cy="60" 
      r="54" 
      fill="none" 
      stroke="#06B6D4" 
      stroke-width="12"
      stroke-dasharray="339.3"
      stroke-dashoffset="67.9"
      stroke-linecap="round"
      class="transition-all duration-1000"
    />
  </svg>
  
  <!-- Score in Center -->
  <div class="absolute inset-0 flex items-center justify-center">
    <span class="text-4xl font-bold text-gray-900">82</span>
  </div>
</div>
```

**Calculation:**
- Circumference = 2 × π × r = 2 × 3.14159 × 54 = 339.3
- Dashoffset = Circumference × (1 - score/100)
- Example: 82% = 339.3 × (1 - 0.82) = 61.1

---

### **Score Card**

**Purpose:** Display metric with label

**Design:**
```html
<div class="bg-white rounded-xl p-4 shadow-md">
  <div class="text-sm text-gray-600 mb-1">Bat Speed</div>
  <div class="text-3xl font-bold text-gray-900">75<span class="text-lg text-gray-600">mph</span></div>
</div>
```

---

## 7️⃣ LISTS & ITEMS

### **Session History Item**

**Design:**
```html
<button class="w-full flex items-center justify-between p-4 bg-white rounded-xl hover:bg-gray-50 transition-colors">
  <div class="flex items-center gap-3">
    <div class="w-12 h-12 rounded-xl bg-cyan-50 flex items-center justify-center">
      <IconActivity class="w-6 h-6 text-cyan-600" />
    </div>
    <div class="text-left">
      <div class="font-semibold text-gray-900">Session #5</div>
      <div class="text-sm text-gray-600">Dec 26, 2025</div>
    </div>
  </div>
  <div class="flex items-center gap-3">
    <div class="text-right">
      <div class="text-lg font-bold text-cyan-600">82</div>
      <div class="text-xs text-gray-600">KRS</div>
    </div>
    <IconChevronRight class="w-5 h-5 text-gray-400" />
  </div>
</button>
```

---

### **Drill Card**

**Design:**
```html
<div class="bg-white rounded-2xl overflow-hidden shadow-md">
  <!-- Priority Badge -->
  <div class="px-4 pt-4">
    <span class="inline-block px-3 py-1 rounded-full bg-red-50 border border-red-500 text-red-700 text-xs font-semibold">
      #1 PRIORITY
    </span>
  </div>
  
  <!-- Content -->
  <div class="p-4 flex gap-4">
    <!-- Thumbnail -->
    <div class="w-24 h-24 rounded-xl bg-gray-200 flex-shrink-0 overflow-hidden">
      <img src="drill-thumb.jpg" alt="Drill thumbnail" class="w-full h-full object-cover" />
    </div>
    
    <!-- Info -->
    <div class="flex-1">
      <div class="text-xs text-gray-600 mb-1">FOCUS: Transfer</div>
      <h3 class="font-semibold text-gray-900 mb-2">Medicine Ball Rotations</h3>
      <p class="text-sm text-gray-600 mb-3">Build explosive hip rotation power...</p>
      <div class="text-xs text-gray-500">⏱️ 10 minutes</div>
    </div>
  </div>
  
  <!-- CTA -->
  <div class="px-4 pb-4">
    <button class="w-full py-3 bg-cyan-500 text-white font-semibold rounded-xl hover:bg-cyan-600 transition-colors">
      Watch Demo
    </button>
  </div>
</div>
```

---

## 8️⃣ MODALS & OVERLAYS

### **Modal Container**

**Design:**
```html
<!-- Overlay -->
<div class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  <!-- Modal -->
  <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
    <!-- Header -->
    <div class="flex items-center justify-between p-6 border-b border-gray-200">
      <h2 class="text-xl font-bold text-gray-900">Confirm Action</h2>
      <button class="w-10 h-10 flex items-center justify-center rounded-lg hover:bg-gray-100">
        <IconX size={20} />
      </button>
    </div>
    
    <!-- Body -->
    <div class="p-6">
      <p class="text-gray-600">Are you sure you want to proceed?</p>
    </div>
    
    <!-- Footer -->
    <div class="flex gap-3 p-6 border-t border-gray-200">
      <button class="flex-1 py-3 border border-gray-300 rounded-xl font-semibold hover:bg-gray-50">
        Cancel
      </button>
      <button class="flex-1 py-3 bg-cyan-500 text-white rounded-xl font-semibold hover:bg-cyan-600">
        Confirm
      </button>
    </div>
  </div>
</div>
```

---

## 9️⃣ FEEDBACK

### **Toast Notification**

**Design:**
```html
<!-- Success Toast -->
<div class="fixed top-4 right-4 z-50 bg-white rounded-2xl shadow-2xl p-4 flex items-center gap-3 animate-slide-in">
  <div class="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center">
    <IconCheck class="w-5 h-5 text-green-600" />
  </div>
  <div>
    <div class="font-semibold text-gray-900">Upload Complete</div>
    <div class="text-sm text-gray-600">Processing your swing...</div>
  </div>
</div>
```

---

### **Loading Spinner**

**Design:**
```html
<div class="w-8 h-8 border-4 border-gray-200 border-t-cyan-500 rounded-full animate-spin"></div>
```

---

### **Skeleton Loader**

**Design:**
```html
<div class="space-y-4 animate-pulse">
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
  <div class="h-32 bg-gray-200 rounded"></div>
</div>
```

---

## 🔟 CAMERA OVERLAY (Live Mode)

### **Pose Dot**

**Design:**
```html
<div class="absolute w-3 h-3 rounded-full bg-cyan-400 border-2 border-white shadow-lg animate-pulse"
     style="left: 45%; top: 30%">
</div>
```

**Color States:**
- Green: On target (#10B981)
- Yellow: Close (#F59E0B)
- Red: Off target (#EF4444)
- Cyan: Neutral (#06B6D4)

---

### **Coach Cue Card**

**Design:**
```html
<div class="absolute bottom-24 left-4 right-4 bg-white/90 backdrop-blur-md rounded-2xl p-4 shadow-2xl">
  <div class="flex items-center gap-3">
    <div class="w-10 h-10 rounded-full bg-cyan-50 flex items-center justify-center flex-shrink-0">
      <IconTarget class="w-5 h-5 text-cyan-600" />
    </div>
    <p class="text-sm font-medium text-gray-900">
      Stay balanced in your setup. Weight 60/40 on back leg.
    </p>
  </div>
</div>
```

---

## 📦 Component Export Checklist

- [ ] All 25+ components documented
- [ ] Tailwind classes provided
- [ ] States specified (hover, active, disabled)
- [ ] Accessibility notes included
- [ ] Color variants defined
- [ ] Responsive behavior noted
- [ ] Animation specs provided

---

**Status:** COMPONENTS SPECIFIED  
**Next:** Create screen mockups using these components

---

*End of Component Library Specification*
