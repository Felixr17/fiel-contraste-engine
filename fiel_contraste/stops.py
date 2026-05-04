"""Route metadata: map points, slugs, and image placeholder paths."""

STOPS = [
    {
        "id": "segovia",
        "name_key": "stop_name_segovia",
        "lat": 40.9482,
        "lon": -4.1184,
        "map_label_key": "map_segovia",
        "images": {
            "past": "assets/stop1_past.jpg",
            "present": "assets/stop1_present.jpg",
        },
    },
    {
        "id": "mint_museum",
        "name_key": "stop_name_mint",
        "lat": 40.4228,
        "lon": -3.6688,
        "map_label_key": "map_mint",
        "images": {
            "past": "assets/stop2_past.jpg",
            "present": "assets/stop2_present.jpg",
        },
    },
    {
        "id": "anthropology",
        "name_key": "stop_name_anthro",
        "lat": 40.4081,
        "lon": -3.6891,
        "map_label_key": "map_anthro",
        "images": {
            "past": "assets/stop3_past.jpg",
            "present": "assets/stop3_present.jpg",
        },
    },
    {
        "id": "euro_sol",
        "name_key": "stop_name_euro",
        "lat": 40.4168,
        "lon": -3.7038,
        "map_label_key": "map_euro",
        "images": {
            "past": "assets/stop4_past.jpg",
            "present": "assets/stop4_present.jpg",
        },
    },
    {
        "id": "peseta_10000",
        "name_key": "stop_name_peseta",
        "lat": 40.4187,
        "lon": -3.6944,
        "map_label_key": "map_peseta",
        "images": {
            "past": "assets/stop5_past.jpg",
            "present": "assets/stop5_present.jpg",
        },
    },
    {
        "id": "plaza_mayor",
        "name_key": "stop_name_plaza",
        "lat": 40.4155,
        "lon": -3.7075,
        "map_label_key": "map_plaza",
        "images": {
            "past": "assets/stop6_past.jpg",
            "present": "assets/stop6_present.jpg",
        },
    },
]

STOP_ORDER = [s["id"] for s in STOPS]
