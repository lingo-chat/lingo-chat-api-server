import { Controller, Get, Req, Res, UseGuards } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthGuard } from '@nestjs/passport';
import { Request, Response } from 'express';

@Controller('auth')
export class AuthController {
	constructor(private readonly authService: AuthService) {}

	@Get('google')
	@UseGuards(AuthGuard('google'))
	async googleLogin() {}

	@Get('google/callback')
	@UseGuards(AuthGuard('google'))
	async googleLoginCallback(@Req() req: Request, @Res() res: Response) {
		let result = await this.authService.googleOAuthLogin({ req, res });
		return res.status(200).json(result);
	}
}
