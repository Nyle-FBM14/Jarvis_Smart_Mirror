//DAILY EVENTS
function updateCalendarSection(daily_events){
    let calendar_section = document.getElementById("calendar_section");
    calendar_section.innerHTML = "";
    let header = document.createElement("h1");
    header.innerHTML = "Today's Events";
    for(let i = 0; i < daily_events.length; i++){
        fetch(`../event.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            //fill out placeholders
            html = html.replace(/\[event_var\]/g, daily_events[i]['title']);
            html = html.replace(/\[event_start_var\]/g, daily_events[i]['start']);
            html = html.replace(/\[event_end_var\]/g, daily_events[i]['end']);
            if(daily_events[i]['location'] != null){
                html = html.replace(/\[event_location_var\]/g, daily_events[i]['location']);
            }
            else{
                html = html.replace(/\[event_location_var\]/g, "Unavailable");
            }
            

            let temp = document.createElement('div');
            temp.style.border = "solid 1px #E28DA8";
            temp.style.borderRadius = "25px";
            temp.style.marginTop = "5px";
            temp.style.maxHeight = "120px";
            temp.style.padding = "5px 0px 5px 20px";
            temp.innerHTML = html;
            calendar_section.appendChild(temp);
            
        });
    }
}

eel.expose(updateDailyEventsData);
function updateDailyEventsData() {
    eel.getDayEvents()().then(function(daily_events) {
        updateCalendarSection(daily_events);
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}

//WEEKLY EVENTS
function updateWeekView(events){
    for(let i = 0; i < events.length; i++){
        let weekday = events[i]['weekday'];
        let time = events[i]['time'];
        let cell_id = `${weekday}_${time}`;
        console.log(cell_id)
        let cell = document.getElementById(cell_id);
        cell.innerHTML = "";
        fetch(`../event.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            //fill out placeholders
            html = html.replace(/\[event_var\]/g, events[i]['title']);
            html = html.replace(/\[event_start_var\]/g, events[i]['start']);
            html = html.replace(/\[event_end_var\]/g, events[i]['end']);
            if(events[i]['location'] != null){
                html = html.replace(/\[event_location_var\]/g, events[i]['location']);
            }
            else{
                html = html.replace(/\[event_location_var\]/g, "Unavailable");
            }
            

            let temp = document.createElement('div');
            temp.style.border = "solid 1px #E28DA8";
            temp.style.borderRadius = "25px";
            temp.style.marginTop = "5px";
            temp.style.maxHeight = "120px";
            temp.style.padding = "5px 0px 5px 20px";
            temp.innerHTML = html;
            cell.appendChild(temp);
            
        });
    }
}
eel.expose(openWeekView);
function openWeekView() {
    let weekView = document.getElementById("calendar_week");
    weekView.style.display = "block";
    eel.getWeekEvents()().then(function(weekly_events) {
        updateWeekView(weekly_events);
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}
//INITIALIZE MAIN PAGE
updateDailyEventsData();

eel.expose(reloadMainPage); //can move to main.js if other sections implement an expanded view, this just closes week view
function reloadMainPage() {
    let weekView = document.getElementById("calendar_week");
    weekView.style.display = "none";
}