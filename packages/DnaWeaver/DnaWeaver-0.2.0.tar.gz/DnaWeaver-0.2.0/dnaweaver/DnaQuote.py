"""Classes to represent assembly strategies in DnaWeaver."""

import itertools as itt
from copy import deepcopy
from collections import defaultdict
import tempfile
import os
import json
try:
    from StringIO import StringIO
except ImportError:  # python 3
    from io import StringIO

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import DNAAlphabet
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
from .biotools import blast_sequence


class DnaQuote:
    """Class to represent the Quote returned by a DNA source in response to
    a quote request for a given DNA sequence.

    Parameters
    -----------

    source
      The DnaSource which issued the quote



    sequence

    price

    accepted

    lead_time

    assembly_plan
      A dict of the form { (start1, end1): op1, (start2, end2): op2, ...}
      where the `(start, end)` represent sub-segments of the final sequence and
      `op1, op2` represent the AssemblyOperations that create the corresponding
      fragments

     metadata

     message

     id
       A string identifying uniquely the assembly operation


     deadline
       Deadline for the operation (see the `propagate_deadline` method for this
       class) i.e. in how many time units it should be finished. This is for
       drawing assembly timelines.

    """

    def __init__(self, source, sequence, price=None, accepted=True,
                 lead_time=None, assembly_plan=None, metadata={}, message="",
                 id=None, deadline=None):
        self.source = source
        self.accepted = accepted
        self.price = price
        self.lead_time = lead_time
        self.sequence = sequence
        self.message = message
        self.assembly_plan = assembly_plan
        self.metadata = metadata
        self.id = id
        self.deadline = None

    def __repr__(self):
        if self.accepted:
            infos = "price %.02f" % self.price
            if self.lead_time is not None:
                infos = infos + " - lead_time %0.1f" % self.lead_time
        else:
            infos = "refused: %s" % self.message
        return "From %s - %s - %s" % (self.source, infos, self.message)

    def compute_full_assembly_tree(self, id_prefix="S"):
        """ """

        counter = itt.count()

        def rec(quote):
            if not quote.accepted:
                return quote

            if any([hasattr(quote.source, attr) for attr in [
                   "dna_source", "primers_dna_source"]]):
                if quote.assembly_plan is None:
                    quote = quote.source.get_quote(
                        quote.sequence,
                        max_lead_time=quote.lead_time,
                        with_assembly_plan=True
                    )
                segments = {
                    segment: rec(subquote)
                    for segment, subquote in
                    sorted(quote.assembly_plan.items(),
                           key=lambda item: item[0])
                }
                quote.assembly_plan = segments
            if id_prefix:
                quote.id = id_prefix + "%05d" % next(counter)
            return quote

        rec(self)

        if id_prefix:
            self.id = id_prefix + "%05d" % next(counter)

    def compute_fragments_final_locations(self):
        """Compute the final location of the fragments.

        Examples
        --------

        >>> quote.compute_full_assembly_tree()
        >>> quote.compute_fragments_final_locations()
        >>> some_subquote = print quote.assembly_plan.values()[0]
        >>> print (some_subquote.final_location)
        """
        self.compute_full_assembly_tree()
        quotes = self.tree_as_list()
        quotes_dict = {quote.id: quote for quote in quotes}
        _, temp_fasta = tempfile.mkstemp(suffix=".fa")
        with open(temp_fasta, "w+") as f:
            for quote in quotes:
                f.write(">%s\n%s\n" % (quote.id, quote.sequence))
        results = blast_sequence(self.sequence,
                                 subject=temp_fasta,
                                 word_size=10, perc_identity=100)

        if isinstance(results, list):
            alignments = sum([rec.alignments for rec in results], [])
        else:
            alignments = results.alignments

        for al in alignments:
            hit = max(al.hsps, key=lambda hit: hit.align_length)
            final_location = sorted((hit.query_start, hit.query_end))
            matching_segment = sorted((hit.sbjct_start, hit.sbjct_end))
            quotes_dict[al.hit_def].final_location = final_location
            quotes_dict[al.hit_def].matching_segment = matching_segment
        os.remove(temp_fasta)

    def tree_as_list(self):
        """Return a list containing the current AssemblyOperation and all its
        sub-operations and their respective sub-operations.

        Said otherwise, it flattens the assembly tree into the list of all
        nodes.
        """
        result = [self]
        if self.assembly_plan is not None:
            result += sum([
                child.tree_as_list()
                for segment, child in self.assembly_plan.items()
            ], [])
        return result

    def assembly_tree_as_dict(self, as_json=False, json_indent=None):
        """Return a JSON-like version of the nested tree.

        Parameters
        ----------

        as_json
          If True, a JSON string is returned, else the result is a dict object.

        json_indent
          number of spaces in the JSON indentation (for pretty printing). The
          default None means that the JSON will be on one line (TODO: check).



        Returns
        -------

          {
          "id": self.id,
          "source": self.source.name,
          "price": self.price,
          "lead_time": self.lead_time,
          "sequence": self.sequence,
          "message": self.message,
          "metadata" = self.metadata,
          "assembly_plan": { (start1, end1): {(subquote_1)},
                             (start2, end2): {(subquote_2)},
                           }
         }
        """
        final_location = (self.final_location if
                          hasattr(self, "final_location")
                          else None)
        matching_segment = (self.matching_segment if
                            hasattr(self, "matching_segment")
                            else None)

        assembly_plan = []
        if self.assembly_plan is not None:
            for (segment, quote) in self.assembly_plan.items():
                quote_as_dict = quote.assembly_tree_as_dict()
                quote_as_dict["segment_start"] = segment[0]
                quote_as_dict["segment_end"] = segment[1]
                assembly_plan.append(quote_as_dict)
        tree = {
            "id": self.id,
            "source": self.source.name,
            "price": self.price,
            "lead_time": self.lead_time,
            "sequence": self.sequence,
            "message": self.message,
            "metadata": self.metadata,
            "assembly_plan": assembly_plan,
            "final_location": final_location,
            "matching_segment": matching_segment,
            "accepted": self.accepted
        }

        if as_json:
            return json.dumps(tree, indent=json_indent)
        else:
            return tree


    def propagate_deadline(self, deadline):
        """Add a `deadline` attribute to the quote and propagate it to
        the quote's children by taking into account the duration of operations

        For instance if "self" has a duration of 5 and receives a deadline
        of 8, the quotes that "self" depends on will receive a deadline of
        8-5=3.
        """
        self.deadline = deadline
        children_deadline = deadline - self.step_duration
        if self.assembly_plan is not None:
            for segment, child in self.assembly_plan.items():
                child.propagate_deadline(children_deadline)

    @property
    def step_duration(self):
        """Duration of the final step of the assembly in the quote.

        Inferred by substracting the lead time of children operations to the
        lead time of this operation.
        """
        children_lead_time = self.children_overall_lead_time()
        if children_lead_time is None:
            return self.lead_time
        else:
            return self.lead_time - self.children_overall_lead_time()

    def compute_assembly_levels(self):
        """Return edges and levels for drawing the assembly graph nicely.

        """

        levels = defaultdict(lambda: [])
        edges = []

        def rec(subtree, depth=0):

            levels[depth].append(subtree)

            if subtree.assembly_plan is not None:
                for other in subtree.assembly_plan.values():
                    edges.append((other, subtree))
                    rec(other, depth + 1)
        rec(self)
        levels = [levels[i] for i in sorted(levels.keys())][::-1]
        levels = [sorted(level, key=lambda e: e.id)[::-1] for level in levels]
        return edges, levels

    def assembly_step_summary(self):
        """Return a print-friendly, simple string of the ordering plan."""
        plan = "\n  ".join(
            str(segment) + ": " + str(quote)
            for segment, quote in sorted(self.assembly_plan.items())
        )
        final_txt = "Ordering plan:\n  %s\n  Price:%.02f" % (plan, self.price)
        if self.lead_time is not None:
            final_txt = final_txt + ", total lead_time:%.1f" % self.lead_time
        return final_txt

    def children_total_price(self):
        """Return the total price of all sub-operations (apart from current)"""
        # print ([quote.accepted for quote in self.assembly_plan.values()])
        return sum(quote.price for quote in self.assembly_plan.values())

    def children_overall_lead_time(self):
        """Return the max lead time of all sub-operation (current one not
        included)"""
        if self.assembly_plan is None:
            return None
        lead_times = [quote.lead_time for quote in self.assembly_plan.values()]
        if len(lead_times) == 0:
            return None
        elif any(lead_time is None for lead_time in lead_times):
            return None
        else:
            return max(lead_times)

    def cuts_indices(self):
        """Return the locations of the `cuts` where the sequence is assembled.
        """
        return sorted([segment[1] for segment in self.assembly_plan])[:-1]

    def to_SeqRecord(self, record=None, record_id=None):
        """Return a Biopython seqrecord of the quote.

        >>> record = to_SeqRecord(solution)
        >>> # Let's plot with DnaVu:
        >>> from dnavu import create_record_plot
        >>> from bokeh.io import output_file, show
        >>> output_file("view.html")
        >>> plot = create_record_plot(record)
        >>> show(plot)
        """
        if record_id is None:
            record_id = self.id
        if record is None:
            record = SeqRecord(Seq(self.sequence, DNAAlphabet()), id=record_id)
        else:
            record = deepcopy(record)

        if self.assembly_plan is not None:
            features = [
                SeqFeature(
                    FeatureLocation(segment[0], segment[1], 1),
                    type="Feature",
                    qualifiers={
                        "name": quote.id,
                        "source": quote.source,
                        "price": quote.price,
                        "lead_time": quote.lead_time
                    }
                )
                for segment, quote in self.assembly_plan.items()
            ]
            record.features = features + record.features
        return record


    def to_genbank(self, filename=None, filehandle=None,
                   record=None, record_id=None):
        record = self.to_SeqRecord(record=record, record_id=record_id)
        if filename is not None:
            with open(filename, "w+") as f:
                SeqIO.write(record, f, "genbank")
        else:
            output = StringIO()
            SeqIO.write(record, output, "genbank")
            return output.getvalue()
