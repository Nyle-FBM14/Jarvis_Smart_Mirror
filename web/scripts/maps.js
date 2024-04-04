eel.expose(showMap);
function showMap(map_data) {
    let map_section = document.getElementById("map_section");
    map_section.innerHTML = "";
    fetch(`../map.html`)
    .then(res => {
        if(res.ok) {
            return res.text();
        }
    }).then(html => {
        html = html.replace(/\[origin_var\]/g, map_data['origin']);
        html = html.replace(/\[destination_var\]/g, map_data['destination']);
        html = html.replace(/\[map_var\]/g, map_data['map']);
        html = html.replace(/\[directions_var\]/g, map_data['directions']);
        
        map_section.innerHTML = html;
    });
}