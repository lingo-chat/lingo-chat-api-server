import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { Redis } from 'ioredis';
import redisConfiguration from 'src/global/configs/redis.configuration';
import { RedisStorageService } from './redis-storage.service';

@Module({
	imports: [
		ConfigModule.forRoot({
			isGlobal: true,
			load: [redisConfiguration],
		}),
	],
	providers: [
		{
			provide: 'REDIS_CLIENT',
			useFactory: (configService: ConfigService) => {
				return new Redis({
					host: configService.getOrThrow('REDIS_HOST'),
					port: configService.getOrThrow('REDIS_PORT'),
					db: configService.getOrThrow('REDIS_DB'),
				});
			},
			inject: [ConfigService],
		},
		RedisStorageService,
	],
	exports: ['REDIS_CLIENT', RedisStorageService],
})
export class RedisModule {}
