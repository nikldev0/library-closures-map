import csv
import time
import requests  # <-- now available after you installed it

INPUT  = "library_closures_since_2010.csv"
OUTPUT = "libraries_2010_geo.csv"


def geocode(postcode: str):
    """Return (lat, lon) for a UK postcode using postcodes.io."""
    url = f"https://api.postcodes.io/postcodes/{postcode}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data["status"] == 200:
                return data["result"]["latitude"], data["result"]["longitude"]
    except requests.RequestException as e:
        print(f"Request error for {postcode}: {e}")
    return None, None


# ----------------------------------------------------------------------
# Main processing loop
# ----------------------------------------------------------------------
with open(INPUT, newline="", encoding="utf-8") as src, \
     open(OUTPUT, "w", newline="", encoding="utf-8") as dst:

    reader = csv.DictReader(src)
    fieldnames = reader.fieldnames + ["lat", "lon"]
    writer = csv.DictWriter(dst, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Remove any whitespace inside the postcode (e.g., "SW1A 1AA" → "SW1A1AA")
        cleaned_pc = row["Postcode"].replace(" ", "")
        lat, lon = geocode(cleaned_pc)
        row["lat"], row["lon"] = lat, lon
        writer.writerow(row)

        # Respect the free API’s rate limit
        time.sleep(0.1)

print(f"Finished – output written to {OUTPUT}")
