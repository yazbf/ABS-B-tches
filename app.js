const map = L.map('map').setView([52.0, 5.0], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const trajectories = {};
const markers = {};

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

        const prediction = await response.json();

        console.log(prediction);

        if (prediction.error)
            return;

        // Remove old line
        if (trajectories[icao]) {
            map.removeLayer(trajectories[icao]);
        }

        trajectories[icao] = L.polyline([
            prediction.start,
            prediction.end
        ], {
            color: 'red'
        }).addTo(map);
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

markers[icao].on("click", async () => {

    const response = await fetch(
        `http://127.0.0.1:8000/predict/${icao}`
    );

    const prediction = await response.json();

    console.log(prediction);
});