from itertools import product
from typing import Callable, Iterable, Iterator, List, Tuple

from .match import LexerRuleMatcher
from .results import LexerRuleMaker
from ..rules import RuleMapItem, StenoRule
from ..system import StenoSystem
from spectra_lexer.core import Component
from spectra_lexer.utils import str_without

# Default size of generated indices (maximum word size).
_DEFAULT_INDEX_SIZE = 12


class StenoLexer(Component):
    """ The main lexer engine. Uses trial-and-error stack based analysis to gather all possibilities for steno
        patterns it can find, then sorts among them to find what it considers the most likely to be correct. """

    need_all_keys = resource("config:lexer:need_all_keys", False,
                             desc="Only return results that match every key in the stroke.")

    _matcher: LexerRuleMatcher          # Master rule-matching dictionary.
    _rulemaker: LexerRuleMaker          # Makes rules from lexer results.
    _cleanse: Callable[[str], str]      # Performs thorough conversions on RTFCRE steno strings.

    def __init__(self):
        """ Set up the matcher with an empty rule dictionary. """
        super().__init__()
        self._matcher = LexerRuleMatcher()
        self._rulemaker = LexerRuleMaker()

    @on_resource("system")
    def set_system(self, system:StenoSystem) -> None:
        self._cleanse = system.layout.cleanse_from_rtfcre
        self._matcher.load(system)
        self._rulemaker.set_converter(system.layout.to_rtfcre)

    @on("lexer_query")
    def query(self, keys:str, word:str) -> StenoRule:
        """ Return and send out the best rule that maps the given key string to the given word. """
        return self._output(self._query(keys, word))

    @on("lexer_query_product")
    def query_product(self, keys:Iterable[str], words:Iterable[str]) -> StenoRule:
        """ As arguments, take iterables of keys and words and test every possible pairing.
            Return and send out the best rule out of all combinations. """
        pairs = list(product(keys, words))
        rules = [r for p in pairs for r in self._process(*p)]
        rule = self._rulemaker.best_rule(rules, *pairs[0])
        return self._output(rule)

    def _query(self, keys:str, word:str) -> StenoRule:
        return self._rulemaker.best_rule(list(self._process(keys, word)), keys, word)

    def _output(self, rule:StenoRule) -> StenoRule:
        self.engine_call("new_output", rule)
        return rule

    @on("lexer_query_all")
    def query_all(self, items:Iterable[Tuple[str, str]]) -> List[StenoRule]:
        """ Run the lexer in parallel on all (keys, word) translations in <items> and return a list of results.
            Only keep results with all keys matched to reduce garbage. """
        self.need_all_keys = True
        results = self.engine_call("parallel_starmap", self._query, items)
        # Delete the attribute when finished to re-expose the class config setting.
        del self.need_all_keys
        self.engine_call("new_bulk_output", results)
        return results

    def _process(self, keys:str, word:str) -> Iterator[tuple]:
        """ Given a string of formatted s-keys and a matching translation, use steno rules to match keys to printed
            characters in order to generate a series of complete rule maps that could possibly produce the translation.
            Yield each result that isn't optimized away. Use heavy optimization when possible. """
        match_rules = self._matcher.match
        need_all_keys = self.need_all_keys
        # Thoroughly cleanse and parse the key string into s-keys format first (user strokes cannot be trusted).
        skeys = self._cleanse(keys)
        # To match sentence beginnings and proper names, the word must be converted to lowercase.
        lword = word.lower()
        # The queue is a list of tuples, each containing the state of the lexer at some point in time.
        # Each tuple includes the keys not yet matched, the current position in the word, and the current rule map.
        # Initialize the queue with the start position ready and start processing.
        queue = [(skeys, 0, [])]
        queue_add = queue.append
        # Simple iteration over a list is much faster than popping from a deque. Nothing *actually* gets removed
        # from the list; for practical purposes, the iterator pointer can be considered the start of the queue.
        for skeys_left, wordptr, rulemap in queue:
            letters_left = lword[wordptr:]
            # Get the rules that would work as the next match in order from fewest keys matched to most.
            for (r, r_skeys, r_letters, r_letter_count) in match_rules(skeys_left, letters_left, skeys, word):
                # Make a copy of the current map and add the new rule + its location in the word.
                new_wordptr = wordptr + letters_left.find(r_letters)
                new_map = rulemap + [RuleMapItem(r, new_wordptr, r_letter_count)]
                skeys_unmatched = str_without(skeys_left, r_skeys)
                # A "complete" map is one that matches every one of the keys to a rule.
                # If we need all keys to be matched, don't add incomplete maps.
                if not skeys_unmatched or not need_all_keys:
                    yield new_map, skeys_unmatched, keys, word
                    if not skeys_unmatched:
                        # If all keys are matched, continue without adding to the queue.
                        continue
                # Add a queue item with the remaining keys, the new position in the word, and the new map.
                queue_add((skeys_unmatched, new_wordptr + r_letter_count, new_map))
