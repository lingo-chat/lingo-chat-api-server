import { Inject, Injectable } from '@nestjs/common';
import { JwtService as Jwt } from '@nestjs/jwt';
import { ConfigType } from '@nestjs/config';
import { vaultClient } from 'src/global/configs/vault.configuration';
import { OAuth2Client } from 'google-auth-library';
import { UsersService } from 'src/users/users.service';
import { TokenPayload } from 'src/global/interfaces/token.payload';
import jwtConfiguration from 'src/global/configs/jwt.configuration';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from 'src/users/entities/user.entity';

@Injectable()
export class AuthService {
	private vault: any;
	private client: OAuth2Client;

	constructor(
		private readonly jwt: Jwt,
		@Inject(jwtConfiguration.KEY)
		private config: ConfigType<typeof jwtConfiguration>,
		private readonly usersService: UsersService,
		@InjectRepository(User)
		private readonly userRepository: Repository<User>,
	) {
		this.vault = vaultClient();
		this.client = new OAuth2Client(process.env.OAUTH_GOOGLE_CLIENT_ID);
	}

	generateAccessToken(payload: TokenPayload) {
		return this.jwt.sign(payload, {
			secret: this.config.access.secretKey,
			expiresIn: `${this.config.access.expirationTime}s`,
		});
	}

	generateRefreshToken(payload: TokenPayload) {
		return this.jwt.sign(payload, {
			secret: this.config.refresh.secretKey,
			expiresIn: `${this.config.refresh.expirationTime}s`,
		});
	}

	async getGoogleOAuthCredentials() {
		try {
			const result = await this.vault.read('lingo-chat/data/google_oauth');

			return {
				clientID: result.data.OAUTH_GOOGLE_CLIENT_ID,
				clientSecret: result.data.OAUTH_GOOGLE_SECRET,
			};
		} catch (e) {
			throw new Error('Failed to retrieve Google OAuth keys from Vault');
		}
	}

	async googleOAuthLogin({ req }) {
		const { user } = req;
		const { provider, provideId, name, email } = user;

		const isExist = await this.usersService.isUserExist({ provide_id: provideId });
		if (!isExist) await this.usersService.createGoogleUser(user);

		const findUser = await this.usersService.findUser({ provide_id: provideId });

		const accessToken = await this.generateAccessToken({
			provider: provider,
			provideId: provideId,
			name: name,
		});

		const refreshToken = await this.generateRefreshToken({
			provider: provider,
			provideId: provideId,
			name: name,
		});

		await this.userRepository.update(
			{
				id: findUser.id,
			},
			{
				visit_count: (findUser.visit_count += 1),
				last_visit_date: Date(),
				refresh_token: refreshToken,
			},
		);

		return {
			accessToken,
			refreshToken,
		};
	}

	async refresh(user: User) {
		const payload: TokenPayload = {
			provider: user.provider,
			provideId: user.provide_id,
			name: user.name,
		};
		return {
			accessToken: this.generateAccessToken(payload),
		};
	}
}
