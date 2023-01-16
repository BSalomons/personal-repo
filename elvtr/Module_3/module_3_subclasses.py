from datetime import date

class Pet:
    def __init__(self, name: str, sex: str, birthdate: date):
        self._name = name
        self._sex = sex
        self.birthdate = birthdate

    @property
    def sex(self):
        return self._sex

    @property
    def name(self) -> str:
        return self._name

    def age(self) -> int:
        age = date.today() - self.birthdate
        return int(age.days / 365.24)

class Cat(Pet):
    def speak(self):
        return 'meow'

class Dog(Pet):
    def speak(self):
        return 'woof'

if __name__ == '__main__':
    bday1 = date.fromisoformat('2019-12-31')
    cat1 = Pet(name='Florence', sex='female', birthdate=bday1)
    print(f'The vet will see {cat1.name}, a {cat1.age()}-year-old {cat1.sex}.')

    bday2 = date.fromisoformat('2008-04-06')
    dog1 = Dog(name='Maddie', sex='female', birthdate=bday2)
    print(f'The vet will see {dog1.name}, a {dog1.age()}-year-old {dog1.sex}.')
    print(f'{dog1.name} says {dog1.speak()}')

    # Since Florence was instantiated as a Pet (not a Cat), the object does not know how to speak()
    print(f'{cat1.name} says {cat1.speak()}')



