document.getElementById("getRoutesBtn").addEventListener("click", async function() {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;

    if (!origin || !destination) {
        alert("Please enter both origin and destination.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/getRoutes?origin=${origin}&destination=${destination}`);
        const data = await response.json();

        if (data.error) {
            alert("Error fetching routes.");
            return;
        }

        document.getElementById("taxiDetails").innerHTML = `
            <h3>🚖 Taxi</h3>
            <p>Distance: ${data.taxi.distance} km</p>
            <p>Time: ${data.taxi.time} mins</p>
            <p>Fare: ${data.taxi.fare}</p>
        `;

        document.getElementById("busDetails").innerHTML = `
            <h3>🚌 Bus</h3>
            <p>Distance: ${data.bus.distance} km</p>
            <p>Time: ${data.bus.time} mins</p>
            <p>Fare: ${data.bus.fare}</p>
        `;

        document.getElementById("bikeDetails").innerHTML = `
            <h3>🏍️ Bike</h3>
            <p>Distance: ${data.bike.distance} km</p>
            <p>Time: ${data.bike.time} mins</p>
            <p>Fare: ${data.bike.fare}</p>
        `;

        document.getElementById("mixedDetails").innerHTML = `
            <h3>🚆🚌🛺 Mixed Transport</h3>
            <p>Distance: ${data.mixed.distance} km</p>
            <p>Time: ${data.mixed.time} mins</p>
            <p>Fare: ${data.mixed.fare}</p>
        `;

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to fetch routes.");
    }
});
