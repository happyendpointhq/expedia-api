"""Search hotels in a city for real dates, then open the cheapest one.

    python quickstart.py "new york"
"""

import sys

from client import find, get, nightly_with_taxes, stay

query = sys.argv[1] if len(sys.argv) > 1 else "new york"
nights = 3
check_in, check_out = stay(days_ahead=30, nights=nights)

# 1. Every hotel search takes a region_id from /locations.
place = find(query, kinds=("CITY", "MULTICITY"))
print(f"{place['full_name']} -> region_id {place['region_id']}")

# 2. Cheapest first for 2 adults, 3 nights, 30 days out. Totals include taxes and fees.
#    A city region reaches past the city: the cheapest "New York" rows are often in New
#    Jersey, so the state is printed too. Use a neighbourhood region_id to stay inside.
results = get(
    "/hotels/search",
    region_id=place["region_id"],
    check_in=check_in,
    check_out=check_out,
    adults=2,
    sort="price_low_to_high",
)
print(f"{results['result_count']['label']} for {check_in} to {check_out}\n")
for hotel in results["hotels"][:10]:
    rating = hotel.get("guest_rating") or {}
    score = f"{rating['score']}/10 ({rating['review_count']})" if rating.get("score") else "no rating"
    kind = hotel.get("unit_details") or f"{hotel.get('star_rating') or '?'} star"
    print(f"${hotel['price']['total']:>9,.2f} total  ${nightly_with_taxes(hotel, nights):>7,.2f}/night  "
          f"{score:<15} {kind[:22]:<22} {(hotel.get('address') or {}).get('region') or '':<3} {hotel['name']}")

# 3. The full record of the cheapest hotel: address, check-in rules and any fees paid at
#    the property.
first = results["hotels"][0]
details = get("/hotels/details", hotel_id=first["hotel_id"])
policies = details.get("policies") or {}
print(f"\n{details['name']} ({'vacation rental' if details.get('is_vacation_rental') else 'hotel'})")
print(f"  {(details.get('address') or {}).get('line')}")
print(f"  check-in from {(policies.get('check_in') or {}).get('start_time')}, "
      f"check-out {(policies.get('check_out') or {}).get('time')}")
# The fee list mixes headings with charges; the charges are the lines with an amount.
for fee in (details.get("fees") or {}).get("mandatory") or []:
    if any(ch.isdigit() for ch in fee):
        print(f"  paid at the property: {fee[:100]}")
print(first["url"])
