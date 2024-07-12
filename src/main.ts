import { NestFactory, Reflector } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { TransformInterceptor } from './global/interceptors/transform.interceptor';
import { ClassSerializerInterceptor } from '@nestjs/common';

async function bootstrap() {
	const app = await NestFactory.create(AppModule);
	const configService = app.get(ConfigService);
	const PORT = configService.getOrThrow('SERVER_PORT');
	const reflector = new Reflector();

	app.useGlobalInterceptors(new TransformInterceptor(reflector), new ClassSerializerInterceptor(reflector));

	await app.listen(PORT);
}
bootstrap();
