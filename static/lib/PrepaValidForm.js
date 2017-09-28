function ChargementForm(Form){
    var pathSelect=document.getElementById("PathSelected").value;
    console.log(pathSelect);
    //Form.PathSelected.value = encodeURIComponent(pathSelect);
    var FilesSelected=document.getElementById("FilesSelected").value;
    //Vérification du contenu du formulaire pour alerte et blocage
    var chxAction = Form.ChxAction.value;
    var lblAction = "";
    switch(chxAction) {
        case "NvDossier":
                if (pathSelect == ""){alert("Pas de répertoire selectionné");return false;}
            if (Form.NomNvDossier.value == ""){alert("Veuillez indiquer un nom pour le nouveau dossier");return false;}
                lblAction = "Création du dossier " + Form.NomNvDossier.value + " dans le répertoire " + pathSelect;
                break;
        case "RenameFile":
                if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
                 if (FilesSelected.indexOf(";") > 0){alert("Vous ne pouvez renommer qu'un fichier à la fois");return false;}
                if (Form.NomNvFile.value == ""){alert("Veuillez indiquer un nouveau nom pour le fichier");return false;}
                lblAction = "Changement de nom du fichier " + FilesSelected + " en " + Form.NomNvFile.value;
                break;
        case "Copier":

        case "Deplacer":
            if (pathSelect == ""){alert("Pas de répertoire selectionné");return false;}
            if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
            lblAction = chxAction + " les fichiers " + FilesSelected.replace(";","\n") + "\n dans le répertoire " + pathSelect;
            break;
        case "SupprimerFichiers":
            if (FilesSelected == ""){alert("Pas de fichier selectionné");return false;}
            lblAction = "Supprimer les fichiers " + FilesSelected.replace(";","\n");
            break;
        case "SupprimerDossier":
            if (pathSelect == ""){alert("Pas de répertoire selectionné");return false;}
            lblAction = "Supprimer le répertoire " + pathSelect;
            break;
        default:
            alert("Veuillez renseigner une action (" + chxAction + ")");
            return false;
    }
    if (confirm(lblAction + "\n\nEtes vous sûr ?") != true) {return false;  }
}
