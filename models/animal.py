from database import db


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("centers.id"))
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    species = db.Column(db.Integer, db.ForeignKey('species.id'))
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(120), nullable=True)

    def __init__(self, center_id, name, age, species, price=None, description=None):
        self.center_id = center_id
        self.name = name
        self.age = age
        self.species = species
        self.price = price
        self.description = description

    @staticmethod
    def json(animal):
        return {'id': animal.id, 'center_id': animal.center_id, 'name': animal.name,
                'age': animal.age, 'species': animal.species, 'price': animal.price,
                'description': animal.description
                }

    @staticmethod
    def get_all_animals():
        return [Animal.json(animal) for animal in Animal.query.all()]

    @staticmethod
    def get_animal_by_id(_id):
        animal = Animal.query.filter_by(id=_id).first()
        if animal:
            return Animal.json(animal)
        else:
            return {}

    @staticmethod
    def add_animal(_name, _center_id, _age, _species, _price=None, _description=None):
        new_animal = Animal(_center_id, _name, _age, _species, _price, _description)
        db.session.add(new_animal)
        db.session.commit()


    @staticmethod
    def is_valid_object(animal):
        return 'name' in animal and 'center_id' in animal and 'age' in animal and 'species' in animal

    @staticmethod
    def update_animal_center_id(_id, _center_id):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.center_id = _center_id
        db.session.commit()

    @staticmethod
    def update_animal_name(_id, _name):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.name = _name
        db.session.commit()

    @staticmethod
    def update_animal_age(_id, _age):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.age = _age
        db.session.commit()

    @staticmethod
    def update_animal_species(_id, _species):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.species = _species
        db.session.commit()

    @staticmethod
    def update_animal_price(_id, _price):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.price = _price
        db.session.commit()

    @staticmethod
    def update_animal_age(_id, _description):
        animal_to_update = Animal.query.filter_by(id=_id).first()
        animal_to_update.description = _description
        db.session.commit()


    @staticmethod
    def replace_animal(_id, _center_id, _name, _age, _species, _price=None, _description=None):
        replace_animal = Animal.query.filter_by(id=_id).first()
        replace_animal.center_id = _center_id
        replace_animal.name = _name
        replace_animal.age = _age
        replace_animal.species = _species
        if _price:
            replace_animal.price = _price
        if _description:
            replace_animal.description = _description
        db.session.commit()



