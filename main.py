from fastapi import FastAPI, HTTPException
from models import Depense
from database import create_depense, get_all_depenses, get_depense_by_id, update_depense, delete_depense

app = FastAPI()




@app.get("/depenses")
def lister_depenses():
    return get_all_depenses()


@app.post("/depenses")
def ajouter_depense(depense : Depense):
    create_depense(depense.montant, depense.categorie, depense.date, depense.user_id)
    return {"message": "Dépense créée"}


@app.put("/depenses/{id}")
def mettre_a_j_depense(id: int, depense_maj: Depense):
    depense = get_depense_by_id(id)
    
    if depense is None:
        raise HTTPException(status_code=404, detail="Dépense introuvable")
    
    update_depense(id, depense_maj.montant, depense_maj.categorie, depense_maj.date, depense_maj.user_id)
    
    return {"message": "Dépense modifiée"}


@app.delete("/depenses/{id}")
def supprimer_depense(id: int):
    depense = get_depense_by_id(id)
    
    if depense is None:
        raise HTTPException(status_code=404, detail="depense introuvable")
    
    delete_depense(id)
    
    return {"message": "depense supprimé"}


from database import total_par_categorie, total_par_mois


@app.get("/stats/categorie")
def dep_par_cat():
    return total_par_categorie()


@app.get("/stats/mois")
def dep_par_mois():
    return total_par_mois()