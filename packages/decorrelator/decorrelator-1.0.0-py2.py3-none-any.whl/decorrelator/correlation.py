import pymc3 as pm
import numpy as np
import theano.tensor as tt
from astroML.density_estimation import XDGMM
from sklearn.mixture import GaussianMixture
from theano import scan, shared
import theano
theano.config.compute_test_value = "ignore"

from decorrelator.base import BaseModel


def _multivariate_normal_convolution_likelihood(model_covariance, model_mu, data_mu, data_covariance):
    covariance = data_covariance + model_covariance   # shape: (npoints, ndim, ndim) + (ndim, ndim); broadcast to the left
    fn = lambda cov, x: pm.MvNormal.dist(mu=model_mu, cov=cov).logp(x)  # shape (1, )
    result, _ = scan(fn, sequences=[covariance, data_mu], outputs_info=None)  # shape (npoints, )
    return result


class CorrelationModel(BaseModel):
    """
    Return correlation PyMC3 model which works by fitting a Gaussian to the data
    :param values: Measurment data, np.NDArray, shape == (nmeas, ndim)
    :param prior_eta: The shape parameter (eta > 0) of the LKJ distribution. eta = 1
                      implies a uniform distribution of the correlation matrices;
                      larger values put more weight on matrices with few correlations.
    :param prior_width: Width of the HalfCauchy prior distribution on the standard deviations
    :param controlling_models: The models which describe a linear relation between `values` and the
    :return:
    """

    def __init__(self, name, variable_names, data, data_covariances=None, controlling_relations=None):
        self.ndim = data.shape[1]
        super().__init__(name, variable_names, data, data_covariances)
        self.controlling_relations = [] if controlling_relations is None else controlling_relations
        self.resolve_controlling()
        self.construct()


    def initialise(self):
        nmeas, ndim = self.data.shape

        lower_idxs = np.tril_indices(ndim, k=-1)
        if self.data_covariances is not None:
            xdgmm = XDGMM(1, 1000, verbose=True)
            xdgmm.fit(self.data, self.data_covariances)
            guess_mu = xdgmm.mu[0]
            guess_Sigma = xdgmm.V[0]
        else:
            gmm = GaussianMixture(1, max_iter=1000, covariance_type='full').fit(self.data)
            guess_mu = gmm.means_[0]
            guess_Sigma = gmm.covariances_[0]
        guess_chol = np.linalg.cholesky(guess_Sigma)
        guess_packed_chol = guess_chol[lower_idxs]
        return guess_mu, guess_Sigma, guess_packed_chol, guess_chol


    def construct_prior(self, prior_eta=1, prior_width=2.5):
        nmeas, ndim = self.data.shape
        guess_mu, guess_Sigma, guess_packed_chol, guess_chol = self.initialise()

        pm.LKJCholeskyCov('packed_L', n=ndim, eta=float(prior_eta), sd_dist=pm.HalfCauchy.dist(float(prior_width)))
        pm.Normal('mu', self.data.mean(axis=0), self.data.std(axis=0), shape=self.ndim, testval=guess_mu)


    def resolve_controlling(self):
        residuals = {}
        for controlled in self.controlling_relations:

            x, y = controlled.variable_names
            ix, iy = self.variable_names.index(x), self.variable_names.index(y)
            _x, _y = shared(self.data[:, ix]), shared(self.data[:, iy])
            _residual = _y - controlled.relation(_x)
            residuals[y] = _residual
        # correct order, use data i if there are no controlling factors for it
        self.residual_data = tt.stacklists([residuals.get(i, d) for d, i in zip(self.data.T, self.variable_names)]).T


    def construct_likelihood(self):
        lower_idxs = np.tril_indices(self.data.shape[-1], k=-1)

        L = pm.expand_packed_triangular(self.ndim, self.model['packed_L'])
        Sigma = pm.Deterministic('Sigma', L.dot(L.T))
        std = tt.sqrt(tt.diag(Sigma))
        corr = Sigma / tt.outer(std, std)
        pm.Deterministic('corr_coeffs', corr[lower_idxs])

        if self.data_covariances is None:
            pm.MvNormal('like', mu=self.model['mu'], chol=L, observed=self.residual_data)
        else:
            like = _multivariate_normal_convolution_likelihood(Sigma, self.model['mu'], self.residual_data, self.data_covariances)
            pm.Potential('like', like)

    def traceplot(self, varnames=None, combined=True):
        if varnames is None:
            varnames = ['corr_coeffs', 'mu']
        return super().traceplot(varnames, combined)




def plot_ellipse(mu, cov, ax, alpha=0.5, color='k', zorder=10):
    var, U = np.linalg.eig(cov)
    angle = 180. / np.pi * np.arccos(np.abs(U[0, 0]))
    e = Ellipse(mu, 2 * np.sqrt(5.991 * var[0]),
                2 * np.sqrt(5.991 * var[1]),
                angle=angle)
    e.set_alpha(alpha)
    e.set_facecolor(color)
    e.set_zorder(zorder)
    ax.add_artist(e)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    import seaborn as sns

    N = 10000

    mu_actual = np.array([1, -2])
    Sigma_actual = np.array([[0.5, -0.3],
                             [-0.3, 1.]])

    x = np.random.multivariate_normal(mu_actual, Sigma_actual, size=N)

    fig, ax = plt.subplots(figsize=(8, 6))
    blue, _, red, *_ = sns.color_palette()
    ax.scatter(x[:, 0], x[:, 1], c='k', alpha=0.05, zorder=11)
    plot_ellipse(mu_actual, Sigma_actual, ax, color=blue)

    correlation = CorrelationModel('correlation', ['x', 'y'], x)
    correlation.sample(500)


    mu_inference = correlation.best_fit['mu']
    Sigma_inference = correlation.best_fit['Sigma']
    correlation.traceplot(['corr_coeffs'])

    plot_ellipse(mu_inference, Sigma_inference, ax, color=red)
    plt.show()