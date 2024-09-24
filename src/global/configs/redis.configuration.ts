import { registerAs } from '@nestjs/config';

export default registerAs('redisConfiguration', () => ({
	redisCache: {
		host: process.env.REDIS_CACHE_HOST,
		port: process.env.REDIS_CACHE_PORT,
		db: process.env.REDIS_CACHE_DB,
	},
}));
