from __future__ import division

import warnings

from numpy import (
    all as npall,
    asarray,
    atleast_2d,
    clip,
    copyto,
    dot,
    empty,
    full,
    inf,
    isfinite,
    log,
    min as npmin,
    newaxis,
    sum as npsum,
    zeros,
)
from numpy.linalg import LinAlgError

from ..util import hsolve, log2pi


class FastScanner(object):
    r"""Approximated fast inference over several covariates.

    Specifically, it computes the log of the marginal likelihood

    .. math::

        \log p(\mathbf y)_j = \log \mathcal N\big(~ \mathrm X\mathbf b_j^*
        + \mathbf{m}_j \alpha_j^*,~
        s_j^* (\mathrm K + v \mathrm I) ~\big),

    for optimal :math:`\mathbf b_j`, :math:`\alpha_j`, and :math:`s_j^*`
    values.
    Vector :math:`\mathbf{m}_j` is the candidate defined by the i-th column
    of matrix ``M`` provided to method
    :func:`.fast_scan`. Variance :math:`v` is not optimised for performance reasons.
    The method assumes the user has provided a reasonable value for it.

    Parameters
    ----------
    y : array_like
        Real-valued outcome.
    X : array_like
        Matrix of covariates.
    QS : tuple
        Economic eigendecomposition ``((Q0, Q1), S0)`` of ``K``.
    v : float
        Variance due to iid effect.

    Notes
    -----
    The implementation requires further explanation as it is somehow obscure.
    Let :math:`\mathrm B_i=\mathrm Q_i\mathrm D_i^{-1}\mathrm Q_i^{\intercal}`
    for :math:`i \in \{0, 1\}` and
    :math:`\mathrm E_j = [\mathrm X;~ \mathbf m_j]`.
    The matrix resulted from
    :math:`\mathrm E_j^{\intercal}\mathrm B_i\mathrm E_j`
    is represented by the variable ``ETBE``, and
    four views of such a matrix are given by the variables ``XTBX``,
    ``XTBM``, ``MTBX``, and ``MTBM``.
    Those views represent
    :math:`\mathrm X^{\intercal}\mathrm B_i\mathrm X`,
    :math:`\mathrm X^{\intercal}\mathrm B_i\mathbf m_j`,
    :math:`\mathbf m_j^{\intercal}\mathrm B_i\mathrm X`, and
    :math:`\mathbf m_j^{\intercal}\mathrm B_i\mathbf m_j`, respectively.
    """

    def __init__(self, y, X, QS, v):

        y = asarray(y, float)
        X = atleast_2d(asarray(X, float).T).T

        if not npall(isfinite(y)):
            raise ValueError("Not all values are finite in the outcome array.")

        if not npall(isfinite(X)):
            raise ValueError("Not all values are finite in the `X` matrix.")

        if v < 0:
            raise ValueError("Variance has to be non-negative.")

        if not isfinite(v):
            raise ValueError("Variance has to be a finite value..")

        D = []
        if QS[1].size > 0:
            D += [QS[1] + v]
        if QS[1].size < y.shape[0]:
            D += [full(y.shape[0] - QS[1].size, v)]
        yTQ = [dot(y.T, Q) for Q in QS[0] if Q.size > 0]
        XTQ = [dot(X.T, Q) for Q in QS[0] if Q.size > 0]

        yTQDi = [l / r for (l, r) in zip(yTQ, D) if npmin(r) > 0]
        yTBy = npsum([npsum(i * i / j) for (i, j) in zip(yTQ, D) if npmin(j) > 0])
        yTBX = [dot(i, j.T) for (i, j) in zip(yTQDi, XTQ)]
        XTQDi = [i / j for (i, j) in zip(XTQ, D) if npmin(j) > 0]

        self._yTBy = yTBy
        self._yTBX = yTBX
        self._ETBE = [_ETBE(i, j) for (i, j) in zip(XTQDi, XTQ)]
        self._yTBE = [empty(len(i) + 1) for i in yTBX]
        self._XTQ = XTQ
        self._yTQDi = yTQDi
        self._XTQDi = XTQDi
        self._scale = None
        self._QS = QS
        self._D = D
        self._X = X
        self._y = y

    @property
    def _nsamples(self):
        return self._QS[0][0].shape[0]

    @property
    def _ncovariates(self):
        return self._X.shape[1]

    def _static_lml(self):
        n = self._nsamples
        static_lml = -n * log2pi - n
        static_lml -= sum(npsum(_safe_log(D)) for D in self._D)
        return static_lml

    def _fast_scan_chunk(self, M):
        M = asarray(M, float)

        if not M.ndim == 2:
            raise ValueError("`M` array must be bidimensional.")

        if not npall(isfinite(M)):
            raise ValueError("One or more variants have non-finite value.")

        MTQ = [dot(M.T, Q) for Q in self._QS[0] if Q.size > 0]
        yTBM = [dot(i, j.T) for (i, j) in zip(self._yTQDi, MTQ)]
        XTBM = [dot(i, j.T) for (i, j) in zip(self._XTQDi, MTQ)]
        D = self._D
        MTBM = [npsum(i / j * i, 1) for i, j in zip(MTQ, D) if npmin(j) > 0]

        lmls = full(M.shape[1], self._static_lml())
        effsizes = empty(M.shape[1])

        if self._ncovariates == 1:
            self._1covariate_loop(lmls, effsizes, yTBM, XTBM, MTBM)
        else:
            self._multicovariate_loop(lmls, effsizes, yTBM, XTBM, MTBM)

        return lmls, effsizes

    def _multicovariate_loop(self, lmls, effsizes, yTBM, XTBM, MTBM):

        ETBE = self._ETBE
        yTBE = self._yTBE
        tuple_size = len(yTBE)
        if self._scale is not None:
            scale = self._scale

        for i in range(tuple_size):
            yTBE[i][:-1] = self._yTBX[i]

        for i in range(XTBM[0].shape[1]):

            for j in range(tuple_size):
                yTBE[j][-1] = yTBM[j][i]
                ETBE[j].set_XTBM(XTBM[j][:, [i]])
                ETBE[j].set_MTBM(MTBM[j][i])

            beta = _solve(sum(j.value for j in ETBE), sum(j for j in yTBE))
            beta = (beta[:-1][:, newaxis], beta[-1:])
            bstar = _bstar_unpack(beta, self._yTBy, yTBE, ETBE)

            if self._scale is None:
                scale = bstar / self._nsamples
            else:
                lmls[i] += self._nsamples - bstar / scale

            lmls[i] -= self._nsamples * _safe_log(scale)
            effsizes[i] = beta[1][0]

        lmls /= 2

    def _1covariate_loop(self, lmls, effsizes, yTBM, XTBM, MTBM):
        ETBE = self._ETBE
        yTBX = self._yTBX
        XTBX = [i.XTBX for i in ETBE]
        yTBy = self._yTBy

        A00 = sum(i.XTBX[0, 0] for i in ETBE)
        A01 = sum(i[0, :] for i in XTBM)
        A11 = sum(i for i in MTBM)

        b0 = sum(i[0] for i in yTBX)
        b1 = sum(i for i in yTBM)

        beta = hsolve(A00, A01, A11, b0, b1)
        beta = (beta[0][newaxis, :], beta[1])

        bstar = _bstar(beta, yTBy, yTBX, yTBM, XTBX, XTBM, MTBM)

        if self._scale is None:
            scale = bstar / self._nsamples
        else:
            scale = full(len(lmls), self._scale)
            lmls += self._nsamples - bstar / scale

        lmls -= self._nsamples * _safe_log(scale)
        lmls /= 2
        effsizes[:] = beta[1]

    def fast_scan(self, M, verbose=True):
        r"""LML and fixed-effect sizes of each marker.

        If the scaling factor ``s`` is not set by the user via method
        :func:`set_scale`, its optimal value will be found and
        used in the calculation.

        Parameters
        ----------
        M : array_like
            Matrix of fixed-effects across columns.
        verbose : bool, optional
            ``True`` for progress information; ``False`` otherwise.
            Defaults to ``True``.

        Returns
        -------
        :class:`numpy.ndarray`
            Log of the marginal likelihoods.
        :class:`numpy.ndarray`
            Fixed-effect sizes.
        """
        from tqdm import tqdm

        if M.ndim != 2:
            raise ValueError("`M` array must be bidimensional.")
        p = M.shape[1]

        lmls = empty(p)
        effect_sizes = empty(p)

        if verbose:
            nchunks = min(p, 30)
        else:
            nchunks = min(p, 1)

        chunk_size = (p + nchunks - 1) // nchunks

        for i in tqdm(range(nchunks), desc="Scanning", disable=not verbose):
            start = i * chunk_size
            stop = min(start + chunk_size, M.shape[1])

            l, e = self._fast_scan_chunk(M[:, start:stop])

            lmls[start:stop] = l
            effect_sizes[start:stop] = e

        return lmls, effect_sizes

    def null_lml(self):
        r"""Log of the marginal likelihood for the null hypothesis.

        Returns
        -------
        float
            Log of the marginal likelihood.
        """
        n = self._nsamples

        ETBE = self._ETBE
        yTBX = self._yTBX

        A = sum(i.XTBX for i in ETBE)
        b = sum(yTBX)
        beta = _solve(A, b)
        sqrdot = self._yTBy - dot(b, beta)

        lml = self._static_lml()

        if self._scale is None:
            scale = sqrdot / n
        else:
            scale = self._scale
            lml += n
            lml -= sqrdot / scale

        return (lml - n * log(scale)) / 2

    def set_scale(self, scale):
        r"""Set the scaling factor.

        Calling this method disables the automatic scale learning.

        Parameters
        ----------
        scale : float
            Scaling factor.
        """
        self._scale = scale

    def unset_scale(self):
        r"""Unset the scaling factor.

        If called, it enables the scale learning again.
        """
        self._scale = None


