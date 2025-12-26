# Screen 10: Motor Profile Result

**Screen Name**: Motor Profile Result  
**Route**: `/motor-profile/[id]`  
**Complexity**: MEDIUM (Card-based presentation)  
**Priority**: P1 (Important)

---

## 📐 Layout Overview

```
┌───────────────────────────────┐
│  ← Back              Share 🔗 │
├───────────────────────────────┤
│                               │
│  Your Motor Profile           │
│                               │
│  ┌─────────────────────────┐ │
│  │                         │ │
│  │  [Motor Profile Icon]   │ │ ← Hero card
│  │        ⭐              │ │   (color-coded)
│  │                         │ │
│  │    THE SPINNER          │ │
│  │ Quick hands, short path │ │
│  │                         │ │
│  │  Confidence: 88%        │ │
│  │  ■■■■■■■■■□             │ │
│  └─────────────────────────┘ │
│                               │
│  What This Means              │
│  ┌─────────────────────────┐ │
│  │ Spinners generate bat   │ │
│  │ speed through quick,    │ │
│  │ compact movements...    │ │
│  └─────────────────────────┘ │
│                               │
│  Your Strengths               │
│  ✓ Fast tempo (3.2:1)        │
│  ✓ Compact swing path        │
│  ✓ Quick hands               │
│                               │
│  Areas to Develop             │
│  → Increase ground force     │
│  → Improve transfer eff      │
│                               │
│  [View Recommended Drills]    │
│  [Take Movement Assessment]   │
│                               │
└───────────────────────────────┘
```

---

## 🎨 Motor Profile Types

### 1. Spinner (Green)
- **Icon**: ⭐
- **Color**: #10B981 (Success Green)
- **Tagline**: "Quick hands, short path. Let it fly."
- **Characteristics**: Fast tempo, compact swing

### 2. Slingshotter (Amber)
- **Icon**: 🎯
- **Color**: #F59E0B (Amber)
- **Tagline**: "Whip it through. Power from the stretch."
- **Characteristics**: Elastic loading, explosive release

### 3. Whipper (Red)
- **Icon**: ⚡
- **Color**: #EF4444 (Error Red)
- **Tagline**: "Rotational beast. Unleash the tornado."
- **Characteristics**: High rotation, violent turn

### 4. Torquer (Purple)
- **Icon**: 💪
- **Color**: #8B5CF6 (Purple)
- **Tagline**: "Strength wins. Ground it and pound it."
- **Characteristics**: Power-based, force generation

### 5. Tilter (Blue)
- **Icon**: 📐
- **Color**: #3B82F6 (Blue)
- **Tagline**: "Leverage master. Angles create power."
- **Characteristics**: Optimal angles, mechanical efficiency

### 6. Hybrid (Pink)
- **Icon**: 🔀
- **Color**: #EC4899 (Pink)
- **Tagline**: "Best of all worlds. Balanced power."
- **Characteristics**: Versatile, balanced attributes

---

## 🎨 Visual Specifications

### Hero Card
```css
background: linear-gradient(135deg, [profile-color] 0%, [darker-shade] 100%);
color: #FFFFFF;
border-radius: 16px;
padding: 32px;
text-align: center;
margin-bottom: 24px;
box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
```

**Icon**: 96px, white, centered

**Profile Name**:
```css
font-size: 28px;
font-weight: 700;
margin: 16px 0 8px;
```

**Tagline**:
```css
font-size: 16px;
opacity: 0.9;
font-style: italic;
margin-bottom: 24px;
```

**Confidence Bar**:
```css
width: 100%;
max-width: 200px;
margin: 0 auto;
```

---

## 📊 Analytics Events

```typescript
analytics.track('Motor Profile Viewed', {
  profileType: string,
  confidence: number,
});

analytics.track('View Drills Clicked', {
  profileType: string,
});

analytics.track('Retake Assessment Clicked');
```

---

**Priority**: P1  
**Complexity**: MEDIUM  
**Estimated Dev Time**: 6-8 hours (Phase 2)

---

*Last Updated: December 28, 2025*
