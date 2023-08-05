from gym.envs.registration import register

register(
	id='nav_env-v0',
	entry_point='Egistic_Nav_Env.envs:NavEnv',
	)
register(
	id='foo-extrahard-v0',
	entry_point='Egistic_Nav_Env.envs:NavExtraHardEnv',
	)
