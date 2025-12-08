from matchers import All, And, Or, PlaysIn, HasAtLeast, HasFewerThan


class QueryBuilder:
    def __init__(self, matcher=All()):
        self._matcher = matcher

    def build(self):
        return self._matcher

    def plays_in(self, team):
        return QueryBuilder(And(self._matcher, PlaysIn(team)))

    def has_at_least(self, number, stat):
        return QueryBuilder(And(self._matcher, HasAtLeast(number, stat)))

    def has_fewer_than(self, number, stat):
        return QueryBuilder(And(self._matcher, HasFewerThan(number, stat)))

    def one_of(self, *matchers):
        return QueryBuilder(Or(*[matcher.build() for matcher in matchers]))
