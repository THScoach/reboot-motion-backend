# 🎨 Catching Barrels - Brand Assets Specification

**Version:** 1.0  
**Date:** December 26, 2025  
**Status:** Design Specification (Ready for Implementation)

---

## 🏷️ Brand Overview

**Brand Name:** Catching Barrels  
**Tagline:** "Know your kinetic potential"  
**Industry:** Baseball performance technology  
**Target Audience:** Athletes (ages 12-30), Coaches, Parents

**Brand Personality:**
- **Professional:** Data-driven, scientific
- **Athletic:** Performance-focused, competitive
- **Approachable:** Friendly, encouraging
- **Modern:** Tech-forward, innovative

---

## 🎨 Logo Design

### **Primary Logo: CB Monogram**

**Design Concept:**
- Interlocking "C" and "B" letters
- Geometric, modern sans-serif
- Gradient: Electric cyan to deep blue
- Circular badge format

**Specifications:**
```
Size: 120×120px (minimum)
Format: SVG (scalable)
Colors: 
  - Start: #06B6D4 (Electric Cyan)
  - End: #0891B2 (Deep Cyan)
Stroke: None
Fill: Linear gradient (135° angle)
Border: 2px solid #06B6D4 (optional outer ring)
```

**SVG Code Template:**
```svg
<svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#06B6D4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0891B2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Outer Circle (Optional) -->
  <circle cx="60" cy="60" r="58" fill="none" stroke="#06B6D4" stroke-width="2"/>
  
  <!-- CB Monogram -->
  <!-- C Letter -->
  <path d="M 75 35 A 25 25 0 0 0 45 35 L 45 85 A 25 25 0 0 0 75 85 L 75 75 A 15 15 0 0 1 55 75 L 55 45 A 15 15 0 0 1 75 45 Z" 
        fill="url(#logoGradient)" />
  
  <!-- B Letter (Simplified) -->
  <path d="M 50 45 L 65 45 A 7.5 7.5 0 0 1 65 60 L 50 60 L 50 45 M 50 60 L 67 60 A 12.5 12.5 0 0 1 67 85 L 50 85 Z" 
        fill="url(#logoGradient)" />
</svg>
```

**Usage:**
- App icon (1024×1024)
- Splash screen (centered)
- Favicon (simplified version)
- Loading spinner (animated rotation)

---

### **Secondary Logo: Full Wordmark**

**Text:** "Catching Barrels"

**Typography:**
```
Font: Inter Bold (700)
Size: 32px
Color: #1F2937 (Dark Gray)
Letter Spacing: -0.02em (tight)
Text Transform: None (Title Case)
```

**Layout Options:**

**Option A: Horizontal**
```
[CB Logo] Catching Barrels
```

**Option B: Stacked**
```
    [CB Logo]
Catching Barrels
```

**Usage:**
- Header/navigation
- Marketing materials
- Login/signup screens

---

### **Tertiary Logo: KRS Badge**

**Text:** "Powered by KRS™"

**Design:**
```
Background: Linear gradient (#06B6D4 to #0891B2)
Text Color: White (#FFFFFF)
Padding: 8px 16px
Border Radius: 24px (pill shape)
Font: Inter Semibold (600)
Size: 14px
Shadow: 0 2px 4px rgba(6, 182, 212, 0.2)
```

**HTML/CSS Template:**
```html
<div class="krs-badge">
  Powered by KRS™
</div>

<style>
.krs-badge {
  display: inline-block;
  background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 24px;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(6, 182, 212, 0.2);
}
</style>
```

**Usage:**
- Splash screen (below main logo)
- About/settings page
- Marketing footer

---

## 📱 App Icon Design

### **iOS/Android App Icon**

**Size:** 1024×1024px  
**Format:** PNG (with transparency for shadows)  
**Border Radius:** 22.37% (Apple standard)

**Design:**
```
Background: Linear gradient (#06B6D4 to #0891B2)
Icon: CB Monogram (white, centered)
Padding: 180px from edges
Shadow: Subtle inner shadow for depth
```

**Layers:**
1. Background gradient (full size)
2. CB monogram (664×664px, centered)
3. Optional: Subtle texture overlay (5% opacity)

**Export Sizes:**
- 1024×1024 (App Store)
- 512×512 (Play Store)
- 180×180 (Apple Touch Icon)
- 192×192 (Android)
- 152×152 (iPad)
- 120×120 (iPhone)

---

### **Favicon Set**

**Sizes Needed:**
- 16×16 (browser tab)
- 32×32 (browser bookmark)
- 64×64 (desktop shortcut)
- 180×180 (Apple touch icon)

