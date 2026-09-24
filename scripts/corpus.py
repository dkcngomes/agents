"""Shared paddy corpus. Facts sourced from the Sri Lanka Department of Agriculture
(Rice Research and Development Institute), doa.gov.lk. Kept short and chunk-shaped
on purpose: each entry is one retrievable idea."""

DOCS = [
    {
        "id": "var-3month",
        "category": "variety",
        "source": "RRDI — Rice varieties, 3 month age class",
        "text": "Three-month age class rice varieties released in Sri Lanka include Bg 300, Bg 301, "
                "Bw 302, At 303, Bg 304, Bg 305, At 306 and At 307. These mature in roughly 90 days and "
                "are chosen when the season is short or water is likely to run out early.",
    },
    {
        "id": "var-3.5month",
        "category": "variety",
        "source": "RRDI — Rice varieties, 3.5 month age class",
        "text": "Three-and-a-half-month age class varieties include Bg 350, Bw 351, Bg 352, At 353, "
                "At 354, Ld 355, Ld 356, Bg 357, Bg 358, Bg 359, Bg 360, Bw 361, At 362, Bw 363 and Bw 364. "
                "The 3.5 month group is the most widely planted in Sri Lanka, covering about 73% of "
                "cultivated area in 2023.",
    },
    {
        "id": "var-4month",
        "category": "variety",
        "source": "RRDI — Rice varieties, 4 month age class",
        "text": "Four-month age class varieties include Bw 400, Bg 401, At 402, Bg 403, Bg 405 and the "
                "hybrid Bg 407(H). Four-and-a-half-month varieties include Bg 379-2, Bg 11-11, Bg 450, "
                "Bw 451, Bw 452 and Bw 453.",
    },
    {
        "id": "var-popular",
        "category": "variety",
        "source": "RRDI — Varietal adoption 2023",
        "text": "By cultivated extent in 2023 the most adopted single varieties were At 362 at 14.25% and "
                "Bg 352 at 12.84%. Long grain varieties accounted for 73% of extent and white-pericarp "
                "varieties for 80%.",
    },
    {
        "id": "fert-3month",
        "category": "fertilizer",
        "source": "RRDI — Fertilizer recommendation, irrigated, Intermediate and Dry Zone, 3 month varieties",
        "text": "For a THREE MONTH age class variety under irrigation in the Intermediate or Dry Zone, apply "
                "urea as follows, timed from the date of establishment: 55 kg/ha basal, 50 kg/ha at 2 weeks, "
                "75 kg/ha at 4 weeks, 65 kg/ha at 6 weeks and 35 kg/ha at 7 weeks. Total urea is 225 kg/ha. "
                "TSP is 25 kg/ha at 4 weeks and 35 kg/ha at 6 weeks, total 55 kg/ha. MOP total is 60 kg/ha. "
                "Zinc sulphate is 5 kg/ha applied basally.",
    },
    {
        "id": "fert-3.5month",
        "category": "fertilizer",
        "source": "RRDI — Fertilizer recommendation, irrigated, Intermediate and Dry Zone, 3.5 month varieties",
        "text": "For a THREE AND A HALF MONTH age class variety under irrigation in the Intermediate or Dry "
                "Zone the urea amounts are identical to the three month schedule — 55 kg/ha basal, 50 kg/ha "
                "at 2 weeks, 75 kg/ha at 4 weeks, 65 kg/ha at 6 weeks — but the final 35 kg/ha top dressing "
                "is applied at 8 weeks instead of 7 weeks, because the crop takes longer to reach panicle "
                "initiation. Total urea is again 225 kg/ha.",
    },
    {
        "id": "fert-zinc",
        "category": "fertilizer",
        "source": "RRDI — Micronutrients",
        "text": "Zinc sulphate at 5 kg/ha is applied basally in the irrigated Intermediate and Dry Zone "
                "recommendation. Zinc deficiency shows as bronzing and stunting in young plants, most often "
                "on alkaline or heavily levelled soils.",
    },
    {
        "id": "seed-rate",
        "category": "establishment",
        "source": "RRDI — Direct sowing, seed rate",
        "text": "Recommended seed paddy rate for direct sowing depends on grain size. For medium grain "
                "varieties, 23 to 25 g per 1000 seeds, use about 100 kg/ha. For small grained Samba types, "
                "use about 75 to 80 kg/ha. Sowing heavier than this wastes seed and raises lodging risk "
                "without raising yield.",
    },
    {
        "id": "panicle-target",
        "category": "establishment",
        "source": "RRDI — Crop density",
        "text": "The potential yield of a healthy rice crop corresponds to roughly 350 to 400 panicles per "
                "square metre. Counting panicles in a quarter square metre frame at maturity is the simplest "
                "field check of whether establishment was adequate.",
    },
    {
        "id": "water-seeding",
        "category": "establishment",
        "source": "RRDI — Modified water seeding method",
        "text": "In the modified water seeding method, seed is soaked in water for 24 hours and incubated for "
                "48 hours before sowing. The field must be properly levelled to hold a shallow water depth of "
                "2 to 2.5 cm at sowing, held at that level until 7 to 10 days after sowing, then raised to "
                "4 to 5 cm as in normal irrigated conditions.",
    },
    {
        "id": "water-seeding-weeds",
        "category": "establishment",
        "source": "RRDI — Modified water seeding, weed control",
        "text": "Modified water seeding suppresses weeds without herbicide because rice tolerates anaerobic "
                "germination and most grasses and sedges do not. Herbicide application for grasses and sedges "
                "is therefore not required. Aquatic weeds may still appear and can be treated with a suitable "
                "herbicide at 2 to 3 weeks after sowing.",
    },
    {
        "id": "water-seeding-varieties",
        "category": "variety",
        "source": "RRDI — Modified water seeding, suitable varieties",
        "text": "Varieties suited to modified water seeding include Bg 300, At 308, Bg 310, Bw 351, Bw 367, "
                "Bg 366, Bg 380 and Bg 379-2. Bg 300 is identified as particularly suitable for this method.",
    },
    {
        "id": "seed-quality",
        "category": "establishment",
        "source": "RRDI — Seed quality",
        "text": "Certified seed paddy with a germination percentage above 85% should be used. Seed below that "
                "threshold gives patchy establishment that no amount of later fertilizer will correct.",
    },
    {
        "id": "seasons",
        "category": "season",
        "source": "DOA — Cultivation seasons",
        "text": "Sri Lanka has two paddy seasons. Maha runs roughly September to March on the north-east "
                "monsoon and is the major season with more reliable rainfall. Yala runs roughly May to August "
                "on the south-west monsoon, is the minor season, and depends much more heavily on irrigation "
                "in the Dry Zone.",
    },
    {
        "id": "land-prep-water",
        "category": "water",
        "source": "RRDI — Water management, land preparation",
        "text": "The highest water use in the whole rice crop is during land preparation. Keeping land "
                "preparation short and timing it to capture rainfall at the right point in the season is the "
                "single largest saving available in irrigation water use.",
    },
    {
        "id": "maturity-adoption",
        "category": "season",
        "source": "RRDI — Socio-economics",
        "text": "The 3.5 month maturity age group was adopted on 73% of cultivated area in 2023. Age class "
                "drives the fertilizer schedule, the irrigation calendar and the harvest date, so it is the "
                "first thing to establish about any paddy field before giving advice.",
    },
]

QUESTIONS = {
    "cold_open": "I am growing Bg 300 under irrigation in the Dry Zone. Exactly how much urea should I apply, "
                 "and at what times? Give me the schedule in kg per hectare.",
    "contrast": "And what changes if I switch to Bg 352 instead?",
    "no_tool": "Hi! What sort of questions can you help me with?",
}