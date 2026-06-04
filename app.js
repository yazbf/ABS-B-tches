const map = L.map('map').setView([52.0, 5.0], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const trajectories = {};
const markers = {};
const explosions = {};

//defined once at the top, not recreated every second
const explosionIcon = L.icon({
    iconUrl: 'explosion/Preview.gif', //found on itchio shoutout to https://ansimuz.itch.io/explosion-animations-pack
    iconSize: [80, 80],
    iconAnchor: [40, 40],
});

function showExplosion(icao, lat, lon) {
    if (explosions[icao]) {
        map.removeLayer(explosions[icao]);
    }

    explosions[icao] = L.marker([lat, lon], {
        icon: explosionIcon,
        zIndexOffset: 1000 //on top of everything else
    }).addTo(map);

    // Create a fresh Audio each time so overlapping explosions work fine
    const crashSound = new Audio('explosion/explosions.wav'); // sound remixed by me but taken from freesound.org
    crashSound.play();

    setTimeout(() => {
        if (explosions[icao]) {
            map.removeLayer(explosions[icao]);
            delete explosions[icao];
        }
    }, 3000); // tune to match gif length
}

async function updatePlanes() {
    const response = await fetch("http://127.0.0.1:8000/planes");
    const planes = await response.json();

    for (const [icao, plane] of Object.entries(planes)) {

        if (!plane.latitude || !plane.longitude)
            continue;

        if (!markers[icao]) {

            markers[icao] = L.marker([
                plane.latitude,
                plane.longitude
            ]).addTo(map);

            markers[icao].on("click", async () => {

                const response = await fetch(
                    `http://127.0.0.1:8000/predict/${icao}`
                );

                const prediction = await response.json(); //{start: [lat, lng], end: [lat, lng], fall_time_s: seconds until impact}

                if (prediction.error)
                    return;

                //remove old trajectory line since plane crashed
                if (trajectories[icao]) {
                    map.removeLayer(trajectories[icao]);
                }

                trajectories[icao] = L.polyline([
                    prediction.start,
                    prediction.end
                ], {
                    color: 'red'
                }).addTo(map);

                // Wait for the plane to "travel" the trajectory, then boom! from the prediction, fall_time_s is the time until impact, if not provided default to 3 seconds for dramatic effect
                const delayMs = (prediction.fall_time_s ?? 3) * 1000;

                setTimeout(() => {
                    //remove the trajectory line
                    if (trajectories[icao]) {
                        map.removeLayer(trajectories[icao]);
                        delete trajectories[icao];
                    }

                    //show explosion at crash site
                    const [endLat, endLng] = prediction.end;
                    showExplosion(icao, endLat, endLng);

                }, delayMs);
            });
        }

        markers[icao].bindPopup(`
            <b>${plane.callsign || "Unknown"}</b><br>
            Altitude: ${plane.altitude || "?"} ft<br>
            Speed: ${plane.speed || "?"} knots
        `);
    }
}

setInterval(updatePlanes, 1000);