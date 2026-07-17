from pydantic import BaseModel

class Depense(BaseModel):
    montant: float
    categorie: str
    date: str
    user_id: int