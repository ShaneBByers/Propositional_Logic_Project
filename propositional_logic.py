class Expr(object):

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))


class Atom(Expr):

    def __init__(self, name):
        self.name = name
        self.hashable = name

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name
        pass

    def __repr__(self):
        return "Atom(" + self.name + ")"
        pass

    def atom_names(self):
        return set(self.name)
        pass

    def evaluate(self, assignment):
        return assignment[self.name]
        pass

    def to_cnf(self):
        return self
        pass


class Not(Expr):

    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg

    def __eq__(self, other):
        return type(self) == type(other) and self.arg == other.arg
        pass

    def __repr__(self):
        return "Not(" + repr(self.arg) + ")"
        pass

    def atom_names(self):
        return self.arg.atom_names()
        pass

    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)
        pass

    def to_cnf(self):
        if type(self.arg) == type(self):
            return self.arg.arg.to_cnf()
        elif type(self.arg) == And:
            or_list = []
            for item in self.arg.conjuncts:
                new_not = Not(item.to_cnf()).to_cnf()
                or_list.append(new_not)
            return Or(*or_list).to_cnf()
        elif type(self.arg) == Or:
            and_list = []
            for item in self.arg.disjuncts:
                new_not = Not(item.to_cnf()).to_cnf()
                and_list.append(new_not)
            return And(*and_list).to_cnf()
        else:
            return Not(self.arg.to_cnf())
        pass


class And(Expr):

    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts

    def __eq__(self, other):
        return type(self) == type(other) and self.conjuncts == other.conjuncts
        pass

    def __repr__(self):
        return_string = "And("
        for (i, item) in enumerate(self.conjuncts):
            if i == len(self.conjuncts) - 1:
                return_string += repr(item) + ")"
            else:
                return_string += repr(item) + ", "
        return return_string
        pass

    def atom_names(self):
        return_set = set()
        for item in self.conjuncts:
            return_set.update(item.atom_names())
        return return_set
        pass

    def evaluate(self, assignment):
        for item in self.conjuncts:
            if not item.evaluate(assignment):
                return False
        return True
        pass

    def to_cnf(self):
        new_list = []
        for item in self.conjuncts:
            if type(item) == type(self):
                for inner_item in item.conjuncts:
                    new_list.append(inner_item.to_cnf())
            else:
                new_list.append(item.to_cnf())
        return And(*new_list)
        pass


class Or(Expr):

    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts

    def __eq__(self, other):
        return type(self) == type(other) and self.disjuncts == other.disjuncts
        pass

    def __repr__(self):
        return_string = "Or("
        for (i, item) in enumerate(self.disjuncts):
            if i == len(self.disjuncts) - 1:
                return_string += repr(item) + ")"
            else:
                return_string += repr(item) + ", "
        return return_string
        pass

    def atom_names(self):
        return_set = set()
        for item in self.disjuncts:
            return_set.update(item.atom_names())
        return return_set
        pass

    def evaluate(self, assignment):
        for item in self.disjuncts:
            if item.evaluate(assignment):
                return True
        return False
        pass

    def to_cnf(self):
        new_list = []
        for item in self.disjuncts:
            if type(item) == type(self):
                for inner_item in item.disjuncts:
                    new_list.append(inner_item.to_cnf())
            else:
                new_list.append(item.to_cnf())
        new_or = Or(*new_list)
        for item in new_or.disjuncts:
            if type(item) == And:
                new_and_list = []
                for loop_item in new_or.disjuncts:
                    if item is not loop_item:
                        new_and_list.append(loop_item)
                old_and_list = []
                for and_item in item.conjuncts:
                    old_and_list.append(and_item)
                return_and_list = []
                for old_and_item in old_and_list:
                    new_or_list = [old_and_item]
                    for new_and_item in new_and_list:
                        new_or_list.append(new_and_item)
                    return_or_list = Or(*new_or_list).to_cnf()
                    return_and_list.append(return_or_list)
                return_and = And(*return_and_list).to_cnf()
                return return_and
        return Or(*new_list)
        pass


class Implies(Expr):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        return type(self) == type(other) and self.left == other.left and self.right == other.right
        pass

    def __repr__(self):
        return "Implies(" + repr(self.left) + ", " + repr(self.right) + ")"
        pass

    def atom_names(self):
        return_set = set()
        return_set.update(self.left.atom_names())
        return_set.update(self.right.atom_names())
        return return_set
        pass

    def evaluate(self, assignment):
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)
        pass

    def to_cnf(self):
        return Or(Not(self.left.to_cnf()).to_cnf(), self.right.to_cnf()).to_cnf()
        pass


class Iff(Expr):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        return type(self) == type(other) and \
               ((self.left == other.left and self.right == other.right) or
                (self.left == other.right and self.right == other.left))
        pass

    def __repr__(self):
        return "Iff(" + repr(self.left) + ", " + repr(self.right) + ")"
        pass

    def atom_names(self):
        return_set = set()
        return_set.update(self.left.atom_names())
        return_set.update(self.right.atom_names())
        return return_set
        pass

    def evaluate(self, assignment):
        return (self.left.evaluate(assignment) and self.right.evaluate(assignment)) or \
               (not self.right.evaluate(assignment) and not self.left.evaluate(assignment))
        pass

    def to_cnf(self):
        return And(Or(Not(self.left.to_cnf()).to_cnf(), self.right.to_cnf()).to_cnf(), Or(self.left.to_cnf(), Not(self.right.to_cnf()).to_cnf()).to_cnf()).to_cnf()
        pass


def satisfying_assignments_gen(expr):
    curr_values = []
    for _ in range(len(expr.atom_names())):
        curr_values.append(True)

    for i in range(pow(2, len(curr_values))):
        curr_dict = {}
        for (pos, j) in enumerate(expr.atom_names()):
            if i % pow(2, pos) == 0:
                curr_values[pos] = not curr_values[pos]
            curr_dict[j] = curr_values[pos]
        if expr.evaluate(curr_dict):
            yield curr_dict
    pass


def satisfying_assignments(expr):
    for x in satisfying_assignments_gen(expr):
        print x
    pass
