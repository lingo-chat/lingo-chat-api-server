import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule } from '@nestjs/config';
import { validationSchema } from './global/configs/validation.schema';
import { DatabaseModule } from './database/database.module';
import { UsersModule } from './users/users.module';
import { AuthModule } from './auth/auth.module';
import { WebsocketClientModule } from './websocket-client/websocket-client.module';
import jwtConfiguration from './global/configs/jwt.configuration';

@Module({
	imports: [
		ConfigModule.forRoot({
			isGlobal: true,
			cache: true,
			load: [jwtConfiguration],
			envFilePath: `.${process.env.NODE_ENV}.env`,
			validationSchema,
		}),
		DatabaseModule,
		UsersModule,
		AuthModule,
		WebsocketClientModule,
	],
	controllers: [AppController],
	providers: [AppService],
})
export class AppModule {}
