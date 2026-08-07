from fastapi import FastAPI, HTTPException
from models import Depense
from database import create_depense
from database import get_all_depenses, get_depense_by_id, get_depenses_by_user
from database import update_depense, delete_depense
from database import total_depenses_par_utilisateur

app = FastAPI()



@app.get("/depenses")
def lister_depenses():
    return get_all_depenses()


@app.get("/depenses/{id}")
def lister_depense_id(id : int):
    depense = get_depense_by_id(id)

    if depense is None:
        raise HTTPException(status_code=404, detail="depense introuvable")

    return depense


@app.get("/depenses/utilisateur/{user_id}")
def lister_depense_user_id(user_id: int):
    depenses = get_depenses_by_user(user_id)
    return depenses


@app.get("/depenses/utilisateur/{user_id}/total")
def total_depenses_user_id(user_id: int):
    total = total_depenses_par_utilisateur(user_id)
    return {"user_id": user_id, "total": total}



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