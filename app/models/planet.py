from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    radius = db.Column(db.Float)
    moons = db.relationship("Moon", back_populates="planet")
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet= Planet(name=planet_data["name"],
                           description=planet_data["description"],
                           radius=planet_data["radius"])
        return new_planet

    def to_dict(self):
        return dict(
            id = self.id,
            name= self.name,
            description= self.description,
            radius= self.radius
        )