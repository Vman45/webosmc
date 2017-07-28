function ConfirmExec(){
    var FileSelect=$('#treeFic').tree('getSelectedNode').fullname;
    if (FileSelect == undefined){alert("Pas de script selectionné");return false;}
    var lblAction = "Vous aller executer le script " + FileSelect;
    if (confirm(lblAction + "\n\nEtes vous sûr ?")) {
        $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
        var content = $SCRIPT_ROOT+"/gestionFichier/_retScripts"+encodeURIComponent(FileSelect);
        $.getJSON(content,
           function(data) {
                var sortie = "<br><br><br><hr>";
                sortie += "<h2>retour script :</h2>" 
                sortie += data.output;
                if (data.error != null && data.error != ''){
                    sortie += "<h3>ERREUR :</h3>" 
                    sortie += '<br>' + data.error;
                }
                sortie += "<br><br><hr>";
                $("#scriptresult").html(sortie);
            }
        );
    }
        else {    return false;  }
}
function OuvertureEdition(){
     var FileSelect=$('#treeFic').tree('getSelectedNode').fullname;
    if (FileSelect == undefined){alert("Pas de script selectionné");return false;}
    var lblAction = "Vous aller Modifier le script " + FileSelect;
    if (confirm(lblAction + "\n\nEtes vous sûr ?")) {
        //var page = url_for('scriptModif',username=user.username);
        //var nom = '';
        //var option = '';
        //window.open(page,nom,option);
        changeaffiche("ButtonChoix",false);
        changeaffiche("scriptmodif",true);
        RecupContenuFichier(FileSelect);
        // Récupération du contenu du fichier
    }
       else {    return false;  }
}

function RecupContenuFichier(Fichier){
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
        var content = $SCRIPT_ROOT+"/gestionFichier/_modScripts"+encodeURIComponent(Fichier);
        $.getJSON(content,
           function(data) { 
                $("#Scriptcontenu").text(data.content);
                $("#TitreFichier").text(data.name);
                $("#FileSelected").text(data.name);
            }
        );
}

function ChargementForm(Form){
var lblAction = "Vous allez modifier un fichier important !";
if (confirm(lblAction + "\n\nEtes vous sûr ?")) {    //alert("oui")  
}
  else {    return false;  }
}
function changeaffiche(element,visible){
    var targetElement;
    targetElement = document.getElementById(element) ;
    if (visible == true){targetElement.style.display = "" ;}
    else{targetElement.style.display = "none" ;}
}