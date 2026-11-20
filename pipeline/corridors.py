"""
The transit network this demonstration draws.

Corridor names, modes, project phases and station-area names are real Twin Cities
facts. The geometry is schematic: coordinates live in a 0-100 space that puts each
corridor roughly where it belongs relative to the two downtowns, so the map reads
correctly without pretending to be survey-accurate.

Downtown Minneapolis sits at about (38, 44). Downtown Saint Paul at about (58, 47).
"""

# Each corridor carries: the name the Council uses, the mode, the project phase as
# of the analysis period, the schematic path, and its station areas in order.
CORRIDORS = [
    {
        "id": "blue",
        "name": "METRO Blue Line",
        "mode": "LRT",
        "phase": "operation",
        "path": [[38, 44], [40, 49], [42, 54], [45, 59], [46, 63], [47, 67]],
        "stations": [
            "Downtown East", "Cedar-Riverside", "Franklin Av", "Lake St / Midtown",
            "38th St", "46th St", "50th St / Minnehaha", "VA Medical Center",
            "Fort Snelling", "Terminal 1", "Bloomington Central", "Mall of America",
        ],
    },
    {
        "id": "green",
        "name": "METRO Green Line",
        "mode": "LRT",
        "phase": "operation",
        "path": [[38, 44], [42, 44.6], [46, 45.2], [50, 45.9], [54, 46.4], [58, 47]],
        "stations": [
            "West Bank", "Stadium Village", "Prospect Park", "Westgate", "Raymond Av",
            "Fairview Av", "Snelling Av", "Hamline Av", "Lexington Pkwy", "Victoria St",
            "Dale St", "Western Av", "Capitol / Rice St", "Union Depot",
        ],
    },
    {
        "id": "swlrt",
        "name": "METRO Green Line Extension",
        "mode": "LRT",
        "phase": "construction",
        "path": [[38, 44], [34, 44.8], [30, 45.6], [26, 46.4], [22, 47.6], [19, 49]],
        "stations": [
            "Bryn Mawr", "West Lake St", "Beltline Blvd", "Wooddale Av", "Louisiana Av",
            "Downtown Hopkins", "Shady Oak", "Opus", "City West", "Eden Prairie Town Center",
        ],
    },
    {
        "id": "bottin",
        "name": "METRO Blue Line Extension",
        "mode": "LRT",
        "phase": "pre-development",
        "path": [[38, 44], [36, 40], [34.5, 36], [33, 32], [31, 28.5]],
        "stations": [
            "Plymouth Av", "Penn Av", "Robbinsdale", "Bass Lake Rd", "63rd Av",
            "Brooklyn Blvd", "Oak Grove Pkwy",
        ],
    },
    {
        "id": "gold",
        "name": "METRO Gold Line",
        "mode": "BRT",
        "phase": "operation",
        "path": [[58, 47], [62, 47], [66, 47.4], [70, 47.8], [73, 48.2]],
        "stations": [
            "Mounds Blvd", "Earl St", "Etna St", "White Bear Av", "Sun Ray",
            "3M", "Maplewood", "Woodbury Theatre",
        ],
    },
    {
        "id": "orange",
        "name": "METRO Orange Line",
        "mode": "BRT",
        "phase": "operation",
        "path": [[38, 44], [39.5, 49], [41, 55], [42.5, 61], [44, 68]],
        "stations": [
            "12th St", "Lake St / I-35W", "46th St / I-35W", "66th St",
            "American Blvd", "Knox Av", "Burnsville Center",
        ],
    },
    {
        "id": "aline",
        "name": "METRO A Line",
        "mode": "BRT",
        "phase": "operation",
        "path": [[51, 37], [51, 41], [50.5, 45.4], [50, 50], [49.6, 54]],
        "stations": [
            "Rosedale", "County Rd B", "Como Av", "Hewitt Av", "Snelling / University",
            "Selby Av", "Grand Av", "Randolph Av", "46th St Station",
        ],
    },
    {
        "id": "cline",
        "name": "METRO C Line",
        "mode": "BRT",
        "phase": "operation",
        "path": [[38, 44], [36.6, 40], [35.4, 36], [34.2, 32.5]],
        "stations": [
            "Olson Mem Hwy", "Plymouth Av", "Golden Valley Rd", "Lowry Av",
            "Dowling Av", "Brooklyn Center",
        ],
    },
    {
        "id": "dline",
        "name": "METRO D Line",
        "mode": "BRT",
        "phase": "planning",
        "path": [[34.2, 32.5], [36, 38], [38, 44], [39, 50], [40, 56], [41, 62]],
        "stations": [
            "Brooklyn Center", "Emerson / Fremont", "Penn / Lowry", "7th St N",
            "Chicago / Lake", "Chicago / 38th", "Bloomington Av", "Mall of America",
        ],
    },
]

# Comparable places without high-frequency transit. The analysis compares corridor
# movement against these, which is what separates displacement from base mobility.
CONTROL_CORRIDORS = [
    {"id": "ctl-ne", "name": "Control - NE Ramsey",   "path": [[60, 38], [65, 35], [70, 32.5]]},
    {"id": "ctl-sw", "name": "Control - SW Hennepin", "path": [[26, 56], [22, 60], [19, 64]]},
    {"id": "ctl-se", "name": "Control - S Dakota",    "path": [[55, 62], [59, 66], [62, 70]]},
    {"id": "ctl-nw", "name": "Control - NW Anoka",    "path": [[42, 24], [46, 21], [50, 19]]},
]

PHASES = ["pre-development", "planning", "construction", "operation"]

FIRST_YEAR = 2008
LAST_YEAR = 2025
