from ..DnaQuote import DnaQuote
from .DnaSource import DnaSource

class DnaSourcesComparator(DnaSource):
    """Special source that compares quotes from other DnaSources.

    Upon receiving a sequence, that source will submit the sequence to
    Downstream sources, which deliver each one optimal quote. The comparator
    then returns the one quote with the lowest price.

    Parameters
    ----------

    suppliers
      List of `DnaSources` that

    memoize
      Whether the quotes should be kept in memory to avoid re-computing the
      same quote several times. Can accelerate computations but is
      RAM-expensive.
    """
    class_description = "DNA sources comparator"
    operation_type = "comparison"
    report_fa_symbol = u""
    report_fa_symbol_plain = u"circle-o"
    report_color = "#000000"

    def __init__(self, suppliers=(), memoize=False, sequence_constraints=(),
                 name="comparator"):
        self.set_suppliers(suppliers)
        self.memoize = memoize
        self.sequence_constraints = sequence_constraints
        self.memoize_dict = {}
        self.name = name

    def get_best_price(self, sequence, max_lead_time=None,
                       with_assembly_plan=False):
        """Returns a price-optimal DnaQuote for the given sequence.

        Parameters
        ----------

        sequence (str)
          The sequence submitted to the Dna Source for a quots

        max_lead_time (float)
          If provided, the quote returned is the best quote (price-wise) whose
          lead time is less or equal to max_lead_time.

        with_assembly_plan
          If True, the assembly plan is added to the quote
        """

        best_quote = None
        best_basepair_price = 1e8
        for source in sorted(self.suppliers,
                             key=lambda s: s.min_basepair_price):
            # print (self.name, len(sequence), source)
            if source.min_basepair_price > best_basepair_price:
                break
            quote = source.get_quote(sequence, max_lead_time=max_lead_time,
                                     with_assembly_plan=with_assembly_plan)
            # print ('=>', quote.accepted, quote.price)
            if not quote.accepted:
                continue
            quote_basepair_price = quote.price / float(len(sequence))
            if quote_basepair_price < best_basepair_price:
                best_quote = quote
                best_basepair_price = quote_basepair_price
        # print ('---- went for ', best_quote.source)
        if best_quote is None:
           return DnaQuote(self, sequence, accepted=False,
                           message="Sequence was rejected by all sources.")
        return best_quote

    def additional_dict_description(self):
        return {
            "dna sources": [source.name for source in self.suppliers],
        }
    @staticmethod
    def from_dict(data):
        return DnaSourcesComparator(
             name=data['name'], suppliers=data['suppliers'])

    def set_suppliers(self, suppliers):
        self.suppliers = suppliers
        if len(suppliers):
            self.min_basepair_price = min([supplier.min_basepair_price
                                           for supplier in suppliers])
        else:
            self.min_basepair_price = None
    
    def suggest_cuts(self, sequence):
      return sorted(set([
        cut
        for supplier in self.suppliers
        if hasattr(supplier, 'suggest_cuts')
        for cut in supplier.suggest_cuts(sequence)
      ]))
