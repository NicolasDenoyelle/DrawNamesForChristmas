import random

from mail import Email


class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.hash = hash((name, email))

    def Name(self) -> str:
        return self.name

    def Email(self) -> str:
        return self.email

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.name}: {self.email}"

    def __hash__(self):
        return self.hash


class DrawResult:
    draws = {}

    def __init__(self, draws: set[(Person, Person)] = []):
        self.draws = draws

    def __len__(self):
        return len(self.draws)

    def __iter__(self):
        return self.draws.__iter__()

    def __repr__(self):
        out = ""
        for (giver, receiver) in self.draws:
            out += f"{repr(giver)} -> {repr(receiver)}\n"
        return out

    def __str__(self):
        out = ""
        for (giver, receiver) in self.draws:
            out += f"{giver} -> {receiver}\n"
        return out

    @staticmethod
    def EmailTemplate(sender, receiver) -> Email:
        santa_email = "santa.claus@christmas.com"
        message = (
            f"OhOohOooh! {sender.Name()},\n\n"
            "I am delighted to announce you that your have been chosen "
            f"to gift {receiver.Name()} an awesome thoughtful present "
            "this christmas.\n"
            "Everyone is excited to find out what you have in store!\n\n"
            "Merry Chrismas,\nSanta"
        )
        return Email(santa_email, sender.Email(), message)

    def IntoEmails(self) -> list[Email]:
        return [
            DrawResult.EmailTemplate(sender, receiver)
            for (sender, receiver) in self.draws
        ]


class DrawList:
    vertex = set()
    edges = set()

    def __init__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return

        persons = kwargs.get("persons", {})
        self.vertex = self.vertex.union(set(persons))
        self.edges = self.edges.union(
            {(p0, p1) for p0 in persons for p1 in persons if p0 != p1}
        )

        links = kwargs.get("links", {})
        self.edges = self.edges.union(links)
        for (p0, p1) in links:
            self.vertex.add(p0)
            self.vertex.add(p1)

        skip = kwargs.get("skip", {})
        self.edges = {e for e in self.edges if e not in skip}

    def _draw_all_backtrack_(self, n):
        if n == 0 or len(self.edges) < n:
            return []
        if n == 1:
            return [random.choice(list(self.edges))]

        for edge in random.sample(list(self.edges), len(self.edges)):
            draw_list = DrawList()
            draw_list.edges = [
                e for e in self.edges if (e[0] != edge[0] and e[1] != edge[1])
            ]
            other_edges = draw_list._draw_all_backtrack_(n - 1)
            if len(other_edges) + 1 == n:
                return [edge] + other_edges
        return []

    def DrawAll(self) -> DrawResult:
        return DrawResult(self._draw_all_backtrack_(len(self.vertex)))

    def __len__(self):
        return len(self.edges)

    def __str__(self):
        ret = ""
        for (p0, p1) in self.edges:
            ret += f"{repr(p0)} -> {repr(p1)}\n"
        return ret


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


def test_zero():
    assert len(DrawList().DrawAll()) == 0


def test_one():
    p = Person("name", "email")
    d = DrawList(persons={p})
    assert len(d) == 0
    r = d.DrawAll()
    assert len(r) == 0


def test_two():
    p1 = Person("name1", "email1")
    p2 = Person("name2", "email2")
    d = DrawList(persons={p1, p2})
    assert len(d) == 2

    r = d.DrawAll()
    assert len(r) == 2


def check_draw_result(n, result):
    # Check there is no doubles in gifters
    gifters = [g for (g, _) in result]
    assert len(gifters) == len(set(gifters))

    # Check there is no doubles in gift receivers
    receivers = [r for (_, r) in result]
    assert len(receivers) == len(set(receivers))

    # Everyone gifts and receives once
    assert len(gifters) == n
    assert len(receivers) == n
    assert len(result) == n


def test_fully_connected():
    for n in range(3, 20):
        persons = {Person(f"name{i}", f"email{i}") for i in range(0, n)}
        draw = DrawList(persons=persons)
        assert len(draw) == n * (n - 1)
        result = draw.DrawAll()
        check_draw_result(n, result)


def test_cycle():
    for n in range(3, 20):
        links = [
            (
                Person(f"name{i}", f"email{i}"),
                Person(f"name{(i+1)%n}", f"email{(i+1)%n}"),
            )
            for i in range(0, n)
        ]
        draw = DrawList(links=links)
        assert len(draw) == n
        result = draw.DrawAll()
        check_draw_result(n, result)


def test_cycle_and_all_to_one():
    for n in range(3, 20):
        links = []
        for i in range(0, n):
            p0 = Person(f"name{i}", f"email{i}")
            p1 = Person(f"name{(i+1)%n}", f"email{(i+1)%n}")
            pn = Person("name0", "email0")
            links += [(p0, p1), (p0, pn), (p1, pn)]
        draw = DrawList(links=links)
        result = draw.DrawAll()
        check_draw_result(n, result)
