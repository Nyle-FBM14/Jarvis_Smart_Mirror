//DAILY EVENTS
function updateCalendarSection(daily_events){
    let times = ["12AM", "1AM", "2AM", "3AM", "4AM", "5AM", "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM", "11PM"];
    let calendar_section = document.getElementById("calendar_section");
    calendar_section.innerHTML = "";
    for(let i = 0; i < daily_events.length; i++){
        fetch(`./event.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            //fill out placeholders
            if(daily_events[i]['dates'].length > 1){
                html = html.replace(/\[event_end_var\]/g, "continued");
            }
            else if(daily_events[i]['time_slots'][daily_events[i]['time_slots'].length - 1] == 12){
                html = html.replace(/\[event_end_var\]/g, "12AM");
            }
            else{
                html = html.replace(/\[event_end_var\]/g, times[daily_events[i]['time_slots'][daily_events[i]['time_slots'].length - 1] + 1]);
            }
            html = html.replace(/\[event_var\]/g, daily_events[i]['title']);
            html = html.replace(/\[event_start_var\]/g, times[daily_events[i]['time_slots'][0]]);
            html = html.replace(/\[event_location_var\]/g, daily_events[i]['location']);

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
eel.expose(openWeekView);
function openWeekView() {
    let calendar_section = document.getElementById("calendar_section");
    calendar_section.innerHTML = "";
    fetch(`./weekView.html`)
    .then(res => {
        if(res.ok) {
            return res.text();
        }
    }).then(html => {
        calendar_section.innerHTML = html;
    });
}
//INITIALIZE MAIN PAGE
updateDailyEventsData();

eel.expose(reloadMainPage); //can move to main.js if other sections implement an expanded view
function reloadMainPage() {
    updateDailyEventsData();
}