class _ETBE(object):
    def __init__(self, XTQDi, XTQ):
        n = XTQDi.shape[0] + 1
        self._data = empty((n, n))
        self._data[:-1, :-1] = dot(XTQDi, XTQ.T)

    @property
    def value(self):
        return self._data

    @property
    def XTBX(self):
        return self._data[:-1, :-1]

    @property
    def XTBM(self):
        return self._data[:-1, -1:]

    @property
    def MTBX(self):
        return self._data[-1:, :-1]

    @property
    def MTBM(self):
        return self._data[-1:, -1]

    def set_XTBM(self, XTBM):
        copyto(self.XTBM, XTBM)
        copyto(self.MTBX, XTBM.T)

    def set_MTBM(self, MTBM):
        copyto(self.MTBM, MTBM)


def _bstar(beta, yTBy, yTBX, yTBM, XTBX, XTBM, MTBM):
    from numpy_sugar.linalg import dotd

    r = full(MTBM[0].shape[0], yTBy)
    r -= 2 * sum(dot(i, beta[0]) for i in yTBX)
    r -= 2 * sum(i * beta[1] for i in yTBM)
    r += sum(dotd(beta[0].T, dot(i, beta[0])) for i in XTBX)
    r += sum(dotd(beta[0].T, i * beta[1]) for i in XTBM)
    r += sum(npsum(beta[1] * i * beta[0], axis=0) for i in XTBM)
    r += sum(beta[1] * i * beta[1] for i in MTBM)
    return r


def _bstar_unpack(beta, yTBy, yTBE, ETBE):
    nc = beta[0].shape[0]
    yTBX = [j[:nc] for j in yTBE]
    yTBM = [j[nc:] for j in yTBE]
    XTBX = [j.XTBX for j in ETBE]
    XTBM = [j.XTBM for j in ETBE]
    MTBM = [j.MTBM for j in ETBE]
    return _bstar(beta, yTBy, yTBX, yTBM, XTBX, XTBM, MTBM)


def _solve(A, y):
    from numpy_sugar.linalg import rsolve

    try:
        beta = rsolve(A, y)
    except LinAlgError:
        msg = "Could not converge to the optimal"
        msg += " effect-size of one of the candidates."
        msg += " Setting its effect-size to zero."
        warnings.warn(msg, RuntimeWarning)
        beta = zeros(A.shape[0])

    return beta


def _safe_log(x):
    from numpy_sugar import epsilon

    return log(clip(x, epsilon.small, inf))
