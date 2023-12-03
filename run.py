from draw import DrawList, Person
from mail import Server

people = {
    Person("Kaitlin", "personne1@gmail.com"): ["Nicolas"],
    Person("Nicolas", "personne2@gmail.com"): ["Kaitlin"],
    Person("Paulette", "personne3@gmail.com"): ["George"],
    Person("George", "personne4@gmail.com"): ["Paulette"],
    Person("Christopher", "personne5@gmail.com"): [],
    Person("Kara", "personne6@gmail.com"): ["Lydia"],
    Person("Lydia", "personne7@gmail.com"): ["Kara"],
}

pair_skip = {
    (p0, p1)
    for (p0, v) in people.items()
    for s in v
    for p1 in people.keys()
    if s == p1.Name()
}
choices = DrawList(persons=people.keys(), skip=pair_skip)
draw = choices.DrawAll()

reveal = True
server = Server()
for email in draw.IntoEmails():
    server.Send(email)
    if reveal:
        print(f"{email.message}\n-------------------------\n")

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_draw():
    assert len(draw) == len(people)
