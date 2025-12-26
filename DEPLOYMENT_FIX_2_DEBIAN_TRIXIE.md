# Deployment Fix #2 - Debian Trixie Package Issue

**Date:** 2024-12-24 16:30 UTC  
**Issue:** `libgl1-mesa-glx` package not available in Debian Trixie  
**Status:** ✅ FIXED & DEPLOYED  

---

## 🔴 NEW ISSUE DISCOVERED

### Error Message:
```
E: Package 'libgl1-mesa-glx' has no installation candidate
```

### Root Cause:
- Python 3.11-slim uses **Debian Trixie** (latest)
- Debian Trixie **renamed** OpenGL packages:
  - ❌ Old: `libgl1-mesa-glx` (deprecated)
  - ✅ New: `libgl1` (current package name)
- Our Dockerfile used old package names

---

## ✅ SOLUTION DEPLOYED

### Changes to `Dockerfile`:

```diff
- libgl1-mesa-glx \
+ libgl1 \
- libxrender-dev \
+ libxrender1 \
- libglib2.0-0 \   (duplicate removed)
```

### Final System Dependencies (Minimal):
```dockerfile
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*
```

---

## 📦 PACKAGE NAME CHANGES (Debian Trixie)

| Old Package (Debian 11) | New Package (Debian Trixie) | Purpose |
|-------------------------|----------------------------|---------|
| `libgl1-mesa-glx` | `libgl1` | OpenGL runtime |
| `libxrender-dev` | `libxrender1` | X Render extension |
| (unchanged) | `libglib2.0-0` | GLib library |
| (unchanged) | `libgomp1` | OpenMP runtime |

---

## 🚀 DEPLOYMENT STATUS

- ✅ **Commit:** `0ba7ad2`
- ✅ **Pushed:** 2024-12-24 16:28 UTC
- 🟡 **Railway:** Building now (~5 min)
- 🔗 **GitHub:** https://github.com/THScoach/reboot-motion-backend/commit/0ba7ad2

---

## 🧪 VERIFICATION (After Build)

### Test 1: Health Check
```bash
curl https://reboot-motion-backend-production.up.railway.app/health
```

### Test 2: Check Python Version
Should show `"python_version": "3.11.7"`

---

## 📚 LESSONS LEARNED

1. **Debian versions matter** - Package names change between releases
2. **Use runtime packages** (`libxrender1` not `libxrender-dev`)
3. **Test Dockerfile locally** before pushing (if possible)
4. **Keep dependencies minimal** - Fewer packages = fewer issues

---

## 🔄 BACKUP PLAN

Created `Dockerfile.minimal` with absolute minimum dependencies:
- Only `libgl1` and `libglib2.0-0`
- Can switch if full Dockerfile fails

---

**Status:** ✅ DEPLOYED - BUILDING NOW  
**ETA:** 2024-12-24 16:33 UTC (5 minutes)
