import { Injectable, OnModuleInit } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { Strategy, Profile, VerifyCallBack } from 'passport-google-oauth20';

@Injectable()
export class GoogleStrategy extends PassportStrategy(Strategy, 'google') {
	constructor() {
		super({
			clientID: process.env.OAUTH_GOOGLE_CLIENT_ID,
			clientSecret: process.env.OAUTH_GOOGLE_SECRET,
			callbackURL: process.env.OAUTH_GOOGLE_REDIRECT,
			scope: ['email', 'profile'],
		});
	}

	async validate(accessToken: string, refreshToken: string, profile: Profile, done: VerifyCallBack) {
		const { id, name, emails } = profile;

		const user = {
			provider: 'google',
			provideId: id,
			name: name,
			email: emails[0],
		};

		// Include accessToken to validate login state with each login request.
		return done(null, user, accessToken);
	}
}
