function updateTime() {
    // Get the current time
    var currentTime = new Date();

    // Format the time as HH:MM:SS
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();

    // Add leading zeros if necessary
    hours = (hours < 10 ? "0" : "") + hours;
    minutes = (minutes < 10 ? "0" : "") + minutes;
    seconds = (seconds < 10 ? "0" : "") + seconds;

    // Construct the time string
    var timeString = hours + ":" + minutes + ":" + seconds;

    // Update the content of the span element
    document.getElementById('time').textContent = timeString;
}

// Call updateTime every second to update the time
setInterval(updateTime, 1000);

// Call updateTime once initially to avoid initial delay
updateTime();

/* adding the sections */
let username = "Guest";
eel.getUsername()().then(function(name) {
    username = name;
    document.getElementById("username").innerHTML = username;
}).catch(function(error) {
    console.error("Error fetching data:", error);
});