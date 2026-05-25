"""
Deep content additions — critical missing knowledge for first-time homebuilder.
One section per phase, injected before </main>.
Covers irreversible decisions, money-saving tips, Nepal-specific issues.
"""

def sec(sid, icon, title, subtitle, body):
    return f'''
<div class="sec open" id="{sid}">
<div class="sec-head" onclick="toggle('{sid}')">
  <div class="sec-icon">{icon}</div>
  <div class="sec-title"><h3>{title}</h3><p>{subtitle}</p></div>
  <div class="sec-badge">Must Read</div>
  <span class="sec-arrow">▼</span>
</div>
<div class="sec-body">
{body}
</div>
</div>'''

def t(b): return f'<div class="tip-box"><strong>💡 Know This</strong> {b}</div>'
def w(b): return f'<div class="warn-box"><strong>⚠️ Critical</strong> {b}</div>'
def g(b): return f'<div class="good-box"><strong>✅ Do This</strong> {b}</div>'
def tbl(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><tr>{th}</tr>{tr}</table>'

SECTIONS = {

'phase-0.html': sec('s-critical0','💰','Money and Legal — Before Touching a Single Brick',
'The financial and legal decisions that determine success or failure',
w('Most first-time homebuilders in Nepal go over budget by 30–40% and regret many decisions. The root cause is almost always: started construction without a proper plan, contract, or budget.') +
'<h4>BOQ — Bill of Quantities (Most Important Document Nobody Talks About)</h4>' +
t('A BOQ is a detailed list of EVERY material needed to build your house — with quantities, unit rates, and total cost. Example: "RCC M25 concrete for columns — 12 cubic metres @ NPR 8,500/m³ = NPR 102,000". A BOQ for your house covers 50–100 line items.') +
g('Ask your structural engineer or a quantity surveyor to prepare a BOQ before signing any contract. Cost: NPR 10,000–25,000. This one document lets you compare quotes from contractors fairly, track every rupee spent, and immediately detect if a contractor is cutting corners on material quantities.') +
w('Without a BOQ, a contractor can reduce steel from 100kg per cubic metre to 70kg. You cannot detect this. With a BOQ, you know exactly how much steel should be used and can weigh/check delivery quantities.') +
'<h4>Realistic Cost Estimate for Pokhara (2025–2026)</h4>' +
tbl(['Item','Cost Per Sq Ft','Notes'],
[['Basic structure only (no finishes)','NPR 1,800–2,200','Foundation, columns, walls, slab only'],
 ['Mid-range complete house','NPR 2,800–3,500','Structure + basic finishes, tiles, paint'],
 ['Good quality complete house','NPR 3,800–5,000','Structure + quality finishes, modular kitchen'],
 ['Premium quality house','NPR 5,500–8,000+','Premium finishes, imported fittings, full smart features']]) +
t('For your 1800 sq ft G+2 house: budget NPR 70–90 lakh for good quality, NPR 50–65 lakh for mid-range. This is TOTAL cost including everything except furniture. Add 15–20% contingency on top.') +
'<h4>Neighbour NOC (No Objection Certificate)</h4>' +
w('In Nepal, if you build a wall on or near a shared boundary, you must get written NOC from the neighbour. Without this, they can file a complaint that stops construction legally — even after you have spent millions. Get this BEFORE foundation.') +
g('Visit both neighbours, explain your plan, show them your building line, and get a signed letter saying they have no objection to your construction. Keep original copies. This takes one afternoon but can prevent months of legal delays.') +
'<h4>Temporary Electricity and Water for Construction</h4>' +
t('Construction needs electricity (for power tools, lighting, welding) and water (for concrete mixing, curing, cleaning). Arrange a temporary connection or agreement with neighbours before starting. Without this, workers use improvised solutions — like adding less water to concrete because there is not enough supply — which compromises quality.') +
'<h4>Plinth Height — Flood and Damp Protection</h4>' +
w('Plinth height = how high your ground floor sits above the natural ground or road level. Minimum 600mm (2 feet) above road level for Pokhara. Many contractors build at road level to save material. Then: rain splash damages the wall base, mosquitoes breed in dampness, and road resurfacing (which raises road level over years) eventually puts your ground floor below road level causing flooding.') +
g('Tell your engineer and contractor: "Plinth height minimum 600mm above road level." This costs very little extra but protects the house permanently.')),

'phase-1.html': sec('s-critical1','🔬','Foundation — Decisions You Cannot Change Later',
'Get these right the first time — there is no second chance',
'<h4>Concrete Cube Test — Your Quality Proof</h4>' +
t('During every structural concrete pour, ask your engineer to take concrete cube samples (150mm × 150mm × 150mm cubes). These are sent to a certified lab and tested at 7 days and 28 days. The lab report tells you the actual strength of your concrete. This is the ONLY way to know if you got M25 or weaker.') +
g('Cost: NPR 500–1,500 per cube test. Take samples from: foundation footings, columns (each pour), roof slab. Keep all lab reports. If contractor disputes quality later, you have scientific proof. Without cube tests, you have only words.') +
'<h4>Slump Test — Field Check for Water-Cement Ratio</h4>' +
t('A slump test checks concrete workability on site — takes 2 minutes. You fill a cone-shaped mould with fresh concrete, lift the cone, and measure how much the concrete "slumps" (drops). For M25 structural concrete: slump should be 50–100mm. If it slumps 150mm+, too much water was added — reject the batch.') +
g('Ask your engineer to demonstrate a slump test on the first day. After that, you can do it yourself to spot-check batches.') +
'<h4>Plinth Beam — The Level of Your Entire House</h4>' +
w('The plinth beam (horizontal RCC beam at ground level) is the most important reference level in your house. Everything — every wall, every column height, every floor level — is measured from the plinth beam. If this beam is not perfectly level (horizontal) across the entire footprint, your entire house will be slightly tilted. Every door will stick. Every floor will slope.') +
g('Before your contractor pours the plinth beam concrete: check the level with a laser level or water level across all four corners and across the centre. All points must read exactly the same. This check takes 30 minutes but prevents years of problems.') +
'<h4>Filled Land vs Natural Ground — Critical Discovery</h4>' +
w('If any part of your 30×60 plot was previously a rice field, pond, or lower ground that was filled with soil or debris, that filled area behaves differently under load. It compresses and settles, causing differential settlement — one side of your house sinks more than the other. This causes diagonal cracks in walls, doors that jam, and in severe cases structural failure.') +
t('Ask your soil test engineer specifically: "Is any part of this plot filled land?" If yes: that area needs deeper foundation (reaching original undisturbed soil below the fill) or pile foundation. The extra cost is significant but non-negotiable.') +
'<h4>Foundation Drainage — Protecting the Foundation From Groundwater</h4>' +
g('Around the perimeter of your foundation, install a French drain (perforated pipe surrounded by gravel, covered with geotextile fabric, sloped to outlet). This drains groundwater away from the foundation. In Pokhara with heavy monsoon, groundwater pressure on a foundation without drainage causes hydrostatic pressure that slowly damages waterproofing. Cost: NPR 5,000–10,000. Benefit: 50 years of foundation health.')),

'phase-2.html': sec('s-critical2','📐','Structure — The Irreversible Decisions',
'Once the slab is cast, these cannot be changed without demolishing and rebuilding',
'<h4>Floor-to-Floor Height — Most Underestimated Decision</h4>' +
w('Standard Nepal contractor practice: 9 feet (2.74m) floor-to-floor height. This saves material and cost. But with 9ft ceiling: a standard door (7ft) leaves only 2ft above the door — it feels cramped. 10ft (3.05m) floor-to-floor is the MINIMUM for a comfortable, airy house. 10.5ft is ideal for your ground floor (parents room and living area).') +
tbl(['Floor','Recommended Height','Reason'],
[['Ground floor (parents + living)','10.5 ft (3.2m)','Elderly people + guests — needs to feel spacious'],
 ['First floor (your floor)','10 ft (3.05m)','Bedroom comfort and AC efficiency'],
 ['Second floor (rental)','9.5 ft (2.9m)','Slightly lower is acceptable for rental'],
 ['Terrace parapet wall','4 ft (1.2m) minimum','Safety — no lower than this']]) +
g('Tell your engineer and contractor: "I want 10.5ft floor-to-floor on ground floor, 10ft on first floor." The extra material cost is less than NPR 20,000 per floor but the comfort benefit lasts a lifetime and increases resale value significantly.') +
'<h4>Sunshade (Chajja) Above Every Window</h4>' +
w('Pokhara receives some of the highest rainfall in Nepal. A window without a sunshade (chajja) — the horizontal concrete projection above a window — allows: rain to drive directly into the window gap, water stains on the wall below the window, direct sun making rooms hot. After the house is built, adding a sunshade means cutting into the wall and is very expensive.') +
g('Specify to your structural engineer: 300mm (1 foot) deep sunshade/chajja above every window. For living room windows facing the road: 450mm deep. For kitchen window: 300mm. The chajja must have a 15-degree downward tilt and a drip edge on the underside. This is designed at structural stage — request it now.') +
'<h4>Shuttering (Formwork) Removal Timing</h4>' +
w('Shuttering is the wooden/metal mould around concrete that keeps it in shape while it sets. Removing it too early is extremely dangerous. The contractor wants to remove it fast (so the formwork can be reused sooner). You must insist on minimum times.') +
tbl(['Element','Minimum Time Before Removal','Why'],
[['Column sides','24–48 hours','Sides can be removed early but concrete must not be loaded'],
 ['Beam sides','7 days','Beam must gain strength on sides first'],
 ['Slab (bottom support)','21 days minimum — ideally 28 days','Slab carries full load — premature removal causes sag and permanent deformation'],
 ['Beam bottom support','21 days minimum','Beam must reach design strength before carrying its own weight']]) +
t('Write these timings in your contract. Ask your structural engineer to visit on the day shuttering is removed from slabs and approve it. A slab whose shuttering was removed at 10 days instead of 21 days may look fine but has permanent internal cracking that reduces its strength by 30%.') +
'<h4>Balcony Design — Waterproofing and Railing Height</h4>' +
w('Balconies are the most neglected structural element in Nepal. Most balcony leaks in houses occur because: the balcony slab slope is wrong (water pools instead of draining), the balcony-to-wall junction is not waterproofed, the railing posts go THROUGH the slab creating water channels.') +
g('For your balcony: 1) Slab must slope minimum 1:40 toward the drain (steeper than indoor floors). 2) Install a full waterproofing membrane before tiles. 3) Railing posts must have base plates bolted to the slab surface — NOT drilled through the slab. 4) Railing height minimum 1.1 metres (Nepal building code requirement). 5) Balcony drain connected to rainwater pipe, not sewage.')),

'phase-5.html': sec('s-critical3','💧','Waterproofing — The Hidden Failures',
'90% of waterproofing failures happen at joints and transitions — not on flat surfaces',
'<h4>Sump Tank Waterproofing — Often Forgotten</h4>' +
w('Your underground sump tank stores water you DRINK. If the tank is not properly waterproofed inside AND outside, two problems occur: 1) Groundwater seeps IN, contaminating your drinking water with soil bacteria and chemicals. 2) Water seeps OUT, wasting money and damaging the soil structure around your foundation.') +
g('Specify: apply crystalline waterproofing compound to the concrete mix when casting the sump tank. After curing, apply 2 coats of food-safe waterproof coating on the INSIDE of the tank (Sika Monotop or similar food-safe product). This is different from roof waterproofing — must be food-safe. Fit a manhole cover with mosquito-proof mesh to prevent dengue mosquito breeding.') +
'<h4>Wall-to-Floor Junction — The Most Common Leak Point</h4>' +
t('In bathrooms and kitchen, the joint where the wall meets the floor is the highest-risk point for water leakage. Water seeps through this joint and damages the wall below and the room below. Most waterproofing failures in bathrooms start at corners, not the flat floor.') +
g('Specify to waterproofing contractor: apply a cove fillet (a rounded mortar fill in all corners where wall meets floor, creating a curved rather than sharp 90-degree corner) BEFORE applying waterproofing membrane. Then apply the membrane continuously from floor up the wall and into the cove. Never apply membrane in a sharp corner — it tears there from movement.') +
'<h4>Compound and Boundary Wall Waterproofing</h4>' +
t('Your compound/boundary wall is exposed to rain on both sides. Without a proper coping (top cap) on the wall, water enters the top of the wall, saturates it, causes white salt stains (efflorescence), and eventually crumbles the wall from inside.') +
g('Specify: cast a continuous sloped RCC coping (cap) on top of the entire compound wall, minimum 75mm thick, sloped on both sides to shed water. Apply waterproof mortar for the coping. This extends compound wall life from 10 years to 50+ years.') +
'<h4>Efflorescence — White Salt Marks on Walls</h4>' +
t('Efflorescence = white chalky deposits on the outside of walls. Cause: water soaks through the wall, picks up mineral salts from cement and brick, and deposits them when it evaporates on the surface. It looks ugly and indicates ongoing water infiltration.') +
w('Prevention is far easier than cure. Prevention: correct waterproofing, waterproof plaster, and waterproof paint on all external walls. If it appears after construction: do NOT paint over it. Remove with diluted acid wash, identify and stop the water source, let wall dry completely (takes weeks), then repaint with anti-efflorescence primer first.')),

'phase-3.html': sec('s-critical4','💧','Plumbing — Sizing and System Design',
'Get the sizes right or you will have poor water pressure and constant blockages',
'<h4>Water Tank Sizing — How Much You Actually Need</h4>' +
w('Most first-time builders install tanks that are too small. Then: water runs out daily, pump runs continuously, pressure is low during peak morning usage. Size your tanks correctly from the start — changing tank size later means breaking construction.') +
tbl(['Tank','Recommended Size','Minimum Size','Calculation Basis'],
[['Underground sump','12,000–15,000 litres','8,000 litres','3 days storage for family of 6'],
 ['Overhead tank','3,000 litres','2,000 litres','1 day peak usage buffer'],
 ['Total water stored','15,000–18,000 litres','10,000 litres','Critical for Pokhara supply interruptions']]) +
t('Pokhara municipal water supply is intermittent — sometimes off for 2–3 days. With 15,000 litres stored, your family can live normally for 5–7 days without any municipal supply.') +
'<h4>Vent Pipe — The Overlooked Part of Drainage</h4>' +
w('Every drain system needs a vent pipe — a pipe that rises from the drainage system up through the roof and opens to outside air. Without a vent: when water flows down a drain, it creates a vacuum that sucks the water OUT of every P-trap it passes. All your P-traps fail simultaneously. Every drain in the house smells like sewer.') +
g('Ask your plumber: "Where is the vent pipe on your drainage plan?" A proper drainage design has one main vent pipe per floor (typically 50mm diameter, rises through walls or externally and opens 500mm above roof level). If your plumber does not know what a vent pipe is, get a different plumber.') +
'<h4>Rainwater and Sewage — Must Be Completely Separate</h4>' +
w('In Nepal, many builders connect roof rainwater drain pipes to the sewage system. This is illegal, causes sewage backup into bathrooms during heavy rain, and overloads the municipal sewer. Roof rainwater = clean. It must go to: your underground sump tank (for reuse) OR directly to a soakpit OR to the road storm drain — NEVER to the sewage system.') +
'<h4>Hard Water — Test and Plan Before Installing Pipes</h4>' +
t('Before finalising your plumbing plan, test your municipal water for TDS (Total Dissolved Solids) and hardness. In many areas of Pokhara, hardness is 200–400 ppm — moderate to hard. Above 200 ppm: scale builds inside pipes and geysers, white marks on all taps, poor soap lather. Ask your plumber to send a water sample to a lab (NPR 500–1,000).') +
g('If TDS > 300 or hardness > 200 ppm: install a whole-house water softener on the main supply line before it splits into hot and cold. This single installation prevents: geyser failure (scale inside), blocked tap aerators, white tile stains, dry skin. Return on investment within 3 years.')),

'phase-4.html': sec('s-critical5','⚡','Electrical — Load Planning and Future Capacity',
'Size your electrical system for the house you will have in 10 years, not just today',
'<h4>Load Calculation — Critical Before Meter Application</h4>' +
t('Total electrical load = sum of all appliances you will ever run simultaneously. This determines what size electricity meter and connection you apply for.') +
tbl(['Appliance','Typical Load','Notes'],
[['Each AC unit','1,500–2,000W','Count all planned ACs'],
 ['Induction cooktop','2,000–3,500W','High load — dedicated circuit'],
 ['Electric geyser (each)','2,000–3,000W','Multiple in house'],
 ['Washing machine','500–1,000W',''],
 ['Refrigerator','150–300W','Always on'],
 ['Lights and fans total','500–800W','Whole house'],
 ['Miscellaneous','1,000W','TV, computer, chargers etc']]) +
w('Add up all loads. For a G+2 house in Nepal with ACs: likely 15,000–20,000W total. Single phase meter handles maximum 5,000–7,000W. You NEED three-phase connection (तीन फेज). Apply for three-phase from Nepal Electricity Authority (NEA) from the beginning. Changing from single to three-phase later requires separate application, additional cost, and takes months.') +
g('Tell NEA when applying for your meter: "I need a 3-phase, 15kVA (or 20kVA) connection for a G+2 residential building." Higher kVA capacity means higher monthly demand charge but eliminates tripping issues forever.') +
'<h4>Underground Cable for Gate, Garden, CCTV</h4>' +
t('Any cable going underground (to gate motor, garden lights, external CCTV, compound wall lights) must be ARMOURED cable — it has a steel armour braid that protects against digging damage and rodents. Normal PVC wire underground fails within 2–3 years.') +
g('During construction: bury armoured cable in 600mm deep trenches (below normal digging depth) inside a conduit pipe, with a concrete slab over the trench. Mark the cable route on a drawing and photograph before backfilling. Getting the cable map wrong means digging up the garden 5 years later.') +
'<h4>Earthing System — Critical in Lightning-Prone Pokhara</h4>' +
w('Standard practice in Nepal: one earth pit near the main panel. This is NOT adequate for Pokhara where lightning is frequent and the hills create static electric conditions. For your house: minimum 2 earth pits (separated by minimum 5 metres), copper wire earthing, and a lightning arrester rod on the roof connected to the earthing system.') +
g('Ask your electrician specifically: "What is the earthing resistance reading?" Should be below 1 ohm ideally, maximum 5 ohms. Test with a digital earth resistance meter in your presence. Earth pits should be inspected every 2 years and topped up with salt/charcoal mixture to maintain low resistance.')),

'phase-6.html': sec('s-critical6','🪟','Windows and Doors — Details That Affect Daily Life',
'Small decisions that affect comfort, security and maintenance for 20+ years',
'<h4>Window Frame Depth Must Match Wall Thickness</h4>' +
w('Your walls are 230mm thick (with plastering, approximately 250mm total). If you order UPVC windows with a frame depth of only 60mm, the window frame will sit sunken inside the wall with 190mm of exposed plastered reveal on each side. This: looks bad, is harder to seal against rain, and requires separate window board installation. Frame depth should match wall thickness.') +
g('When ordering windows, specify: "I need frame depth of 200mm to match my 230mm wall." Most UPVC suppliers can customise frame depth. If using 100mm frame depth, specify a 100mm window board (typically granite or teak) for the inner reveal.') +
'<h4>Door Frame Size — Importance of Correct Reveal</h4>' +
t('Door frame "reveal" = the part of the door frame that sticks out from the wall surface. In Nepal, standard door frames are 100mm wide but walls are 230mm thick. This leaves a 130mm reveal that must be filled with architrave (decorative trim). Specify whether you want flush (architrave covers the gap) or colonial-style (wider decorative profile). Decide before carpentry begins — changing afterwards requires removing the frame.') +
'<h4>Ventilation Louvers for Utility/Store Rooms</h4>' +
w('Utility rooms, store rooms, and under-stair storage often have no windows. Without ventilation, these spaces become damp, develop mould, and damage stored items. Termites also prefer dark, damp, unventilated spaces.') +
g('Install fixed ventilation louvers (slatted openings that allow air but block rain) in the walls of every closed utility and store room. Minimum one louver high on the wall (for hot air exhaust) and one low (for cool air inlet). Cover with fine stainless steel mesh to prevent insects. This single step keeps these rooms dry and usable.') +
'<h4>Security Bars — Design Them Into the Structure</h4>' +
t('Ground floor window security bars (grilles) are typically added after construction as a separate afterthought. When done this way, the grilles are surface-mounted and can be pulled off. When planned during construction: the grille frame is embedded into the window opening during masonry — embedded grilles cannot be removed without breaking the wall.') +
g('Ask your mason to embed 16mm steel rods or a pre-fabricated grille frame into the window reveal during wall construction, BEFORE the window frame is installed. The window then goes inside the embedded grille frame. This is the most secure method and looks cleaner than surface-mounted grilles.')),

'phase-7.html': sec('s-critical7','🔲','Flooring — What Nobody Tells You Before You Start',
'Decisions under the tiles that affect the floor for its entire lifetime',
'<h4>Skirting — The Most Forgotten Element in Planning</h4>' +
t('Skirting = the tile, stone, or wood strip that runs along the bottom of every wall where it meets the floor. Skirting: protects the wall base from mop water, vacuum cleaners, furniture being pushed against walls, and feet. Without skirting: the wall base paint chips, plaster gets wet from mopping, and the floor-wall junction looks unfinished.') +
g('Plan skirting during the flooring phase. Standard: 100mm tall skirting tile matching or contrasting with floor tile. Skirting must be installed AFTER floor tiles but BEFORE wall paint. Most builders install floor tiles, then paint walls, then try to add skirting — which is backwards and leads to messy paint edges on tiles. Tell your mason: "Install skirting tiles before the painter starts."') +
'<h4>Subfloor Screed — What Goes Under Your Tiles</h4>' +
w('Before any tile is laid, the concrete slab surface must be covered with a screed (a thin layer of sand-cement mortar, approximately 40–60mm thick). The screed: creates a perfectly level surface for tiling, hides all structural imperfections, carries pipe/wire chases, and allows achieving the correct floor slope for bathrooms. Without screed, tiles are laid directly on rough slab — they crack, hollow, and pop within 5 years.') +
t('The screed must cure for minimum 7 days before tiles are laid. Rushing screed curing = hollow tiles = tiles popping off.') +
'<h4>Tile Layout Plan — Avoiding Ugly Cut Tiles at Entrance</h4>' +
t('Before laying any tiles, your mason should dry-lay (place without adhesive) the tiles from the centre of the main entrance room outward to find the cut pattern. The goal: entrance to every room and the most visible areas should have full tiles. Cut tiles (partial tiles) should be pushed to less visible areas (under furniture, inside wardrobes, behind doors).') +
g('Ask the mason: "Please show me the dry layout before starting." Reject any layout where a cut tile of less than half-size appears at the entrance or the most visible wall. The mason should adjust the starting point to avoid this.') +
'<h4>Height Difference Between Rooms — Plan It Now</h4>' +
t('In many houses, the floor of one room is slightly higher or lower than the adjacent room due to different screed thicknesses. Particularly: bathroom floors are lower than bedroom floors (to contain water), and sometimes kitchen floors are slightly different. These transitions must be planned and executed deliberately — not left to chance.') +
g('Tell your tile mason: "Bedroom floor to bathroom floor: 15mm step down (creates a lip that prevents water flowing out). Kitchen floor level: same as dining room." Write this on a sketch. The level transitions happen in the screed stage, not the tile stage.')),

'phase-8.html': sec('s-critical8','🎨','Paint — Problems That Appear After You Move In',
'The paint problems most common in Pokhara and exactly how to fix them before they start',
'<h4>Damp Patches After Monsoon — Diagnose Before Painting</h4>' +
w('If any wall shows a damp patch or stain, painting over it is the WORST thing to do. Paint traps the moisture inside, which causes the paint to blister and peel within weeks. The damp patch then looks worse than before.') +
g('If you see damp patches on any wall: 1) Find the source (terrace leakage? pipe behind wall? rising damp from ground?). 2) Fix the source completely. 3) Let the wall dry completely — in Pokhara weather this takes 2–4 weeks of dry weather minimum. 4) Apply anti-damp primer (Sika or equivalent). 5) Then paint. Skipping any step means repainting within 6 months.') +
'<h4>Treating Existing Cracks Before Painting</h4>' +
tbl(['Crack Type','What It Means','Treatment Before Paint'],
[['Hairline crack (< 0.5mm, surface only)','Normal settling — cosmetic only','Fill with premium wall putty, sand smooth when dry'],
 ['Medium crack (0.5–2mm, through plaster)','Possible minor settlement or drying shrinkage','Hack out V-groove, fill with polymer cement mortar, prime'],
 ['Wide crack (> 2mm, follows mortar joints)','Possible structural settlement — show engineer FIRST','Get engineer to assess — may need structural repair before painting'],
 ['Diagonal crack from corner of door/window','Classic shrinkage — common in new buildings','Fill with flexible sealant not rigid putty — allows movement']]) +
'<h4>Number of Coats — What Professionals Use</h4>' +
tbl(['Surface','Correct Application Sequence'],
[['Internal walls','1 coat wall primer → 2 coats putty (sand each) → 1 coat primer → 2 coats finish emulsion'],
 ['External walls','1 coat exterior primer → 2 coats exterior emulsion (premium brand only)'],
 ['Ceiling','1 coat ceiling primer → 2 coats white ceiling emulsion'],
 ['New metal (gate/grille)','Wire brush → red oxide primer → 2 coats enamel or epoxy']]) +
t('Total minimum coats for internal walls = 6 layers. Most contractors do 3 layers (primer + 2 coats) to save time. The difference between 3 and 6 layers is: 3 = paint lasts 3–4 years before fading and cracking. 6 = paint lasts 8–10 years.') +
'<h4>Repainting Cycle — Plan for the Future</h4>' +
t('Interior emulsion: repaint every 5–7 years. Exterior weatherproof: repaint every 3–5 years (Pokhara monsoon is harsh). Metal gates: repaint every 3 years. Budget NPR 50,000–80,000 for a full exterior repaint of your house. Do not wait until paint is peeling — repaint while surface is still intact for better adhesion and lower cost.')),

'phase-9.html': sec('s-critical9','🍳','Kitchen — Design That Survives Daily Use',
'Practical details that affect every single day you cook and work in the kitchen',
'<h4>The Kitchen Triangle — Efficiency Rule</h4>' +
t('The kitchen work triangle = the path between your three main work centres: refrigerator (storage), sink (prep/wash), and stove (cooking). The total perimeter of this triangle should be 4–8 metres. Too small = cramped. Too large = inefficient. Two people cannot cross each other\'s triangle path — this is why good kitchen design always plans for this.') +
g('Show your architect/kitchen designer this triangle for your specific L-shaped or U-shaped layout. In your plot (30ft wide, 24ft usable), the kitchen will likely be L-shaped. The ideal L-kitchen: sink on one arm, stove on the other arm, refrigerator at the corner or near the entrance to the kitchen.') +
'<h4>Load Capacity of Base Cabinets</h4>' +
w('Kitchen base cabinets must support: the weight of the countertop (granite 20mm = 50kg per sq metre), plus contents (dishes, pots, groceries), plus the force of someone leaning on the counter. Total load per metre of cabinet = 80–120kg. Cabinet carcass (body) in particle board CANNOT support this — it collapses within 2–3 years. 18mm BWR plywood is the only acceptable material.') +
'<h4>Kitchen Lighting — The Three Types You Need</h4>' +
tbl(['Light Type','Where','Why'],
[['General (ambient)','Ceiling — bright overhead','See the whole kitchen clearly'],
 ['Task (under-cabinet)','Under wall cabinets pointing at counter','No shadow when chopping — critical for safety'],
 ['Accent','Inside glass-fronted cabinets (if any)','Aesthetic — optional but premium look']]) +
t('Under-cabinet LED strip lights cost NPR 3,000–5,000 for the whole kitchen. Install them during the kitchen fitting stage — wiring must be planned into the wall during construction. These dramatically reduce eye strain during cooking and make the kitchen feel more premium.') +
'<h4>Chimney Maintenance — The Most Neglected Kitchen Item</h4>' +
t('Kitchen chimney filters must be cleaned every 2–3 months in a Nepali kitchen (high oil content in cooking). If filters are not cleaned: suction drops to near zero within 6 months, oil accumulates in the duct creating a fire risk, and the motor overloads and burns out. Budget NPR 500–1,000 per year for professional chimney cleaning.')),

'phase-10.html': sec('s-critical10','🚿','Bathrooms — What Affects Comfort Every Single Day',
'The bathroom decisions you will think about twice a day for the next 30 years',
'<h4>Instant vs Storage Geyser — Full Comparison</h4>' +
tbl(['Feature','Storage Geyser (15–35L tank)','Instant Geyser (no tank)'],
[['Hot water delivery','Takes 15–20 min to heat','Instant — hot in 5 seconds'],
 ['Electricity use','High — heats full tank even if small shower','Low — heats only water that flows'],
 ['Flow rate','Good (tank pressure = steady flow)','Limited (depends on pressure, may feel weak)'],
 ['Cost','NPR 5,000–12,000','NPR 8,000–20,000'],
 ['Reliability','Very high, simple mechanism','Good, but heating element sensitive to hard water'],
 ['Recommended for Nepal','✅ Yes — reliable, handles load shedding better','Possible but needs good water pressure']]) +
t('Recommendation for Pokhara: storage geyser (25–35 litre) in each bathroom. Simple, reliable, handles intermittent water pressure well. Instant geyser works poorly when water pressure is low — which is common in Nepal.') +
'<h4>Hard Water Impact on Bathroom Fittings</h4>' +
w('Hard water (high mineral content) destroys bathroom fittings faster than you think. Scale deposits block tap aerators within 1 year, clog showerheads within 2 years, and build up inside geyser tanks reducing capacity by 30% within 5 years.') +
g('Solution: install tap aerators that can be unscrewed and cleaned (not fixed type). Clean aerators and showerheads monthly by soaking in white vinegar for 30 minutes — removes scale completely. Use descaler tablet in geyser tank once a year. If water is very hard (above 300 ppm), install a water softener on the main supply (Phase 4 covers this).') +
'<h4>Bathroom Door — Open Outward or Inward?</h4>' +
t('Unlike other doors in the house (which should open inward), bathroom doors should open OUTWARD. Reason: if someone falls and is lying against the inward-opening door, rescuers cannot open it. An outward-opening bathroom door can always be opened from outside regardless of what is behind it on the inside.') +
g('Specify to your carpenter and door supplier: "All bathroom doors must open outward (into the corridor or bedroom, not into the bathroom)." This is especially important for the elderly parents\' bathroom on the ground floor.') +
'<h4>Ventilation — Minimum Requirements for Healthy Bathrooms</h4>' +
tbl(['Bathroom Type','Minimum Ventilation','Best Practice'],
[['Bathroom with window','1 openable window minimum','Window + exhaust fan on timer'],
 ['Internal bathroom (no window)','Exhaust fan mandatory','150mm exhaust fan running 30 min after use (use timer switch)'],
 ['Master bathroom','Window + exhaust fan','Window for natural, fan for quick exhaust']]) +
w('A bathroom without adequate ventilation develops black mould within 2 years. Mould causes: respiratory problems for the family, damage to wall paint and tiles, perpetual musty smell. Prevention cost: exhaust fan NPR 2,000–4,000. Mould removal and repainting cost: NPR 15,000–30,000.')),

'phase-11.html': sec('s-critical11','🛋️','Interiors — The Professional Handover Process',
'How to protect your money at the end of construction — the snag list process',
'<h4>Snag List — The Professional Handover Process</h4>' +
t('A "snag list" (also called a defect list or punch list) is a written document listing EVERY imperfection, incomplete item, or quality issue found in the house before final payment is made to the contractor. This is standard practice in professional construction worldwide but almost nobody does it in Nepal.') +
g('Before making your final payment to any contractor, walk through every single room systematically and write down every issue. Give the contractor this written list and pay the final amount only after EVERY item is fixed to your satisfaction. Hold back minimum 10% of the contract value as retention until all snags are resolved.') +
'<h4>What to Check on Your Snag Walk</h4>' +
tbl(['Area','What to Check'],
[['Every room','All walls plumb (use spirit level), no cracks, paint uniform, no brush marks'],
 ['All floors','No hollow tiles (tap test), grouting complete, no lippage (tiles at different heights)'],
 ['All doors','Opens/closes without sticking, locks work, door stop prevents wall damage'],
 ['All windows','Open/close smoothly, locks engage, no gaps when closed, mesh intact'],
 ['All bathrooms','Drains flow, no leaks at joints, shower pressure adequate, exhaust fan works'],
 ['Electrical','Every switch and socket tested, all MCBs labelled, earthing tested'],
 ['Plumbing','All taps open fully, no leaks under sinks, water pressure adequate at all outlets'],
 ['External','All drains clear, compound wall complete, gate opens smoothly, no exposed wire ends']]) +
'<h4>Documents to Collect Before Final Payment</h4>' +
w('Before paying the final bill to your contractor, ensure you have received all of these:') +
'<ul><li>Signed completion certificate from your structural engineer</li><li>All concrete cube test reports from the lab</li><li>Electrical earthing test report (from electrician)</li><li>Plumbing pressure test report</li><li>Waterproofing flood test photograph/report</li><li>Warranty letter from contractor (minimum 1 year for structural defects, 6 months for finishing)</li><li>All material certificates (steel MTC, cement quality certificates)</li><li>Keys to all doors, windows, lock combinations</li><li>All appliance manuals and warranty cards</li><li>Contact numbers of plumber and electrician who did the work</li></ul>' +
g('These documents are your legal protection. If a structural crack appears in Year 3, your contractor says "not my problem." With a signed completion certificate and concrete cube test reports showing correct quality, you have grounds to demand they fix it. Without documents, you have nothing.') +
'<h4>One Year Defect Liability Period</h4>' +
t('Standard in construction contracts worldwide: the contractor is responsible for fixing defects that appear within 1 year of handover at no cost to you. This is called the Defect Liability Period (DLP). Include this clause in your contract and keep the contractor\'s contact details. Within the first monsoon after moving in, check all waterproofing carefully — if any leakage appears, it must be fixed under DLP.')),

'phase-12.html': sec('s-critical12','🌿','Outdoor — Completing Your Home',
'The outdoor elements that protect the house and complete the property',
'<h4>Compound Wall Foundation — Same Standard as House</h4>' +
w('Most people treat compound wall as an afterthought and ask the mason to build it on shallow footings. A compound wall standing 1.8m tall in Pokhara\'s earthquake zone needs a proper foundation — minimum 600mm deep, with a concrete footing. A compound wall that collapses during an earthquake can injure people on the road and creates legal liability for you.') +
g('Specify to your engineer: include compound wall in the structural design. Foundation depth same as plinth beam level. Wall reinforcement: vertical 10mm rods at every 1.5m, horizontal 8mm rod every 500mm height. This compound wall will stand for 50 years and survive earthquakes.') +
'<h4>Gate Selection and Long-Term Costs</h4>' +
tbl(['Gate Type','Pros','Cons','Best For Your Plot'],
[['Manual swing gate (single/double leaf)','Cheapest, no maintenance','Takes road space when opening','Not ideal — 16ft road too narrow'],
 ['Manual sliding gate','No road space needed','Needs good track, regular maintenance','Good option'],
 ['Automated sliding gate','Convenience, security, opens remotely','Higher cost (NPR 40,000–80,000), needs electricity, maintenance','Recommended if budget allows'],
 ['Boom barrier','Vehicle-only access','No pedestrian filter','Commercial use only']]) +
t('For your 16ft road: sliding gate is the only practical option. When choosing automatic, ensure: backup battery for power cuts (standard in Nepal conditions), manual override (to open when motor fails), and get a local technician trained on the brand you buy for maintenance.') +
'<h4>Rainwater Harvesting — Turn Pokhara\'s Rain Into an Asset</h4>' +
t('Pokhara receives approximately 3,900mm of rainfall annually (one of Nepal\'s highest). Your 30×60ft (1,800 sq ft = 167 sq m) roof collects approximately 650,000 litres of rain per year. Even capturing 30% of this gives you 195,000 litres — roughly 7 months of your family\'s total water needs.') +
g('Simple system: route all roof drain pipes to your underground sump tank with a first-flush diverter (a simple device that discards the first 20 litres per rain event which contains dust — the rest is clean). Cost of adding this to your existing plumbing plan: NPR 5,000–10,000. Annual saving: reduced municipal water bill + independence from supply interruptions.') +
'<h4>Post-Construction CCTV Installation Checklist</h4>' +
tbl(['Camera Position','Coverage','Height','Type Recommended'],
[['Front gate (outward)','Road and approaching people','3m (on gate pillar top)','2MP night vision'],
 ['Front entrance (inward)','Gate area and driveway','3.5m (on house wall)','2MP night vision'],
 ['Rear (facing drainage passage)','Back boundary and passage','3m (rear wall)','2MP night vision'],
 ['Staircase interior','Internal staircase for night safety','2.5m','Standard 2MP']]) +
t('During construction: run the conduit (empty pipe) for all 4 camera positions. Add a Cat6 or coaxial cable to each position. Add a power outlet near each camera position. Cost of adding conduit during construction: NPR 2,000. Cost of adding cable routes after plastering: NPR 15,000–25,000 (wall breaking required).'))
}

# Inject sections
for filename, content in SECTIONS.items():
    try:
        with open(filename, encoding='utf-8') as f: html = f.read()
        if 's-critical' not in html and '</main>' in html:
            html = html.replace('</main>', content + '\n</main>', 1)
            with open(filename, 'w', encoding='utf-8') as f: f.write(html)
            print(f'  ✓ {filename}')
        elif 's-critical' in html:
            print(f'  skip (already has critical section): {filename}')
        else:
            print(f'  ✗ no </main>: {filename}')
    except Exception as e:
        print(f'  ✗ {filename}: {e}')
print('Done')
