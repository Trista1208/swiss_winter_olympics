# Swiss Olympic Qualification Criteria - Milano Cortina 2026

This folder contains all the qualification criteria files for Swiss Olympic sports participating in the 2026 Winter Olympics in Milano Cortina, Italy.

## 📁 Criteria Files

### Individual Sports Criteria
- **`Biathlon_Hauptkriterien.txt`** - Biathlon qualification routes (14 athletes)
- **`Alpine_Skiing_Hauptkriterien.txt`** - Alpine skiing qualification routes (57 athletes)
- **`Cross_Country_Skiing_Hauptkriterien.txt`** - Cross-country skiing routes (29 athletes)
- **`Freestyle_Skiing_Hauptkriterien.txt`** - Freestyle skiing qualification routes (49 athletes)
- **`Bobsleigh_Hauptkriterien.txt`** - Bobsleigh qualification routes (22 athletes)
- **`Figure_Skating_Hauptkriterien.txt`** - Figure skating qualification routes (6 athletes)

### Documentation
- **`Swiss_Olympic_Qualification_Overview.txt`** - Complete overview of all sports criteria

## 🏔️ Milano Cortina 2026 Olympics

**Date**: February 6-22, 2026  
**Location**: Milano & Cortina d'Ampezzo, Italy  
**Total Swiss Athletes**: 177 across 6 winter sports

## 📋 Qualification Structure

Each sport follows a similar 5-route qualification system:

1. **Route 1**: World Championships podium + World Cup performance
2. **Route 2**: Previous season World Cup + Current season World Cup  
3. **Route 3**: Single outstanding World Cup result
4. **Route 4**: Multiple good World Cup results
5. **Route 5**: Continental/Lower level + World Cup combination

## 🎯 Implementation Status

- **✅ Biathlon**: Fully implemented qualification system
- **✅ All Sports**: Criteria files created and documented
- **🔄 Other Sports**: Ready for implementation in athlete lookup system

## 📊 File Format

All criteria files use a consistent YAML-like structure:

```yaml
Sport: "Sport Name"
Is Olympic Discipline: "Yes"
Class: "Seniors"
Team Members: "No/Yes/Varies"

selection_paths:
  any_of:
    # Route 1: Description
    - all_of:
        - condition:
            Comp.SetDetail: "Competition Series"
            Date/Year: criteria
            Rank:
              interval: [min, max]
            count_at_least: number
```

## 🔧 Usage

These criteria files are used by:
- Qualification checking systems
- Athlete lookup applications
- Team selection dashboards
- Performance analysis tools

## 📈 Athletes by Sport

| Sport | Athletes | Status |
|-------|----------|---------|
| Alpine Skiing | 57 | Criteria defined |
| Freestyle Skiing | 49 | Criteria defined |
| Cross-Country Skiing | 29 | Criteria defined |
| Bobsleigh | 22 | Criteria defined |
| Biathlon | 14 | **Fully implemented** |
| Figure Skating | 6 | Criteria defined |
| **Total** | **177** | **Ready** |

---

**🏔️ Swiss Olympic Team Selection System**  
*Milano Cortina 2026 Winter Olympics Preparation*
