function ChargementForm(Form){
    var pathSelect=$('#treePath').tree('getSelectedNode').fullname;
    Form.PathSelected.value = encodeURIComponent(pathSelect);
    var nodes = $('#treeFic').tree('getSelectedNodes');
    var FilesSelected="";
    for (var i=0;i < nodes.length; i++){
        FilesSelected +=  encodeURIComponent(nodes[i].fullname) + ';';
    }
    Form.FilesSelected.value = FilesSelected;	
    //Vérification du contenu du formulaire pour alerte et blocage
    var chxAction = Form.ChxAction.value;
    var lblAction = "";
    switch(chxAction) {
        case "NvDossier":
                if (pathSelect == undefined){alert("Pas de répertoire selectionné");return false;}
            if (Form.NomNvDossier.value == ""){alert("Veuillez indiquer un nom pour le nouveau dossier");return false;}
                lblAction = "Création du dossier " + Form.NomNvDossier.value + " dans le répertoire " + pathSelect;
                break;
        case "RenameFile":
                if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
                 if (nodes.length > 1){alert('Vous ne pouvez renommer qu\'un fichier à la fois');return false;}
                if (Form.RenameFile.value == ""){alert("Veuillez indiquer un nouveau nom pour le fichier");return false;}
                lblAction = "Changement de nom du fichier " + FilesSelected + " en " + Form.NomNvFile.value;
                break;
        case "Copier":

        case "Deplacer":
            if (pathSelect == undefined){alert("Pas de répertoire selectionné");return false;}
            if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
            lblAction = chxAction + " les fichiers " + FilesSelected + "\n dans le répertoire " + pathSelect;
            break;
        case "SupprimerFichiers":
            if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
            lblAction = "Supprimer les fichiers " + FilesSelected
            break;
        case "SupprimerDossier":
            if (pathSelect == undefined){alert("Pas de répertoire selectionné");return false;}
            lblAction = "Supprimer le répertoire " + pathSelect
            break;		
        default:
            alert("Veuillez renseigner une action (" + chxAction + ")");
            return false;
    }
    if (confirm(lblAction + "\n\nEtes vous sûr ?")) {    //alert("oui")  
    }
    else {    return false;  }
}
