import { Body, Controller, Get, Post, Req, Res, UseFilters, UseGuards } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthGuard } from '@nestjs/passport';
import { Request, Response } from 'express';
import { ResponseMessage } from 'src/global/decorators/response-key.decorator';
import { AuthReponseMessage } from './classes/auth.response.message';
import { GetUser } from 'src/global/decorators/get-user.decorator';
import { User } from 'src/users/entities/user.entity';
import { JwtExceptionFilter } from 'src/global/filters/jwt-exception.filter';
import { RtGuard } from './guard/refresh.token.guard';
import { ConfigService } from '@nestjs/config';

@Controller('auth')
@UseFilters(JwtExceptionFilter)
export class AuthController {
	constructor(
		private readonly authService: AuthService,
		private readonly configService: ConfigService,
	) {}

	@Get('google')
	@UseGuards(AuthGuard('google'))
	async googleLogin() {}

	@Get('google/callback')
	@UseGuards(AuthGuard('google'))
	@ResponseMessage(AuthReponseMessage.LOG_IN)
	async googleLoginCallback(@Req() req: Request, @Res() res: Response) {
		const reactAppBase = this.configService.getOrThrow('REACT_APP_BASE');
		const result = await this.authService.googleOAuthLogin({ req });
		res.cookie('access-token', result.accessToken, { httpOnly: false, secure: false });
		res.cookie('refresh-token', result.refreshToken, { httpOnly: false, secure: false });
		res.cookie('user-name', result.userName);
		res.redirect(`${reactAppBase}`);
	}

	@Post('refresh')
	@UseGuards(RtGuard)
	@ResponseMessage(AuthReponseMessage.REFRESH)
	async refresh(@GetUser() user: User) {
		return await this.authService.refresh(user);
	}

	@Post('verify-token')
	async verifyToekn(@Body('token') token: string) {
		return await this.authService.verifyToken(token);
	}
}
