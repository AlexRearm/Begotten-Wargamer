#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Конвертер JSON-базы армии (rules/) в BSData XML (.gst/.cat) для NewRecruit.
Структура выходных каталогов повторяет официальные каталоги 40k:
- юнит -> группы моделей ("1 Сержант", "5-10 Стражей") с min/max
- внутри модели: вложенные оружия (min1/max1), группы выбора снаряжения (1/1),
  опции "1 на каждые N моделей" через модификаторы set max
Использование:
  python export_bsdata.py <rules_dir> <out_dir>
"""
import json, os, sys, hashlib
from xml.sax.saxutils import escape

GS_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"

def uid(*parts):
    h = hashlib.md5("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:10]
    return "b" + h

def esc(v):
    return escape(str(v), {'"': "&quot;"})

def constraint(field, scope, value, ctype, cid=None, child_sel=False):
    cid = cid or uid("con", field, scope, value, ctype)
    inc = "true" if child_sel else "false"
    return (f'<constraint id="{cid}" field="{field}" scope="{scope}" value="{value}" '
            f'percentValue="false" shared="true" includeChildSelections="{inc}" '
            f'includeChildForces="false" type="{ctype}"/>')

def build_gst(system):
    cats = system["categories"]
    p = []
    p.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    p.append(f'<gameSystem id="{uid(system["id"])}" name="{esc(system["name"])}" '
             f'xmlns="{GS_NS}" revision="{system.get("revision",1)}" '
             f'battleScribeVersion="2.03" authorName="{esc(system.get("authorName",""))}">')
    p.append('<publications><publication id="pub-main" name="Begotten Wargame Rules" shortName="BWG" publisher=""/></publications>')
    p.append(f'<costTypes><costType id="{uid("pts")}" name="pts" defaultCostLimit="0" hidden="false"/></costTypes>')
    p.append('<profileTypes>')
    def ptype(name, stats):
        chars = "".join(f'<characteristicType id="{uid("ct",name,s)}" name="{esc(s)}"/>' for s in stats)
        return f'<profileType id="{uid("pt",name)}" name="{name}"><characteristicTypes>{chars}</characteristicTypes></profileType>'
    p.append(ptype("Unit", system["statsModel"]))
    p.append(ptype("Weapon", system["statsWeapon"] + ["Abilities"]))
    p.append(ptype("Ability", ["Description"]))
    p.append('</profileTypes>')
    p.append('<categoryEntries>' + "".join(
        f'<categoryEntry id="{uid("cat",c["id"])}" name="{esc(c["name"])}" hidden="false"/>'
        for c in cats) + '</categoryEntries>')
    links = "".join(
        f'<categoryLink id="{uid("cl",c["id"])}" name="{esc(c["name"])}" targetId="{uid("cat",c["id"])}" primary="{str(c["id"]=="troops").lower()}" hidden="false"/>'
        for c in cats)
    p.append(f'<forceEntries><forceEntry id="{uid("force")}" name="Армия" hidden="false">'
             f'<categoryLinks>{links}</categoryLinks></forceEntry></forceEntries>')
    p.append('</gameSystem>')
    return "\n".join(p)

def stat_chars(pt_name, stats_map, stats_order):
    return "".join(
        f'<characteristic typeId="{uid("ct",pt_name,s)}" name="{esc(s)}">{esc(stats_map.get(s,"-"))}</characteristic>'
        for s in stats_order)

def weapon_profile(unit_id, w, system):
    wm = {s: w.get(s, "-") for s in system["statsWeapon"]}
    wm["Abilities"] = w.get("abilities", "-") or "-"
    return (f'<profile id="{uid("pr",unit_id,w["id"])}" name="{esc(w["name"])}" hidden="false" '
            f'typeId="{uid("pt","Weapon")}" typeName="Weapon">'
            f'<characteristics>{stat_chars("Weapon", wm, system["statsWeapon"]+["Abilities"])}</characteristics></profile>')

def upgrade_weapon_entry(unit_id, model_name, w, system, points=0, minv=0, maxv=1, extra_mods=""):
    """Опция-оружие (upgrade) со встроенным профилем."""
    eid = uid("up", unit_id, model_name, w["id"], points)
    maxid = uid("maxc", unit_id, model_name, w["id"], points)
    cons = ""
    if minv:
        cons += constraint("selections", "parent", minv, "min")
    cons += f'<constraint id="{maxid}" field="selections" scope="parent" value="{maxv}" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" type="max"/>'
    mods = f'<modifiers>{extra_mods}</modifiers>' if extra_mods else ""
    return (f'<selectionEntry id="{eid}" name="{esc(w["name"])}" type="upgrade" hidden="false" collective="false">'
            f'{mods}<profiles>{weapon_profile(unit_id + model_name, w, system)}</profiles>'
            f'<constraints>{cons}</constraints>'
            f'<costs><cost typeId="{uid("pts")}" name="pts" value="{points}"/></costs>'
            f'</selectionEntry>'), eid, maxid

def build_model_entry(system, unit, m, wbyid):
    """Одна строка состава отряда (модель) со снаряжением."""
    unit_id = unit["id"]
    mid = uid("model", unit_id, m["name"])
    out = []
    out.append(f'<selectionEntry id="{mid}" name="{esc(m["name"])}" type="model" hidden="false" collective="false" import="true">')
    out.append(f'<constraints>{constraint("selections","parent",m.get("max",1),"max")}</constraints>')
    # штатное оружие (всегда в руках)
    fixed = []
    for wid in m.get("weapons", []):
        w = wbyid.get(wid)
        if w:
            fx, _, _ = upgrade_weapon_entry(unit_id, m["name"], w, system, points=0, minv=1, maxv=1)
            fixed.append(fx)
    # опции "1 на каждые N" и просто лимитированные
    opts = list(m.get("options", []))
    opt_entries = []
    total_max = sum(mm.get("max", 1) for mm in unit.get("models", []))
    for opt in opts:
        w = wbyid.get(opt.get("takeWeapon", ""))
        if not w:
            continue
        per = int(opt.get("perModels", 0) or 0)
        pts = opt.get("points", 0)
        if per > 0:
            mods = []
            k, n = per, 1
            while k <= total_max:
                mods.append(
                    f'<modifier type="set" field="{{MAXID}}" value="{n}"><conditions>'
                    f'<condition field="selections" scope="{uid("unit", unit["faction"], unit_id)}" value="{k}" '
                    f'percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" '
                    f'childId="model" type="atLeast"/></conditions></modifier>')
                k += per; n += 1
            fx, _, maxid = upgrade_weapon_entry(unit_id, m["name"], {**w, "name": opt.get("name") or w["name"]},
                                                system, points=pts, minv=0, maxv=0,
                                                extra_mods="".join(mods))
            opt_entries.append(fx.replace("{MAXID}", maxid))
        else:
            mx = int(opt.get("max", 1) or 1)
            fx, _, _ = upgrade_weapon_entry(unit_id, m["name"], {**w, "name": opt.get("name") or w["name"]},
                                            system, points=pts, minv=0, maxv=mx)
            opt_entries.append(fx)
    # группы выбора снаряжения (например, оружие сержанта, 1/1)
    groups = []
    for ch in m.get("choices", []):
        gid = uid("chg", unit_id, m["name"], ch["name"])
        entries = []
        first_id = None
        for o in ch.get("options", []):
            w = wbyid.get(o.get("weapon", ""))
            if not w:
                continue
            fx, eid, _ = upgrade_weapon_entry(unit_id, m["name"] + ch["name"], w, system,
                                              points=o.get("points", 0), minv=0, maxv=1)
            if first_id is None:
                first_id = eid
            entries.append(fx)
        if not entries:
            continue
        groups.append(
            f'<selectionEntryGroup id="{gid}" name="{esc(ch["name"])}" hidden="false" collective="false" defaultSelectionEntryId="{first_id}">'
            f'<constraints>{constraint("selections","parent",1,"min")}{constraint("selections","parent",1,"max")}</constraints>'
            f'<selectionEntries>{"".join(entries)}</selectionEntries></selectionEntryGroup>')
    inner = fixed + opt_entries
    if inner:
        out.append(f'<selectionEntries>{"".join(inner)}</selectionEntries>')
    if groups:
        out.append(f'<selectionEntryGroups>{"".join(groups)}</selectionEntryGroups>')
    out.append(f'<costs><cost typeId="{uid("pts")}" name="pts" value="{m.get("pointsPerModel",0)}"/></costs>')
    out.append('</selectionEntry>')
    return "".join(out)

def build_cat(system, faction):
    model_stats = system["statsModel"]
    p = []
    p.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    p.append(f'<catalogue id="{uid(faction["id"])}" name="{esc(faction["name"])}" '
             f'gameSystemId="{uid(system["id"])}" gameSystemRevision="{system.get("revision",1)}" '
             f'xmlns="{CAT_NS}" revision="{faction.get("revision",1)}" battleScribeVersion="2.03" '
             f'authorName="{esc(system.get("authorName",""))}" library="false">')
    if faction.get("description"):
        p.append(f'<comment>{esc(faction["description"])}</comment>')
    p.append('<selectionEntries>')
    for unit in faction.get("units", []):
        unit["faction"] = faction["id"]
        u = uid("unit", faction["id"], unit["id"])
        wbyid = {w["id"]: w for w in unit.get("weapons", [])}
        p.append(f'<selectionEntry id="{u}" name="{esc(unit["name"])}" type="unit" hidden="false" '
                 f'collective="false" import="true" publicationId="pub-main">')
        catid = uid("cat", unit.get("category", "troops"))
        p.append(f'<categoryLinks><categoryLink id="{uid("ucl",unit["id"])}" name="{esc(unit.get("category",""))}" '
                 f'targetId="{catid}" primary="true" hidden="false"/></categoryLinks>')
        # профили: статы каждой модели + все оружия справочно + способности
        p.append('<profiles>')
        for m in unit.get("models", []):
            p.append(f'<profile id="{uid("pr",unit["id"],m["name"])}" name="{esc(m["name"])}" hidden="false" '
                     f'typeId="{uid("pt","Unit")}" typeName="Unit">'
                     f'<characteristics>{stat_chars("Unit", m.get("stats",{}), model_stats)}</characteristics></profile>')
        for a in unit.get("abilities", []):
            p.append(f'<profile id="{uid("pr",unit["id"],a["name"])}" name="{esc(a["name"])}" hidden="false" '
                     f'typeId="{uid("pt","Ability")}" typeName="Ability"><characteristics>'
                     f'<characteristic typeId="{uid("ct","Ability","Description")}" name="Description">{esc(a["text"])}</characteristic>'
                     f'</characteristics></profile>')
        p.append('</profiles>')
        if unit.get("keywords"):
            p.append(f'<rules><rule id="{uid("kw",unit["id"])}" name="Кейворды" hidden="false">'
                     f'<description>{esc(", ".join(unit["keywords"]))}</description></rule></rules>')
        if unit.get("lore"):
            p.append(f'<rules><rule id="{uid("lore",unit["id"])}" name="Описание" hidden="false">'
                     f'<description>{esc(unit["lore"])}</description></rule></rules>')
        # группы моделей: "1 Сержант", "5-10 Стражей"
        models = list(unit.get("models", []))
        # совместимость: старые unit.options относятся к первой не-сержантской модели
        legacy = unit.get("options", [])
        if legacy:
            for m in models:
                if not m.get("leader"):
                    m.setdefault("options", [])
                    m["options"] = list(m["options"]) + legacy
                    break
        p.append('<selectionEntryGroups>')
        for m in models:
            mn, mx = m.get("min", 1), m.get("max", 1)
            gname = f'{mn} {m["name"]}' if mn == mx else f'{mn}-{mx} {m["name"]}'
            gid = uid("grp", unit["id"], m["name"])
            mid = uid("model", unit["id"], m["name"])
            p.append(f'<selectionEntryGroup id="{gid}" name="{esc(gname)}" hidden="false" collective="false" defaultSelectionEntryId="{mid}">')
            p.append(f'<constraints>{constraint("selections","parent",mn,"min")}{constraint("selections","parent",mx,"max")}</constraints>')
            p.append(f'<selectionEntries>{build_model_entry(system, unit, m, wbyid)}</selectionEntries>')
            p.append('</selectionEntryGroup>')
        p.append('</selectionEntryGroups>')
        base = unit.get("points", 0)
        if base:
            p.append(f'<costs><cost typeId="{uid("pts")}" name="pts" value="{base}"/></costs>')
        p.append('</selectionEntry>')
    p.append('</selectionEntries>')
    p.append('</catalogue>')
    return "\n".join(p)

def main():
    rules_dir, out_dir = sys.argv[1], sys.argv[2]
    with open(os.path.join(rules_dir, "system.json"), encoding="utf-8") as f:
        system = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    for old in os.listdir(out_dir):
        if old.endswith((".gst", ".cat")):
            os.remove(os.path.join(out_dir, old))
    with open(os.path.join(out_dir, f'{system["name"]}.gst'), "w", encoding="utf-8") as f:
        f.write(build_gst(system))
    made = [f'{system["name"]}.gst']
    fdir = os.path.join(rules_dir, "factions")
    for fn in sorted(os.listdir(fdir)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(fdir, fn), encoding="utf-8") as f:
            faction = json.load(f)
        name = f'{faction["name"]}.cat'
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(build_cat(system, faction))
        made.append(name)
    print("OK:", ", ".join(made))

if __name__ == "__main__":
    main()
