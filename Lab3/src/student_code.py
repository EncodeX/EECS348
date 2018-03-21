from util import *
from logical_classes import *

verbose = 0


class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            fact_rule (Fact|Rule) - the actual instance fact or rule added to KB
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        result_fr = fact_rule
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                printv("\tAlready in the KB", 0, verbose, [])
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    result_fr = self.facts[ind]
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)

        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                printv("\tAlready in the KB", 0, verbose, [])
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    result_fr = self.rules[ind]
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
        return result_fr

    def kb_assert(self, statement):
        """Assert a fact or rule into the KB

        Args:
            statement (Statement):
                Statement we're asserting in the format produced by read.py
        """
        printv("Asserting {!r}", 0, verbose, [statement])
        self.kb_add(Fact(statement) if factq(statement) else Rule(statement))
        printv("\tIs Fact? {!r}\n\n", 0, verbose, [factq(statement)])

    def kb_ask(self, statement):
        """Ask if a fact is in the KB

        Args:
            statement (Statement)
                - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False
                - list of Bindings if result found, False otherwise
        """
        printv("Asking {!r}", 0, verbose, [statement])
        if factq(statement):
            f = Fact(statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            r = bindings_lst if bindings_lst.list_of_bindings else False
            printv("\t Answer is: {!r}", 0, verbose, [True if r else False])
            return r

        else:
            print "Invalid ask:", statement
            return False

    def kb_retract(self, statement):
        """Retract a fact from the KB

        Args:
            statement (Statement)
                - Statement to be asked (will be converted into a Fact)

        Returns:
            None
        """
        # printv("Retracting {!r}", 0, verbose, [statement])
        ####################################################
        # Student code goes here                           #
        ####################################################

        f = Fact(statement)
        for fact in self.facts:
            if match(fact.statement, f.statement):
                self.kb_retract_helper(fact, True)
                break

    def kb_retract_helper(self, fact_rule, from_command):
        printv("From command? {!r} Retracting {!r}", 0,
               verbose, [from_command, str(fact_rule)])
        # check if the retract command is sent by test
        if fact_rule.asserted and from_command:
            fact_rule.asserted = False
            if len(fact_rule.supported_by) != 0:
                printv("\t It is supported by others! {!r}", 0, verbose, [
                       fact_rule.supported_by])
                return
        # delete reference in fact & rule inferred this
        for sf, sr in fact_rule.supported_by:
            if isinstance(fact_rule, Fact):
                if fact_rule in sf.supports_facts:
                    sf.supports_facts.remove(fact_rule)
                if fact_rule in sr.supports_facts:
                    sr.supports_facts.remove(fact_rule)
            elif isinstance(fact_rule, Rule):
                if fact_rule in sf.supports_rules:
                    sf.supports_rules.remove(fact_rule)
                if fact_rule in sr.supports_rules:
                    sr.supports_rules.remove(fact_rule)

        if fact_rule.asserted:
            printv("\tAsserted fact/rule!", 0, verbose, [])
            if not from_command:
                printv("\tNot from Command, skipping", 0, verbose, [])
                return

        for f in fact_rule.supports_facts:
            # print "\n===\n", str(fact_rule), "supports", str(f), "===\n"
            one_way_support = True
            fr_to_delete = None
            for fact_and_rule in f.supported_by:
                if fact_rule not in fact_and_rule:
                    one_way_support = False
                else:
                    fr_to_delete = fact_and_rule
            if one_way_support:
                self.kb_retract_helper(f, False)
            if fr_to_delete:
                f.supported_by.remove(fr_to_delete)
        for r in fact_rule.supports_rules:
            # print "\n===\n", str(fact_rule), "supports", str(r), "===\n"
            one_way_support = True
            fr_to_delete = None
            for fact_and_rule in r.supported_by:
                if fact_rule not in fact_and_rule:
                    one_way_support = False
                else:
                    fr_to_delete = fact_and_rule
            if one_way_support:
                self.kb_retract_helper(r, False)
            if fr_to_delete:
                r.supported_by.remove(fr_to_delete)

        # delete it self
        if isinstance(fact_rule, Fact):
            self.facts.remove(fact_rule)
        elif isinstance(fact_rule, Rule):
            self.rules.remove(fact_rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
               [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here                           #
        ####################################################

        # Look up the facts!
        rule_to_examine = rule.lhs[0]
        rules_left = rule.lhs[1:]
        bindings = match(rule_to_examine, fact.statement)
        if bindings:
            printv('\n\tMatched {!r} and {!r}\n\twith bindings: {!r}', 0,
                   verbose, [rule_to_examine, fact.statement, bindings])
            # Add new Fact / Rule
            if len(rules_left) == 0:
                printv('\tRule become fact!\n', 0, verbose, [])
                new_fact = Fact(instantiate(
                    rule.rhs, bindings), [[fact, rule]])
                new_fact = kb.kb_add(new_fact)
                if new_fact not in fact.supports_facts:
                    fact.supports_facts.append(new_fact)
                if new_fact not in rule.supports_facts:
                    rule.supports_facts.append(new_fact)
                printv('\tNew fact: {!r}\n', 0, verbose,
                       [new_fact.statement])
            else:
                new_lhs = []
                for r in rules_left:
                    new_lhs.append(instantiate(r, bindings))
                new_rhs = instantiate(rule.rhs, bindings)
                new_rule = Rule([new_lhs, new_rhs], [[fact, rule]])
                new_rule = kb.kb_add(new_rule)
                if new_rule not in fact.supports_rules:
                    fact.supports_rules.append(new_rule)
                if new_rule not in rule.supports_rules:
                    rule.supports_rules.append(new_rule)
                printv('\tNew rule: {!r}\n', 0, verbose,
                       [[new_lhs, new_rhs]])
