# Screen 11: Drills Library

**Screen Name**: Drills Library  
**Route**: `/drills`  
**Complexity**: MEDIUM-HIGH (Grid + Detail views)  
**Priority**: P1

---

## 📐 List View Layout

```
┌───────────────────────────────┐
│  ← Back          Drills   🔍  │
├───────────────────────────────┤
│  [Filter: All ▼] [Sort: ▼]   │
│                               │
│  ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Drill │ │Drill │ │Drill │  │
│  │  1   │ │  2   │ │  3   │  │
│  │      │ │      │ │      │  │
│  └──────┘ └──────┘ └──────┘  │
│  ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Drill │ │Drill │ │Drill │  │
│  │  4   │ │  5   │ │  6   │  │
│  └──────┘ └──────┘ └──────┘  │
└───────────────────────────────┘
│  Home  Upload  Report  More  │
└───────────────────────────────┘
```

---

## 📐 Detail View Layout

```
┌───────────────────────────────┐
│  ← Back to Drills             │
├───────────────────────────────┤
│                               │
│  [Video Preview 16:9]         │
│  ▶️                           │
│                               │
│  Hip Rotation Drill           │
│  ⭐⭐⭐⭐⭐ 4.8 (124)         │
│                               │
│  Duration: 5 min              │
│  Difficulty: Intermediate     │
│  Equipment: None              │
│                               │
│  Benefits                     │
│  • Increase hip mobility      │
│  • Improve rotational power   │
│  • Better weight transfer     │
│                               │
│  Instructions                 │
│  1. Stand with feet...        │
│  2. Rotate hips...            │
│  3. Keep shoulders...         │
│                               │
│  [Start Drill]                │
│  [Add to My Routine]          │
│                               │
└───────────────────────────────┘
```

---

## 🎨 Drill Card

```css
.drill-card {
  width: 100%;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 200ms, box-shadow 200ms;
}\n\n.drill-card:hover {\n  transform: translateY(-4px);\n  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);\n}\n```\n\n**Thumbnail**: 16:10 aspect ratio, gradient overlay\n**Title**: 16px semibold\n**Meta**: Duration, difficulty badges\n\n---\n\n## 🏷️ Drill Categories\n\n- All Drills\n- Recommended for You\n- Brain (Motor Profile)\n- Body (Creation)\n- Bat (Transfer)\n- Ball (Outcomes)\n- Warm-up\n- Strength\n- Mobility\n\n---\n\n**Priority**: P1  \n**Complexity**: MEDIUM-HIGH  \n**Est. Time**: 8-10 hours (Phase 3)\n\n---\n\n*Last Updated: December 28, 2025*\n", "old_string": ""}]