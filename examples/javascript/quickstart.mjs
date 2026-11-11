// Expedia API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs "new york"

const HOST = 'expedia18.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Expedia API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const query = process.argv[2] ?? 'new york';
const day = (offset) => new Date(Date.now() + offset * 86400000).toISOString().slice(0, 10);
const [checkIn, checkOut] = [day(30), day(33)];

// Hotel searches take a region_id from /locations. Ids are strings: keep them that way.
const { results } = await get('/locations', { query, type: 'hotels' });
const place = results.find((row) => row.type === 'CITY' || row.type === 'MULTICITY');
if (!place) throw new Error(`No Expedia city matches ${query}`);

// Send dates: without them the price is for a one-night stay Expedia picks.
const search = await get('/hotels/search', {
  region_id: place.region_id,
  check_in: checkIn,
  check_out: checkOut,
  adults: 2,
  sort: 'price_low_to_high',
});
console.log(`${place.full_name}: ${search.result_count.label}, ${checkIn} to ${checkOut}`);
for (const hotel of search.hotels.slice(0, 10)) {
  // price.total includes taxes and fees; price.per_night does not.
  console.log(`${hotel.price.total_formatted.padStart(14)}  ${hotel.name}`);
}
