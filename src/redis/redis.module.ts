import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { Redis } from 'ioredis';
import redisConfiguration from 'src/global/configs/redis.configuration';
import { RedisCacheService } from './redis-cache.service';

@Module({
	imports: [
		ConfigModule.forRoot({
			isGlobal: true,
			load: [redisConfiguration],
		}),
	],
	providers: [
		{
			provide: 'REDIS_CACHE_CLIENT',
			useFactory: (configService: ConfigService) => {
				const redisConfig = configService.get('redisConfiguration');
				return new Redis({
					host: redisConfig.redisCache.host,
					port: redisConfig.redisCache.port,
					db: redisConfig.redisCache.db,
				});
			},
			inject: [ConfigService],
		},

		RedisCacheService,
	],
	exports: ['REDIS_CACHE_CLIENT', RedisCacheService],
})
export class RedisModule {}
