import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { vaultClient } from 'src/global/configs/vault.configuration';
import { GoogleStrategy } from './strategy/google.token.strategy';
import { UsersModule } from 'src/users/users.module';
import { JwtModule as Jwt } from '@nestjs/jwt';
import { AtStrategy } from './strategy/access.token.strategy';
import { RtStrategy } from './strategy/refresh.token.strategy';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from 'src/users/entities/user.entity';

@Module({
	imports: [Jwt.register({}), UsersModule, TypeOrmModule.forFeature([User])],
	providers: [
		AuthService,
		{
			provide: 'VAULT_CLIENT',
			useFactory: vaultClient,
		},
		GoogleStrategy,
		AtStrategy,
		RtStrategy,
	],
	controllers: [AuthController],
})
export class AuthModule {}
