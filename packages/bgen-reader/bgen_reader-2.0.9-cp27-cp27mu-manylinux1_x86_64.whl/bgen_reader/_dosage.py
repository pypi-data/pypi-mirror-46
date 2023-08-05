import warnings
from numpy import asarray, newaxis

from ._helper import genotypes_to_allele_counts, get_genotypes
from ._dask import array_shape_reveal


def convert_to_dosage(p, nalleles, ploidy):
    r"""Convert probabilities to dosage.

    Parameters
    ----------
    p : array_like
        Allele probabilities.
    nalleles : int
        Number of alleles.
    ploidy : int
        Number of complete sets of chromosomes.

    Returns
    -------
    :class:`numpy.ndarray`
        Dosage matrix.

    Deprecated
    ----------
    Since version 2.0.5. Please use :func:`compute_dosage` instead.
    """
    warnings.warn(
        "Deprecated in favor of `bgen_reader.compute_dosage.", DeprecationWarning
    )
    g = get_genotypes(ploidy, nalleles)
    c = genotypes_to_allele_counts(g)
    return (asarray(c, float).T * p).sum(1)


def allele_frequency(expec):
    r"""Compute allele frequency from its expectation.

    Parameters
    ----------
    expec : array_like
        Allele expectations encoded as a variants-by-samples-by-alleles matrix.

    Returns
    -------
    :class:`numpy.ndarray`
        Allele frequencies encoded as a variants-by-alleles matrix.
    """
    ploidy = expec.shape[-1]
    if expec.ndim < 3:
        n = 1
    else:
        n = expec.shape[1]
    return expec.sum(-2) / (ploidy * n)


def compute_dosage(expec, alt=None):
    r"""Compute dosage from allele expectation.

    Parameters
    ----------
    expec : array_like
        Allele expectations encoded as a variants-by-samples-by-alleles matrix.
    ref : array_like
        Allele reference of each locus. The allele having the minor allele frequency
        for the provided ``expec`` is used as the reference if `None`. Defaults to
        `None`.

    Returns
    -------
    :class:`numpy.ndarray`
        Dosage encoded as a variants-by-samples matrix.

    Examples
    --------

    .. doctest::

    >>> from bgen_reader import read_bgen, allele_expectation, example_files
    >>> from bgen_reader import compute_dosage
    >>>
    >>> with example_files("example.32bits.bgen") as filepath:
    ...     bgen = read_bgen(filepath, verbose=False)
    ...     e = allele_expectation(bgen["genotype"], nalleles=2, ploidy=2)
    ...     dosage = compute_dosage(e).compute()
    ...     print(dosage.shape)
    ...     print(dosage)
    (199, 500)
    [[       nan 1.93575854 1.91558579 ... 1.94351192 0.10894776 1.01101689]
     [1.98779296 1.97802735 0.02111815 ... 1.95492412 1.00897216 1.02255316]
     [0.01550294 0.99383543 1.97933958 ... 1.98681641 1.99041748 1.99603272]
     ...
     [1.99319479 1.980896   1.98767124 ... 1.9943846  1.99716186 1.98712159]
     [0.01263467 0.09661863 0.00869752 ... 0.00643921 0.00494384 0.01504517]
     [0.99185182 1.94860838 0.99734497 ... 0.02914425 1.97827146 0.9515991 ]]
    """
    if alt is None:
        return expec[..., -1]
    try:
        return expec[alt, :, alt]
    except NotImplementedError:
        alt = asarray(alt, int)
        return asarray(expec, float)[alt, :, alt]


def allele_expectation(p, nalleles, ploidy):
    r"""Allele expectation.

    Compute the expectation of each allele from the given probabilities.
    It accepts three shapes of matrices:
    - unidimensional array of probabilities;
    - bidimensional samples-by-alleles probabilities array;
    - and three dimensional variants-by-samples-by-alleles array.

    Parameters
    ----------
    p : array_like
        Allele probabilities.
    nalleles : int
        Number of alleles.
    ploidy : int
        Number of complete sets of chromosomes.

    Returns
    -------
    :class:`numpy.ndarray`
        Last dimension will contain the expectation of each allele.

    Examples
    --------

    .. doctest::

    >>> from texttable import Texttable
    >>> from bgen_reader import read_bgen, allele_expectation, example_files
    >>>
    >>> sampleid = "sample_005"
    >>> rsid = "RSID_6"
    >>>
    >>> with example_files("example.32bits.bgen") as filepath:
    ...     bgen = read_bgen(filepath, verbose=False)
    ...
    ...     locus = bgen["variants"].query("rsid == '{}'".format(rsid)).index
    ...     sample = bgen["samples"].query("id == '{}'".format(sampleid)).index
    ...
    ...     nalleles = bgen["variants"].loc[locus, "nalleles"].item()
    ...     ploidy = 2
    ...
    ...     p = bgen["genotype"][locus[0], sample[0]].compute()
    ...     # For unphased genotypes only.
    ...     e = allele_expectation(bgen["genotype"][locus[0], sample[0]], nalleles, ploidy)
    ...
    ...     alleles = bgen["variants"].loc[locus, "allele_ids"].item().split(",")
    ...
    ...     print(Texttable().add_rows(
    ...         [
    ...             ["", "AA", "AG", "GG", "E[.]"],
    ...             ["p"] + list(p) + [1.0],
    ...             ["#" + alleles[0], 2, 1, 0, e[0]],
    ...             ["#" + alleles[1], 0, 1, 2, e[1]],
    ...         ]
    ...     ).draw())
    +----+-------+-------+-------+-------+
    |    |  AA   |  AG   |  GG   | E[.]  |
    +====+=======+=======+=======+=======+
    | p  | 0.012 | 0.987 | 0.001 | 1     |
    +----+-------+-------+-------+-------+
    | #A | 2     | 1     | 0     | 1.011 |
    +----+-------+-------+-------+-------+
    | #G | 0     | 1     | 2     | 0.989 |
    +----+-------+-------+-------+-------+
    >>> print("variant: {}".format(rsid))
    variant: RSID_6
    >>> print("sample : {}".format(sampleid))
    sample : sample_005

    Note
    ----
    This function supports unphased genotypes only.
    """
    g = get_genotypes(ploidy, nalleles)
    c = asarray(genotypes_to_allele_counts(g), float)
    c = c.T.reshape((1,) * (p.ndim - 1) + (c.shape[1], c.shape[0]))
    p = array_shape_reveal(p)
    return (c * p[..., newaxis, :]).sum(-1)
