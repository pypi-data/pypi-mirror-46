from stable_baselines.common.policies import register_policy, MlpPolicy, FeedForwardPolicy


class JassPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(JassPolicy, self).__init__(*args, **kwargs,
                                         net_arch=[dict(pi=[128, 128, 128], vf=[128, 128, 128])],
                                         feature_extraction="mlp")


# Register the policy, it will check that the name is not already taken
register_policy('JassPolicy', JassPolicy)
