"""Add smart reminders section to each of the 12 phase pages."""

import re

def tip(text): return f'<div class="tip-box" style="margin:8px 0;"><strong>💡 Smart Tip</strong>{text}</div>'
def warn(text): return f'<div class="warn-box" style="margin:8px 0;"><strong>⚠️ Important</strong>{text}</div>'
def good(text): return f'<div class="good-box" style="margin:8px 0;"><strong>✅ Do This</strong>{text}</div>'

def make_section(sid, icon, title, subtitle, body):
    return f'''
<div class="sec open" id="{sid}">
<div class="sec-head" onclick="toggle('{sid}')">
  <div class="sec-icon">{icon}</div>
  <div class="sec-title"><h3>{title}</h3><p>{subtitle}</p></div>
  <div class="sec-badge">Extra Tips</div>
  <span class="sec-arrow">▼</span>
</div>
<div class="sec-body">
{body}
</div>
</div>'''

ADDITIONS = {

'phase-0.html': make_section('s-smart0','🧠','Smart Planning — Things Most People Miss','Critical decisions before touching a single brick',
tip('Start construction between October and February in Pokhara. Avoid June–September (monsoon). Never lay foundation during monsoon — rain floods pits, weakens soil.') +
warn('Always keep a 15–20% extra budget beyond your estimate. Construction in Nepal almost always costs more than planned due to material price changes and unexpected issues.') +
tip('Register your building plan with the local municipality (Nagarpalika) BEFORE starting. Building without approval = demolition order possible. Municipal stamp on your drawings is mandatory.') +
good('Get COPIES of every document from every professional before making final payment. Soil test report, structural drawings, signed contract — everything. Keep a folder.') +
warn('Never share ownership of land with multiple people before construction. Unclear ownership causes construction to stop legally. Make sure Lal Purja is in one clear name.') +
tip('If you plan to take a bank loan, start the process 3–4 months before construction. Banks are slow. Construction cannot wait for banks.') +
good('Take out construction insurance. It covers: worker injury, theft of materials, fire, natural disaster damage during construction. Very cheap compared to cost of a claim.')),

'phase-1.html': make_section('s-smart1','🧠','Smart Foundation — Critical Checks','What experienced builders know',
warn('Check your plot for OLD wells, septic tanks, or tree roots underground before excavating. Old wells collapse. Tree roots cause foundation cracking later.') +
tip('Take photographs of foundation steel from ALL angles before concrete is poured. These photos are your permanent proof that steel was correct. Useful if disputes arise with contractor later.') +
good('Lay a 75mm (3 inch) layer of Plain Cement Concrete (PCC) at the bottom of every foundation pit BEFORE placing steel. This creates a clean, level base and prevents steel from touching soil.') +
warn('Never allow the excavator to dig deeper than the required depth by mistake — compacted soil at the base is crucial. If over-dug, fill with PCC not loose soil.') +
tip('Anti-termite treatment: apply chemical (Chlorpyrifos or similar) to the soil around and under the foundation before backfilling. In Nepal, termites destroy wood, wiring insulation, and door frames within 5 years without treatment.') +
good('Mark the exact column positions on the ground with paint or pegs BEFORE excavation begins. Verify these match the structural drawing. A 2-inch error in column position can cause structural problems.')),

'phase-2.html': make_section('s-smart2','🧠','Smart Structure — What Saves Lives','Earthquake-safe details that most contractors skip',
warn('Lintel beam (small RCC beam) is required above EVERY opening — every door, every window, every ventilator hole. Not just main doors. Even a small 6-inch ventilator needs a lintel. Without it, walls crack from the corner of every opening during earthquakes.') +
tip('Tie beams: run a horizontal RCC beam connecting all columns at each floor level. This ties the entire structure together. Without tie beams, columns act individually and fail independently during earthquakes.') +
warn('Never allow workers to add extra water to column or beam concrete "to make it flow better." This is the #1 cause of weak structures. The vibrator machine does the same job safely.') +
good('Column-beam junctions (joints): this is the most critical point in earthquake resistance. The steel ties (stirrups) at joints must be closely spaced — 75mm apart, NOT the standard 150mm. Ask your engineer specifically about "ductile detailing at joints."') +
tip('Do not allow masonry (brick/block) walls to be built directly touching columns without starter bars. Columns need "column starter bars" projecting into the wall for proper connection.') +
warn('Never cut notches or holes in beams for pipes or wires after casting. This seriously weakens the beam. All pipe and wire routes must be planned BEFORE structure is cast — run sleeves (empty pipes) inside the concrete.')),

'phase-5.html': make_section('s-smart3','🧠','Smart Waterproofing — Common Failures','Why waterproofing fails and how to prevent it',
warn('Apply waterproofing membrane only when temperature is between 10°C and 35°C. In Pokhara winter (December–February), night temperatures drop below 10°C. Cold temperatures prevent membrane from curing correctly and it will fail in the first monsoon.') +
tip('Parapet wall (the low wall at the edge of your terrace) is the most common failure point. Water collects at the parapet base. The waterproofing membrane MUST go up the parapet wall minimum 300mm (1 foot) above the terrace level.') +
good('Before applying any waterproofing, fill ALL cracks in the concrete slab with polymer-modified repair mortar. Even hairline cracks. Waterproofing membrane cannot bridge cracks — it tears there first.') +
warn('Expansion joint: if your terrace is longer than 6 metres, it needs an expansion joint (a controlled crack line with flexible filler). Without it, the slab cracks randomly from thermal expansion and tears the waterproofing.') +
tip('Test all terrace drain outlets BEFORE waterproofing begins. Pour water down each drain and confirm it flows freely. A blocked drain after waterproofing means water pools and finds the weakest point.') +
good('After the flood test passes and tiles are laid, check the underside of the slab (the ceiling of the room below) once more after the first heavy monsoon rain. A small damp patch is easier to fix early than after years of water damage.')),

'phase-3.html': make_section('s-smart4','🧠','Smart Plumbing — Details That Save Repairs','Professional plumber tricks for 30-year problem-free plumbing',
tip('Mark the exact location of every embedded pipe on a sketch/photo BEFORE plastering walls. When you need to drill a screw 5 years later, you will know exactly where pipes are and avoid puncturing them.') +
good('Gas pipe planning: decide NOW whether you will use LPG cylinder (bottle) or piped gas. If cylinder, plan the cylinder storage area (outside/well-ventilated). If piped gas in future, run an empty conduit now.') +
warn('Grease trap: kitchen drain water contains oil and grease that solidifies in pipes over years and blocks them. Install a small grease trap (interceptor) in the kitchen drain line before it connects to the main drain. Cleaning every 6 months prevents permanent blockage.') +
tip('Hot water pipe insulation in Pokhara winters: wrap ALL hot water pipes with foam lagging (pipe insulation sleeve). Without it, you wait 5 minutes for hot water while the cold water sitting in the pipe drains away. With insulation, hot water arrives in 30 seconds.') +
good('Provide an access panel (small removable section in wall or floor) at every major plumbing junction — where pipes meet, where valves are. This 30-minute extra work during construction saves wall-breaking later for every repair.') +
warn('Never use plastic flexible hose (the silver braided type) for permanent connections inside walls. Use only rigid CPVC. Flexible hoses split within 5–7 years. Use flexible hose only for the final short connection from wall to taps/toilet.')),

'phase-4.html': make_section('s-smart5','🧠','Smart Electrical — Safety and Future-Proofing','Critical electrical details for Nepal conditions',
warn('Lightning protection is critical in Pokhara — the city has high lightning frequency due to proximity to hills. Install a lightning arrester (lightning rod) on the roof connected to a proper earthing system. One lightning strike can destroy all electronics in the house and start a fire.') +
good('Label every single MCB (circuit breaker) in your distribution board with a permanent marker or label. Write what each one controls: "Bedroom 1 lights", "Kitchen sockets", "AC Bedroom 2". This seems minor but saves enormous confusion during repairs and when power cuts happen.') +
tip('Pokhara has frequent load shedding and voltage fluctuations. Install a Voltage Stabilizer on the main panel and/or individual stabilizers for sensitive equipment (refrigerator, TV, computer). Voltage fluctuations silently kill expensive appliances.') +
warn('Install a surge protector device (SPD) in your main distribution board. During monsoon storms, power surges come through the electricity supply and fry all electronics. An SPD costs little but protects everything.') +
good('Plan for battery backup (inverter/UPS) from day one. Route a separate circuit for essential lights and fan in each bedroom through the inverter output. When power cuts happen at night, these rooms still have light without any switching needed.') +
tip('Every bathroom geyser switch MUST be outside the bathroom. This is both a safety requirement and a practical one — you switch on the geyser 20 minutes before entering the bathroom, not while standing wet inside.')),

'phase-6.html': make_section('s-smart6','🧠','Smart Windows and Doors — Security and Longevity','What to check beyond size and material',
warn('Ground floor windows: install security grilles (iron/steel bars) on all windows that a person could climb through. Paint the grilles with epoxy paint to prevent rust. This is standard practice in Nepal and provides peace of mind.') +
good('All doors should swing INWARD (into the room), not outward into a corridor. Inward-swinging doors: safer (harder to force open from outside), space-efficient in narrow corridors, and the standard for all bedroom and bathroom doors.') +
tip('Door threshold: the strip at the bottom of a door frame. For elderly-friendly rooms (ground floor especially), use ZERO threshold — the floor continues flat under the door with no step up. Even a 10mm threshold causes trips for elderly people.') +
warn('Window sill slope verification: after the granite sill is installed, pour water on it. Watch which direction it flows. Water must flow OUTWARD (away from the house). If it flows inward, the sill is installed at wrong angle — rain water will enter the wall. Ask mason to correct it immediately, before it sets permanently.') +
good('All external door frames should be fixed to the wall with stainless steel frame anchors (not just mortar). In earthquake zone, door frames fixed with only mortar pop out during shaking. Steel anchors keep the frame integrated with the wall structure.') +
tip('For the main entrance door: use a door with a steel core (steel sheet inside a wood frame). Pure wood doors warp in Pokhara humidity and become difficult to close within 3–5 years. Steel core doors stay true permanently.')),

'phase-7.html': make_section('s-smart7','🧠','Smart Flooring — Professional Finishing Details','Details that separate good tiling from excellent tiling',
tip('Allow tiles to sit in the room for 24 hours before laying them. Tiles need to acclimatize to the room temperature and humidity. Tiles laid cold and then warming up expand and pop (tent) off the floor.') +
good('Floor leveling: check the floor level with a long spirit level or laser level BEFORE tiling begins. If the floor is not level, the tile layer must first apply a self-leveling compound. An uneven floor causes tiles to rock and crack at the edges.') +
warn('Grout color test: apply a small amount of grout between two tiles and let it dry completely before committing. Grout looks very different wet vs dry — usually lighter when dry. Confirm the dried color works with your tile color before grouting the whole floor.') +
tip('Expansion gaps: leave a 10mm gap around the perimeter of every room (where floor tiles meet the wall). This gap is filled with silicone sealant, not grout. Without this gap, tiles have nowhere to expand in summer heat and they crack or pop up.') +
good('Staircase nosing: the front edge of every step must have an anti-skid nosing strip. The best type has a small lip that prevents the foot from slipping forward. Colour: use a contrasting colour to the step (e.g., dark strip on light steps) so elderly people can see each step edge clearly.') +
warn('After tiling is complete and before grouting: walk over EVERY tile pressing firmly. Any tile that makes a hollow "click" sound is not bonded — it will crack under furniture or heavy footsteps. ALL hollow tiles must be re-laid before grouting.')),

'phase-8.html': make_section('s-smart8','🧠','Smart Paint — Professional Application Details','How to make paint last 10 years instead of 3',
warn('New plaster must cure for minimum 28 days before ANY paint is applied. Fresh plaster is alkaline — paint applied on fresh plaster peels within 1–2 years. In Pokhara, wait for the plaster to fully dry and show no damp patches before painting.') +
tip('Pokhara best painting months: October, November, December, January, February. These are dry months with low humidity. Avoid painting in monsoon (June–September) — paint will not dry properly and will have poor adhesion.') +
good('Paint sequence: 1) Fill all cracks and holes with putty. 2) Sand smooth when dry. 3) Apply one coat primer. 4) Let dry 4–6 hours. 5) Apply first coat emulsion. 6) Let dry 4 hours minimum. 7) Apply second coat. Never rush between coats — the most common reason paint peels early is painting the second coat too soon.') +
warn('Exterior paint: apply only between 8 AM and 4 PM. Never paint when rain is expected within 4 hours. Never paint in direct hot midday sun — the surface dries too fast before the paint can bond. Early morning and late afternoon is ideal.') +
tip('Metal gate and grille painting sequence: 1) Wire brush to remove all rust. 2) Apply red oxide primer immediately (rust reforms within hours of cleaning). 3) Let cure 24 hours. 4) Apply 2 coats of enamel paint. Without red oxide primer, metal paint peels within 1 year.') +
good('Keep leftover paint in a sealed container with the colour code written on the lid. Store away from direct sun and frost. You will need this for touch-ups after furniture is moved in and walls get scuffed.')),

'phase-9.html': make_section('s-smart9','🧠','Smart Kitchen and Wardrobes — Daily Use Details','What you only realise after living in the house for 6 months',
tip('Kitchen chimney sizing: for Nepali cooking (high flame, lot of frying and spices), you need minimum 1000 m³/hour suction capacity. Standard 600 m³/hour chimneys are undersized for this cooking style and will not remove smell fully. Ask specifically for "1000 m³/hr" when buying.') +
warn('Counter height should be personalised. Standard is 850mm but this is based on average international heights. Measure the primary cook in your family: elbow height when standing minus 100–150mm = ideal counter height. If your mother is 155cm tall, 820mm counter is better for her.') +
good('Install under-counter LED strip lights (pointing downward toward the counter). This illuminates the work surface directly without any shadow. Night cooking becomes dramatically easier. This costs very little if wiring is planned before kitchen is installed.') +
tip('LPG gas cylinder location: plan a dedicated, ventilated space for gas cylinders OUTSIDE the kitchen or in a separate vented cabinet. Gas cylinders in enclosed kitchen spaces are a fire risk. Many Pokhara kitchens keep cylinders outside the window — this works well.') +
warn('Wardrobe hanging rail strength: use 25mm diameter steel tube for the hanging rail, not plastic or thin rod. Suits and heavy jackets can weigh 5–8 kg each, and a full wardrobe rail carries 30–50 kg. Thin rods sag and fall within 2 years. Steel tube never sags.') +
good('Wardrobe interior: line the base of the wardrobe with cedar wood strips or place cedar blocks inside. Cedar naturally repels moths and silverfish (which eat woollen suits and shawls) and keeps clothes smelling fresh. No chemicals needed.')),

'phase-10.html': make_section('s-smart10','🧠','Smart Bathrooms — Long-Term Comfort','Details that make bathrooms work perfectly for 20 years',
tip('Geyser size guide: 15 litre geyser = only enough for one quick shower. 25 litre = sufficient for one full shower with washing. 35 litre = two people can shower back to back. For your parents (ground floor), install 35 litre. For other bathrooms, 25 litre is fine.') +
warn('Geyser installation height: mount it as high as possible on the wall (close to ceiling). Hot water pressure is better when the geyser is higher than the shower. If the geyser is low, shower pressure becomes weak — especially noticeable when the tank is partially heated.') +
good('Install a pressure relief valve (PRV) on every geyser. This is the small valve that releases pressure if the geyser overheats. Without PRV, a malfunctioning geyser can burst. This is mandatory safety equipment — check your electrician installs it.') +
tip('Mirror positioning: mount bathroom mirror so that the CENTER of the mirror is at average eye height of your family (typically 155–165cm from floor for most Nepali families). A mirror mounted too high or too low is uncomfortable daily.') +
warn('Exhaust fan must discharge OUTSIDE the house — not into the ceiling void (between ceiling and slab). Exhausting into the ceiling void creates moisture, mould, and breeding ground for insects. Run the exhaust fan duct directly through the wall or roof to outside air.') +
good('For elderly bathroom (parents room): install a fold-down shower seat or provision for one. This allows showering while seated which becomes necessary after any health issue, surgery, or in old age. The wall provision (embedded mounting plates) costs nothing now; the seat can be added later.')),

'phase-11.html': make_section('s-smart11','🧠','Smart Interiors — Move In Ready','Lessons from people who have lived in new houses',
tip('Move into the house for 3 MONTHS before buying all final furniture. You will discover which corners are unused, where natural light actually falls, where you actually sit, and what storage you actually need. Most people who furnish immediately regret several purchases.') +
warn('Air conditioner placement: do NOT install AC directly above where people sit, sleep, or eat. Cold air blowing directly on a person for hours causes health problems. Mount AC on the wall so that cold air blows along the length of the room, not directly down on furniture.') +
good('False ceiling: only install where genuinely needed — to hide visible pipes, ugly beam soffits, or wire clusters. A full false ceiling throughout the house reduces room height, reduces ventilation, and adds significant cost. Minimal use is smarter.') +
tip('Furniture buying sequence: Buy in this order for best results: 1) Essential beds and dining first (so you can live). 2) Wait 2 months. 3) Kitchen cabinetry. 4) Wait 1 month. 5) Sofas and storage. 6) Decorative items last — buy these over years, not all at once.') +
warn('Storage for important documents: install a small hidden safe (wall safe or floor safe) in the master bedroom or study. Store: Lal Purja original, passport, birth certificates, property documents. Do not keep originals in an easily accessible place.') +
good('Internet/data points: before closing walls, install Cat6 data cable to every room — living room (2 points), bedrooms (1 each), study (2 points), and one outdoor point for potential CCTV or gate camera. Wireless is convenient but wired internet is 10x more reliable for working from home.')),

'phase-12.html': make_section('s-smart12','🧠','Smart Outdoor — Security, Safety, and Future Use','The outside of your house is the first and last impression',
warn('Compound wall height: minimum 1.8 metres (6 feet) for privacy and security. In Nepal building regulations, compound walls up to 1.5–1.8m typically do not need special structural design. Check your municipality\'s rules for exact allowed height in your area.') +
tip('Gate recommendation for 16ft road: sliding gate (moves sideways along the wall) is better than swing gate (opens outward) for a narrow road. A swing gate opening outward into a 16ft road blocks passing traffic and causes daily friction with neighbours.') +
good('CCTV camera positions for your plot: 1) Front gate (pointing at entrance), 2) Back/rear (covering the drainage passage side), 3) One covering the main entrance door. These three positions give complete coverage. Route conduit for camera cables during construction even if you do not install cameras immediately.') +
warn('Driveway/parking slope: the area in front of your gate (within the 8ft setback) should slope AWAY from the house — toward the road. If it slopes toward the house, rainwater pools against the compound wall and enters the foundation. Slope minimum 1:40 away from house.') +
tip('Rainwater harvesting: route your roof drain pipes to your underground sump tank instead of to the drain. In Pokhara with heavy monsoon, you can collect 50,000–80,000 litres of rainwater during monsoon season. This is free, clean water for the rest of the year and reduces water bills significantly.') +
good('Solar panel readiness: even if not installing solar now, during construction embed four anchor points on the south-facing roof slope (for solar panel mounting), run a 6mm copper conduit from roof to your main electrical panel, and ensure the roof structure is designed to carry 150kg extra load. Adding solar later then costs 5% of what it costs without preparation.'))

}

# Inject each addition into the respective page
for filename, content in ADDITIONS.items():
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    # Insert before </main>
    if '</main>' in html and 's-smart' not in html:
        html = html.replace('</main>', content + '\n</main>')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {filename}')
    elif 's-smart' in html:
        print(f'  skip (already has smart section): {filename}')
    else:
        print(f'  ✗ no </main> found: {filename}')

print('\nDone — smart content added to all 12 phase pages')
