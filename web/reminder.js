function updateReminderSection(incomplete_tasks){
    let reminder_section = document.getElementById("reminders_list");
    reminder_section.innerHTML = "";
    for(let i = 0; i < incomplete_tasks.length; i++){
        fetch(`./reminders.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            html = html.replace(/\[reminder_var\]/g, incomplete_tasks[i]);
            
            let temp = document.createElement('div');
            temp.style.display = "flex";
            temp.innerHTML = html;
            reminder_section.appendChild(temp);
        });
    }
}

eel.expose(updateReminderData);
function updateReminderData() {
    Promise.all([
        eel.getReminders()()
    ]).then(function(responses) {
        updateReminderSection(responses[0]);
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}
//INITIALIZE MAIN PAGE
eel.load_reminders()().then(function() {
    return Promise.all([
        eel.getReminders()()
    ]);
}).then(function(responses) {
    updateReminderSection(responses[0]);
}).catch(function(error) {
    console.error("Error fetching data:", error);
});