**Design:**
- Simplified CB monogram
- Solid color (#06B6D4) for small sizes
- No gradient (better rendering at tiny sizes)

**ICO Format:**
Include all sizes in single .ico file for maximum compatibility.

---

## 🎨 Color Palette

### **Primary Colors**

**Electric Cyan (Primary Accent)**
```
Name: Electric Cyan
Hex: #06B6D4
RGB: 6, 182, 212
Usage: Primary CTAs, links, KRS scores, active states
```

**Deep Cyan (Primary Hover)**
```
Name: Deep Cyan
Hex: #0891B2
RGB: 8, 145, 178
Usage: Hover states, pressed states, gradients
```

### **Background Colors**

**Light Gray (Primary Background)**
```
Name: Light Gray
Hex: #FAFAFA
RGB: 250, 250, 250
Usage: Page backgrounds
```

**White (Card Background)**
```
Name: White
Hex: #FFFFFF
RGB: 255, 255, 255
Usage: Cards, modals, input fields
```

### **4B Framework Colors**

**Brain - Purple**
```
Background: #EDE9FE
Text: #7C3AED
Icon: #A78BFA
```

**Body - Blue**
```
Background: #DBEAFE
Text: #2563EB
Icon: #60A5FA
```

**Bat - Green**
```
Background: #D1FAE5
Text: #059669
Icon: #34D399
```

**Ball - Red**
```
Background: #FEE2E2
Text: #DC2626
Icon: #F87171
```

---

## 🖼️ Brand Usage Guidelines

### **Do's**
✅ Use CB monogram as primary logo  
✅ Maintain gradient direction (top-left to bottom-right)  
✅ Keep adequate white space around logo (minimum 20px)  
✅ Use on light or dark backgrounds  
✅ Scale proportionally

### **Don'ts**
❌ Don't alter gradient colors  
❌ Don't rotate or skew logo  
❌ Don't add effects (drop shadows, outlines)  
❌ Don't place on busy backgrounds  
❌ Don't stretch or distort

---

## 📐 Logo Sizing

### **Minimum Sizes**
- Digital: 32×32px
- Print: 0.5 inches (36px at 72dpi)
- Favicon: 16×16px (simplified version)

### **Clear Space**
Maintain clear space equal to the height of the "C" letter on all sides.

---

## 🎭 Brand Applications

### **1. Splash Screen**
```
Layout:
- Centered CB monogram (120×120px)
- "Catching Barrels" wordmark (below, 16px gap)
- "Know your kinetic potential" tagline (below, 8px gap, gray)
- "Powered by KRS™" badge (bottom, 40px from edge)
Background: Light gradient (#FAFAFA to #F5F5F7)
```

### **2. Loading States**
```
Animation: CB monogram rotating (360° in 2 seconds, linear)
Size: 48×48px
Background: White card with shadow
```

### **3. Empty States**
```
Icon: Simplified CB monogram (64×64px, gray)
Text: "No sessions yet" (below)
CTA: "Upload Your First Swing" button
```

---

## 📦 Export Checklist

### **Logo Files**
- [ ] CB_Monogram.svg (vector)
- [ ] CB_Monogram@1x.png (120×120)
- [ ] CB_Monogram@2x.png (240×240)
- [ ] CB_Monogram@3x.png (360×360)
- [ ] CB_Wordmark.svg (vector)
- [ ] CB_Wordmark@1x.png
- [ ] CB_Wordmark@2x.png
- [ ] KRS_Badge.svg

### **App Icons**
- [ ] AppIcon_1024.png (1024×1024, rounded)
- [ ] AppIcon_512.png
- [ ] AppIcon_180.png (Apple Touch Icon)
- [ ] AppIcon_192.png (Android)

### **Favicons**
- [ ] favicon.ico (multi-size)
- [ ] favicon-16x16.png
- [ ] favicon-32x32.png
- [ ] favicon-64x64.png
- [ ] apple-touch-icon.png (180×180)

---

## 🎨 Design Tokens

**Brand Colors (CSS Variables)**
```css
:root {
  /* Brand Colors */
  --brand-primary: #06B6D4;
  --brand-primary-hover: #0891B2;
  --brand-primary-light: #CFFAFE;
  
  /* Logo Gradient */
  --logo-gradient: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);
  
  /* Backgrounds */
  --bg-primary: #FAFAFA;
  --bg-secondary: #FFFFFF;
}
```

---

## 🚀 Implementation Notes

**For Designers:**
1. Create CB monogram in vector editor (Figma/Illustrator)
2. Apply gradient (135° angle)
3. Export at all required sizes
4. Generate app icons with rounded corners

**For Developers:**
1. Import SVG logos as React components
2. Use CSS variables for colors
3. Implement loading animation with CSS keyframes
4. Add logos to public/ folder

---

**Status:** READY FOR IMPLEMENTATION  
**Next:** Create mockups in Figma or proceed to component design

---

*End of Brand Assets Specification*
