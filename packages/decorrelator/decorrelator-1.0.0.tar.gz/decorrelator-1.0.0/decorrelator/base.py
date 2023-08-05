import numpy as np
import pymc3 as pm
import theano

from decorrelator.estimation import find_mode


class BaseModel:
    ndim = None

    def __init__(self, name, variable_names, data, data_covariances=None):
        self.name = name
        self.variable_names = variable_names
        self.data = np.atleast_2d(data)
        assert self.data.ndim == 2,  "Data must be of shape (npoints, ndim={})".format(self.ndim)
        assert self.data.shape[-1] == self.ndim, "Data must be of shape (npoints, ndim={})".format(self.ndim)
        self.z = theano.shared(self.data, 'z')
        if data_covariances is not None:
            self.data_covariances = np.atleast_3d(data_covariances)
            assert self.data_covariances.ndim == 3, "Data must be of shape (npoints, ndim={})".format(self.ndim)
            assert self.data_covariances.shape[-2:] == (self.ndim, self.ndim), "Data must be of shape (npoints, ndim=2)"
            assert self.data_covariances.shape[0] == self.data.shape[0]
            self.s = theano.shared(self.data_covariances, 's')
        else:
            self.data_covariances = None
        self.model = pm.Model(self.name)


    def construct(self):
        with self.model:
            self.construct_prior()
            self.construct_likelihood()


    def initialise(self):
        raise NotImplementedError


    def construct_prior(self):
        raise NotImplementedError


    def construct_likelihood(self):
        raise NotImplementedError


    def sample(self, steps=500, cores=4, **pymc_kwargs):
        with self.model:
            self.trace = pm.sample(steps, cores=cores, **pymc_kwargs)
            mode_hpd = {k.replace(self.model.name+'_', ''): v for k,v in find_mode(self.trace).items()}
            self.best_fit = {k: v[0] for k, v in mode_hpd.items()}
            self.best_fit_hpd = {k: v[1] for k, v in mode_hpd.items()}


    def posterior_predictive(self, *args, **kwargs):
        raise NotImplementedError


    def chain_figure(self, varnames, combined=True):
        from chainconsumer import ChainConsumer
        fig = ChainConsumer()
        draws = np.asarray([self.trace.get_values(self.name+'_'+v, combine=False, squeeze=False) for v in varnames])
        if combined:
            draws = draws.reshape(len(varnames), -1)
            fig.add_chain(draws, varnames, 'all chains')
        else:
            for i in range(draws.shape[1]):
                fig.add_chain(draws[:, i], varnames, "chain {}".format(i))
        return fig


    def traceplot(self, varnames, combined=True):
        return pm.traceplot(self.trace, [self.name+'_'+v for v in varnames], combined=combined, lines=self.best_fit)


    def __getitem__(self, item):
        try:
            self.trace[self.name+'_'+item]
        except AttributeError:
            raise AttributeError('Sampler not yet run!')
