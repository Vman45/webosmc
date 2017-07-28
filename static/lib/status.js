var counter = 0;
var intervalId = null;
function stop(){
  clearInterval(intervalId);
  document.getElementById("bip").innerHTML = "";	
}
function bip(){
    document.getElementById("bip").innerHTML = counter + " secondes passées";
    counter++;
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    var content = $SCRIPT_ROOT+"/_majData";
    $.getJSON($SCRIPT_ROOT+"/_majData",
        function(data) {
            /* temperature graph*/
            var gauge = new LinearGauge({
                renderTo: 'canvas-temp',
                width: 120,
                height: 300,
                units: "°C",
                minValue: 0,
                startAngle: 90,
                ticksAngle: 180,
                valueBox: true,
                maxValue: 120,
                majorTicks: ["0","10","20","30","40","50","60","70","80","90","100","110","120"],
                minorTicks: 5,
                strokeTicks: true,
                highlights: [
                    {"from": 100,"to": 120,"color": "#000"},
                    {"from": 80,"to": 100,"color": "rgba(200, 50, 50, .75)"},
                    {"from": 60,"to": 80,"color": "rgba(200, 170, 50, .75)"},
                    {"from": 40,"to": 60,"color": "rgba(50, 205, 50, .75)"}
                ],
                colorPlate: "#fff",
                borderShadowWidth: 10,
                borders: false,
                needleType: "arrow",
                needleWidth: 2,
                needleCircleSize: 7,
                needleCircleOuter: true,
                needleCircleInner: false,
                barWidth: 15,
                valueDec:1,
                animateOnInit:true,
                animationRule: "elastic",
                animationDuration: 300,
                
                value: data.temperature
            }).draw();
            
             var gauge = new LinearGauge({
                renderTo: 'canvas-cpu',
                width: 120,
                height: 100,
                units: "CPU %",
                minValue: 0,
                startAngle: 90,
                ticksAngle: 180,
                valueBox: true,
                maxValue: 100,
                majorTicks: ["0","20","40","60","80","100"],
                minorTicks:0,
                strokeTicks: false,
                highlights: [
                    {"from": 80,"to": 100,"color": "rgba(200, 50, 50, .75)"},
                    {"from": 60,"to": 80,"color": "rgba(200, 170, 50, .75)"},
                    {"from": 40,"to": 60,"color": "rgba(50, 205, 50, .75)"}
                ],
                colorPlate: "#fff",
                borderShadowWidth: 10,
                borders: false,
                needleType: "arrow",
                needleWidth: 2,
                needleCircleSize: 0,
                needleCircleOuter: true,
                needleCircleInner: false,
                animationDuration: 1500,
                animationRule: "linear",
                barWidth: 15,
                barBeginCircle: false,
                value: data.cpuusage.average ,
               colorBarProgress:"#000",
               colorBarProgressEnd:"#fff",
                            ticksWidth:4,
               ticksPadding:0,
               tickSide: "left",
                numberSide: "left",
                needleSide: "left",
               animateOnInit:true
            }).draw();
            var sortie = "<hr>";
            sortie += "<h2>Processus :</h2>";
            for(elt in data.processes){
                sortie += "<li>" + data.processes[elt].name + " : " + (data.processes[elt].lstPID == "" ? "OFF !!" : data.processes[elt].lstPID) + "</li>";
            };
            sortie += "<hr>";
            sortie += "<table><tr><th>Nom</th><th>CPU</th><th>PID</th></tr>"
            for(elt in data.allprocesses){
            
                sortie += "<tr><th>" + data.allprocesses[elt].name + "</th><td>" + data.allprocesses[elt].cpu_percent + "</td><td>" + data.allprocesses[elt].pid + "</td></tr>";
            };
            sortie += "</table><hr>";
            
            
            $("#processus").html(sortie);
            
            sortie = "<h2>Généralités</h2><ul>";
            sortie += "<li>hostname  " + data.hostname + "</li>";
            sortie += "<li>uptime : " + data.uptime + "</li>";
            sortie += "<li>cpufrequency : " + data.cpufrequency + "</li>";
            sortie += "<li>Connexions : " + data.ip.IPadress + "</li><ul>";
            sortie += "<li>détail Général  : sent=" + data.ip.detail.lo.bytes_sent + "   received=" + data.ip.detail.lo.bytes_recv + "</li>";
            sortie += "<li>détail Ethernet : sent=" + data.ip.detail.eth0.bytes_sent + "   received=" + data.ip.detail.eth0.bytes_recv + "</li>";
            sortie += "<li>détail Wi-Fi    : sent=" + data.ip.detail.wlan0.bytes_sent + "   received=" + data.ip.detail.wlan0.bytes_recv + "</li></ul>";
            sortie += "</ul><hr>";
            $("#gen").html(sortie);
            
            sortie = "<h2>Processeur</h2><ul>";
            sortie += "<li>Nb cpu : " + data.numcpu + "</li>";
            sortie += "<li>cpuusage :</li><ul>";
            sortie += "<li>average : " + data.cpuusage.average + "</li>";
            sortie += "<li>values : " + data.cpuusage.values + "</li></ul>";
            sortie += "</ul><hr>";
            $("#cpu").html(sortie);
            
            sortie = "<h2>Mémoire</h2>";
            sortie += "<li>total : " + data.memory.total + "</li>";
            sortie += "<li>used : " + data.memory.used + "</li>";
            sortie += "<li>available : " + data.memory.available + "</li>";
            sortie += "<li>free : " + data.memory.free + "</li>";
            sortie += "<hr>";
            $("#mem").html(sortie);

            sortie = "<h2>Disques</h2>";
            for(elt in data.disk){
                sortie += "<li>disk device : " + data.disk[elt].device + "( mountpoint : " +  data.disk[elt].mountpoint + ", fstype : " + data.disk[elt].fstype + " )<ul>";
                sortie+= "<li>total : " + data.disk[elt].total + "</li>";
                sortie+= "<li>used  : " + data.disk[elt].used + "</li>";
                sortie+= "<li>free  : " + data.disk[elt].free + " ( " + data.disk[elt].percent + " % )</li>";
                sortie+= "</ul></li>";
            };
            sortie += "<hr>";
            $("#disk").html(sortie);

            
        }
    );
}
