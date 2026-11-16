#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Конвертер JSON-базы армии (rules/) в BSData XML (.gst/.cat) для NewRecruit.

Использование:
  python export_bsdata.py <rules_dir> <out_dir>
"""
import json, os, sys, hashlib
from xml.sax.saxutils import escape

GS_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"

def uid(*parts):
    h = hashlib.md5("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:10]
    return "b" + h  # id должен начинаться с буквы

def esc(v):
    return escape(str(v), {'"': "&quot;"})

def constraint(field, scope, value, ctype, cid=None, shared=True):
    cid = cid or uid("con", field, scope, value, ctype)
    return (f'<constraint id="{cid}" field="{field}" scope="{scope}" value="{value}" '
            f'percentValue="false" shared="{str(shared).lower()}" includeChildSelections="false" '
            f'includeChildForces="false" type="{ctype}"/>')

def build_gst(system):
    cats = system["categories"]
    model_stats = system["statsModel"]
    weapon_stats = system["statsWeapon"] + ["Abilities"]
    p = []
    p.append(f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    p.append(f'<gameSystem id="{uid(system["id"])}" name="{esc(system["name"])}" '
             f'xmlns="{GS_NS}" revision="{system.get("revision",1)}" '
             f'battleScribeVersion="2.03" authorName="{esc(system.get("authorName",""))}">')
    p.append('<publications><publication id="pub-main" name="Begotten Wargame Rules" shortName="BWG" publisher=""/></publications>')
    p.append(f'<costTypes><costType id="{uid("pts")}" name="pts" defaultCostLimit="0" hidden="false"/></costTypes>')
    p.append('<profileTypes>')
    def ptype(name, stats):
        chars = "".join(f'<characteristicType id="{uid("ct",name,s)}" name="{esc(s)}"/>' for s in stats)
        return f'<profileType id="{uid("pt",name)}" name="{name}"><characteristicTypes>{chars}</characteristicTypes></profileType>'
    p.append(ptype("Unit", model_stats))
    p.append(ptype("Weapon", weapon_stats))
    p.append(ptype("Ability", ["Description"]))
    p.append('</profileTypes>')
    p.append('<categoryEntries>' + "".join(
        f'<categoryEntry id="{uid("cat",c["id"])}" name="{esc(c["name"])}" hidden="false"/>'
        for c in cats) + '</categoryEntries>')
    links = "".join(
        f'<categoryLink id="{uid("cl",c["id"])}" name="{esc(c["name"])}" targetId="{uid("cat",c["id"])}" primary="{str(c["id"]=="troops").lower()}" hidden="false"/>'
        for c in cats)
    p.append(f'<forceEntries><forceEntry id="{uid("force")}" name="Армия" hidden="false">'
             f'<categoryLinks>{links}</categoryLinks>'
             f'<constraints>{constraint("selections","force",1,"min")}</constraints>'
             f'</forceEntry></forceEntries>')
    p.append('</gameSystem>')
    return "\n".join(p)

def stat_chars(pt_name, stats_map, stats_order):
    out = []
    for s in stats_order:
        v = stats_map.get(s, "-")
        out.append(f'<characteristic typeId="{uid("ct",pt_name,s)}" name="{esc(s)}">{esc(v)}</characteristic>')
    return "".join(out)

def build_cat(system, faction):
    model_stats = system["statsModel"]
    weapon_stats = system["statsWeapon"] + ["Abilities"]
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
        u = uid("unit", faction["id"], unit["id"])
        p.append(f'<selectionEntry id="{u}" name="{esc(unit["name"])}" type="unit" hidden="false" '
                 f'collective="false" import="true" publicationId="pub-main">')
        # категория
        catid = uid("cat", unit.get("category", "troops"))
        p.append(f'<categoryLinks><categoryLink id="{uid("ucl",unit["id"])}" name="{esc(unit.get("category",""))}" '
                 f'targetId="{catid}" primary="true" hidden="false"/></categoryLinks>')
        # профили: модели, оружие, способности
        p.append('<profiles>')
        for m in unit.get("models", []):
            p.append(f'<profile id="{uid("pr",unit["id"],m["name"])}" name="{esc(m["name"])}" hidden="false" '
                     f'typeId="{uid("pt","Unit")}" typeName="Unit">'
                     f'<characteristics>{stat_chars("Unit", m.get("stats",{}), model_stats)}</characteristics></profile>')
        for w in unit.get("weapons", []):
            wm = {s: w.get(s, "-") for s in system["statsWeapon"]}
            wm["Abilities"] = w.get("abilities", "-") or "-"
            p.append(f'<profile id="{uid("pr",unit["id"],w["id"])}" name="{esc(w["name"])}" hidden="false" '
                     f'typeId="{uid("pt","Weapon")}" typeName="Weapon">'
                     f'<characteristics>{stat_chars("Weapon", wm, weapon_stats)}</characteristics></profile>')
        for a in unit.get("abilities", []):
            p.append(f'<profile id="{uid("pr",unit["id"],a["name"])}" name="{esc(a["name"])}" hidden="false" '
                     f'typeId="{uid("pt","Ability")}" typeName="Ability"><characteristics>'
                     f'<characteristic typeId="{uid("ct","Ability","Description")}" name="Description">{esc(a["text"])}</characteristic>'
                     f'</characteristics></profile>')
        p.append('</profiles>')
        # состав отряда
        p.append('<selectionEntryGroups>')
        grp = uid("grp", unit["id"])
        p.append(f'<selectionEntryGroup id="{grp}" name="Состав отряда" hidden="false" collective="false" defaultSelectionEntryId="">')
        p.append(f'<constraints>{constraint("selections","parent",1,"min")}{constraint("selections","parent",len(unit.get("models",[1])),"max")}</constraints>')
        p.append('<selectionEntries>')
        for m in unit.get("models", []):
            mid = uid("model", unit["id"], m["name"])
            p.append(f'<selectionEntry id="{mid}" name="{esc(m["name"])}" type="model" hidden="false" collective="true">')
            p.append(f'<constraints>{constraint("selections","parent",m.get("min",1),"min")}'
                     f'{constraint("selections","parent",m.get("max",1),"max")}</constraints>')
            p.append(f'<costs><cost typeId="{uid("pts")}" name="pts" value="{m.get("pointsPerModel",0)}"/></costs>')
            p.append('</selectionEntry>')
        p.append('</selectionEntries></selectionEntryGroup>')
        p.append('</selectionEntryGroups>')
        # опции оружия ("1 на каждые N моделей")
        if unit.get("options"):
            p.append('<selectionEntries>')
            total_max = sum(m.get("max", 1) for m in unit.get("models", []))
            main_model_id = uid("model", unit["id"], unit["models"][0]["name"]) if unit.get("models") else ""
            for opt in unit["options"]:
                oid = uid("opt", unit["id"], opt["name"])
                maxc = uid("maxc", unit["id"], opt["name"])
                p.append(f'<selectionEntry id="{oid}" name="{esc(opt["name"])}" type="upgrade" hidden="false" collective="false">')
                p.append(f'<constraints>{constraint("selections","parent",0,"min")}'
                         f'<constraint id="{maxc}" field="selections" scope="parent" value="0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" type="max"/></constraints>')
                per = int(opt.get("perModels", 5))
                mods = []
                k = per
                while k <= total_max:
                    mods.append(f'<modifier type="increment" field="{maxc}" value="1"><conditions>'
                                f'<condition field="selections" scope="parent" targetId="{main_model_id}" value="{k}" '
                                f'percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" '
                                f'childId="any" type="atLeast"/></conditions></modifier>')
                    k += per
                if mods:
                    p.append('<modifiers>' + "".join(mods) + '</modifiers>')
                pts = opt.get("points", 0)
                p.append(f'<costs><cost typeId="{uid("pts")}" name="pts" value="{pts}"/></costs>')
                p.append('</selectionEntry>')
            p.append('</selectionEntries>')
        # кейворды как infoGroups? — кладём в rules
        if unit.get("keywords"):
            p.append(f'<rules><rule id="{uid("kw",unit["id"])}" name="Кейворды" hidden="false">'
                     f'<description>{esc(", ".join(unit["keywords"]))}</description></rule></rules>')
        if unit.get("lore"):
            p.append(f'<rules><rule id="{uid("lore",unit["id"])}" name="Описание" hidden="false">'
                     f'<description>{esc(unit["lore"])}</description></rule></rules>')
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
    gst = build_gst(system)
    with open(os.path.join(out_dir, f'{system["name"]}.gst'), "w", encoding="utf-8") as f:
        f.write(gst)
    fdir = os.path.join(rules_dir, "factions")
    made = [f'{system["name"]}.gst']
    for fn in sorted(os.listdir(fdir)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(fdir, fn), encoding="utf-8") as f:
            faction = json.load(f)
        cat = build_cat(system, faction)
        name = f'{faction["name"]}.cat'
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(cat)
        made.append(name)
    print("OK:", ", ".join(made))

if __name__ == "__main__":
    main()
