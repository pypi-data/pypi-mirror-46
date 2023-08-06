#!/usr/bin/env python3

from defaultdict import DefaultDict

class HashList(list):
    """A list featuring hashes on each item, intended for minimal diffs."""
    def __init__(self, iterable=[]):
        super().__init__(iterable)
        self.update_hashes()
        
    def update_hashes(self):
        """Update the hashes of the items in this list."""
        self._hash_count = DefaultDict(default=0)
        self._hash_list = []
        for item in self:
            item_hash = hash(item)
            hash_occurance = self._hash_count[item_hash]

            self._hash_count[item_hash] += 1
            self._hash_list.append((item_hash, hash_occurance))

    def find_hash_index(self, item_hash, hash_occurance=0):
        """Find the index where the nth instance of the hash appears.

        hash_occurance is 0-indexed.
        """
        return self._hash_list.index((item_hash, hash_occurance))

    def iter_with_hash_index(self):
        """Iterator yields (i, item, item_hash, hash_occurance)."""
        for i in range(len(self)):
            item = self[i]
            item_hash, hash_occurance = self._hash_list[i]
            yield (i, item, item_hash, hash_occurance)

    def diff(self, others):
        """Compare this HashList to a list of other HashLists

        This obeys the following rules:
        - Every unique item is displayed at least once
        - Every item in the first list appears in that list's order,
        along with its index in the other lists
        - Repeated items in the first list appear multiple times
        - These rules are repeated for the following lists, ignoring
        items that have been shown previously unless the current list
        repeats the item more than any previous list
        - Repeated items have as many diff entries as they have appearances

        Returns a list of compounds in the format:
        {'item': item, 'matches': (<index in self>, <index in others[0]>, ...)}

        For lists not containing an item, or enough copies of an item,
        the index reported is None

        See this package's readme.md file for an example.
        """
        all_to_compare = [self]

        for b in others:
            all_to_compare.append(b)

        result = []
        seen_hashes_count = DefaultDict(default=0)

        for hlist_num in range(len(all_to_compare)):
            a = all_to_compare[hlist_num]
            remaining_to_compare = all_to_compare[hlist_num+1:]

            for i, item, item_hash, hash_occurance in a.iter_with_hash_index():
                if hash_occurance < seen_hashes_count[item_hash]:
                    continue
                seen_hashes_count[item_hash] += 1

                matches = [None] * hlist_num + [i]

                for b in remaining_to_compare:
                    try:
                        j = b.find_hash_index(item_hash, hash_occurance)
                    except ValueError:
                        j = None

                    matches.append(j)

                result.append({'item': item, 'matches': tuple(matches)})

        return result

