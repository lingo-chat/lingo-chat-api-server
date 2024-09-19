import { NestFactory, Reflector } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { TransformInterceptor } from './global/interceptors/transform.interceptor';
import { ClassSerializerInterceptor, ValidationPipe } from '@nestjs/common';
import { CorsOptions } from '@nestjs/common/interfaces/external/cors-options.interface';
import { IoAdapter } from '@nestjs/platform-socket.io';

async function bootstrap() {
	const app = await NestFactory.create(AppModule);
	const configService = app.get(ConfigService);
	const PORT = configService.getOrThrow('SERVER_PORT');
	const reflector = new Reflector();

	app.useGlobalInterceptors(new TransformInterceptor(reflector), new ClassSerializerInterceptor(reflector));

	app.useGlobalPipes(
		new ValidationPipe({
			transform: true,
			transformOptions: {
				enableImplicitConversion: true,
			},
		}),
	);

	const corsOptions: CorsOptions = {
		origin: '*',
		methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
		credentials: true,
	};
	app.enableCors(corsOptions);

	app.useWebSocketAdapter(new IoAdapter(app));

	await app.listen(PORT);
}
bootstrap();
