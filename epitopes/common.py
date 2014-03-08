
def split_classes(
        values,
        noisy_labels = 'majority',
        unique_sequences = True,
        verbose = True):
    """
    Given a dataframe mapping epitope strings to percentages in [0,1],
    split them into two sets (positive and negative examples.

    Values for `noisy_labels`:
    - majority = epitope is Positive if majority of its results are Positive
    - negative = epitope is Negative if any result is Negative
    - positive = epitope is Positive if any result is Positive
    - drop = remove any epitopes with contradictory results
    - keep = leave contradictory results in both positive and negative sets
    """
    if noisy_labels == 'majority':
        pos_mask = values >= 0.5
    elif noisy_labels == 'positive':
        pos_mask = values > 0
    else:
        pos_mask = values == 1.0

    neg_mask = ~pos_mask
    pos = pos_mask.index[pos_mask]
    neg = neg_mask.index[neg_mask]

    pos_set = set(pos)
    neg_set = set(neg)

    if verbose:
        print "# positive sequences", len(pos)
        print "# negative sequences", len(neg)

    noisy_set = pos_set.intersection(neg_set)

    if verbose:
        print "# unique positive", len(pos_set)
        print "# unique negative", len(neg_set)
        print "# overlap %d (%0.4f)" % (len(noisy_set), \
          float(len(noisy_set)) / len(pos_set))

    if noisy_labels != 'majority':
        if (noisy_labels == 'drop') or (noisy_labels == 'negative'):
            pos_set = pos_set.difference(noisy_set)
        if (noisy_labels == 'drop') or (noisy_labels == 'positive'):
            neg_set = neg_set.difference(noisy_set)
    if unique_sequences:
        return pos_set, neg_set
    else:
        pos = [epitope for epitope in pos if epitope not in pos_set]
        neg = [epitope for epitope in neg if epitope not in neg_set]
        return pos, neg