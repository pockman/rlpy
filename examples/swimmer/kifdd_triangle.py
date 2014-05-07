from rlpy.Domains import Swimmer
from rlpy.Agents import Q_Learning, SARSA
from rlpy.Representations import *
from rlpy.Policies import eGreedy
from rlpy.Policies.SwimmerPolicy import SwimmerPolicy
from rlpy.Experiments import Experiment
import numpy as np
from hyperopt import hp
from rlpy.Representations import FastKiFDD

param_space = {
    'kernel_resolution':
    hp.loguniform("kernel_resolution", np.log(5), np.log(50)),
    'discover_threshold':
    hp.loguniform(
        "discover_threshold",
        np.log(1e4),
        np.log(1e8)),
    'lambda_': hp.uniform("lambda_", 0., 1.),
    'boyan_N0': hp.loguniform("boyan_N0", np.log(1e1), np.log(1e5)),
    'initial_alpha': hp.loguniform("initial_alpha", np.log(5e-2), np.log(1))}


def make_experiment(
        id=1, path="./Results/Temp/{domain}/{agent}/{representation}/",
        discover_threshold=.05,
        boyan_N0=1885.42,
        lambda_=0.5879,
        initial_alpha=0.1,
        kernel_resolution=10.7920):
    max_steps = 1000000
    num_policy_checks = 10
    checks_per_policy = 1
    active_threshold = 0.05
    max_base_feat_sim = 0.5
    sparsify = 10

    domain = Swimmer()
    kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
        / kernel_resolution
    representation = FastKiFDD(domain, sparsify=sparsify,
                               kernel=gaussian_kernel,
                               kernel_args=[kernel_width],
                               active_threshold=active_threshold,
                               discover_threshold=discover_threshold,
                               normalization=False,
                               max_active_base_feat=100,
                               max_base_feat_sim=max_base_feat_sim)
    policy = SwimmerPolicy(representation)
    #policy = eGreedy(representation, epsilon=0.1)
    stat_bins_per_state_dim = 20
    # agent           = SARSA(representation,policy,domain,initial_alpha=initial_alpha,
    # lambda_=.0, alpha_decay_mode="boyan", boyan_N0=boyan_N0)
    agent = SARSA(
        representation, policy, domain, lambda_=lambda_, initial_alpha=initial_alpha,
        alpha_decay_mode="boyan", boyan_N0=boyan_N0)
    experiment = Experiment(**locals())
    return experiment

if __name__ == '__main__':
    from rlpy.Tools.run import run_profiled
    # run_profiled(make_experiment)
    experiment = make_experiment(1)
    experiment.run(visualize_performance=1, visualize_learning=True)
    # experiment.plot()
    # experiment.save()
    from rlpy.Tools import plt
    plt.figure()
    for i in range(9):
        plt.plot(experiment.state_counts_learn[i], label="Dim " + str(i))
    plt.legend()
