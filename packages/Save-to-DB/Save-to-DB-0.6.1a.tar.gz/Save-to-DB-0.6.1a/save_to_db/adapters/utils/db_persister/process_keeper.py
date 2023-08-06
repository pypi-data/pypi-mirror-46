from collections import defaultdict


class ItemTrack(object):    

    def __init__(self, item):
        self.item = item
        self.models = []
        self.fkeys = defaultdict(list)
        
        # grabbing `None` fkeys
        for fkey in item.relations:
            if fkey in item and item[fkey] is None:
                self.fkeys[fkey].append(None)


class ProcessKeeper(defaultdict):
    
    def __init__(self, item_structure=None):
        super().__init__(list)
        
        if item_structure:
            for item_cls, items in item_structure.items():
                for item in items:
                    self[item_cls].append(ItemTrack(item))
        
    def is_empty(self):
        for value in self.values():
            if value:
                return False
        return True