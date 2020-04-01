# -*- coding: utf-8 -*-
"""
Copyright TorchKGE developers
@author: Armand Boschin <aboschin@enst.fr>
"""

from torch.nn import Module, MarginRankingLoss, SoftMarginLoss
from torch import ones_like


class MarginLoss(Module):
    """Margin loss as it was defined in `TansE paper
    <https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data>`_
    by Bordes et al. in 2013. This class implements `torch.nn.Module` interface.

    """
    def __init__(self, margin):
        super().__init__()
        self.loss = MarginRankingLoss(margin=margin, reduction='sum')

    def forward(self, positive_triplets, negative_triplets):
        """
        Parameters
        ----------
        positive_triplets: `torch.Tensor`, dtype: `torch.float`, shape: (batch_size)
            Scores of the true triplets as returned by the `forward` methods of the models.
        negative_triplets: `torch.Tensor`, dtype: `torch.float`, shape: (batch_size)
            Scores of the negative triplets as returned by the `forward` methods of the models.

        Returns
        -------
        loss: `torch.FloatTensor`, shape: (n_facts, dim)
            Loss of the form :math:`\\max\\{0, \\gamma - f(h,r,t) + f(h',r',t')\\}` where :math:`\\gamma` is the margin
            (defined at initialization), :math:`f(h,r,t)` is the score of a true fact and :math:`f(h',r',t')` is
            the score of the associated negative fact.
        """
        return self.loss(positive_triplets, negative_triplets, target=ones_like(positive_triplets))


class LogisticLoss(Module):
    """Logistic loss as it was defined in `TansE paper
    <https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data>`_
    by Bordes et al. in 2013. This class implements `torch.nn.Module` interface.

    """
    def __init__(self):
        super().__init__()
        self.loss = SoftMarginLoss(reduction='sum')

    def forward(self, positive_triplets, negative_triplets):
        """
        Parameters
        ----------
        positive_triplets: `torch.Tensor`, dtype: `torch.float`, shape: (batch_size)
            Scores of the true triplets as returned by the `forward` methods of the models.
        negative_triplets: `torch.Tensor`, dtype: `torch.float`, shape: (batch_size)
            Scores of the negative triplets as returned by the `forward` methods of the models.
        Returns
        -------
        loss: `torch.FloatTensor`, shape: (n_facts, dim)
            Loss of the form :math:`\\log(1+ \\exp(\\eta \\times f(h,r,t))` where :math:`f(h,r,t)` is the score of
            the fact and :math:`\\eta` is either 1 or -1 if the fact is true or false.
        """
        targets = ones_like(positive_triplets)
        return self.loss(positive_triplets, targets) + self.loss(negative_triplets, -targets)
