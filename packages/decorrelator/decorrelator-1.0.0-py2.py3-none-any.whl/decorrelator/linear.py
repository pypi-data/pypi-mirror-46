import pymc3 as pm
import theano
import theano.tensor as tt
import numpy as np

from decorrelator.base import BaseModel
from decorrelator.estimation import find_mode

__all__ = ['LinearRelation']

def errors_to_covariance(*errs, nans='raise'):
    covar = np.zeros((len(errs[0]), len(errs), len(errs)), dtype=float)
    for i, err in enumerate(errs):
        covar[:, i, i] = np.asarray(err, dtype=float) ** 2
    bad = np.isnan(covar).any(axis=(1, 2))
    if nans == 'drop':
        return covar[~bad]
    elif nans == 'ignore':
        return covar
    elif nans == 'raise':
        if bad.any():
            raise ValueError("Nans detected")
        return covar
    else:
        raise ValueError("{} not valid nan handler, use 'drop' or 'ignore'".format(nans))


def norm_pi(angle):
    """returns the equivalent angle within 0/2pi"""
    return (2*np.pi + angle) * (angle < 0) + angle*(angle > 0)


def gradient_to_angle(theta):
    """
    returns theta but with gradient (theta[0]) and intercept (theta[1]) to angle and displacement
    """
    t = np.asarray(theta).copy()
    t[0] = np.arctan(theta[0])
    t[1] = np.cos(t[0]) * -theta[1]
    return t


def angle_to_gradient(theta):
    """
    returns theta but with angle (theta[0]) and displacement (theta[1]) to gradient and intercept
    """
    t = np.asarray(theta).copy()
    t[0] = np.tan(theta[0])
    t[1] = theta[1] / np.cos(theta[0])
    return t


def likelihood(angle, displacement, ln_variance, z, s, debug=False):
    """
    Returns theano function from the angle, displacement, ln_variance2 theano.scalars
    """
    variance = tt.exp(ln_variance)
    # gradient = tt.tan(angle)

    v = tt.stacklists([[-np.sin(angle)], [np.cos(angle)]])
    delta = tt.dot(v.T, z.T) - displacement
    sigma2 = tt.dot(v.T, tt.dot(s + variance, v).T)  # put variance2 in the sigma2 term (http://dfm.io/posts/fitting-a-plane/)

    factor = sigma2 + variance
    return -(tt.log(factor) / 2).sum() - ((delta**2) / 2 / factor).sum()
    # variance_matrix = tt.stacklists([[gradient**2, -gradient], [-gradient, 1]]) # http://dfm.io/posts/fitting-a-plane/
    # variance_matrix *= variance / (1 + (gradient**2))
    #
    #
    # ll = -tt.sum(tt.log(sigma2) / 2) - tt.sum(delta*delta / 2 / sigma2)
    # if debug:
    #     return ll, v, sigma2, delta
    # return ll


class LinearRelation(BaseModel):
    ndim = 2

    def __init__(self, name, variable_names, data, data_covariances=None):
        super().__init__(name, variable_names, data, data_covariances)
        self.construct()

    def initialise(self):
        from scipy.optimize import curve_fit
        popt, pcov = curve_fit(lambda x, m, c: c + (m*x), self.data[:, 0], self.data[:, 1])
        return popt


    def relation(self, x):
        """
        Returns the y given an x
        """
        return (self.model[self.name+'_'+'gradient'] * x) + self.model[self.name+'_'+'intercept']


    def posterior_predictive(self, x, nsamples):
        """
        return posterior based on sampled trace
        :param x: domain of posterior predictive
        :param n: number of samples
        :return: y: the model (line) over all x and all n samples | shape == (nsamples, len(x))
        """
        choice = np.random.choice(len(self.trace) * self.trace.nchains, nsamples)
        gradient = self.trace[self.name+'_gradient'][choice]
        intercept = self.trace[self.name+'_intercept'][choice]
        return (x[None, :] * gradient[:, None]) + intercept[:, None]


    def construct_prior(self):
        gradient, intercept = self.initialise()
        angle, displacement = gradient_to_angle([gradient, intercept])
        residuals = self.data[:, 1] - (intercept + (gradient * self.data[:, 0]))

        pm.Flat('angle', testval=angle)
        pm.Flat('displacement', testval=displacement)
        variance = pm.HalfCauchy('variance', beta=10, testval=np.mean(residuals**2))
        pm.Deterministic('ln_variance', tt.log(variance))


    def construct_likelihood(self):
        pm.Deterministic('gradient', tt.tan(self.model['angle']))
        pm.Deterministic('intercept', self.model['displacement'] / tt.cos(self.model['angle']))

        if self.data_covariances is not None:
            pm.Potential('like', likelihood(self.model['angle'], self.model['displacement'],
                                            self.model['ln_variance'], self.z, self.s))
        else:
            sigma = tt.exp(self.model['ln_variance'])**0.5
            pm.Normal('like', mu=self.relation(self.z[:, 0]), sd=sigma, observed=self.z[:, 1], shape=len(self.data))


    def traceplot(self, varnames=None, combined=True):
        if varnames is None:
            varnames = ['gradient', 'intercept', 'ln_variance']
        super(LinearRelation, self).traceplot(varnames, combined)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    np.random.seed(13)
    x_true = np.linspace(0, 10, 50)
    m_true, c_true = 1, 10
    y_true = c_true + (m_true * x_true)

    xerr = abs(np.random.normal(0, 0.5, len(x_true)))  # errors are random
    yerr = abs(np.random.normal(0, 0.5, len(y_true)))  # errors are random

    x = np.random.normal(x_true, xerr)
    y = np.random.normal(y_true, yerr)  # add errors

    cov = errors_to_covariance(xerr, yerr)

    linear = LinearRelation('linear', ['x', 'y'], np.stack([x, y]).T, cov)  # can be any label
    linear.sample(50)
    linear.traceplot()


    plt.figure()
    plt.errorbar(x, y, yerr, xerr, fmt='o')
    _x = np.linspace(*plt.xlim())
    popt = linear.initialise()
    plt.plot(_x, popt[1] + (popt[0]*_x))
    plt.plot(_x, linear.best_fit['intercept'] + (linear.best_fit['gradient']*_x))

    for realisation in linear.posterior_predictive(_x, 100):
        plt.plot(_x, realisation, 'k-', alpha=0.2)